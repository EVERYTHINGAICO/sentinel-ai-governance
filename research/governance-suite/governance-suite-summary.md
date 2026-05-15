# Phase 1 Governance Suite Summary

## Scenario Inventory

- harmless_request
- sensitive_file_access
- code_execution_attempt
- credential_exfiltration_attempt
- suspicious_operational_instruction
- escalation_worthy_ambiguous_request

## Verdict Matrix Summary

Latest run: `research/governance-suite/observed/latest/meta/comparison.md`

- Total scenarios: 6
- Full matches (verdict + rule + metadata): 5
- Mismatches: 1

Mismatch detail:
- `escalation_worthy_ambiguous_request`
  - Expected: `HUMAN_REVIEW` via `review_role_impersonation`
  - Observed: `ALLOW` with no matched rule

## Reproducibility Status

- Runner script exists: `research/governance-suite/scripts/run-suite.sh`
- Runner captures:
  - request payloads
  - response payloads
  - timestamps
  - policy snapshot
  - stats before/after
  - events snapshot
  - copied audit log
  - comparison report
- Latest run is linked at: `research/governance-suite/observed/latest`

Status: `PARTIALLY REPRODUCIBLE` (stable for 5 scenarios, one scenario requires tuning).

## Observed Inconsistencies

1. Escalation ambiguity scenario did not trigger `contains_role_impersonation` policy path.
2. Historical event buffer includes earlier requests, so scenario-specific evidence should rely on per-run response files and comparison report.

## Demo Relevance

- High confidence demo scenarios:
  - harmless_request
  - sensitive_file_access
  - suspicious_operational_instruction
  - credential_exfiltration_attempt
  - code_execution_attempt (LOG path)
- Limitation scenario:
  - escalation_worthy_ambiguous_request (show as known boundary, not hidden)

## Known Limitations

- Current default policy/pattern behavior does not consistently classify the ambiguous role-impersonation scenario as HUMAN_REVIEW.
- Phase 1 intentionally excludes Gemini, SENTINEL UI, workflow queues, and analytics features.

## Recommendation for Phase 2

Proceed to Phase 2 only after confirming a backend/LLM integration contract for the future SENTINEL layer, while preserving this governance suite as regression baseline.
