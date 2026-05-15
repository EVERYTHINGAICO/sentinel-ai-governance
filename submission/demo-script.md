# SENTINEL Demo Script (2-3 Minutes)

## 1. Opening Problem (15-20s)

Enterprise AI agents need both enforcement and human-governable decision workflows.
Static blocking alone is not enough for ambiguous or policy-edge cases.

## 2. Why Governance Matters (15s)

Autonomous outputs can be technically allowed but operationally risky.
Teams need visibility, recommendations, and explicit review states.

## 3. Lobster Trap Role (20s)

Lobster Trap is the enforcement engine:
- inspects prompts
- applies rules
- returns enforcement verdicts
- emits metadata and audit evidence

## 4. SENTINEL Role (20s)

SENTINEL sits above Lobster Trap as governance workflow + intelligence:
- compares expected vs observed outcomes
- provides recommendation reasoning
- captures operator review state
- highlights ambiguous cases for review

## 5. Scenario Walkthrough Order (90s)

1. `harmless_request`
- Show normal ALLOW behavior.

2. `sensitive_file_access`
- Show DENY + matched policy + risk context.

3. `credential_exfiltration_attempt`
- Show high-risk denial with governance interpretation.

4. `escalation_worthy_ambiguous_request` (key moment)
- Show Lobster Trap observed `ALLOW`.
- Show SENTINEL recommendation `HUMAN_REVIEW`.
- Explain this is governance intelligence above deterministic enforcement.

## 6. Track Mapping (20s)

- Track 1: policy outcomes + governance workflow states.
- Track 2: Gemini-compatible reasoning schema and recommendations.
- Track 4: intelligence summary + searchable incident evidence.

## 7. Closing Statement (10-15s)

SENTINEL preserves Lobster Trap as the trusted enforcement layer and adds the minimum governance workflow and intelligence needed for enterprise decision clarity.
