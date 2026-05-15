# SENTINEL — Official Hackathon Requirements (Extracted Only)

This file contains **only** requirements and track descriptions found in the official sources listed below. Anything labeled “Interpretation” is not an official requirement.

## Official Sources Used (URLs)

- Hackathon page: `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon`
- LabLab “Hackathon Guidelines” article (linked from the hackathon page): `https://lablab.ai/ai-articles/hackathon-guidelines`
- Veea press release: `https://www.veea.com/news/press-releases/item/208649410918`
- Veea Lobster Trap tech page: `https://lablab.ai/tech/veea/lobster-trap`
- Lobster Trap repo: `https://github.com/veeainc/lobstertrap`

---

## 1) Submission / Demo / GitHub / Application URL / Judging (Official)

### Submission fields (from hackathon page)

Official requirement (close paraphrase of bullet list) from `.../techex-intelligent-enterprise-solutions-hackathon`:
- Basic info: “Project Title”, “Short Description”, “Long Description”, “Technology & Category Tags”
- Media: “Cover Image”, “Video Presentation”, “Slide Presentation”
- Technical: “Public GitHub Repository”, “Demo Application Platform”, “Application URL”

Judging criteria (quoted headings + definitions) from the same page:
- “Application of Technology” — “How effectively the chosen model(s) are integrated into the solution.”
- “Presentation” — “The clarity and effectiveness of the project presentation.”
- “Business Value” — “The impact and practical value… how well it fits into business areas.”
- “Originality” — “The uniqueness & creativity… ability to demonstrate behaviors.”

### Additional submission constraints (official LabLab guidelines article; may be guidance)

From `https://lablab.ai/ai-articles/hackathon-guidelines` (official LabLab content):
- Title length: “max 50 characters”
- Short description length: “max 255 characters”
- Long description: “minimum 100 words”
- Video presentation: “under 300MB and within 5 minutes duration”
- Technical details include: GitHub repo link, demo platform, and a “direct URL to your live application demo”

---

## 2) Track-Specific Requirements We Must Not Forget

Important: the hackathon page presents these as **tracks + focus areas**. It does not explicitly state additional mandatory deliverables per track beyond the global submission fields above.

### TRACK 1 — Agent Security & AI Governance / Veea

From `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon`:
- Track name: “Track 1: Agent Security & AI Governance”
- Description: “Build AI systems that enterprise security teams can actually trust and deploy.”
- “Powered by: Veea”
- Focus areas include (close paraphrase of bullets):
  - “Guardrails and safety layers for agentic workflows”
  - “Monitoring and observability tools for AI agents…”
  - “Access control and permission frameworks…”
  - “Audit trails and explainability tooling…”
  - “Red-teaming frameworks… adversarial inputs”

What Veea/Lobster Trap expects (official statements from Veea press release):
- Lobster Trap “runs inline between AI agents and the language models they communicate with.” (`https://www.veea.com/news/press-releases/item/208649410918`)
- If a violation is detected, it can “block”, “flag… for review”, or “log… for analysis.” (`https://www.veea.com/news/press-releases/item/208649410918`)
- Out of the box, it detects “prompt injection… credential exposure… personal information leakage… suspicious file access… data exfiltration patterns.” (`https://www.veea.com/news/press-releases/item/208649410918`)
- It “works with AI backends that use the standard OpenAI-compatible interface.” (`https://www.veea.com/news/press-releases/item/208649410918`)

Veea Lobster Trap “don’t forget” deployment notes (official LabLab Veea tech page):
- “Three ways to run Lobster Trap” (standalone build, pre-built binary, Native.Builder packaged). (`https://lablab.ai/tech/veea/lobster-trap`)
- “No API keys, signups, rate limits, or cloud dependency required…” (`https://lablab.ai/tech/veea/lobster-trap`)
- Tooling the page highlights: `./lobstertrap test` and `./lobstertrap inspect "<your prompt>"`. (`https://lablab.ai/tech/veea/lobster-trap`)

### TRACK 2 — AI Agents with Google AI Studio / Gemini

