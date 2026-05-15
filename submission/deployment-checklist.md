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

- [ ] Build static payload:
  - `sentinel-wrapper/scripts/build_dataset.py`
  - `rm -rf submission/site && mkdir -p submission/site/data`
  - `cp -r sentinel-wrapper/public/* submission/site/`
  - `cp sentinel-wrapper/data/scenarios.json submission/site/data/scenarios.json`
- [ ] Validate static payload locally:
  - `cd submission/site && python3 -m http.server 8899`
  - open `http://localhost:8899/index.html`
- [ ] Publish static files from `sentinel-wrapper/public/` + `sentinel-wrapper/data/`
- [ ] Push to GitHub branch configured for Pages (for example `gh-pages`) or `/docs` strategy
- [ ] Ensure generated `data/scenarios.json` is included
- [ ] Confirm hosted URL loads `public/index.html`
- [ ] Confirm hosted URL can fetch `data/scenarios.json`

## D. Environment Variable Checks

Replay mode:
- [ ] No runtime environment variables required

Optional real Gemini mode (future):
- [ ] `GEMINI_API_KEY` or `GOOGLE_API_KEY` available if re-running live validation harness

## E. Demo Verification

- [ ] Scenario list visible and filter/search works
- [ ] Intelligence snapshot displays counts
- [ ] Operator state selector works
- [ ] Ambiguous case highlight is visible
- [ ] Track 1/2/4 narrative is clear in under 3 minutes

## F. Browser Verification

- [ ] Chrome latest
- [ ] Edge latest
- [ ] Mobile responsive check

## G. Final Submission Checklist

- [ ] Public repository link prepared
- [ ] Application URL prepared
- [ ] Demo video script finalized (`submission/demo-script.md`)
- [ ] Submission copy finalized (`submission/submission-copy.md`)
- [ ] Slide outline finalized (`submission/slides-outline.md`)
