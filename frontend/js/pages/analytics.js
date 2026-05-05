/**
 * Analytics Page — Charts and metrics
 */
const AnalyticsPage = {
  async render() {
    const c = document.getElementById('page-container');
    c.innerHTML = `
      <div class="kpi-grid" id="analytics-kpis">${Array(3).fill('<div class="skeleton skeleton-card" style="height:100px"></div>').join('')}</div>
      <div class="grid-2">
        <div class="card">
          <div class="card-header"><h3 class="card-title">🏥 Chunks by Department</h3></div>
          <div id="analytics-dept-chart"><div class="skeleton skeleton-card"></div></div>
        </div>
        <div class="card">
          <div class="card-header"><h3 class="card-title">📊 Document Types</h3></div>
          <div id="analytics-types"><div class="skeleton skeleton-card"></div></div>
        </div>
      </div>
      <div class="card" style="margin-top:22px">
        <div class="card-header"><h3 class="card-title">🕐 Query History</h3></div>
        <div id="analytics-history"><div class="skeleton skeleton-card"></div></div>
      </div>`;
    this._load();
  },

  async _load() {
    try {
      const [overview, stats, depts, history] = await Promise.all([
        API.analyticsOverview(),
        API.documentStats(),
        API.departments(),
        API.queryHistory(),
      ]);
      this._renderKPIs(overview, stats);
      this._renderDeptChart(depts.departments || []);
      this._renderTypes(stats);
      this._renderHistory(history.history || []);
    } catch (e) { showToast(e.message, 'error'); }
  },

  _renderKPIs(o, s) {
    document.getElementById('analytics-kpis').innerHTML = `
      <div class="kpi-card"><div class="kpi-icon green">📄</div><div class="kpi-value">${s.total_documents || 0}</div><div class="kpi-label">Total Documents</div></div>
      <div class="kpi-card"><div class="kpi-icon blue">🧩</div><div class="kpi-value">${s.total_chunks || 0}</div><div class="kpi-label">Total Chunks</div></div>
      <div class="kpi-card"><div class="kpi-icon orange">🏷️</div><div class="kpi-value">${Object.keys(s.departments || {}).length}</div><div class="kpi-label">Departments</div></div>`;
  },

  _renderDeptChart(depts) {
    const el = document.getElementById('analytics-dept-chart');
    if (!depts.length) { el.innerHTML = '<p style="color:var(--text-muted);font-size:0.85rem">No data</p>'; return; }
    renderBarChart(el, depts.map(d => ({ label: d.department, value: d.chunk_count })), 'blue');
  },

  _renderTypes(stats) {
    const el = document.getElementById('analytics-types');
    const types = stats.doc_types || {};
    if (!Object.keys(types).length) { el.innerHTML = '<p style="color:var(--text-muted);font-size:0.85rem">No data</p>'; return; }
    renderBarChart(el, Object.entries(types).map(([k, v]) => ({ label: k, value: v })), 'orange');
  },

  _renderHistory(hist) {
    const el = document.getElementById('analytics-history');
    if (!hist.length) { el.innerHTML = '<div class="empty-state"><p class="empty-state-text">No queries recorded yet</p></div>'; return; }
    el.innerHTML = `<table class="data-table">
      <thead><tr><th>Question</th><th>Time</th><th>Latency</th><th>Conflicts</th><th>Sources</th></tr></thead>
      <tbody>${hist.slice(0, 20).map(h => `<tr>
        <td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${this._esc(h.question)}</td>
        <td style="font-size:0.78rem;color:var(--text-muted)">${new Date(h.timestamp).toLocaleString()}</td>
        <td>${h.elapsed_seconds}s</td>
        <td><span class="tag tag-${h.conflict_count > 0 ? 'red' : 'green'}">${h.conflict_count}</span></td>
        <td>${h.source_count || '-'}</td>
      </tr>`).join('')}</tbody></table>`;
  },

  _esc(s) { const d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; },
};