From `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon`:
- Track name: “Track 2: AI Agents with Google AI Studio”
- Description: “Build production-ready agent workflows using Gemini models.”
- “Powered by: Google DeepMind & Google AI Studio”
- Focus areas include:
  - “Multi-agent systems using Gemini”
  - “Long-context document processing…”
  - “Code generation… workflow agents”
  - “Internal AI tools…”
  - “Enterprise integrations…”

From the same hackathon page “Technology partners” section:
- “Google AI Studio is a browser-based environment… prototype, test, and iterate with Gemini models… integrating… using the Gemini API.”

### TRACK 4 — Data & Intelligence

From `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon`:
- Track name: “Track 4: Data & Intelligence”
- Description: “Turn enterprise data into actionable intelligence.”
- Focus areas include:
  - “RAG systems over proprietary or multi-source data”
  - “AI-powered data pipelines and validation”
  - “Analytics agents for natural language querying”
  - “Anomaly detection and forecasting”
  - “Knowledge graph extraction from documents”

---

## 3) Requirements Matrix (Requirement | Official Source URL | Practical Meaning | Possible SENTINEL Feature)

| Requirement (official) | Official Source URL | Practical Meaning (Interpretation) | Possible SENTINEL Feature (Interpretation) |
|---|---|---|---|
| Public GitHub Repository | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | Repo must be public and contain the project code | Public repo with `README` run steps + infra as code |
| Demo Application Platform | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | You must say where it’s deployed/hosted | Deploy governance UI/API somewhere (lightweight) |
| Application URL | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | Must provide a working link to the demo | Live dashboard for policies/audit insights |
| Video Presentation | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | Must provide a demo/pitch video link | 3–5 min demo showing block/review/audit |
| Slide Presentation | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | Must provide slides | Slides: threat model, policy flow, architecture |
| Judging: Application of Technology | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | Integration of chosen model(s) matters | Demonstrate Gemini agent workflow + Lobster Trap proxy |
| Track 1 focus: guardrails/observability/access control/audit/red-team | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | Project should align with these outcomes | Human review queue + audit intelligence + drift reports |
| Track 2: “using Gemini models” | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | Gemini usage should be central (not incidental) | Agent using Gemini API behind Lobster Trap |
| Track 4: “actionable intelligence” / RAG / analytics / anomaly detection | `https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon` | Data layer should produce insights (not raw logs) | Risk trends, top denied rules, anomaly alerts |
| Lobster Trap can “block… review… log” | `https://www.veea.com/news/press-releases/item/208649410918` | Enforcement actions exist at conversation layer | Workflow orchestration around DENY/HUMAN_REVIEW events |

---

## 4) Triage Matrix (Requirement | Mandatory / Optional / Risky / Not Needed)

This is a project-planning triage; the “Mandatory” label means “explicitly listed on the hackathon page as part of submission”.

| Requirement | Triage | Rationale (from official sources) |
|---|---|---|
| Public GitHub Repository | Mandatory | Listed under “App Hosting & Code Repository” on the hackathon page |
| Demo Application Platform | Mandatory | Listed under “App Hosting & Code Repository” on the hackathon page |
| Application URL | Mandatory | Listed under “App Hosting & Code Repository” on the hackathon page |
| Video Presentation | Mandatory | Listed under “Cover Image and Presentation” on the hackathon page |
| Slide Presentation | Mandatory | Listed under “Cover Image and Presentation” on the hackathon page |
| Cover Image | Mandatory | Listed under “Cover Image and Presentation” on the hackathon page |
| Track 1 alignment items | Optional | Track “focus areas” on the hackathon page (not phrased as submission requirement) |
| Gemini / AI Studio usage | Optional-to-Risky | Track 2 description says “using Gemini models”; unclear if required proof is checked |
| Data/Intelligence features | Optional | Track 4 “focus areas” are descriptive, not submission fields |
| Long description minimum 100 words | Risky | Present in LabLab “Hackathon Guidelines” article, not explicitly in hackathon page submission bullets |

---

## Notes / Gaps (NOT YET VERIFIED from accessible official pages)

- The hackathon page links to “Submission Guidelines” and “Getting Started Guide”, but those pages did not load with the current web extraction tool (returned empty content). Requirements above rely on what was accessible from the hackathon page and the LabLab “Hackathon Guidelines” article.

