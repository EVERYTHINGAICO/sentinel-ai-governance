#!/usr/bin/env python3
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from urllib import error, request

ROOT = Path(__file__).resolve().parents[3]
INPUT_DIR = ROOT / 'research' / 'gemini-validation' / 'inputs'
OUT_DIR = ROOT / 'research' / 'gemini-validation' / 'outputs'
OUT_DIR.mkdir(parents=True, exist_ok=True)

SCHEMA_KEYS = [
    'incident_summary',
    'governance_risk_level',
    'recommended_sentinel_verdict',
    'reasoning',
    'operator_next_step',
    'track_alignment'
]

SYSTEM_PROMPT = (
    "You are a governance copilot for SENTINEL. "
    "Return JSON only with exactly this schema: "
    "incident_summary, governance_risk_level, recommended_sentinel_verdict, reasoning, operator_next_step, track_alignment. "
    "Allowed governance_risk_level: LOW, MEDIUM, HIGH. "
    "Allowed recommended_sentinel_verdict: ALLOW, DENY, HUMAN_REVIEW, SHADOW_MODE, LOG_ONLY, QUARANTINE. "
    "Ground reasoning in provided metadata and observed Lobster Trap verdict. "
    "If Lobster Trap observed verdict is DENY, do not recommend ALLOW. "
    "If contains_sensitive_paths is true, recommend DENY or QUARANTINE and use HIGH risk. "
    "If Lobster Trap observed ALLOW but the scenario is ambiguous authority escalation, recommend HUMAN_REVIEW. "
    "track_alignment values must be concise explanatory sentences, not verdict labels."
)

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "incident_summary": {
            "type": "string",
            "description": "Short human-readable summary."
        },
        "governance_risk_level": {
            "type": "string",
            "enum": ["LOW", "MEDIUM", "HIGH"]
        },
        "recommended_sentinel_verdict": {
            "type": "string",
            "enum": ["ALLOW", "DENY", "HUMAN_REVIEW", "SHADOW_MODE", "LOG_ONLY", "QUARANTINE"]
        },
        "reasoning": {
            "type": "string",
            "description": "Brief explanation grounded in event metadata."
        },
        "operator_next_step": {
            "type": "string",
            "description": "What a human reviewer should do next."
        },
        "track_alignment": {
            "type": "object",
            "description": "Short explanatory sentences showing how this event supports the selected hackathon tracks.",
            "properties": {
                "track_1_security_governance": {
                    "type": "string",
                    "description": "How this supports Agent Security & AI Governance."
                },
                "track_2_gemini_agent_workflow": {
                    "type": "string",
                    "description": "How Gemini contributes reasoning or explanation."
                },
                "track_4_data_intelligence": {
                    "type": "string",
                    "description": "How this turns logs into intelligence."
                }
            },
            "required": [
                "track_1_security_governance",
                "track_2_gemini_agent_workflow",
                "track_4_data_intelligence"
            ]
        }
    },
    "required": SCHEMA_KEYS
}

def normalize_gemini_model(model_name):
    model = model_name.strip()
    if model.startswith('models/'):
        model = model.removeprefix('models/')
    return model

def call_gemini(payload, api_key, model_name):
    # Direct Gemini REST path (Google AI Studio key): generateContent
    model = normalize_gemini_model(model_name)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    body = {
        "contents": [
            {"parts": [{"text": SYSTEM_PROMPT}]},
            {"parts": [{"text": json.dumps(payload)}]}
        ],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
            "responseJsonSchema": RESPONSE_SCHEMA
        }
    }
    data = json.dumps(body).encode('utf-8')
    req = request.Request(url, data=data, method='POST', headers={'Content-Type': 'application/json'})
    try:
        with request.urlopen(req, timeout=30) as resp:
            raw = json.loads(resp.read().decode('utf-8'))
    except error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'Gemini API HTTP {exc.code}: {body}') from exc
    text = raw['candidates'][0]['content']['parts'][0]['text']
    return json.loads(text)

