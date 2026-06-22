/* ============================================================
   NYC Taxi Pulse — Dashboard Logic
   app.js
   ============================================================ */

const API_BASE = 'https://ideal-telegram-7v4g7vp7977q2r669-5000.app.github.dev';

const BOROUGH_COLORS = {
  Manhattan:       '#1D9E75',
  Brooklyn:        '#378ADD',
  Queens:          '#BA7517',
  Bronx:           '#D4537E',
  'Staten Island': '#7F77DD',
  EWR:             '#999999'
};

const TIME_OF_DAY_ORDER = ['Morning', 'Afternoon', 'Evening', 'Night'];

const PAYMENT_LABELS = {
  '1': 'Credit Card',
  '2': 'Cash',
  '3': 'No Charge',
  '4': 'Dispute',
  '5': 'Unknown',
  '6': 'Voided'
};

let hourlyInst = null;
let fareInst   = null;
let donutInst  = null;

async function fetchTopZones() {
  const res = await fetch(`${API_BASE}/api/insights/top-zones`);
  return res.json();
}
async function fetchAvgFareByTime() {
  const res = await fetch(`${API_BASE}/api/insights/avg-fare-by-time`);
  return res.json();
}
async function fetchPaymentTypes() {
  const res = await fetch(`${API_BASE}/api/insights/payment-types`);
  return res.json();
}
async function fetchTrips(borough, timeOfDay) {
  let url = `${API_BASE}/api/trips?limit=1000`;
  if (borough   && borough   !== 'all') url += `&borough=${encodeURIComponent(borough)}`;
  if (timeOfDay && timeOfDay !== 'all') url += `&time_of_day=${encodeURIComponent(timeOfDay)}`;
  const res = await fetch(url);
  return res.json();
}
async function fetchBoroughs() {
  const res = await fetch(`${API_BASE}/api/zones/boroughs`);
  return res.json();
}

function fmtNum(n)   { return Number(n).toLocaleString(); }
function fmtMoney(n) { return '$' + Number(n).toFixed(2); }

function setStatLoading() {
  ['s-trips','s-fare','s-dist','s-dur','s-peak'].forEach(id => {
    document.getElementById(id).textContent = '…';
  });
}

async function populateBoroughs() {
  try {
    const data   = await fetchBoroughs();
    const select = document.getElementById('f-borough');
    while (select.options.length > 1) select.remove(1);
    data.forEach(row => {
      const opt       = document.createElement('option');
      opt.value       = row.borough;
      opt.textContent = row.borough;
      select.appendChild(opt);
    });
  } catch (err) {
    console.warn('Could not load boroughs:', err);
  }
}

function updateStats(fareByTime, trips) {
  const totalTrips = trips.length;
  const avgFare    = totalTrips ? trips.reduce((s,t) => s + Number(t.fare_amount||0), 0) / totalTrips : 0;
  const avgDist    = totalTrips ? trips.reduce((s,t) => s + Number(t.trip_distance||0), 0) / totalTrips : 0;
  const avgDur     = totalTrips ? trips.reduce((s,t) => s + Number(t.trip_duration_minutes||0), 0) / totalTrips : 0;
  const peak       = fareByTime.reduce((best,row) => Number(row.total_trips) > Number(best.total_trips||0) ? row : best, {});
  document.getElementById('s-trips').textContent = fmtNum(totalTrips);
  document.getElementById('s-fare').textContent  = fmtMoney(avgFare);
  document.getElementById('s-dist').textContent  = avgDist.toFixed(1);
  document.getElementById('s-dur').textContent   = Math.round(avgDur);
  document.getElementById('s-peak').textContent  = peak.time_of_day || '—';
}

function updateHourly(fareByTime) {
  const sorted = TIME_OF_DAY_ORDER.map(t =>
    fareByTime.find(r => r.time_of_day === t) || { time_of_day: t, avg_fare: 0, total_trips: 0 }
  );
  document.getElementById('borough-legend').innerHTML = `
    <span class="legend-item"><span class="legend-sq" style="background:#1D9E75"></span>Avg Fare ($)</span>
    <span class="legend-item"><span class="legend-sq" style="background:#378ADD"></span>Trip Count</span>`;
  if (hourlyInst) hourlyInst.destroy();
  hourlyInst = new Chart(document.getElementById('hourlyChart'), {
    type: 'bar',
    data: {
      labels: sorted.map(r => r.time_of_day),
      datasets: [
        { label:'Avg Fare ($)', data: sorted.map(r => Number(r.avg_fare)), backgroundColor:'#1D9E7599', borderColor:'#1D9E75', borderWidth:1, borderRadius:4, yAxisID:'yFare' },
        { label:'Trip Count',  data: sorted.map(r => Number(r.total_trips)), backgroundColor:'#378ADD55', borderColor:'#378ADD', borderWidth:2, type:'line', tension:0.35, pointRadius:5, fill:false, yAxisID:'yTrips' }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x:      { ticks:{ color:'#8b90a0', font:{size:11} }, grid:{ color:'rgba(255,255,255,0.04)' } },
        yFare:  { type:'linear', position:'left',  beginAtZero:true, ticks:{ color:'#1D9E75', font:{size:10}, callback: v => '$'+v }, grid:{ color:'rgba(255,255,255,0.04)' } },
        yTrips: { type:'linear', position:'right', beginAtZero:true, ticks:{ color:'#378ADD', font:{size:10} }, grid:{ drawOnChartArea:false } }
      }
    }
  });
}

