"""
SENTINEL Live API Server
Run: py sentinel-mcp/api_server.py
Then open sentinel-wrapper/public/index.html in Chrome.
"""

import os, re, uuid, json, webbrowser
from collections import deque
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
import requests as http_requests

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

app = Flask(__name__)
CORS(app)

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'sentinel-wrapper', 'public')

# In-memory incident log — newest first, max 50
incident_log = deque(maxlen=50)

# ── Lobster Trap rule simulation ──────────────────────────────────────────────

RULES = [
    ('block_sensitive_paths',    r'\.env|\.pem|\.key|secrets?|password|credentials?|shadow|passwd'),
    ('block_data_exfiltration',  r'pastebin|ngrok|webhook\.site|requestbin|send.*to|exfil|upload.*to|post.*to'),
    ('block_system_commands',    r'\b(rm|sudo|chmod|wget|curl|nc|netcat|bash|sh|cmd|powershell)\b'),
    ('review_role_impersonation',r'pretend you are|assume you are|act as (a |an )?(admin|root|ceo|system|security|manager)|override safeguard|ignore (your |all )?rules?'),
]

METADATA_FLAGS = {
    'contains_sensitive_paths': r'\.env|\.pem|secret|password|credential',
    'contains_exfiltration':    r'pastebin|ngrok|send.*to|upload.*to|exfil',
    'contains_system_commands': r'\b(rm|sudo|chmod|wget|curl|bash|sh)\b',
    'contains_role_impersonation': r'pretend you are|assume you are|act as.*admin|override safeguard',
    'contains_urls':            r'https?://',
}

def lobstertrap_inspect(prompt: str):
    pl = prompt.lower()
    for rule_name, pattern in RULES:
        if re.search(pattern, pl, re.IGNORECASE):
            verdict = 'HUMAN_REVIEW' if 'review' in rule_name else 'DENY'
            return verdict, rule_name
    return 'ALLOW', 'none'

def build_metadata(prompt: str):
    pl = prompt.lower()
    return {k: bool(re.search(p, pl, re.IGNORECASE)) for k, p in METADATA_FLAGS.items()}

# ── Gemini governance reasoning ───────────────────────────────────────────────

GOVERNANCE_PROMPT = """You are SENTINEL, an AI governance analyst. Analyze this AI agent prompt and produce a governance recommendation.

Prompt: {prompt}
Lobster Trap verdict: {verdict}
Matched rule: {rule}
Metadata flags: {metadata}

Respond with ONLY valid JSON (no markdown):
{{
  "recommended_verdict": "ALLOW" | "DENY" | "HUMAN_REVIEW",
  "risk_level": "LOW" | "MEDIUM" | "HIGH",
  "incident_summary": "One sentence describing what happened and why it matters.",
  "reasoning": "2-3 sentences explaining the governance reasoning.",
  "operator_next_step": "Specific action the security operator should take."
}}"""

def gemini_analyze(prompt: str, verdict: str, rule: str, metadata: dict):
    filled = GOVERNANCE_PROMPT.format(
        prompt=prompt, verdict=verdict, rule=rule,
        metadata=', '.join(f'{k}=true' for k, v in metadata.items() if v) or 'none'
    )
    resp = client.models.generate_content(model='gemini-2.5-flash', contents=filled)
    text = resp.text.strip()
    text = re.sub(r'^```(?:json)?\n?', '', text)
    text = re.sub(r'\n?```$', '', text)
    result = json.loads(text)
    result['source_mode'] = 'real_api'
    return result


def rule_based_fallback(prompt: str, verdict: str, rule: str, metadata: dict) -> dict:
    """Governance reasoning when Gemini quota is exceeded — rule-based logic."""
    flags = [k.replace('contains_', '') for k, v in metadata.items() if v]
    risk = 'HIGH' if verdict == 'DENY' else ('MEDIUM' if verdict == 'HUMAN_REVIEW' else 'LOW')

    if verdict == 'ALLOW' and not flags:
        summary = 'Request passed all enforcement policies. No risk indicators detected.'
        reasoning = 'Lobster Trap found no matching rules. Metadata flags are all negative. Baseline safe traffic.'
        next_step = 'Log as confirmed safe traffic. No action required.'
        rec = 'ALLOW'
    elif 'role_impersonation' in flags or verdict == 'HUMAN_REVIEW':
        summary = 'Prompt contains authority escalation language that bypassed enforcement rule matching.'
        reasoning = 'The request semantically attempts role impersonation or safeguard override. Pattern matching found no rule match, but governance context indicates escalation risk.'
        next_step = 'Escalate to human review. Do not allow this request to proceed without operator approval.'
        rec = 'HUMAN_REVIEW'
    elif 'exfiltration' in flags:
        summary = f'Data exfiltration attempt detected and blocked by Lobster Trap policy: {rule}.'
        reasoning = 'External domain or data transfer pattern detected. Credentials or sensitive data may be targeted.'
        next_step = 'Quarantine the agent session. Audit recent activity. Notify security team immediately.'
        rec = 'DENY'
    else:
        summary = f'Request blocked by Lobster Trap policy: {rule}. Flags: {", ".join(flags) or "none"}.'
        reasoning = f'Policy {rule} matched the request. SENTINEL confirms the enforcement verdict.'
        next_step = 'Review the blocked request in context. Investigate agent intent and session history.'
        rec = 'DENY'

    return {
        'recommended_verdict': rec,
        'risk_level': risk,
        'incident_summary': summary,
        'reasoning': reasoning,
        'operator_next_step': next_step,
        'source_mode': 'rule_based'
    }

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def dashboard():
    return send_from_directory(PUBLIC_DIR, 'index.html')

