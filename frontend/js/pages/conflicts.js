/**
 * Conflicts Page — Conflict analysis from query history
 */
const ConflictsPage = {
  async render() {
    const c = document.getElementById('page-container');
    c.innerHTML = `
      <div class="card" style="margin-bottom:22px">
        <div class="card-header">
          <h3 class="card-title">⚡ Run Conflict Scan</h3>
        </div>
        <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:16px">
          Ask a question to scan hospital documents for conflicting information. The system uses NLI-based pairwise contradiction detection.
        </p>
        <div class="query-input-wrap">
          <input type="text" id="conflict-input" placeholder="e.g. How has patient satisfaction changed?" value="How has patient satisfaction changed over Q1?">
          <button class="btn btn-primary" id="btn-conflict-scan" onclick="ConflictsPage.scan()">Scan</button>
        </div>
      </div>
      <div id="conflict-results"></div>
      <div class="card" style="margin-top:22px">
        <div class="card-header"><h3 class="card-title">📜 Past Conflicts</h3></div>
        <div id="past-conflicts"><div class="skeleton skeleton-card"></div></div>
      </div>`;
    this._loadHistory();
  },

  async scan() {
    const q = document.getElementById('conflict-input').value.trim();
    if (!q) { showToast('Enter a question', 'error'); return; }
    const btn = document.getElementById('btn-conflict-scan');
    btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>';
    document.getElementById('conflict-results').innerHTML = '<div class="skeleton skeleton-card" style="height:180px"></div>';
    try {
      const r = await API.query(q);
      this._renderResults(r);
    } catch (e) {
      showToast(e.message, 'error');
      document.getElementById('conflict-results').innerHTML = '';
    } finally { btn.disabled = false; btn.textContent = 'Scan'; }
  },

  _renderResults(r) {
    const conflicts = r.conflicts || {};
    const el = document.getElementById('conflict-results');
    if (!conflicts.conflict_count) {
      el.innerHTML = '<div class="card" style="text-align:center;padding:40px"><div style="font-size:2rem;margin-bottom:12px">✅</div><p style="font-weight:600">No Conflicts Detected</p><p style="font-size:0.82rem;color:var(--text-muted)">All retrieved documents are consistent</p></div>';
      return;
    }
    el.innerHTML = `<div class="card" style="border-color:rgba(255,68,102,0.15)">
      <div class="card-header"><h3 class="card-title" style="color:var(--danger)">⚠️ ${conflicts.conflict_count} Conflict(s) Found</h3></div>
      ${(conflicts.conflicts || []).map((cf, i) => `
        <div class="conflict-card">
          <div class="conflict-header">
            <span style="font-weight:600">Conflict #${i + 1}</span>
            <span class="conflict-score">${(cf.contradiction_score * 100).toFixed(0)}% contradiction</span>
          </div>
          <div class="conflict-docs">
            <div class="conflict-doc">
              <div class="conflict-doc-source">${this._esc(cf.doc_a.source)}</div>
              <div class="tag tag-blue" style="margin-bottom:8px">${cf.doc_a.department}</div>
              <div style="color:var(--text-secondary);font-size:0.8rem">${this._esc(cf.doc_a.snippet.substring(0, 250))}</div>
            </div>
            <div class="conflict-doc">
              <div class="conflict-doc-source">${this._esc(cf.doc_b.source)}</div>
              <div class="tag tag-blue" style="margin-bottom:8px">${cf.doc_b.department}</div>
              <div style="color:var(--text-secondary);font-size:0.8rem">${this._esc(cf.doc_b.snippet.substring(0, 250))}</div>
            </div>
          </div>
          <div style="margin-top:12px;padding-top:10px;border-top:1px solid var(--border);display:flex;gap:16px;font-size:0.75rem;color:var(--text-muted)">
            <span>Entailment: ${(cf.entailment_score * 100).toFixed(0)}%</span>
            <span>Neutral: ${(cf.neutral_score * 100).toFixed(0)}%</span>
            <span style="color:var(--danger)">Contradiction: ${(cf.contradiction_score * 100).toFixed(0)}%</span>
          </div>
        </div>`).join('')}
    </div>`;
  },

  async _loadHistory() {
    try {
      const data = await API.queryHistory();
      const withConflicts = (data.history || []).filter(h => h.conflict_count > 0);
      const el = document.getElementById('past-conflicts');
      if (!withConflicts.length) { el.innerHTML = '<p style="font-size:0.85rem;color:var(--text-muted);padding:10px 0">No conflicts in query history yet</p>'; return; }
      el.innerHTML = withConflicts.map(h => `
        <div style="padding:10px 0;border-bottom:1px solid var(--border)">
          <div style="font-weight:500;font-size:0.88rem;margin-bottom:4px">${this._esc(h.question)}</div>
          <div style="display:flex;gap:12px;font-size:0.75rem;color:var(--text-muted)">
            <span class="tag tag-red">${h.conflict_count} conflict(s)</span>
            <span>${new Date(h.timestamp).toLocaleString()}</span>
          </div>
        </div>`).join('');
    } catch (_) {}
  },

  _esc(s) { const d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; },
};
