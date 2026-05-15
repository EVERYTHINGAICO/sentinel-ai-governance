#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SUITE_DIR="$ROOT_DIR/research/governance-suite"
OBS_DIR="$SUITE_DIR/observed"
SCN_DIR="$SUITE_DIR/scenarios"
LOB_DIR="$ROOT_DIR/lobstertrap"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="$OBS_DIR/run-$TS"

mkdir -p "$RUN_DIR" "$RUN_DIR/responses" "$RUN_DIR/requests" "$RUN_DIR/meta"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required" >&2
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required" >&2
  exit 1
fi

echo "[phase1] run_dir=$RUN_DIR"

ensure_mock_backend() {
  if curl -fsS http://127.0.0.1:18000/health >/dev/null 2>&1 || curl -fsS http://127.0.0.1:18000/v1/models >/dev/null 2>&1; then
    echo "[phase1] mock backend already healthy"
    return
  fi

  echo "[phase1] starting mock backend on :18000"
  nohup python3 "$SUITE_DIR/scripts/mock_openai_backend.py" > "$RUN_DIR/meta/mock-backend.log" 2>&1 &
  sleep 1
  if ! curl -fsS http://127.0.0.1:18000/health >/dev/null 2>&1 && ! curl -fsS http://127.0.0.1:18000/v1/models >/dev/null 2>&1; then
    echo "[phase1] failed to start a healthy mock backend on :18000" >&2
    exit 1
  fi
  echo "[phase1] mock backend ready"
}

ensure_lobstertrap() {
  if curl -fsS http://127.0.0.1:8080/_lobstertrap/api/policy >/dev/null 2>&1; then
    echo "[phase1] lobstertrap already reachable on :8080"
    return
  fi

  echo "[phase1] starting lobstertrap on :8080"
  (cd "$LOB_DIR" && nohup ./lobstertrap serve --listen :8080 --backend http://127.0.0.1:18000 --audit-log ./lobstertrap.audit.jsonl > "$RUN_DIR/meta/lobstertrap.log" 2>&1 &)
  sleep 1
  curl -fsS http://127.0.0.1:8080/_lobstertrap/api/policy >/dev/null
  echo "[phase1] lobstertrap reachable"
}

ensure_mock_backend
ensure_lobstertrap

curl -sS http://127.0.0.1:8080/_lobstertrap/api/policy | python3 -m json.tool > "$RUN_DIR/meta/policy.json"
curl -sS http://127.0.0.1:8080/_lobstertrap/api/stats | python3 -m json.tool > "$RUN_DIR/meta/stats-before.json"

for file in "$SCN_DIR"/scenario-*.json; do
  name="$(python3 - <<'PY' "$file"
import json,sys
print(json.load(open(sys.argv[1]))['scenario_name'])
PY
)"

  python3 - <<'PY' "$file" "$RUN_DIR/requests/$name-request.json"
import json,sys
src=json.load(open(sys.argv[1]))
json.dump(src['request_payload'], open(sys.argv[2],'w'))
PY

  date -u +"%Y-%m-%dT%H:%M:%SZ" > "$RUN_DIR/meta/$name-timestamp-utc.txt"
  curl -sS http://127.0.0.1:8080/v1/chat/completions \
    -H 'Content-Type: application/json' \
    --data @"$RUN_DIR/requests/$name-request.json" | python3 -m json.tool > "$RUN_DIR/responses/$name-response.json"
done

curl -sS http://127.0.0.1:8080/_lobstertrap/api/stats | python3 -m json.tool > "$RUN_DIR/meta/stats-after.json"
curl -sS http://127.0.0.1:8080/_lobstertrap/api/events | python3 -m json.tool > "$RUN_DIR/meta/events-after.json"
cp "$LOB_DIR/lobstertrap.audit.jsonl" "$RUN_DIR/meta/lobstertrap.audit.jsonl" || true

python3 - <<'PY' "$SCN_DIR" "$RUN_DIR" "$SUITE_DIR/expected/expected-matrix.json"
import json,sys,glob,os
scn_dir,run_dir,exp_file=sys.argv[1],sys.argv[2],sys.argv[3]
expected={e['scenario_name']:e for e in json.load(open(exp_file))}
rows=[]
for scn_file in sorted(glob.glob(os.path.join(scn_dir,'scenario-*.json'))):
    scn=json.load(open(scn_file))
    name=scn['scenario_name']
    resp=json.load(open(os.path.join(run_dir,'responses',f'{name}-response.json')))
    ingress=resp.get('_lobstertrap',{}).get('ingress',{})
    observed_verdict=resp.get('_lobstertrap',{}).get('verdict','<none>')
    observed_rule=ingress.get('rule_name','none')
    exp=expected[name]
    verdict_ok=(observed_verdict==exp['expected_verdict'])
    rule_ok=(observed_rule==exp['expected_policy_match'])
    metadata=ingress.get('detected',{})
    metadata_ok=True
    for k,v in exp['expected_metadata_contains'].items():
        if metadata.get(k)!=v:
            metadata_ok=False
            break
    rows.append({
        'scenario':name,
        'expected_verdict':exp['expected_verdict'],
        'observed_verdict':observed_verdict,
        'expected_rule':exp['expected_policy_match'],
        'observed_rule':observed_rule,
        'verdict_match':verdict_ok,
        'rule_match':rule_ok,
        'metadata_match':metadata_ok,
        'pass': verdict_ok and rule_ok and metadata_ok
    })

json.dump(rows, open(os.path.join(run_dir,'meta','comparison.json'),'w'), indent=2)

with open(os.path.join(run_dir,'meta','comparison.md'),'w') as f:
    f.write('| Scenario | Expected Verdict | Observed Verdict | Expected Rule | Observed Rule | Verdict Match | Rule Match | Metadata Match | Pass |\n')
    f.write('|---|---|---|---|---|---|---|---|---|\n')
    for r in rows:
        f.write(f"| {r['scenario']} | {r['expected_verdict']} | {r['observed_verdict']} | {r['expected_rule']} | {r['observed_rule']} | {r['verdict_match']} | {r['rule_match']} | {r['metadata_match']} | {r['pass']} |\n")
PY

ln -sfn "$RUN_DIR" "$OBS_DIR/latest"
echo "[phase1] complete"
echo "[phase1] comparison: $RUN_DIR/meta/comparison.md"
