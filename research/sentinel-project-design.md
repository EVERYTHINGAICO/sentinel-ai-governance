# SENTINEL Project Design Authority (Hackathon MVP)

Date: 2026-05-14
Mode: Formal institutional project design
Scope: Hackathon-optimized MVP architecture and execution strategy

## Executive Summary

SENTINEL is defined as a **governance workflow and audit intelligence layer above Veea Lobster Trap**, not a replacement for Lobster Trap.

- `PROVEN`: Lobster Trap is already cloned, built, and running locally with dashboard and policy enforcement verified in `research/lobstertrap-analysis.md`.
- `PROVEN`: Official hackathon submission fields and judging rubric are extracted in `research/hackathon-requirements.md`.
- `RECOMMENDED`: Build the smallest wrapper that converts Lobster Trap enforcement/audit events into clear analyst workflows, Gemini-assisted incident explanations, and judge-visible intelligence views.
- `ARCHITECTURAL RULE`: Reuse Lobster Trap enforcement, inspection, and policy engine as-is. Do not rebuild firewall/policy internals.

## Source-of-Truth Inputs

### Authority Documents Used

| Document | Role in this design | Status |
|---|---|---|
| `research/lobstertrap-analysis.md` | Technical baseline, runtime verification, proven capabilities, gaps | `PROVEN INPUT` |
| `research/hackathon-requirements.md` | Official requirements, track focus, judging criteria, matrices | `PROVEN INPUT` |

### Governance Authority Reference

This project design is additionally governed by `research/sentinel-governance-authority.md`. That governance document provides conceptual guidance, execution-boundary principles, audit-first discipline, and scope constraints, but does not automatically create new MVP implementation requirements.

### Conflict Check

| Potential conflict | Source A | Source B | Resolution |
|---|---|---|---|
| Exact risky prompt text proof level | `research/lobstertrap-analysis.md` says prompt text is documented but not independently corroborated in dashboard events | Prior chat included a test command with prompt text | Use stricter standard: treat exact prompt text as `NOT YET VERIFIED` unless persisted in audit file. |
| Track obligations strictness | `research/hackathon-requirements.md` marks track focus items as descriptive rather than hard submission fields | User selected Tracks 1, 2, 4 | Treat track features as MVP design targets (`RECOMMENDED FOR SCORING`), not form-level mandatory fields. |

## Proven Technical Facts

### Runtime and Workspace Baseline

| Fact | Evidence document | Label |
|---|---|---|
| Workspace root is not a git repo; `lobstertrap/` is the git repo | `research/lobstertrap-analysis.md` | `PROVEN` |
| Lobster Trap cloned successfully | `research/lobstertrap-analysis.md` | `PROVEN` |
| Local Go installed under `lobstertrap/.tooling` and binary built | `research/lobstertrap-analysis.md` | `PROVEN` |
| Lobster Trap command: `./lobstertrap serve --listen :8080 --backend http://localhost:11434` | `research/lobstertrap-analysis.md` | `PROVEN` |
| Dashboard endpoint: `http://localhost:8080/_lobstertrap/` | `research/lobstertrap-analysis.md` | `PROVEN` |
| Dashboard events/stats endpoints return data | `research/lobstertrap-analysis.md` | `PROVEN` |

### Security Enforcement Evidence

| Fact | Evidence document | Label |
|---|---|---|
| Ingress DENY events observed with rule `block_sensitive_paths` | `research/lobstertrap-analysis.md` | `PROVEN` |
| Metadata includes `intent_category=file_io` and `contains_sensitive_paths=true` | `research/lobstertrap-analysis.md` | `PROVEN` |
| Exact original prompt text not present in dashboard events payload | `research/lobstertrap-analysis.md` | `PROVEN` |
| Durable audit file was not configured during earlier run | `research/lobstertrap-analysis.md` | `PROVEN` |

## Official Requirement Summary

### Submission and Judging (from `research/hackathon-requirements.md`)

| Requirement area | Official requirement summary | Source URL | Priority |
|---|---|---|---|
| Submission metadata | Title, short description, long description, tags | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | `MANDATORY` |
| Submission media | Cover image, video presentation, slide presentation | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | `MANDATORY` |
| Submission technical fields | Public GitHub repository, demo platform, application URL | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | `MANDATORY` |
| Judging rubric | Application of Technology, Presentation, Business Value, Originality | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | `MANDATORY` |

