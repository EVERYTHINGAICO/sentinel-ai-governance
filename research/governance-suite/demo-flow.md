# Governance Suite Demo Flow

## Recommended Judge Sequence

1. `harmless_request`
- Proves: benign operations remain usable.
- Track support: Track 1 (trusted deployment), judging presentation clarity.

2. `sensitive_file_access`
- Proves: direct sensitive-path access is denied by policy.
- Track support: Track 1 (guardrails/safety), business value.

3. `suspicious_operational_instruction`
- Proves: destructive operational commands are denied.
- Track support: Track 1 (operational safety), originality via concrete risk case.

4. `credential_exfiltration_attempt`
- Proves: exfiltration-pattern requests are denied.
- Track support: Track 1 (security governance), Track 4 relevance via event intelligence potential.

5. `code_execution_attempt`
- Proves: LOG-only governance behavior exists (observability without full block).
- Track support: Track 1 observability, Track 4 data generation for intelligence layer.

6. `escalation_worthy_ambiguous_request`
- Proves: expected escalation target behavior; currently highlights a gap because observed result did not match expected HUMAN_REVIEW.
- Track support: Track 1 governance workflow narrative; this is best shown as a known limitation with planned policy tuning in a later phase.

## Why this order

- Starts with trust-building baseline (ALLOW), then high-confidence DENY controls, then LOG behavior, then ends with one transparent limitation.
- Keeps the demo credible: it shows strengths and one clearly documented boundary condition.

## Track Mapping Summary

- Track 1: directly demonstrated by ALLOW/DENY/LOG controls and policy/audit evidence.
- Track 2: not yet in Phase 1 scope (no Gemini integration by design).
- Track 4: groundwork established through deterministic event generation and reproducible artifacts.
