// ── CONFIGURACIÓN ──────────────────────────────────────

export { cargarDatos };
// Ruta al reporte.json generado por alertas.py
// Ajusta la ruta según desde dónde abres el index.html
const REPORTE_PATH = '../../gestoria-lopez/p1-alertas-automaticas/reporte.json';


// ── ESTADO GLOBAL ──────────────────────────────────────
let datos = null;

// ── CARGA DE DATOS ─────────────────────────────────────
async function cargarDatos() {
  try {
    const response = await fetch(REPORTE_PATH);
    if (!response.ok) throw new Error('No se pudo cargar el reporte');
    datos = await response.json();
    renderDashboard();
  } catch (e) {
    console.error('Error cargando reporte:', e);
    document.getElementById('alertas-list').innerHTML =
      '<p style="padding:16px;color:#D32F2F;">⚠️ No se pudo cargar el reporte. Ejecuta alertas.py primero.</p>';
  }
}

// ── RENDER PRINCIPAL ───────────────────────────────────
function renderDashboard() {
  renderFecha();
  renderKPIs();
  renderAlertas();
  renderCharts();
  renderClientes();
  renderFooter();
}

// ── FECHA ──────────────────────────────────────────────
function renderFecha() {
  const el = document.getElementById('topbar-fecha');
  if (el) el.textContent = datos.fecha;
}

// ── KPIs ───────────────────────────────────────────────
function renderKPIs() {
  const urgent  = datos.alertas.filter(a => a.dias_restantes <= 5).length;
  const warning = datos.alertas.filter(a => a.dias_restantes > 5 && a.dias_restantes <= 15).length;
  const ok      = datos.alertas.filter(a => a.dias_restantes > 15).length;

  document.getElementById('kpi-total').textContent   = datos.total;
  document.getElementById('kpi-urgent').textContent  = urgent;
  document.getElementById('kpi-warning').textContent = warning;
  document.getElementById('kpi-ok').textContent      = ok;
}

// ── ALERTAS ────────────────────────────────────────────
function renderAlertas() {
  const container = document.getElementById('alertas-list');
  if (!datos.alertas.length) {
    container.innerHTML = '<p style="padding:16px;color:#8A96A8;">✅ No hay alertas pendientes.</p>';
    return;
  }

  // Ordenar por urgencia — menos días primero
  const sorted = [...datos.alertas].sort((a, b) => a.dias_restantes - b.dias_restantes);

  container.innerHTML = sorted.map(a => {
    const { dot, badge, label } = getUrgencia(a.dias_restantes);
    return `
      <div class="alert-row">
        <div class="alert-dot" style="background:${dot};"></div>
        <div class="alert-info">
          <p class="alert-name">${a.obligacion}</p>
          <p class="alert-client">${a.cliente}</p>
        </div>
        <span class="badge ${badge}">${a.dias_restantes} días</span>
      </div>
    `;
  }).join('');
}

// ── CHARTS ─────────────────────────────────────────────
function renderCharts() {
  // Por obligación
  const porObligacion = {};
  datos.alertas.forEach(a => {
    // Extraemos solo el tipo (IVA, IRPF, IS) del nombre completo
    const tipo = a.obligacion.split(' ')[0];
    porObligacion[tipo] = (porObligacion[tipo] || 0) + 1;
  });

  const maxObl = Math.max(...Object.values(porObligacion));
  const coloresObl = ['#3D2B1F', '#7D5A4F', '#A8836F'];

  document.getElementById('chart-obligacion').innerHTML = Object.entries(porObligacion)
    .map(([nombre, count], i) => `
      <div class="bar-row">
        <span class="bar-name">${nombre}</span>
        <div class="bar-track">
          <div class="bar-fill" style="width:${(count/maxObl)*100}%;background:${coloresObl[i % coloresObl.length]};"></div>
        </div>
        <span class="bar-count">${count}</span>
      </div>
    `).join('');

  // Por urgencia
  const urgent  = datos.alertas.filter(a => a.dias_restantes <= 5).length;
  const warning = datos.alertas.filter(a => a.dias_restantes > 5 && a.dias_restantes <= 15).length;
  const ok      = datos.alertas.filter(a => a.dias_restantes > 15).length;
  const maxUrg  = Math.max(urgent, warning, ok);

  document.getElementById('chart-urgencia').innerHTML = [
    { label: '5d',  count: urgent,  color: '#D32F2F' },
    { label: '15d', count: warning, color: '#E67E00' },
    { label: '30d', count: ok,      color: '#2E7D32' },
  ].map(({ label, count, color }) => `
    <div class="bar-row">
      <span class="bar-name" style="color:${color};">${label}</span>
      <div class="bar-track">
        <div class="bar-fill" style="width:${maxUrg ? (count/maxUrg)*100 : 0}%;background:${color};"></div>
      </div>
      <span class="bar-count">${count}</span>
    </div>
  `).join('');
}

// ── CLIENTES ───────────────────────────────────────────
function renderClientes() {
  // Construimos el estado de cada cliente a partir de las alertas
  const clienteMap = {};
  datos.alertas.forEach(a => {
    if (!clienteMap[a.cliente]) {
      clienteMap[a.cliente] = { obligaciones: new Set(), minDias: a.dias_restantes };
    }
    const tipo = a.obligacion.split(' ')[0];
    clienteMap[a.cliente].obligaciones.add(tipo);
    clienteMap[a.cliente].minDias = Math.min(clienteMap[a.cliente].minDias, a.dias_restantes);
  });

  const count = Object.keys(clienteMap).length;
  document.getElementById('clientes-count').textContent = `${count} activos`;

  document.getElementById('clientes-grid').innerHTML = Object.entries(clienteMap)
    .map(([nombre, info]) => {
      const { badge, label } = getUrgencia(info.minDias);
      const obligaciones = [...info.obligaciones].join(' · ');
      return `
        <div class="client-card">
          <p class="client-name">${nombre}</p>
          <p class="client-obligations">${obligaciones}</p>
          <span class="badge ${badge}">${label}</span>
        </div>
      `;
    }).join('');
}

// ── FOOTER ─────────────────────────────────────────────
function renderFooter() {
  const el = document.getElementById('footer-fecha');
  if (el) el.textContent = `Última actualización: ${datos.fecha}`;
}

// ── NAVEGACIÓN ─────────────────────────────────────────
function showSection(seccion) {
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  event.currentTarget.classList.add('active');
  // Las secciones adicionales se implementarán en proyectos futuros
  console.log(`Navegando a: ${seccion}`);
}

// ── HELPERS ────────────────────────────────────────────
function getUrgencia(dias) {
  if (dias <= 5)  return { dot: '#D32F2F', badge: 'badge-urgent',  label: 'urgente' };
  if (dias <= 15) return { dot: '#E67E00', badge: 'badge-warning', label: 'próxima' };
  return              { dot: '#2E7D32', badge: 'badge-ok',      label: 'en plazo' };
}

