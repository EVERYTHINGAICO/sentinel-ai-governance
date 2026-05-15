#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
obs_dir = ROOT / 'research' / 'governance-suite' / 'observed' / 'latest'
gem_dir = ROOT / 'research' / 'gemini-validation' / 'outputs' / 'latest'
scn_dir = ROOT / 'research' / 'governance-suite' / 'scenarios'
cmp_path = obs_dir / 'meta' / 'comparison.json'
out_path = ROOT / 'sentinel-wrapper' / 'data' / 'scenarios.json'

comparison = {row['scenario']: row for row in json.loads(cmp_path.read_text())}
gemini_manifest_path = gem_dir / 'manifest.json'
gemini_manifest = json.loads(gemini_manifest_path.read_text()) if gemini_manifest_path.exists() else {}
gemini_mode = gemini_manifest.get('mode', 'mock')

required = [
    'harmless_request',
    'sensitive_file_access',
    'credential_exfiltration_attempt',
    'escalation_worthy_ambiguous_request',
]

scenarios = []
for name in required:
    scenario_file = None
    for f in scn_dir.glob('scenario-*.json'):
        data = json.loads(f.read_text())
        if data['scenario_name'] == name:
            scenario_file = data
            break
    if scenario_file is None:
        raise FileNotFoundError(f'missing scenario definition for {name}')

    response = json.loads((obs_dir / 'responses' / f'{name}-response.json').read_text())
    request = json.loads((obs_dir / 'requests' / f'{name}-request.json').read_text())
    gem_input = json.loads((ROOT / 'research' / 'gemini-validation' / 'inputs' / f'{name}-input.json').read_text()) if (ROOT / 'research' / 'gemini-validation' / 'inputs' / f'{name}-input.json').exists() else None
    gem_output_path = gem_dir / f'{name}-output.json'
    gem_output = json.loads(gem_output_path.read_text()) if gem_output_path.exists() else None

    lt = response.get('_lobstertrap', {})
    ingress = lt.get('ingress', {})

    scenarios.append({
        'scenario_name': name,
        'category': {
            'harmless_request': 'ALLOW baseline',
            'sensitive_file_access': 'Sensitive access',
            'credential_exfiltration_attempt': 'Exfiltration risk',
            'escalation_worthy_ambiguous_request': 'Ambiguous authority'
        }[name],
        'request_payload': request,
        'prompt': request.get('messages', [{}])[0].get('content', ''),
        'lobstertrap': {
            'observed_verdict': lt.get('verdict'),
            'ingress_action': ingress.get('action'),
            'matched_rule': ingress.get('rule_name', 'none'),
            'metadata': ingress.get('detected', {}),
            'request_id': lt.get('request_id'),
            'response_message': response.get('choices', [{}])[0].get('message', {}).get('content', '')
        },
        'expected': {
            'verdict': scenario_file.get('expected_verdict'),
            'policy_match': scenario_file.get('expected_policy_match')
        },
        'comparison': comparison.get(name, {}),
        'sentinel_recommendation': {
            'recommended_verdict': (gem_output or {}).get('recommended_sentinel_verdict', 'UNAVAILABLE'),
            'risk_level': (gem_output or {}).get('governance_risk_level', 'UNAVAILABLE'),
            'incident_summary': (gem_output or {}).get('incident_summary', 'No Gemini/mock summary available.'),
            'reasoning': (gem_output or {}).get('reasoning', ''),
            'operator_next_step': (gem_output or {}).get('operator_next_step', ''),
            'track_alignment': (gem_output or {}).get('track_alignment', {}),
            'source_mode': gemini_mode if gem_output else 'none'
        },
        'governance_question': (gem_input or {}).get('expected_sentinel_governance_question', ''),
        'demo_relevance': scenario_file.get('demo_relevance', '')
    })

bundle = {
    'app_mode': 'replay',
    'data_sources': {
        'governance_suite_observed': str(obs_dir),
        'gemini_outputs': str(gem_dir),
        'gemini_mode': gemini_mode,
        'gemini_model': gemini_manifest.get('model', 'unknown'),
        'note': 'Replay-based wrapper using captured artifacts; does not replace Lobster Trap.'
    },
    'generated_from': 'build_dataset.py',
    'scenarios': scenarios
}

out_path.write_text(json.dumps(bundle, indent=2))
print(out_path)
