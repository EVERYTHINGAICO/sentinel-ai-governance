# Deployment Checklist

## A. Local Verification

- [ ] Run dataset generation:
  - `sentinel-wrapper/scripts/build_dataset.py`
- [ ] Start local server:
  - `sentinel-wrapper/scripts/serve.sh`
- [ ] Verify UI endpoint:
  - `http://localhost:8787/public/index.html`
- [ ] Verify data endpoint:
  - `http://localhost:8787/data/scenarios.json`

## B. Replay Dataset Integrity

- [ ] Confirm required scenarios exist:
  - harmless_request
  - sensitive_file_access
  - credential_exfiltration_attempt
  - escalation_worthy_ambiguous_request
- [ ] Confirm ambiguous scenario shows:
  - Lobster Trap `ALLOW`
  - SENTINEL `HUMAN_REVIEW`

## C. Deployment Strategy

Selected strategy: **GitHub Pages static hosting**.

### Build static payload (automated via MCP):
- [ ] Use the SENTINEL MCP server:
  - `sentinel_build_dataset` → generates scenarios.json
  - `sentinel_deploy` → copies assets to `submission/site/`

### OR build manually:
- [ ] `python3 sentinel-wrapper/scripts/build_dataset.py`
- [ ] `rm -rf submission/site && mkdir -p submission/site/data`
- [ ] `cp -r sentinel-wrapper/public/* submission/site/`
- [ ] `cp sentinel-wrapper/data/scenarios.json submission/site/data/scenarios.json`

### Validate static payload locally:
- [ ] `cd submission/site && python3 -m http.server 8899`
- [ ] Open `http://localhost:8899/index.html`

### Publish to GitHub Pages:
- [ ] Create or switch to `gh-pages` branch:
  - `git checkout -b gh-pages` (first time)
  - OR `git checkout gh-pages` (if exists)
- [ ] Add and commit site files:
  - `git add submission/site/`
  - `git commit -m "Deploy: GitHub Pages static governance demo"`
- [ ] Push to remote:
  - `git push origin gh-pages`
- [ ] Go to GitHub repo → Settings → Pages → Source: `gh-pages` branch, `/` (root) or `/submission/site`
- [ ] Confirm hosted URL loads `submission/site/index.html`
- [ ] Confirm hosted URL can fetch `submission/site/data/scenarios.json`
- [ ] Expected URL: `https://everythingaico.github.io/sentinel-ai-governance/`

### Fill in URLs after deployment:
- [ ] Update README.md: `Demo Application Platform` → `GitHub Pages`
- [ ] Update README.md: `Demo Application URL` → actual hosted URL
- [ ] Update `submission/submission-copy.md` if it has any URL TODOs

## D. Environment Variable Checks

Replay mode:
- [x] No runtime environment variables required for static demo

Optional real Gemini mode:
- [ ] `GEMINI_API_KEY` available in `.env` if re-running live Gemini validation
- [ ] Run `sentinel_run_gemini` to confirm real API produces structured output
- [ ] Screenshot/capture real Gemini output for slides evidence

## E. Demo Verification

- [ ] Scenario list visible and filter/search works
- [ ] Intelligence snapshot displays verdict counts
- [ ] Operator state selector works (Needs Review / Approved / Rejected / Quarantined)
- [ ] Ambiguous case (escalation_worthy_ambiguous_request) shows ALLOW → HUMAN_REVIEW
- [ ] Track 1/2/4 narrative is clear in under 3 minutes

## F. Browser Verification

- [ ] Chrome latest
- [ ] Edge latest
- [ ] Mobile responsive check

## G. Final Submission Checklist

- [x] Public repository link: `https://github.com/EVERYTHINGAICO/sentinel-ai-governance`
- [ ] Demo Application Platform: GitHub Pages (fill in after deploy)
- [ ] Demo Application URL: `https://everythingaico.github.io/sentinel-ai-governance/` (confirm after deploy)
- [ ] Video presentation recorded and uploaded (max 5 min, under 300MB)
  - Follow `submission/demo-script.md` — show 4 scenarios + MCP command (Step 4b)
- [ ] Slide presentation created and linked (min 6 slides, follow `submission/slides-outline.md`)
- [ ] Cover image confirmed: `assets/sentinel-banner.png`
- [ ] Demo video script finalized: `submission/demo-script.md` ✓
- [ ] Submission copy finalized: `submission/submission-copy.md` ✓
- [ ] Slide outline finalized: `submission/slides-outline.md` ✓