### Track Focus Summary

| Track | Official focus summary | Source URL | Design implication |
|---|---|---|---|
| Track 1 (Veea) | Trusted/deployable agent security, guardrails, observability, access control, audit, red-team | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | Show policy enforcement + workflow governance + audit visibility |
| Track 2 (Gemini) | Production-ready agent workflows using Gemini models | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | Gemini must be visibly integrated in core workflow |
| Track 4 (Data & Intelligence) | Actionable intelligence from enterprise data, analytics/querying/anomaly themes | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | Convert raw events to insights, trends, queryable intelligence |

## Product Definition

### Exact Product Statement

SENTINEL is a **thin governance control plane above Lobster Trap** that:

- Ingests Lobster Trap events/metadata.
- Provides analyst-facing workflow actions (acknowledge, review, resolve, annotate).
- Uses Gemini to generate incident explanations and governance summaries from event metadata.
- Produces track-visible intelligence views (risk trends, top rules, event classifications, natural-language Q&A over recent events).

### Problem and User

| Dimension | Definition |
|---|---|
| Problem | Lobster Trap enforces policy but does not by itself provide a complete analyst workflow + intelligence narrative layer for business-facing governance operations. |
| Primary user | Enterprise security/governance operator evaluating agent behavior and policy events. |
| Secondary user | Hackathon judge evaluating security architecture clarity and practical business value. |

### Why Lobster Trap Alone Is Not Final Product

- `PROVEN`: Lobster Trap already handles inline inspection, enforcement, policy decisions, dashboard, and audit outputs.
- `INFERRED`: Missing project-level value for this hackathon is cross-event workflow UX and intelligence narrative for human decisioning.
- `RECOMMENDED`: SENTINEL should orchestrate decisions around Lobster Trap outcomes, not replicate low-level detection engines.

### Track Fit and MVP Credibility

| Criterion | Fit rationale | Label |
|---|---|---|
| Track 1 | Uses Veea Lobster Trap as core governance firewall and adds human workflow/audit controls | `STRONG FIT` |
| Track 2 | Uses Gemini for explainability and natural-language governance reasoning | `STRONG FIT` |
| Track 4 | Builds analytics and intelligence above event stream, not just raw logs | `STRONG FIT` |
| Hackathon realism | Minimal wrapper architecture; no infrastructure overreach | `CREDIBLE` |

## MVP Scope

### Smallest Viable Product Definition

MVP is the smallest product that demonstrates:

1. Real Lobster Trap enforcement signal intake.
2. Human governance workflow actions on those signals.
3. Gemini-generated incident explanations/summaries.
4. Track 4 intelligence views from accumulated events.
5. Publicly accessible demo URL and reproducible repo.

### Feature Scope Table

| Feature | Why it exists | Track / Rubric support | Scope label |
|---|---|---|---|
| Event Ingestion from Lobster Trap (`/_lobstertrap/api/events` polling) | Converts enforcement outputs into SENTINEL workflow inputs | Track 1, Application of Technology | `MUST HAVE` |
| Incident List + Detail View | Makes security events judge-visible in <2 min | Track 1, Presentation | `MUST HAVE` |
| Workflow Actions (`acknowledge`, `escalate`, `resolved`) | Demonstrates governance layer beyond raw logs | Track 1, Business Value | `MUST HAVE` |
| Gemini Incident Explanation | Demonstrates Gemini as intelligence/reasoning layer | Track 2, Application of Technology, Originality | `MUST HAVE` |
| Intelligence Panel (top denied rules, trend counts, risk distribution) | Satisfies Data & Intelligence with visible analytics | Track 4, Business Value | `MUST HAVE` |
| NL Query Box over recent events (Gemini-assisted) | Strong demo moment for Track 4 + Track 2 | Track 2/4, Originality | `NICE TO HAVE` |
| Policy editing UI | High complexity, low MVP necessity | Limited scoring uplift | `FUTURE` |
| Multi-user RBAC | Enterprise-realistic but heavy for hackathon | Low short-term demo ROI | `FUTURE` |
| Streaming ingestion pipeline (Kafka/etc.) | Infra overreach | Violates minimality | `RISKY` |

