const API = '/api/hosts';
let network = null;
let nodes = null;
let edges = null;

async function fetchHosts() {
  try {
    const res = await fetch(API + '?t=' + Date.now());
    if (!res.ok) return;
    const hosts = await res.json();
    renderGraph(hosts);
    renderTable(hosts);
    document.getElementById('lastScan').textContent =
      'Skan: ' + new Date().toLocaleTimeString('pl-PL') + ' — ' + hosts.length + ' urządzeń';
  } catch (e) {
    document.getElementById('lastScan').textContent = 'Błąd pobierania';
  }
}

function roleClass(role) {
  const r = (role || 'unknown').toLowerCase();
  if (r.includes('gateway')) return 'gateway';
  if (r.includes('router')) return 'router';
  if (r.includes('switch')) return 'switch';
  if (r.includes('ap') || r.includes('access point')) return 'ap';
  if (r.includes('mobile')) return 'mobile';
  if (r.includes('vm') || r.includes('virtual')) return 'vm';
  if (r.includes('pc') || r.includes('computer')) return 'pc';
  return 'unknown';
}

function roleColor(role) {
  const map = { gateway:'#e94560', router:'#f5a623', switch:'#2ed573', pc:'#1e90ff', mobile:'#a55eea', ap:'#ff6b6b', vm:'#7bed9f', unknown:'#555' };
  return map[role] || '#555';
}

function renderGraph(hosts) {
  const container = document.getElementById('graph');
  nodes = new vis.DataSet();
  edges = new vis.DataSet();

  hosts.forEach(h => {
    const ip = h.ip || '';
    const label = h.hostname || ip.split('.').pop();
    nodes.add({
      id: ip,
      label: label,
      title: `${ip}\n${h.mac || ''}\n${h.vendor || ''}\nOS: ${h.os_hint || '?'}\nRola: ${h.role || 'unknown'}`,
      color: { background: roleColor(h.role), border: '#333', highlight: { background: roleColor(h.role), border: '#fff' } },
      shape: h.role?.toLowerCase()?.includes('gateway') ? 'database' : 'dot',
      size: h.role?.toLowerCase()?.includes('gateway') ? 25 : 16
    });
  });

  // Group hosts by subnet for edges
  const subnets = {};
  hosts.forEach(h => {
    const subnet = h.ip?.substring(0, h.ip?.lastIndexOf('.')) + '.0/24';
    if (!subnets[subnet]) subnets[subnet] = [];
    subnets[subnet].push(h.ip);
  });

  hosts.forEach(h => {
    if (h.role?.toLowerCase()?.includes('gateway')) {
      // Connect gateway to other devices in same subnet
      const subnet = h.ip?.substring(0, h.ip?.lastIndexOf('.')) + '.0/24';
      (subnets[subnet] || []).forEach(other => {
        if (other !== h.ip) edges.add({ from: h.ip, to: other, color: { color: '#555' } });
      });
    }
  });

  // Remove disconnected nodes from edges
  const nodeIds = new Set(hosts.map(h => h.ip));
  edges.removeIf(e => !nodeIds.has(e.from) || !nodeIds.has(e.to));

  const data = { nodes, edges };
  const options = {
    physics: { enabled: true, hierarchicalRepulsion: { nodeDistance: 150 } },
    interaction: { hover: true, tooltipDelay: 200 },
    edges: { smooth: { type: 'continuous' } }
  };

  if (network) network.destroy();
  network = new vis.Network(container, data, options);
}

function renderTable(hosts) {
  const tbody = document.getElementById('hostsBody');
  tbody.innerHTML = hosts.map(h => `
    <tr>
      <td>${h.ip||''}</td>
      <td><code>${h.mac||''}</code></td>
      <td>${h.hostname||''}</td>
      <td>${h.vendor||''}</td>
      <td><span class="badge ${roleClass(h.role)}">${h.role||'unknown'}</span></td>
      <td>${h.os_hint||''}</td>
      <td>${(h.open_ports||[]).join(', ')||'-'}</td>
    </tr>
  `).join('');
}

async function runScan() {
  try {
    await fetch('/api/scan', { method: 'POST' });
    setTimeout(fetchHosts, 2000);
  } catch(e) { alert('Skan nie uruchomiony'); }
}

// Auto-refresh every 60s
setInterval(fetchHosts, 60000);
fetchHosts();