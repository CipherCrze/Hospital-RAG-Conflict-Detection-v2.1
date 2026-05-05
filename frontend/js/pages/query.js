/**
 * RAG Q&A Page — Query interface with conflict detection
 */
const QueryPage = {
  async render() {
    const c = document.getElementById('page-container');
    c.innerHTML = `
      <div class="query-input-wrap">
        <input type="text" id="query-input" placeholder="Ask a question about hospital documents..." autocomplete="off">
        <button class="btn btn-primary" id="btn-query" onclick="QueryPage.submit()">
          <span id="query-btn-text">Analyze</span>
        </button>
      </div>
      <div class="demo-queries" id="demo-chips"></div>
      <div id="query-result"></div>`;
    this._loadDemos();
    document.getElementById('query-input').addEventListener('keydown', e => { if (e.key === 'Enter') this.submit(); });
  },

  async _loadDemos() {
    try {
      const data = await API.demoQueries();
      document.getElementById('demo-chips').innerHTML = (data.queries || []).map(q =>
        `<button class="demo-chip" onclick="QueryPage.fillQuery('${q.question.replace(/'/g, "\\'")}')" title="${q.description || ''}">${q.question}</button>`
      ).join('');
    } catch (_) {}
  },

  fillQuery(q) {
    document.getElementById('query-input').value = q;
    this.submit();
  },

  async submit() {
    const input = document.getElementById('query-input');
    const q = input.value.trim();
    if (!q) { showToast('Please enter a question', 'error'); return; }

    const btn = document.getElementById('btn-query');
    const txt = document.getElementById('query-btn-text');
    btn.disabled = true;
    txt.innerHTML = '<span class="spinner"></span>';
    document.getElementById('query-result').innerHTML = this._skeleton();

    try {
      const result = await API.query(q);
      this._renderResult(result, q);
      showToast('Analysis complete', 'success');
    } catch (e) {
      showToast(e.message, 'error');
      document.getElementById('query-result').innerHTML = '';
    } finally {
      btn.disabled = false;
      txt.textContent = 'Analyze';
    }
  },

  _skeleton() {
    return '<div class="card" style="margin-bottom:18px"><div class="skeleton skeleton-title"></div><div class="skeleton skeleton-text"></div><div class="skeleton skeleton-text" style="width:80%"></div><div class="skeleton skeleton-text" style="width:60%"></div></div>';
  },

  _renderResult(r, question) {
    const conf = r.confidence || {};
    const levelClass = (conf.level || 'low').toLowerCase();
    const conflicts = r.conflicts || {};
    const sources = r.sources || [];
    const elapsed = r.elapsed_seconds || 0;

    document.getElementById('query-result').innerHTML = `
      <div class="result-section">
        <!-- Confidence & Timing Bar -->
        <div style="display:flex;gap:14px;align-items:center;margin-bottom:18px;flex-wrap:wrap">
          <span class="tag tag-${levelClass === 'high' ? 'green' : levelClass === 'medium' ? 'orange' : 'red'}">${conf.level || 'Unknown'} Confidence</span>
          <span style="font-size:0.78rem;color:var(--text-muted)">Score: ${conf.score ?? 0}%</span>
          <span style="font-size:0.78rem;color:var(--text-muted)">⏱ ${elapsed}s</span>
          <span style="font-size:0.78rem;color:var(--text-muted)">${sources.length} source(s)</span>
          ${conflicts.conflict_count > 0 ? `<span class="tag tag-red">⚠ ${conflicts.conflict_count} conflict(s)</span>` : '<span class="tag tag-green">✓ No conflicts</span>'}
        </div>
        <div class="confidence-meter" style="margin-bottom:22px">
          <div class="confidence-bar"><div class="confidence-fill ${levelClass}" style="width:${conf.score ?? 0}%"></div></div>
        </div>

        <!-- Answer -->
        <div class="answer-block">
          <h3>📋 Answer</h3>
          <div>${this._md(r.answer || 'No answer generated.')}</div>
        </div>

        <!-- Conflicts -->
        ${conflicts.conflict_count > 0 ? this._renderConflicts(conflicts) : ''}

        <!-- Sources -->
        ${sources.length ? this._renderSources(sources) : ''}

        <!-- Confidence Factors -->
        ${conf.factors && conf.factors.length ? `
          <div class="card" style="margin-top:18px">
            <div class="card-header"><h3 class="card-title">📊 Confidence Factors</h3></div>
            <ul style="list-style:none;padding:0">${conf.factors.map(f => `<li style="padding:6px 0;font-size:0.85rem;color:var(--text-secondary);border-bottom:1px solid var(--border)">• ${this._esc(f)}</li>`).join('')}</ul>
          </div>` : ''}
      </div>`;
  },

  _renderConflicts(c) {
    return `<div class="card" style="margin-bottom:18px;border-color:rgba(255,68,102,0.15)">
      <div class="card-header"><h3 class="card-title" style="color:var(--danger)">⚠️ Detected Conflicts (${c.conflict_count})</h3></div>
      ${(c.conflicts || []).map((cf, i) => `
        <div class="conflict-card">
          <div class="conflict-header">
            <span style="font-weight:600;font-size:0.88rem">Conflict #${i + 1}</span>
            <span class="conflict-score">Contradiction: ${(cf.contradiction_score * 100).toFixed(0)}%</span>
          </div>
          <div class="conflict-docs">
            <div class="conflict-doc">
              <div class="conflict-doc-source">${this._esc(cf.doc_a.source)}</div>
              <div style="color:var(--text-secondary)">${this._esc(cf.doc_a.snippet.substring(0, 200))}...</div>
            </div>
            <div class="conflict-doc">
              <div class="conflict-doc-source">${this._esc(cf.doc_b.source)}</div>
              <div style="color:var(--text-secondary)">${this._esc(cf.doc_b.snippet.substring(0, 200))}...</div>
            </div>
          </div>
        </div>`).join('')}
    </div>`;
  },

  _renderSources(sources) {
    return `<div class="card source-table">
      <div class="card-header"><h3 class="card-title">📑 Source Provenance</h3></div>
      <table class="data-table">
        <thead><tr><th>Document</th><th>Department</th><th>Chunks</th><th>Relevance</th></tr></thead>
        <tbody>${sources.map(s => `
          <tr>
            <td style="font-weight:500">${this._esc(s.source)}</td>
            <td><span class="tag tag-blue">${this._esc(s.department)}</span></td>
            <td>${s.chunks_retrieved}</td>
            <td>${(s.max_similarity * 100).toFixed(0)}%</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </div>`;
  },

  _md(text) {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
  },
  _esc(s) { const d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; },
};