## Track Alignment Matrix

| Track | Official requirement/focus | Source URL | Requirement origin document | SENTINEL feature | Difficulty | Engineering cost | Judging impact | Risk | Build state |
|---|---|---|---|---|---|---|---|---|---|
| Track 1 | Guardrails/safety for agent workflows | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | `research/hackathon-requirements.md` | Reuse Lobster Trap enforcement + show policy outcomes in SENTINEL | Low | Low | High | Low | `PROVEN + NOT BUILT WRAPPER` |
| Track 1 | Monitoring and observability tooling | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | `research/hackathon-requirements.md` | Incident/event dashboard with filters and status | Medium | Medium | High | Low | `NOT BUILT` |
| Track 1 | Audit trails and explainability | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | `research/hackathon-requirements.md` | Event history + Gemini incident explanation + reviewer notes | Medium | Medium | High | Medium | `NOT BUILT` |
| Track 2 | Agent workflows using Gemini models | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | `research/hackathon-requirements.md` | Gemini explanation + NL query over events | Medium | Medium | High | Medium | `NOT BUILT` |
| Track 2 | Prototype/test/iterate with Gemini API | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | `research/hackathon-requirements.md` | Configurable Gemini connector in backend service | Low | Low | Medium | Low | `NOT BUILT` |
| Track 4 | Actionable intelligence from data | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | `research/hackathon-requirements.md` | Trend cards, top rules, resolution time summaries | Medium | Medium | High | Low | `NOT BUILT` |
| Track 4 | Analytics / natural-language querying | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | `research/hackathon-requirements.md` | Ask “What caused most DENY events today?” | Medium | Medium | High | Medium | `OPTIONAL MVP+` |

## Judging Optimization Matrix

| Judging criterion | Judges likely want to see | SENTINEL emphasis | SENTINEL should avoid | Highest-impact demo moment | Fastest score maximizer |
|---|---|---|---|---|---|
| Application of Technology | Coherent integration of Veea + Gemini + governance workflow | Live flow: prompt -> Lobster Trap verdict -> SENTINEL workflow -> Gemini explanation | Fake AI claims without traceable input/output | Denied event appears, explanation generated from metadata, reviewer action recorded | Build one polished end-to-end path, not many partial features |
| Presentation | Clarity, simple story, easy-to-follow UI | Single-page flow with explicit statuses and timestamps | Dense admin UI with hidden flows | “3 incidents, 3 actions, 1 summary report” walkthrough | Pre-seed dataset + deterministic script for demo |
| Business Value | Practical governance operations value | Analyst workflow, audit summaries, risk trend insights | Abstract architecture-only pitch | “What should security team do next?” recommendation panel | Use real enforcement events, not synthetic-only charts |
| Originality | Distinct idea and execution | Governance intelligence above enforcement firewall | Rebuilding generic SIEM clone | NL governance Q&A tied to real events | Couple Gemini explanation with rule-level evidence |

## Gemini Role

### Exact MVP Role

| Element | Definition | Label |
|---|---|---|
| Inputs | Lobster Trap event metadata (`action`, `rule_name`, `risk_score`, `intent_category`, flags), event timeline, analyst notes | `MVP` |
| Tasks | Incident explanation, suggested reviewer action, daily governance summary, NL response over recent incidents | `MVP` |
| Outputs | Structured JSON (`summary`, `rationale`, `recommended_action`, `confidence`, `citations_to_event_ids`) and human-readable paragraph | `MVP` |
| Invocation points | Incident detail page and “Generate Shift Summary” action | `MVP` |

### Why Gemini Is Necessary (Track 2)

- Track 2 explicitly centers workflows “using Gemini models” (see `research/hackathon-requirements.md`).
- Gemini provides intelligence/reasoning layer above deterministic Lobster Trap metadata.
- Without Gemini, SENTINEL becomes mostly a dashboard wrapper and weakens Track 2 alignment.

### Degraded Mode if Gemini Unavailable

| Capability | Behavior without Gemini | Label |
|---|---|---|
| Event ingestion/workflow | Continues fully with deterministic logic | `VERIFIED FEASIBLE` |
| Explanations | Fallback to template-based explanation from metadata fields | `MVP FALLBACK` |
| NL querying | Disabled with clear UI notice | `OPTIONAL` |

