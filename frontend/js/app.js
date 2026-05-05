/**
 * App Shell — Router, sidebar, global functions
 */
(function () {
  const pages = {
    dashboard:  { page: DashboardPage,  title: 'Dashboard',  subtitle: 'System overview and key metrics' },
    query:      { page: QueryPage,      title: 'RAG Q&A',    subtitle: 'Ask questions with conflict detection' },
    documents:  { page: DocumentsPage,  title: 'Documents',  subtitle: 'Browse indexed hospital documents' },
    conflicts:  { page: ConflictsPage,  title: 'Conflicts',  subtitle: 'Analyze conflicting information' },
    analytics:  { page: AnalyticsPage,  title: 'Analytics',  subtitle: 'Charts, metrics, and query history' },
  };

  function getRoute() {
    const hash = location.hash.replace('#/', '') || 'dashboard';
    return pages[hash] ? hash : 'dashboard';
  }

  function navigate() {
    const route = getRoute();
    const config = pages[route];

    // Update header
    document.getElementById('page-title').textContent = config.title;
    document.getElementById('page-subtitle').textContent = config.subtitle;

    // Update active nav
    document.querySelectorAll('.nav-item').forEach(el => {
      el.classList.toggle('active', el.dataset.page === route);
    });

    // Render page
    config.page.render();
  }

  window.addEventListener('hashchange', navigate);

  // Sidebar toggle
  window.toggleSidebar = function () {
    document.getElementById('sidebar').classList.toggle('collapsed');
  };

  // API Key Modal
  window.openApiKeyModal = function () {
    document.getElementById('api-key-modal').classList.add('active');
    setTimeout(() => document.getElementById('api-key-input').focus(), 100);
  };
  window.closeApiKeyModal = function () {
    document.getElementById('api-key-modal').classList.remove('active');
  };
  window.saveApiKey = async function () {
    const key = document.getElementById('api-key-input').value.trim();
    if (!key) { showToast('Enter a valid API key', 'error'); return; }
    try {
      await API.setApiKey(key);
      showToast('API key saved successfully', 'success');
      closeApiKeyModal();
      updateApiStatus(true);
    } catch (e) { showToast(e.message, 'error'); }
  };

  function updateApiStatus(isSet) {
    const el = document.getElementById('api-status');
    const dot = el.querySelector('.status-dot');
    const text = el.querySelector('span');
    dot.classList.toggle('online', isSet);
    dot.classList.toggle('offline', !isSet);
    text.textContent = isSet ? 'API Key Active' : 'API Key Not Set';
  }

  // Check API key on load
  async function init() {
    try {
      const status = await API.apiKeyStatus();
      updateApiStatus(status.is_set);
    } catch (_) {}
    navigate();
  }

  // Handle Enter in modal
  document.getElementById('api-key-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') saveApiKey();
  });

  init();
})();