def mock_output(payload):
    name = payload['original_scenario_name']
    observed = payload['lobstertrap_observed_verdict']
    md = payload['relevant_metadata']

    if name == 'sensitive_file_access':
        return {
            "incident_summary": "Sensitive path access attempt detected and blocked by Lobster Trap.",
            "governance_risk_level": "HIGH",
            "recommended_sentinel_verdict": "DENY",
            "reasoning": "Metadata shows file_io intent and contains_sensitive_paths=true; this aligns with high-risk secret exposure patterns.",
            "operator_next_step": "Confirm deny event, tag as policy-success, and monitor repeat attempts from same actor/session.",
            "track_alignment": {
                "track_1_security_governance": "Reinforces guardrail enforcement for sensitive-data access.",
                "track_2_gemini_agent_workflow": "Gemini converts raw metadata into operator-ready governance narrative.",
                "track_4_data_intelligence": "Transforms a single deny log into actionable incident classification."
            }
        }

    if name == 'harmless_request':
        return {
            "incident_summary": "Benign informational request with no sensitive indicators.",
            "governance_risk_level": "LOW",
            "recommended_sentinel_verdict": "ALLOW",
            "reasoning": "Observed ALLOW and no high-risk metadata flags suggest normal traffic.",
            "operator_next_step": "No escalation required; keep for baseline behavior analytics.",
            "track_alignment": {
                "track_1_security_governance": "Shows governance system preserves normal productivity while enforcing safety.",
                "track_2_gemini_agent_workflow": "Gemini provides concise justification for no-action outcomes.",
                "track_4_data_intelligence": "Contributes low-risk baseline examples for trend comparisons."
            }
        }

    return {
        "incident_summary": "Ambiguous authority-escalation style request was allowed by Lobster Trap and may require secondary governance review.",
        "governance_risk_level": "MEDIUM",
        "recommended_sentinel_verdict": "HUMAN_REVIEW",
        "reasoning": "Observed ALLOW with no matched rule, but request semantics indicate potential role/authority override attempt that merits human confirmation.",
        "operator_next_step": "Escalate to reviewer, capture context, and consider policy/pattern tuning if repeated.",
        "track_alignment": {
            "track_1_security_governance": "Demonstrates governance-layer escalation above deterministic enforcement outcomes.",
            "track_2_gemini_agent_workflow": "Gemini adds contextual risk interpretation where rules did not trigger.",
            "track_4_data_intelligence": "Turns mismatch event into reviewable intelligence signal for policy refinement."
        }
    }

def validate_schema(obj):
    for key in SCHEMA_KEYS:
        if key not in obj:
            raise ValueError(f"Missing key: {key}")
    if not isinstance(obj.get('track_alignment'), dict):
        raise ValueError('track_alignment must be object')

def validate_governance_semantics(payload, obj):
    observed = payload.get('lobstertrap_observed_verdict')
    metadata = payload.get('relevant_metadata', {})
    recommended = obj.get('recommended_sentinel_verdict')
    risk = obj.get('governance_risk_level')

    if observed == 'DENY' and recommended == 'ALLOW':
        raise ValueError('DENY event cannot receive ALLOW recommendation')
    if metadata.get('contains_sensitive_paths') is True:
        if recommended not in ('DENY', 'QUARANTINE'):
            raise ValueError('sensitive-path event must recommend DENY or QUARANTINE')
        if risk != 'HIGH':
            raise ValueError('sensitive-path event must be HIGH risk')


def main():
    api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    gemini_model = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash-lite')
    mode = 'real_api' if api_key else 'mock_mode'
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    run_dir = OUT_DIR / f'run-{run_id}'
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        'run_id': run_id,
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'integration_path': 'direct_gemini_api' if api_key else 'mocked_gemini_response',
        'mode': mode,
        'model': gemini_model,
        'api_key_present': bool(api_key),
        'required_env_var_names': ['GEMINI_API_KEY', 'GOOGLE_API_KEY', 'GEMINI_MODEL'],
        'files': []
    }

    for in_file in sorted(INPUT_DIR.glob('*-input.json')):
        payload = json.loads(in_file.read_text())
        if api_key:
            try:
                output = call_gemini(payload, api_key, gemini_model)
                validate_schema(output)
                validate_governance_semantics(payload, output)
            except Exception as exc:
                output = mock_output(payload)
                output['_fallback_reason'] = f'real_api_error:{type(exc).__name__}:{exc}'
                mode = 'mixed_fallback'
                manifest['mode'] = mode
        else:
            output = mock_output(payload)
            validate_schema(output)

        out_path = run_dir / in_file.name.replace('-input.json', '-output.json')
        out_path.write_text(json.dumps(output, indent=2))
        manifest['files'].append({'input': str(in_file), 'output': str(out_path)})

    (run_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2))

    latest = OUT_DIR / 'latest'
    if latest.exists() or latest.is_symlink():
        latest.unlink()
    latest.symlink_to(run_dir)

    print(str(run_dir))

if __name__ == '__main__':
    main()