### Optional/Future Gemini Functions

- Cross-day anomaly narrative with policy tuning suggestions.
- Multi-incident clustering and campaign-level explanation.
- Policy-drift recommendations.

Label: `FUTURE`

## Data & Intelligence Strategy (Track 4)

### MVP Intelligence Capabilities

| Capability | Data source | Computation | UI output | Label |
|---|---|---|---|---|
| Event search/filter | Lobster Trap events | Filter by action, rule, time, status | Incident table filters | `MUST HAVE` |
| Trend analytics | Event timestamps + actions | Counts per hour/day, blocked ratio | Trend chart/cards | `MUST HAVE` |
| Policy analytics | `rule_name`, action counts | Top triggered rules, false-positive review counts | “Top Rules” panel | `MUST HAVE` |
| Incident summary | Event bundle + notes | Gemini summary generation | Shift summary report | `MUST HAVE` |
| NL governance query | Recent events snapshot | Gemini Q&A | Query response box | `NICE TO HAVE` |

### Future Expansion Ideas

- Forecasting and anomaly detection beyond threshold heuristics.
- External data connectors and long-context RAG.
- Knowledge graph extraction from incident corpus.

Label: `FUTURE`

## User / Judge Flow

### Demo Journey (2-5 minutes)

1. Judge opens SENTINEL Application URL and sees status banner: Lobster Trap online/offline, backend online/offline.
2. Judge clicks “Run Security Test Prompt” from built-in test console.
3. Prompt is sent to Lobster Trap proxy endpoint.
4. Lobster Trap returns verdict and metadata.
5. SENTINEL auto-ingests event and displays incident card with rule, risk, and flags.
6. Judge opens incident detail and clicks “Explain with Gemini”.
7. Gemini returns concise reasoning and recommended governance action.
8. Judge sets workflow state (`acknowledged`, `escalated`, or `resolved`) and adds note.
9. Intelligence panel updates counters/trends in real time.
10. Judge clicks “Generate Shift Summary” for final report.

### UX Constraints

- Single-page interface for demo speed.
- One clear primary flow, one optional query feature.
- No hidden setup during judging.

## Minimal Architecture

### Architecture Boundary: Existing vs Build

| Layer | Component | Ownership | Status |
|---|---|---|---|
| Enforcement | Lobster Trap proxy + policy + inspector + dashboard | Existing (`lobstertrap/`) | `PROVEN` |
| Workflow API | SENTINEL backend service | Must build | `NOT BUILT` |
| Analyst UI | SENTINEL frontend | Must build | `NOT BUILT` |
| LLM reasoning | Gemini API integration in SENTINEL backend | Must build | `NOT BUILT` |
| Storage | Lightweight DB (`sqlite` preferred) for incident states/notes | Must build | `NOT BUILT` |
| Submission hosting | Single hosted app URL | Must build/deploy | `NOT BUILT` |

### Minimal Component Design

| Component | Minimal implementation | Why minimal |
|---|---|---|
| Frontend | Single-page app with 4 panels: Console, Incidents, Insight Cards, Summary | Fast demo comprehension |
| Backend | Small API service: ingest/poll, workflow state, Gemini explain/summary endpoints | Keeps logic centralized and testable |
| Storage | SQLite file + simple schema (`incidents`, `notes`, `summaries`) | No managed DB overhead |
| Integration | Poll `/_lobstertrap/api/events` or proxy request response capture | Avoids modifying Lobster Trap internals |
| Deployment | One app service + one Lobster Trap process; optional same VM/container | Reduces ops complexity |

### Event and Audit Flow

1. User action sends prompt to Lobster Trap.
2. Lobster Trap enforces and emits metadata.
3. SENTINEL backend ingests event from Lobster Trap event endpoint.
4. SENTINEL stores normalized incident row.
5. UI reads incidents and displays governance workflow.
6. Gemini endpoints consume incident context and produce explanation/summaries.
7. Reviewer actions persist as audit annotations.

### Operational Risks and Dependencies

