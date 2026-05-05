/**
 * Simple bar chart component (no dependencies)
 */
function renderBarChart(container, data, colorClass = 'green') {
  if (!data || !data.length) {
    container.innerHTML = '<div class="empty-state"><p class="empty-state-text">No data</p></div>';
    return;
  }
  const max = Math.max(...data.map(d => d.value));
  const html = data.map(d => {
    const pct = max > 0 ? Math.round((d.value / max) * 100) : 0;
    return `<div class="bar-row">
      <span class="bar-label">${d.label}</span>
      <div class="bar-track">
        <div class="bar-fill ${colorClass}" style="width:${pct}%">${d.value}</div>
      </div>
    </div>`;
  }).join('');
  container.innerHTML = `<div class="bar-chart">${html}</div>`;
}

function renderDonutStat(container, label, value, total, color = 'var(--accent)') {
  const pct = total > 0 ? Math.round((value / total) * 100) : 0;
  const circumference = 2 * Math.PI * 40;
  const dashoffset = circumference - (pct / 100) * circumference;
  container.innerHTML = `
    <div style="text-align:center">
      <svg width="100" height="100" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="8"/>
        <circle cx="50" cy="50" r="40" fill="none" stroke="${color}" stroke-width="8"
          stroke-dasharray="${circumference}" stroke-dashoffset="${dashoffset}"
          stroke-linecap="round" transform="rotate(-90 50 50)"
          style="transition: stroke-dashoffset 1s ease"/>
        <text x="50" y="50" text-anchor="middle" dy="0.35em" fill="var(--text-primary)" font-size="18" font-weight="800">${pct}%</text>
      </svg>
      <div style="font-size:0.78rem;color:var(--text-muted);margin-top:6px">${label}</div>
    </div>`;
}
