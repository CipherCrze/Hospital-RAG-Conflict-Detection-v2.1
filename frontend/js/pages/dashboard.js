/**
 * Dashboard Page — Overview with KPI cards
 */
const DashboardPage = {
  async render() {
    const c = document.getElementById('page-container');
    c.innerHTML = `
      <div class="kpi-grid" id="kpi-grid">
        ${this._skeletonKPI(4)}
      </div>
      <div class="grid-2">
        <div class="card">
          <div class="card-header"><h3 class="card-title">Department Distribution</h3></div>
          <div id="dept-chart" class="chart-container"><div class="skeleton skeleton-card"></div></div>
        </div>
        <div class="card">
          <div class="card-header"><h3 class="card-title">Recent Queries</h3></div>
          <div id="recent-queries"><div class="skeleton skeleton-card"></div></div>
        </div>
      </div>`;
    this._load();
  },

  _skeletonKPI(n) {
    return Array(n).fill('<div class="kpi-card"><div class="skeleton skeleton-title"></div><div class="skeleton skeleton-text" style="width:60%"></div></div>').join('');
  },

  async _load() {
    try {
      const [overview, depts] = await Promise.all([
        API.analyticsOverview(),
        API.departments(),
      ]);
      this._renderKPIs(overview);
      this._renderDepts(depts.departments || []);
      this._renderHistory(overview);
    } catch (e) {
      showToast(e.message, 'error');
    }
  },

  _renderKPIs(d) {
    document.getElementById('kpi-grid').innerHTML = `
      ${this._kpi('📄', 'green', d.total_documents, 'Documents Indexed')}
      ${this._kpi('🧩', 'blue', d.total_chunks, 'Text Chunks')}
      ${this._kpi('🔍', 'orange', d.total_queries, 'Queries Executed')}
      ${this._kpi('⚠️', 'red', d.total_conflicts_detected, 'Conflicts Detected')}`;
  },

  _kpi(icon, color, value, label) {
    return `<div class="kpi-card">
      <div class="kpi-icon ${color}">${icon}</div>
      <div class="kpi-value">${value ?? 0}</div>
      <div class="kpi-label">${label}</div>
    </div>`;
  },

  _renderDepts(depts) {
    const el = document.getElementById('dept-chart');
    if (!depts.length) { el.innerHTML = '<div class="empty-state"><p class="empty-state-text">No departments found</p></div>'; return; }
    const colors = ['green','blue','orange','red','green','blue','orange','red'];
    renderBarChart(el, depts.map((d, i) => ({
      label: d.department, value: d.chunk_count,
    })), 'green');
  },

  _renderHistory(overview) {
    const el = document.getElementById('recent-queries');
    API.queryHistory().then(data => {
      const hist = data.history || [];
      if (!hist.length) {
        el.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🔍</div><p class="empty-state-text">No queries yet</p><p class="empty-state-sub">Ask a question in the RAG Q&A tab</p></div>';
        return;
      }
      el.innerHTML = hist.slice(0, 5).map(h => `
        <div style="padding:10px 0;border-bottom:1px solid var(--border);font-size:0.85rem">
          <div style="font-weight:600;margin-bottom:4px">${this._esc(h.question)}</div>
          <div style="display:flex;gap:12px;color:var(--text-muted);font-size:0.75rem">
            <span>⏱ ${h.elapsed_seconds}s</span>
            <span class="tag tag-${h.conflict_count > 0 ? 'red' : 'green'}">${h.conflict_count} conflicts</span>
            <span>${new Date(h.timestamp).toLocaleTimeString()}</span>
          </div>
        </div>`).join('');
    }).catch(() => {});
  },

  _esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; },
};