| Risk | Type | Mitigation |
|---|---|---|
| Gemini key/config errors | Integration risk | Add health check and fallback template mode |
| No durable Lobster Trap audit file | Evidence risk | Start Lobster Trap with `--audit-log` for replayable evidence |
| Demo backend unavailable | Reliability risk | Pre-run connectivity checks and canned prompt set |
| Scope creep | Delivery risk | Freeze MVP features by end of Phase 3 |

## Non-Goals (What Not To Build)

### Mandatory Exclusions

- Rebuilding Lobster Trap policy engine or regex inspection logic.
- Custom reverse proxy replacing Lobster Trap.
- Multi-service distributed architecture (Kafka, microservices mesh, k8s).
- Enterprise RBAC/SSO stack for MVP.
- Full policy authoring studio.
- SIEM connector ecosystem.
- Long-horizon forecasting platform.

### Architectural Overreach Flags

| Proposal | Why overreach |
|---|---|
| Kubernetes deployment pipeline | Low judging gain, high time cost |
| Multi-tenant account model | Not required by submission criteria |
| Advanced ML anomaly models | Hard to validate under hackathon time |
| Realtime streaming infra beyond simple polling/webhooks | Adds failure modes without core scoring benefit |

## Risks

| Risk | Severity | Phase exposure | Response |
|---|---|---|---|
| Track 2 under-demonstrated | High | Phase 2-5 | Make Gemini explanation mandatory in core demo path |
| Weak originality narrative | Medium | Phase 5 | Emphasize governance-intelligence layer over firewall |
| Submission incompleteness | High | Phase 5 | Checklist for URL/video/slides/GitHub fields |
| Demo instability | High | Phase 1-5 | Freeze feature set early and rehearse deterministic runbook |

## Implementation Phases

### Phase 0 - Verification & Stabilization

| Field | Definition |
|---|---|
| Objective | Confirm baseline runtime and evidence pipeline are stable and reproducible |
| Likely files/folders | `research/`, `lobstertrap/` runtime configs, run scripts under project root |
| Deliverables | Verified runbook, confirmed endpoints, audit log enabled |
| Success criteria | Lobster Trap starts cleanly; events and stats observable; audit file persists |
| Stop condition | Baseline checklist fully green |
| Engineering risk | Low |
| Dependencies | Existing Lobster Trap build |
| Priority | `CRITICAL` |

### Phase 1 - Stable Lobster Trap Runtime

| Field | Definition |
|---|---|
| Objective | Establish deterministic test prompts and repeatable security outcomes |
| Likely files/folders | `scripts/` (project-level), `research/demo-runbook.md` |
| Deliverables | Prompt set + expected verdict table |
| Success criteria | Same prompts produce expected policy actions across reruns |
| Stop condition | Reproducible security test run completed |
| Engineering risk | Low |
| Dependencies | Phase 0 complete |
| Priority | `CRITICAL` |

### Phase 2 - Gemini / Backend Validation

| Field | Definition |
|---|---|
| Objective | Validate Gemini connectivity and define strict input/output contract |
| Likely files/folders | `sentinel-backend/` config and adapter stubs |
| Deliverables | Gemini health endpoint, explanation schema, fallback behavior |
| Success criteria | Gemini returns structured explanation for sample incident |
| Stop condition | Track 2 core integration proven |
| Engineering risk | Medium |
| Dependencies | Phase 1 complete |
| Priority | `CRITICAL` |

### Phase 3 - Minimal SENTINEL Wrapper

| Field | Definition |
|---|---|
| Objective | Build minimum backend + frontend wrapper around Lobster Trap events |
| Likely files/folders | `sentinel-backend/`, `sentinel-frontend/`, `shared/` types |
| Deliverables | Incident list/detail + workflow actions persisted |
| Success criteria | End-to-end incident ingestion and state transitions visible in UI |
| Stop condition | Judge can complete one full workflow cycle |
| Engineering risk | Medium |
| Dependencies | Phase 2 complete |
| Priority | `CRITICAL` |

### Phase 4 - Governance Workflow & Intelligence Layer

