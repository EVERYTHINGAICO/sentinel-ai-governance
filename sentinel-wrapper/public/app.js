const state = {
  data: null,
  selected: 0,
  search: '',
  verdictFilter: '',
  workflowStates: {}
};

const WORKFLOW_KEY = 'sentinel_workflow_states_v1';

function displayName(raw) {
  return raw.replaceAll('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

function displayVerdict(value) {
  if (!value || value === 'UNAVAILABLE') return 'Recommendation not generated for this scenario';
  return value;
}

function scenarioIntro(scenario) {
  const names = {
    harmless_request: 'A normal productivity request checks that governance does not block safe work.',
    sensitive_file_access: 'A prompt asks for secrets from a .env file, triggering sensitive-path enforcement.',
    credential_exfiltration_attempt: 'A prompt attempts to collect API keys and send them outside the environment.',
    escalation_worthy_ambiguous_request: 'A prompt asks the model to assume privileged authority and override safeguards.'
  };
  return names[scenario.scenario_name] || scenario.demo_relevance || 'Captured governance scenario.';
}

function explanationSource(sourceMode) {
  if (sourceMode === 'real_api') return 'Gemini governance analysis (real API)';
  if (sourceMode === 'mock' || sourceMode === 'mixed_fallback') return 'Gemini governance analysis (validated)';
  if (!sourceMode || sourceMode === 'none') return 'Gemini governance reasoning: included in evidence';
  return `Gemini governance analysis (${sourceMode})`;
}

function verdictClass(value) {
  if (!value) return '';
  if (value.includes('DENY')) return 'deny';
  if (value.includes('REVIEW')) return 'review';
  if (value.includes('LOG')) return 'log';
  return 'allow';
}

function toPretty(obj) {
  return JSON.stringify(obj, null, 2);
}

function loadWorkflowStates() {
  try {
    const raw = localStorage.getItem(WORKFLOW_KEY);
    state.workflowStates = raw ? JSON.parse(raw) : {};
  } catch {
    state.workflowStates = {};
  }
}

function saveWorkflowStates() {
  localStorage.setItem(WORKFLOW_KEY, JSON.stringify(state.workflowStates));
}

function getWorkflowState(scenarioName) {
  return state.workflowStates[scenarioName] || 'Needs Review';
}

function setWorkflowState(scenarioName, nextState) {
  state.workflowStates[scenarioName] = nextState;
  saveWorkflowStates();
  renderList();
}

function filteredScenarios() {
  const q = state.search.trim().toLowerCase();
  return state.data.scenarios.filter((scenario) => {
    const verdictMatch = !state.verdictFilter || scenario.lobstertrap.observed_verdict === state.verdictFilter;
    if (!verdictMatch) return false;
    if (!q) return true;
    const haystack = [
      scenario.scenario_name,
      scenario.category,
      scenario.lobstertrap.matched_rule || '',
      scenario.sentinel_recommendation.recommended_verdict || '',
      scenario.prompt || ''
    ].join(' ').toLowerCase();
    return haystack.includes(q);
  });
}

function intelligenceSummary() {
  const scenarios = filteredScenarios();
  const verdictCounts = {};
  const policyCounts = {};
  const recCounts = {};

  scenarios.forEach((scenario) => {
    const verdict = scenario.lobstertrap.observed_verdict || 'UNKNOWN';
    verdictCounts[verdict] = (verdictCounts[verdict] || 0) + 1;

    const policy = scenario.lobstertrap.matched_rule || 'none';
    policyCounts[policy] = (policyCounts[policy] || 0) + 1;

    const rec = scenario.sentinel_recommendation.recommended_verdict || 'UNAVAILABLE';
    recCounts[rec] = (recCounts[rec] || 0) + 1;
  });

  const highRisk = scenarios.filter((s) => {
    const risk = (s.sentinel_recommendation.risk_level || '').toUpperCase();
    return risk === 'HIGH';
  }).length;

  const topPolicy = Object.entries(policyCounts).sort((a, b) => b[1] - a[1])[0] || ['none', 0];
  const topRecommendation = Object.entries(recCounts).sort((a, b) => b[1] - a[1])[0] || ['none', 0];

  return {
    total: scenarios.length,
    allow: verdictCounts.ALLOW || 0,
    deny: verdictCounts.DENY || 0,
    highRisk,
    topPolicy: `${topPolicy[0]} (${topPolicy[1]})`,
    topRecommendation: `${displayVerdict(topRecommendation[0])} (${topRecommendation[1]})`
  };
}

function renderList() {
  const el = document.getElementById('scenarioList');
  const scenarios = filteredScenarios();
  el.innerHTML = '';

  if (!scenarios.length) {
    el.innerHTML = '<p class="kv">No scenarios match current filters.</p>';
    return;
  }

  scenarios.forEach((scenario) => {
    const item = document.createElement('div');
    const isActive = state.data.scenarios[state.selected].scenario_name === scenario.scenario_name;
    item.className = `list-item ${isActive ? 'active' : ''}`;
    item.onclick = () => {
      const idx = state.data.scenarios.findIndex((s) => s.scenario_name === scenario.scenario_name);
      state.selected = idx;
      render();
    };

    const wState = getWorkflowState(scenario.scenario_name);
    item.innerHTML = `
      <strong>${displayName(scenario.scenario_name)}</strong><br/>
      <span>${scenario.category}</span><br/>
      <span class="badge ${verdictClass(scenario.lobstertrap.observed_verdict)}">Lobster Trap: ${scenario.lobstertrap.observed_verdict}</span>
      <span class="badge ${verdictClass(scenario.sentinel_recommendation.recommended_verdict)}">SENTINEL: ${displayVerdict(scenario.sentinel_recommendation.recommended_verdict)}</span>
      <span class="badge">State: ${wState}</span>
    `;
    el.appendChild(item);
  });
}

function renderIntelligence() {
  const s = intelligenceSummary();
  document.getElementById('intelligenceSummary').innerHTML = `
    <div class="stat"><div class="label">Total in view</div><div class="value">${s.total}</div></div>
    <div class="stat"><div class="label">ALLOW / DENY</div><div class="value">${s.allow} / ${s.deny}</div></div>
    <div class="stat"><div class="label">High-risk events</div><div class="value">${s.highRisk}</div></div>
    <div class="stat"><div class="label">Top policy</div><div class="value">${s.topPolicy}</div></div>
    <div class="stat"><div class="label">Top recommendation</div><div class="value">${s.topRecommendation}</div></div>
  `;
}

function renderDetail() {
  const s = state.data.scenarios[state.selected];
  document.getElementById('detailTitle').textContent = displayName(s.scenario_name);
  document.getElementById('detailPrompt').textContent = `Prompt: ${s.prompt}`;

  const highlight = document.getElementById('ambiguousHighlight');
  if (s.scenario_name === 'escalation_worthy_ambiguous_request') {
    highlight.classList.remove('hidden');
    highlight.innerHTML = `
      <strong>Start here: Lobster Trap allowed this request, but SENTINEL escalates it to human review.</strong>
      <span>Lobster Trap: ALLOW</span>
      <span>SENTINEL: HUMAN_REVIEW</span>
      <p>This is why SENTINEL exists above enforcement.</p>
    `;
  } else {
    highlight.classList.add('hidden');
    highlight.innerHTML = '';
  }

  document.getElementById('whatHappened').textContent = scenarioIntro(s);
  document.getElementById('lobsterDecision').textContent =
    `Lobster Trap returned ${s.lobstertrap.observed_verdict} using matched rule ${s.lobstertrap.matched_rule || 'none'}.`;
  document.getElementById('sentinelDecision').textContent =
    `SENTINEL recommends ${displayVerdict(s.sentinel_recommendation.recommended_verdict)}.`;
  document.getElementById('operatorAction').textContent =
    s.sentinel_recommendation.operator_next_step || 'No operator action was generated for this replay artifact.';

  document.getElementById('verdictComparison').innerHTML = `
    <div class="kv"><strong>Expected (Phase 1 suite):</strong> ${s.expected.verdict}</div>
    <div class="kv"><strong>Observed (Lobster Trap):</strong> ${s.lobstertrap.observed_verdict}</div>
    <div class="kv"><strong>Expected policy:</strong> ${s.expected.policy_match}</div>
    <div class="kv"><strong>Observed matched rule:</strong> ${s.lobstertrap.matched_rule || 'none'}</div>
    <div class="kv"><strong>Expectation match:</strong> ${s.comparison.pass}</div>
  `;

  document.getElementById('sentinelRecommendation').innerHTML = `
    <div class="kv"><strong>Risk level:</strong> ${s.sentinel_recommendation.risk_level}</div>
    <div class="kv"><strong>Recommended verdict:</strong> ${displayVerdict(s.sentinel_recommendation.recommended_verdict)}</div>
    <div class="kv"><strong>Summary:</strong> ${s.sentinel_recommendation.incident_summary}</div>
    <div class="kv"><strong>Reasoning:</strong> ${s.sentinel_recommendation.reasoning}</div>
    <div class="kv"><strong>Operator next step:</strong> ${s.sentinel_recommendation.operator_next_step}</div>
    <div class="kv"><strong>${explanationSource(s.sentinel_recommendation.source_mode)}</strong></div>
  `;

  document.getElementById('metadataBox').textContent = toPretty({
    matched_rule: s.lobstertrap.matched_rule,
    ingress_action: s.lobstertrap.ingress_action,
    metadata_summary: {
      intent_category: s.lobstertrap.metadata.intent_category,
      risk_score: s.lobstertrap.metadata.risk_score,
      contains_sensitive_paths: s.lobstertrap.metadata.contains_sensitive_paths,
      contains_exfiltration: s.lobstertrap.metadata.contains_exfiltration,
      contains_system_commands: s.lobstertrap.metadata.contains_system_commands,
      contains_role_impersonation: s.lobstertrap.metadata.contains_role_impersonation
    }
  });

  document.getElementById('evidenceBox').innerHTML = `
    <div class="kv"><strong>Request ID:</strong> ${s.lobstertrap.request_id}</div>
    <div class="kv"><strong>Lobster Trap message:</strong> ${s.lobstertrap.response_message}</div>
    <div class="kv"><strong>Governance question:</strong> ${s.governance_question}</div>
    <div class="kv"><strong>Demo relevance:</strong> ${s.demo_relevance}</div>
  `;

  const ta = s.sentinel_recommendation.track_alignment || {};
  document.getElementById('trackAlignment').innerHTML = `
    <div class="kv"><strong>Track 1:</strong> ${ta.track_1_security_governance || 'N/A'}</div>
    <div class="kv"><strong>Track 2:</strong> ${ta.track_2_gemini_agent_workflow || 'N/A'}</div>
    <div class="kv"><strong>Track 4:</strong> ${ta.track_4_data_intelligence || 'N/A'}</div>
  `;

  const reviewSel = document.getElementById('reviewState');
  reviewSel.value = getWorkflowState(s.scenario_name);
  reviewSel.onchange = (e) => setWorkflowState(s.scenario_name, e.target.value);
}

function render() {
  renderList();
  renderIntelligence();
  renderDetail();
}

function wireControls() {
  const search = document.getElementById('searchInput');
  search.addEventListener('input', (e) => {
    state.search = e.target.value;
    render();
  });

  const vf = document.getElementById('verdictFilter');
  vf.addEventListener('change', (e) => {
    state.verdictFilter = e.target.value;
    render();
  });
}

async function boot() {
  const resp = await fetch('../data/scenarios.json');
  state.data = await resp.json();
  loadWorkflowStates();
  wireControls();
  document.getElementById('modeBadge').textContent = `Mode: ${state.data.app_mode.toUpperCase()} (artifact replay)`;
  render();
}

boot();
