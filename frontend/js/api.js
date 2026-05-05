/**
 * API Client — Backend communication layer
 */
const API = {
  BASE: '/api',

  async _fetch(url, opts = {}) {
    try {
      const res = await fetch(this.BASE + url, {
        headers: { 'Content-Type': 'application/json', ...opts.headers },
        ...opts,
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      return await res.json();
    } catch (e) {
      if (e.message === 'Failed to fetch') throw new Error('Backend unreachable. Is the server running?');
      throw e;
    }
  },

  // Health
  health() { return this._fetch('/health'); },

  // API Key
  setApiKey(key) { return this._fetch('/set-api-key', { method: 'POST', body: JSON.stringify({ api_key: key }) }); },
  apiKeyStatus() { return this._fetch('/api-key-status'); },

  // Query
  query(question, apiKey) {
    const body = { question };
    if (apiKey) body.api_key = apiKey;
    return this._fetch('/query', { method: 'POST', body: JSON.stringify(body) });
  },
  demoQueries() { return this._fetch('/demo-queries'); },

  // Documents
  listDocuments() { return this._fetch('/documents'); },
  getDocument(docId) { return this._fetch(`/documents/${encodeURIComponent(docId)}`); },
  reingestDocuments() { return this._fetch('/documents/reingest', { method: 'POST' }); },
  documentStats() { return this._fetch('/documents/stats/overview'); },

  // Analytics
  analyticsOverview() { return this._fetch('/analytics/overview'); },
  departments() { return this._fetch('/analytics/departments'); },
  queryHistory() { return this._fetch('/analytics/query-history'); },
};