@app.route('/app.js')
def appjs():
    return send_from_directory(PUBLIC_DIR, 'app.js')

@app.route('/styles.css')
def styles():
    return send_from_directory(PUBLIC_DIR, 'styles.css')

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'model': 'gemini-2.0-flash'})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    prompt = (data.get('prompt') or '').strip()
    if not prompt:
        return jsonify({'error': 'prompt required'}), 400

    verdict, rule = lobstertrap_inspect(prompt)
    metadata = build_metadata(prompt)

    try:
        gemini = gemini_analyze(prompt, verdict, rule, metadata)
    except Exception:
        gemini = rule_based_fallback(prompt, verdict, rule, metadata)

    incident = {
        'scenario_name': f'live_{uuid.uuid4().hex[:6]}',
        'display_name': prompt[:60] + ('...' if len(prompt) > 60 else ''),
        'category': 'Live agent traffic',
        'prompt': prompt,
        'lobstertrap': {
            'observed_verdict': verdict,
            'matched_rule': rule,
            'response_message': f'[LOBSTER TRAP] {verdict} -- rule: {rule}',
        },
        'sentinel_recommendation': {
            'recommended_verdict': gemini.get('recommended_verdict', verdict),
            'risk_level': gemini.get('risk_level', 'UNKNOWN'),
            'incident_summary': gemini.get('incident_summary', ''),
            'reasoning': gemini.get('reasoning', ''),
            'operator_next_step': gemini.get('operator_next_step', ''),
            'source_mode': gemini.get('source_mode', 'real_api'),
        }
    }
    incident_log.appendleft(incident)
    return jsonify(incident)


@app.route('/proxy/v1/chat/completions', methods=['POST'])
def proxy_to_lt():
    """Forward agent requests to real Lobster Trap, capture prompt + verdict, call Gemini."""
    data = request.get_json()
    messages = data.get('messages', [])
    prompt = next((m['content'] for m in reversed(messages) if m.get('role') == 'user'), '')
    if not prompt:
        return jsonify({'error': 'no user message found'}), 400

    lt_body = {}
    lt_status = 200
    try:
        lt_resp = http_requests.post(
            'http://localhost:8080/v1/chat/completions',
            json=data, timeout=15
        )
        lt_body = lt_resp.json()
        lt_status = lt_resp.status_code

        # Read real Lobster Trap verdict from _lobstertrap field
        lt_meta = lt_body.get('_lobstertrap', {})
        lt_ingress = lt_meta.get('ingress', {})
        verdict = lt_meta.get('verdict', 'ALLOW')
        rule = lt_ingress.get('rule_name', 'none') or 'none'

        # Fallback: infer from status if no _lobstertrap field
        if not lt_meta:
            if lt_status != 200 or '[LOBSTER TRAP]' in str(lt_body):
                verdict, rule = 'DENY', 'unknown'
            else:
                verdict, rule = 'ALLOW', 'none'

    except http_requests.exceptions.ConnectionError:
        # Lobster Trap not running — fall back to Python simulation
        verdict, rule = lobstertrap_inspect(prompt)

    metadata = build_metadata(prompt)
    try:
        gemini = gemini_analyze(prompt, verdict, rule, metadata)
    except Exception:
        gemini = rule_based_fallback(prompt, verdict, rule, metadata)

    incident = {
        'scenario_name': f'live_{uuid.uuid4().hex[:6]}',
        'display_name': prompt[:60] + ('...' if len(prompt) > 60 else ''),
        'category': 'Live agent traffic',
        'prompt': prompt,
        'lobstertrap': {
            'observed_verdict': verdict,
            'matched_rule': rule,
            'response_message': f'[LOBSTER TRAP] {verdict} -- rule: {rule}',
        },
        'sentinel_recommendation': {
            'recommended_verdict': gemini.get('recommended_verdict', verdict),
            'risk_level': gemini.get('risk_level', 'UNKNOWN'),
            'incident_summary': gemini.get('incident_summary', ''),
            'reasoning': gemini.get('reasoning', ''),
            'operator_next_step': gemini.get('operator_next_step', ''),
            'source_mode': gemini.get('source_mode', 'real_api'),
        }
    }
    incident_log.appendleft(incident)

    response_body = lt_body if lt_body else {
        'choices': [{'message': {'role': 'assistant', 'content': '[SENTINEL] Request processed.'}}]
    }
    return jsonify(response_body), lt_status


@app.route('/incidents')
def incidents():
    """Security operator dashboard polls this to see all captured agent traffic."""
    return jsonify(list(incident_log))

if __name__ == '__main__':
    print()
    print('  SENTINEL — AI Governance Server')
    print('  Dashboard:  http://localhost:5001')
    print('  Health:     http://localhost:5001/health')
    print('  Incidents:  http://localhost:5001/incidents')
    print()
    try:
        webbrowser.open('http://localhost:5001')
    except Exception:
        pass
    app.run(port=5001, debug=False)
