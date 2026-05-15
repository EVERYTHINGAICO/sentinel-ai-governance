# SENTINEL

SENTINEL is a governance workflow and operational intelligence layer above Veea Lobster Trap.

It does not replace Lobster Trap enforcement. It interprets Lobster Trap outcomes, highlights governance risk, and supports operator review decisions.

## Product Scope

- **Lobster Trap role (enforcement):** prompt/response inspection, policy matching, enforcement verdicts.
- **SENTINEL role (governance):** workflow states, recommendation interpretation, incident evidence clarity, and compact intelligence summaries.

## Why Replay-Based Architecture Is Intentional

SENTINEL currently runs in replay mode to maximize demo reliability and traceability during hackathon execution.

- Source evidence comes from captured Phase 1 Lobster Trap runs.
- Recommendation outputs come from Phase 2 Gemini-schema validation outputs.
- This avoids live integration instability while preserving a truthful operational story.

## Architecture Summary

- **Enforcement engine:** `lobstertrap/` (unchanged)
- **Governance wrapper:** `sentinel-wrapper/public/*`
- **Replay dataset builder:** `sentinel-wrapper/scripts/build_dataset.py`
- **Data source artifacts:**
  - `research/governance-suite/observed/latest/`
  - `research/gemini-validation/outputs/latest/`

## Track Coverage

- **Track 1 — Agent Security & AI Governance**
  - Shows observed policy verdicts, matched rules, and operator governance states.
- **Track 2 — Gemini / AI Studio Workflow Reasoning**
  - Uses Gemini-compatible structured recommendation schema for incident interpretation.
- **Track 4 — Data & Intelligence**
  - Provides compact intelligence summary and searchable/filterable incident list.

## Current Functionality

### Guided Demo Flow

- Landing section explains SENTINEL in one sentence.
- "How this demo works" maps Lobster Trap, Gemini, and SENTINEL roles.
- "How to use this demo" tells judges exactly what to click and compare.
- Scenario order is designed for judges:
  - Harmless Request
  - Sensitive File Access
  - Credential Exfiltration Attempt
  - Escalation Worthy Ambiguous Request

### Governance Workflow

- Per-scenario operator state:
  - `Needs Review`
  - `Approved`
  - `Rejected`
  - `Quarantined`
- Local browser persistence for fast MVP operation.

### Incident Detail

Each scenario shows:
- scenario name
- observed Lobster Trap verdict
- matched policy/rule
- human-readable explanation first
- recommendation explanation
- recommended SENTINEL governance action
- operator review state
- collapsible technical evidence with metadata summary

### Intelligence Summary

- count by observed verdict
- top matched policy
- high-risk event count
- top governance recommendation
- search/filter over scenarios

### Ambiguous Governance Case

Central demo scenario:
- `escalation_worthy_ambiguous_request`
- Lobster Trap observed: `ALLOW`
- SENTINEL recommendation: `HUMAN_REVIEW`

## Run Locally

```bash
sentinel-wrapper/scripts/build_dataset.py
sentinel-wrapper/scripts/serve.sh
```

Open:
- `http://localhost:8787/public/index.html`

## Demo Scenarios Included

- `harmless_request` -> ALLOW
- `sensitive_file_access` -> DENY
- `credential_exfiltration_attempt` -> DENY
- `escalation_worthy_ambiguous_request` -> ALLOW (Lobster Trap), HUMAN_REVIEW (SENTINEL)

## Deployment Strategy (Phase 5)

Selected strategy: **GitHub Pages static hosting**.

Rationale:
- replay-based static files are already complete,
- no backend or database dependency,
- minimal risk and fastest path to public demo URL.

Proposed deployment path:
1. Ensure `sentinel-wrapper/data/scenarios.json` is regenerated.
2. Publish `sentinel-wrapper/public/` and `sentinel-wrapper/data/` as static site content.
3. Verify route: `/public/index.html` and `/data/scenarios.json` are reachable.

No runtime environment variables are required for replay deployment.

## What Is Real vs Replayed

Real:
- Lobster Trap evidence was generated from actual local policy-enforcement runs.

Replayed:
- UI reads stored artifacts rather than live polling.
- recommendation outputs are read from `research/gemini-validation/outputs/latest/`; current local runs may be `real_api`, `mixed_fallback`, or `mock_mode` depending on API key/quota availability.

## Limitations and Future Work

Current limitations:
- replay-only ingestion in UI
- no shared multi-user persistence
- no deployment automation scripts in this phase

Future (post-hackathon) opportunities:
- optional live Lobster Trap feed mode
- optional real Gemini inference mode with key-backed runtime
- minimal backend persistence for team workflows