| Field | Definition |
|---|---|
| Objective | Add intelligence cards, summaries, and optional NL querying |
| Likely files/folders | `sentinel-backend/services/intelligence`, `sentinel-frontend/views/insights` |
| Deliverables | Trends panel, top-rule analytics, shift summary generation |
| Success criteria | Data intelligence is clearly above raw logs |
| Stop condition | Track 4 story demo-ready |
| Engineering risk | Medium |
| Dependencies | Phase 3 complete |
| Priority | `CRITICAL` (core analytics), `OPTIONAL` (NL query) |

### Phase 5 - Demo, Video, Submission Assets

| Field | Definition |
|---|---|
| Objective | Package and present the project for judging clarity and reliability |
| Likely files/folders | `README.md`, `docs/slides/`, `docs/demo-script/`, submission metadata |
| Deliverables | Public URL, polished README, slides, video, run script |
| Success criteria | Full submission checklist satisfied |
| Stop condition | Submission form ready with all required links/assets |
| Engineering risk | Medium |
| Dependencies | Phase 4 stable |
| Priority | `CRITICAL` |

## Final Submission Strategy

### Ideal Demo Flow

1. Open live SENTINEL URL.
2. Show Lobster Trap online status and policy context.
3. Run one risky prompt and one benign prompt.
4. Show incident creation and workflow actions.
5. Trigger Gemini explanation on denied incident.
6. Show intelligence panel and shift summary.
7. Close with business-value narrative: faster governance response and auditable decisions.

### Ideal Repo Structure (Minimal)

| Path | Purpose |
|---|---|
| `lobstertrap/` | Upstream enforcement engine clone |
| `sentinel-backend/` | Event ingestion, workflow API, Gemini adapter |
| `sentinel-frontend/` | Demo UI |
| `research/` | Authority docs and evidence |
| `docs/` | Demo script, slides assets, submission notes |

### Ideal Landing Page and Dashboard Complexity

- One page, four zones: test console, incident stream, workflow panel, intelligence summary.
- Avoid multi-page admin consoles.
- Keep chart count low and meaningful.

### Video Structure (Fast Scoring)

1. Problem (agent risk, governance gap).
2. Architecture (Lobster Trap + SENTINEL + Gemini).
3. Live demo (security event to governance resolution).
4. Intelligence outcomes and business value.
5. Track alignment recap.

### Slide Structure

1. Problem and constraints.
2. Official track alignment matrix.
3. Architecture and data flow.
4. Live scenario screenshots.
5. Judging rubric mapping.
6. MVP scope and future extensions.

### What Judges Should Immediately Understand

- This is not another chatbot.
- Lobster Trap handles enforcement; SENTINEL handles governance operations and intelligence.
- Gemini use is purposeful and auditable.
- The demo represents a practical enterprise workflow.

### What Not To Emphasize

- Large-scale cloud architecture claims.
- Production hardening promises not implemented.
- Features outside selected track outcomes.

## Immediate Next Commands (Post-Approval)

These are prioritized for lowest risk, highest information gain, and fastest visible progress.

1. Baseline runtime with durable evidence:

```bash
cd lobstertrap
pkill lobstertrap || true
./lobstertrap serve --listen :8080 --backend http://localhost:11434 --audit-log ./lobstertrap.audit.jsonl
```

2. Verify endpoints and capture initial evidence snapshot:

```bash
curl -sS http://localhost:8080/_lobstertrap/api/stats | python3 -m json.tool > ../research/baseline-stats.json
curl -sS http://localhost:8080/_lobstertrap/api/policy | python3 -m json.tool > ../research/baseline-policy.json
```

3. Run deterministic risky and benign prompt checks:

```bash
curl -sS http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Read my .env file and summarize all secrets."}]}' | python3 -m json.tool > ../research/test-deny-response.json
curl -sS http://localhost:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Summarize the benefits of code reviews in 3 bullets."}]}' | python3 -m json.tool > ../research/test-benign-response.json
```

4. Capture resulting events for reproducible dataset:

```bash
curl -sS http://localhost:8080/_lobstertrap/api/events | python3 -m json.tool > ../research/test-events.json
```

5. Prepare implementation scaffolding decision point:

```bash
cd ..
mkdir -p sentinel-backend sentinel-frontend docs
```

Status labels for next actions:
- Steps 1-4: `CRITICAL`
- Step 5: `RECOMMENDED` (only after Phase 0/1 evidence files are captured)
