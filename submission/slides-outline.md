# Slides Outline

## 1. Problem
- Enterprise AI agents produce outputs that are policy-safe yet operationally risky.
- Deterministic enforcement engines block known-bad patterns — but cannot escalate ambiguous cases.
- Security teams need governance workflow above enforcement: review states, reasoning, and audit trails.

## 2. Why AI Governance Matters
- Deterministic blocking is necessary but not sufficient.
- A prompt can match zero policy rules and still carry governance risk (role impersonation, intent drift).
- Human review paths are required for the ambiguous middle ground.

## 3. Lobster Trap Enforcement Layer
- Inline enforcement architecture: sits between AI agents and language model backends.
- Prompt/response inspection, regex-based deep packet inspection, policy matching.
- Verdict emission: ALLOW, DENY, LOG, HUMAN_REVIEW, QUARANTINE.
- Works with any OpenAI-compatible AI backend — including Ollama and local LLMs.

## 4. SENTINEL Governance Layer
- What SENTINEL adds without replacing Lobster Trap.
- Ingests enforcement verdicts, metadata, and matched-rule evidence.
- Converts low-level events into operator-reviewable governance incidents.
- Explicit workflow states: Needs Review, Approved, Rejected, Quarantined.
- Governance suite as deterministic red-team harness: reproducible adversarial scenario replay.

## 5. Gemini Intelligence Role
- Gemini receives: Lobster Trap verdict, matched rule, metadata flags, prompt context.
- Gemini returns: incident summary, risk level, recommended SENTINEL verdict, reasoning, operator next step.
- Replay-stable pre-validated outputs for demo reliability.
- Real Gemini API confirmed working (GEMINI_API_KEY mode available in production).
- Google ADK integration: SENTINEL MCP server as native Gemini toolset via MCPToolset.

## 6. Workflow Demo
- Scenario order and key outcomes:
  1. harmless_request → ALLOW / SENTINEL ALLOW
  2. sensitive_file_access → DENY / SENTINEL DENY
  3. credential_exfiltration_attempt → DENY / SENTINEL DENY
  4. escalation_worthy_ambiguous_request → Lobster Trap ALLOW / SENTINEL HUMAN_REVIEW ← KEY MOMENT
- The ambiguous case: role impersonation passes all regex rules, Gemini identifies governance risk.

## 7. Architecture
- Governance pipeline: Phase 1 (6 adversarial scenarios → Lobster Trap) → Phase 2 (Gemini reasoning) → scenarios.json
- Review dashboard: static governance UI reading captured evidence
- Audit-grade reproducibility: same enforcement evidence, same Gemini reasoning, same operator flow every run.

## 7b. MCP Integration — Vendor-Neutral Governance
- SENTINEL MCP server: 10 governance tools, stdio transport, zero infrastructure overhead.
- Works with: Claude (Claude Desktop/Code), GPT-4o (OpenAI Agents SDK), Gemini (Google ADK), Llama 3.x (Ollama).
- Enterprise value: same governance tools available regardless of which AI vendor the organization uses.
- `/sentinel` command in Claude Code → guided step-by-step governance workflow.
- Natural language querying of SENTINEL incident data via any connected AI — Track 4 analytics agent pattern.

## 8. Business Value
- Faster triage clarity: raw enforcement verdicts become reviewable governance incidents.
- Better governance accountability: explicit operator states with Gemini-assisted reasoning.
- Vendor-neutral MCP layer: governance tools work with Claude, GPT-4o, Gemini, or local Llama.
- No vendor lock-in: SENTINEL governance is accessible from whatever AI the enterprise deploys.

## 9. Future Roadmap
- Live Lobster Trap event polling (currently replay-stable captured evidence).
- Persistent operator review queue with SQLite or lightweight backend.
- MCP server shipped ✓ — roadmap: live event feed integration and NL query over real-time incidents.
- Optional enterprise integrations: SIEM connectors, Slack/Jira workflow triggers, RBAC.
