# Submission Copy Draft

## Project Title

SENTINEL: AI Governance Intelligence Layer Above Lobster Trap

## Short Description

SENTINEL adds governance workflow states, Gemini-powered incident reasoning, and vendor-neutral MCP tooling above Veea Lobster Trap enforcement — turning raw policy verdicts into operator-ready governance decisions.

## Long Description

SENTINEL is an AI governance intelligence layer built above Veea Lobster Trap. Lobster Trap remains the enforcement engine: it performs inline prompt and response inspection, policy matching, and enforcement actions. SENTINEL does not replace or duplicate those controls.

Our contribution is the governance layer that operators need after enforcement: scenario-level evidence clarity, Gemini-generated reasoning, explicit operator review states, and a vendor-neutral MCP integration that makes all governance tools accessible from any enterprise AI platform — Claude, GPT-4o, Gemini, or on-premise Llama models.

The core demo moment: when Lobster Trap returns ALLOW for an ambiguous role-impersonation prompt, SENTINEL's Gemini reasoning escalates it to HUMAN_REVIEW. This ALLOW→HUMAN_REVIEW escalation is the governance gap that deterministic enforcement engines leave, and the insight SENTINEL operationalizes.

The SENTINEL MCP server exposes 10 governance tools over the standard stdio protocol, pre-integrated with Google ADK (Gemini), OpenAI Agents SDK (GPT-4), Claude Code, and Ollama-backed local AI clients. Enterprise teams can invoke SENTINEL governance workflows from whichever AI assistant they already use — with no vendor lock-in.

The governance review dashboard presents captured enforcement evidence, Gemini-structured recommendations, and operator workflow states (Needs Review, Approved, Rejected, Quarantined). Replay-stable captured artifacts enable audit-grade reproducibility for governance demonstrations.

## Technologies Used

- Veea Lobster Trap (Go enforcement proxy — inline policy inspection and verdict emission)
- YAML policy configuration (Lobster Trap rule engine)
- Gemini API via Google AI Studio (structured governance reasoning and incident recommendations)
- SENTINEL MCP Server (Python, stdio transport) — 10 governance tools callable from any MCP-compatible AI
- Compatible AI clients: Claude (Anthropic), GPT-4o (OpenAI Agents SDK), Gemini 2.x (Google ADK), Llama 3.x (Ollama)
- Python governance pipeline (evidence capture, Gemini validation harness, dataset builder)
- Static HTML/CSS/JavaScript governance review dashboard

## Architecture Summary

- Enforcement layer: Lobster Trap (unchanged upstream engine)
- Governance pipeline: Phase 1 (governance suite) → Phase 2 (Gemini validation) → scenarios.json dataset
- Review dashboard: operator-facing governance UI (`sentinel-wrapper/public`)
- Operator workflow states: Needs Review, Approved, Rejected, Quarantined
- MCP integration: `sentinel-mcp/` server bridges 10 SENTINEL governance tools to any AI agent (Google ADK, OpenAI Agents SDK, Claude Code, Ollama)

## Business Value Summary

SENTINEL makes Lobster Trap enforcement outcomes governable at enterprise scale. Security operators move from raw enforcement logs to reviewable incident workflows with Gemini-assisted reasoning. The SENTINEL MCP server extends this governance capability to any AI agent an enterprise deploys — Claude, GPT-4o, Gemini, or on-premise Llama models — eliminating vendor lock-in in the governance layer. The ALLOW→HUMAN_REVIEW escalation path fills the gap that deterministic policy engines leave: prompts that pass rule-matching but carry governance risk.

## Originality Summary

SENTINEL addresses the governance gap that deterministic enforcement engines leave: a prompt can pass all policy rules and still be operationally risky. The ALLOW→HUMAN_REVIEW escalation demonstrates this gap concretely with real Lobster Trap enforcement evidence. The SENTINEL MCP server introduces vendor-neutral governance tooling — the same 10 governance tools work identically whether the operator AI is Claude, GPT-4o, Gemini, or a local Llama model. This multi-AI-compatible governance layer architecture is novel in enterprise AI security tooling.

## Track Mapping Summary

- Track 1 — Agent Security & AI Governance:
  - Policy enforcement evidence + operator HUMAN_REVIEW workflow states
  - Governance suite as deterministic red-team harness: reproducible adversarial scenario replay
  - Audit-grade captured evidence across 6 governance scenarios

- Track 2 — AI Agents with Gemini / AI Studio:
  - Gemini API generates structured incident reasoning (risk level, recommended verdict, operator next step)
  - Google ADK integration: SENTINEL MCP server as native Gemini toolset via MCPToolset
  - Production-ready Gemini agent workflow: any ADK agent can invoke sentinel_run_pipeline, sentinel_inspect_scenarios, and all 10 tools

- Track 4 — Data & Intelligence:
  - Structured analytics above raw enforcement logs: verdict summaries, top triggered rules, risk distributions
  - MCP server enables natural language querying of SENTINEL incident data by any connected AI (analytics agent pattern)
  - Searchable governance evidence with operator state tracking
