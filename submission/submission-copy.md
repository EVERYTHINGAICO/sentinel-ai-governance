# Submission Copy Draft

## Project Title

SENTINEL: Governance Workflow Layer Above Lobster Trap

## Short Description

SENTINEL adds governance workflow states and operational intelligence above Veea Lobster Trap using replay-stable evidence and Gemini-compatible recommendation outputs.

## Long Description

SENTINEL is a lightweight governance workflow and operational intelligence layer built above Veea Lobster Trap. Lobster Trap remains the enforcement engine that performs prompt/response inspection, policy matching, and enforcement actions. SENTINEL does not replace or duplicate those controls.

Our contribution is the layer operators need after enforcement: scenario-level evidence clarity, recommendation context, and explicit review states. The wrapper presents observed Lobster Trap verdicts, matched rules, metadata summaries, and governance recommendations using a structured Gemini-compatible schema. It also highlights ambiguous events where deterministic rules return ALLOW but governance should escalate to HUMAN_REVIEW.

To maximize hackathon reliability and clarity, the current implementation is replay-based. It uses deterministic artifacts generated in Phase 1 and Phase 2 validation, enabling stable demonstrations without introducing unnecessary backend complexity. This produces a clear, testable, and auditable flow suitable for enterprise governance discussions.

## Technologies Used

- Veea Lobster Trap (Go enforcement proxy)
- YAML policy configuration (Lobster Trap policy rules)
- Python scripts (dataset generation and validation harness)
- Static HTML/CSS/JavaScript wrapper UI
- Gemini-compatible structured output schema (mock-mode outputs in current environment)

## Architecture Summary

- Enforcement: Lobster Trap (unchanged)
- Governance wrapper: static replay UI (`sentinel-wrapper/public`)
- Data pipeline: artifact replay from governance suite and gemini-validation outputs
- Review workflow: local operator states (Needs Review, Approved, Rejected, Quarantined)

## Business Value Summary

SENTINEL improves operational decision quality by translating low-level enforcement events into review-ready governance actions. Security teams can quickly identify high-risk incidents, understand policy matches, and handle ambiguous cases with explicit human review steps.

## Originality Summary

The project focuses on the governance gap above enforcement: when to escalate, how to interpret, and how to operationalize policy outcomes. The highlighted ambiguous ALLOW -> HUMAN_REVIEW case demonstrates this layer’s unique value.

## Track Mapping Summary

- Track 1 — Agent Security & AI Governance:
  - policy evidence + operator workflow states + escalation logic
- Track 2 — AI Agents with Gemini / AI Studio:
  - structured recommendation reasoning contract for governance actions
- Track 4 — Data & Intelligence:
  - compact intelligence summaries and searchable incident evidence