function updateHeatmap(trips) {
  const boroughs = [...new Set(trips.map(t => t.pickup_borough).filter(Boolean))].sort();
  const times    = TIME_OF_DAY_ORDER;
  const grid     = {};
  boroughs.forEach(b => { grid[b] = {}; times.forEach(t => { grid[b][t] = 0; }); });
  trips.forEach(t => { if (t.pickup_borough && t.time_of_day && grid[t.pickup_borough]) grid[t.pickup_borough][t.time_of_day]++; });
  const allVals = boroughs.flatMap(b => times.map(t => grid[b][t]));
  const maxV    = Math.max(...allVals) || 1;
  const getColor = ratio => { const stops=['#0f2a1e','#0F6E56','#1D9E75','#5DCAA5','#9FE1CB','#E1F5EE']; return stops[Math.min(Math.floor(ratio*(stops.length-1)),stops.length-1)]; };
  let html = `<div class="heatmap-grid" style="grid-template-columns:110px repeat(${times.length},1fr)">`;
  html += '<div></div>' + times.map(t => `<div class="hm-hour">${t}</div>`).join('');
  boroughs.forEach(b => {
    html += `<div class="hm-label" style="font-size:10px;justify-content:flex-start;padding-left:2px">${b}</div>`;
    times.forEach(t => { const v=grid[b][t]; html += `<div class="hm-cell" style="background:${getColor(v/maxV)}" title="${b}·${t}:${v} trips"></div>`; });
  });
  html += '</div>';
  document.getElementById('heatmap').innerHTML = html;
}

function updateZones(topZones) {
  if (!topZones.length) { document.getElementById('zones-list').innerHTML = '<p style="color:var(--muted);font-size:12px">No data</p>'; return; }
  const max = Number(topZones[0]?.trip_count) || 1;
  document.getElementById('zones-list').innerHTML = topZones.map((z,i) => `
    <div class="zone-row">
      <span class="zone-rank">${i+1}</span>
      <span class="zone-name">${z.borough||'Unknown'}</span>
      <div class="zone-bar-wrap"><div class="zone-bar" style="width:${Math.round(Number(z.trip_count)/max*100)}%"></div></div>
      <span class="zone-count">${(Number(z.trip_count)/1000).toFixed(1)}k</span>
    </div>`).join('');
}

function updateFare(paymentTypes) {
  if (fareInst) fareInst.destroy();
  fareInst = new Chart(document.getElementById('fareChart'), {
    type: 'bar',
    data: {
      labels: paymentTypes.map(p => PAYMENT_LABELS[String(p.payment_type)]||'Type '+p.payment_type),
      datasets: [
        { label:'Trip Count', data:paymentTypes.map(p=>Number(p.count)), backgroundColor:'#1D9E7599', borderColor:'#1D9E75', borderWidth:1, borderRadius:4, yAxisID:'yCount' },
        { label:'Avg Tip ($)', data:paymentTypes.map(p=>Number(p.avg_tip)), backgroundColor:'#BA751755', borderColor:'#BA7517', borderWidth:2, type:'line', tension:0.3, pointRadius:4, fill:false, yAxisID:'yTip' }
      ]
    },
    options: {
      responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{ display:false } },
      scales: {
        x:      { ticks:{ color:'#8b90a0', font:{size:10} }, grid:{ color:'rgba(255,255,255,0.04)' } },
        yCount: { type:'linear', position:'left',  beginAtZero:true, ticks:{ color:'#1D9E75', font:{size:10} }, grid:{ color:'rgba(255,255,255,0.04)' } },
        yTip:   { type:'linear', position:'right', beginAtZero:true, ticks:{ color:'#BA7517', font:{size:10}, callback:v=>'$'+v }, grid:{ drawOnChartArea:false } }
      }
    }
  });
}

function updateDonut(trips) {
  const counts  = {};
  trips.forEach(t => { const b=t.pickup_borough||'Unknown'; counts[b]=(counts[b]||0)+1; });
  const entries = Object.entries(counts).sort((a,b)=>b[1]-a[1]);
  const total   = entries.reduce((s,[,v])=>s+v,0)||1;
  document.getElementById('donut-legend').innerHTML = entries.map(([b,v]) =>
    `<span class="legend-item"><span class="legend-sq" style="background:${BOROUGH_COLORS[b]||'#999'}"></span>${b} ${Math.round(v/total*100)}%</span>`).join('');
  if (donutInst) donutInst.destroy();
  donutInst = new Chart(document.getElementById('donutChart'), {
    type:'doughnut',
    data:{ labels:entries.map(([b])=>b), datasets:[{ data:entries.map(([,v])=>v), backgroundColor:entries.map(([b])=>BOROUGH_COLORS[b]||'#999'), borderWidth:2, borderColor:'#1e2130' }] },
    options:{ responsive:true, maintainAspectRatio:false, cutout:'64%', plugins:{ legend:{ display:false } } }
  });
}

function showError(msg) {
  console.error(msg);
  document.getElementById('s-trips').textContent = 'Error';
}

async function applyFilters() {
  const borough   = document.getElementById('f-borough').value;
  const timeOfDay = document.getElementById('f-hour').value;
  setStatLoading();
  try {
    const [topZones, fareByTime, paymentTypes, trips] = await Promise.all([
      fetchTopZones(), fetchAvgFareByTime(), fetchPaymentTypes(), fetchTrips(borough, timeOfDay)
    ]);
    updateStats(fareByTime, trips);
    updateHourly(fareByTime);
    updateHeatmap(trips);
    updateZones(topZones);
    updateFare(paymentTypes);
    updateDonut(trips);
  } catch (err) {
    showError('API error: ' + err.message);
  }
}

(async () => {
  await populateBoroughs();
  await applyFilters();
})();
