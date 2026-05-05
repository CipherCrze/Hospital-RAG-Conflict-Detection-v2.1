/**
 * Documents Page — Browse and search indexed documents
 */
const DocumentsPage = {
  async render() {
    const c = document.getElementById('page-container');
    c.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:22px;flex-wrap:wrap;gap:12px">
        <input type="text" id="doc-search" placeholder="Search documents..." style="max-width:320px" oninput="DocumentsPage.filter()">
        <button class="btn btn-ghost btn-sm" onclick="DocumentsPage.reingest()">🔄 Re-ingest</button>
      </div>
      <div id="doc-grid" class="doc-grid">${this._skeleton(6)}</div>`;
    this._load();
  },

  _skeleton(n) {
    return Array(n).fill('<div class="skeleton skeleton-card" style="height:140px"></div>').join('');
  },

  _docs: [],

  async _load() {
    try {
      const data = await API.listDocuments();
      this._docs = data.documents || [];
      this._render();
    } catch (e) { showToast(e.message, 'error'); }
  },

  _render(docs) {
    const list = docs || this._docs;
    const el = document.getElementById('doc-grid');
    if (!list.length) { el.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📄</div><p class="empty-state-text">No documents found</p></div>'; return; }
    const tagColors = { 'Quality': 'green', 'Surgery': 'red', 'Finance': 'orange', 'Emergency': 'red', 'Nursing': 'blue', 'Administration': 'blue', 'Infection Control': 'orange', 'Patient Relations': 'orange', 'Human Resources': 'blue', 'General': 'green' };
    el.innerHTML = list.map((d, i) => `
      <div class="doc-card" id="doc-${i}" onclick="DocumentsPage.toggle(${i},'${d.doc_id.replace(/'/g, "\\'")}')">
        <div class="doc-card-header">
          <div>
            <div class="doc-card-title">${this._esc(d.filename)}</div>
            <div class="doc-card-meta">${d.file_size_display} · ${d.doc_type}</div>
          </div>
          <span class="tag tag-${tagColors[d.department] || 'green'}">${d.department}</span>
        </div>
        <div class="doc-preview" id="doc-preview-${i}">Loading...</div>
      </div>`).join('');
  },

  filter() {
    const q = (document.getElementById('doc-search').value || '').toLowerCase();
    this._render(this._docs.filter(d => d.filename.toLowerCase().includes(q) || d.department.toLowerCase().includes(q)));
  },

  async toggle(i, docId) {
    const card = document.getElementById(`doc-${i}`);
    const preview = document.getElementById(`doc-preview-${i}`);
    if (card.classList.contains('expanded')) { card.classList.remove('expanded'); return; }
    card.classList.add('expanded');
    if (preview.textContent === 'Loading...') {
      try {
        const data = await API.getDocument(docId);
        preview.textContent = data.content.substring(0, 800) + (data.content.length > 800 ? '...' : '');
      } catch (e) { preview.textContent = 'Error loading: ' + e.message; }
    }
  },

  async reingest() {
    if (!confirm('Re-ingest all documents? This will rebuild the vector store.')) return;
    showToast('Re-ingesting documents...', 'info');
    try {
      const r = await API.reingestDocuments();
      showToast(r.message || 'Re-ingestion complete', 'success');
    } catch (e) { showToast(e.message, 'error'); }
  },

  _esc(s) { const d = document.createElement('div'); d.textContent = s || ''; return d.innerHTML; },
};
