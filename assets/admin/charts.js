/* charts.js — pure SVG: grouped/stacked bars, line, donut, funnel,
   horizontal bars. Responsive via viewBox, theme-aware via CSS classes
   (.s0…s5 map to variables), accessible (role=img, aria-label, <title>),
   tooltips on hover and keyboard focus. No library. */
import { el, svg } from './dom.js';
import { t } from './i18n.js';
import { fmtNum } from './format.js';

const W = 640;
function niceMax(v) {
  if (!v || v <= 0) return 1;
  const p = Math.pow(10, Math.floor(Math.log10(v)));
  const m = v / p;
  const n = m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10;
  return n * p;
}
function shortNum(v) {
  const a = Math.abs(v);
  if (a >= 1e9) return (v / 1e9).toFixed(1).replace(/\.0$/, '') + 'B';
  if (a >= 1e6) return (v / 1e6).toFixed(1).replace(/\.0$/, '') + 'M';
  if (a >= 1e3) return (v / 1e3).toFixed(a >= 1e5 ? 0 : 1).replace(/\.0$/, '') + 'k';
  return String(Math.round(v * 100) / 100);
}
function wrapChart(node, label, legend) {
  const root = el('div', { class: 'chart' }, node);
  const tip = el('div', { class: 'chart-tip', hidden: true, role: 'tooltip' });
  root.appendChild(tip);
  root.tip = tip;
  if (legend && legend.length) root.appendChild(el('div', { class: 'legend' }, legend.map((s, i) => el('span', { class: 's' + (i % 6) }, el('i'), s))));
  return root;
}
function attachTip(root, shape, text) {
  const show = (e) => {
    const r = root.getBoundingClientRect(); const b = shape.getBoundingClientRect();
    root.tip.textContent = text; root.tip.hidden = false;
    root.tip.style.left = (b.left + b.width / 2 - r.left) + 'px';
    root.tip.style.top = (b.top - r.top) + 'px';
  };
  const hide = () => { root.tip.hidden = true; };
  shape.addEventListener('mouseenter', show); shape.addEventListener('mouseleave', hide);
  shape.addEventListener('focus', show); shape.addEventListener('blur', hide);
  shape.setAttribute('tabindex', '0');
  shape.appendChild(svg('title', null, text));
}

/** barChart({categories:[], series:[{label, values:[]}], stacked, format, height}) */
export function barChart(o) {
  const H = o.height || 240, padL = 44, padB = 28, padT = 10, padR = 8;
  const cats = o.categories || [], series = o.series || [];
  const fmt = o.format || fmtNum;
  const n = cats.length || 1;
  let maxV = 0;
  cats.forEach((c, i) => { const vals = series.map((s) => Number(s.values[i]) || 0); maxV = Math.max(maxV, o.stacked ? vals.reduce((a, b) => a + b, 0) : Math.max(...vals, 0)); });
  const top = niceMax(maxV);
  const plotW = W - padL - padR, plotH = H - padT - padB;
  const y = (v) => padT + plotH - (v / top) * plotH;
  const s = svg('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': o.label || t('misc.chart') }, svg('title', null, o.label || t('misc.chart')));
  for (let g = 0; g <= 4; g++) {
    const v = (top / 4) * g;
    s.appendChild(svg('line', { class: g ? 'grid' : 'axis', x1: padL, x2: W - padR, y1: y(v), y2: y(v) }));
    s.appendChild(svg('text', { x: padL - 6, y: y(v) + 4, 'text-anchor': 'end' }, shortNum(v)));
  }
  const root = wrapChart(s, o.label, series.length > 1 ? series.map((x) => x.label) : null);
  const slot = plotW / n;
  const bw = o.stacked ? Math.min(40, slot * 0.6) : Math.min(28, (slot * 0.7) / Math.max(1, series.length));
  cats.forEach((c, i) => {
    let acc = 0;
    series.forEach((ser, si) => {
      const v = Number(ser.values[i]) || 0;
      const x = o.stacked ? padL + slot * i + (slot - bw) / 2 : padL + slot * i + (slot - bw * series.length) / 2 + bw * si;
      const y0 = o.stacked ? y(acc + v) : y(v);
      const h = o.stacked ? y(acc) - y0 : y(0) - y0;
      const rect = svg('rect', { class: 'bar s' + (si % 6), x, y: y0, width: bw, height: Math.max(0, h), rx: 2 });
      attachTip(root, rect, c + ' · ' + ser.label + ': ' + fmt(v));
      s.appendChild(rect);
      if (o.stacked) acc += v;
    });
    if (n <= 16 || i % Math.ceil(n / 12) === 0) s.appendChild(svg('text', { x: padL + slot * i + slot / 2, y: H - 8, 'text-anchor': 'middle' }, String(c)));
  });
  return root;
}

/** lineChart({categories, series:[{label, values}], format}) */
export function lineChart(o) {
  const H = o.height || 220, padL = 44, padB = 28, padT = 10, padR = 8;
  const cats = o.categories || [], series = o.series || [];
  const fmt = o.format || fmtNum;
  let maxV = 0; series.forEach((sr) => sr.values.forEach((v) => { maxV = Math.max(maxV, Number(v) || 0); }));
  const top = niceMax(maxV);
  const plotW = W - padL - padR, plotH = H - padT - padB;
  const y = (v) => padT + plotH - (v / top) * plotH;
  const x = (i) => padL + (cats.length > 1 ? (plotW * i) / (cats.length - 1) : plotW / 2);
  const s = svg('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': o.label || t('misc.chart') }, svg('title', null, o.label || t('misc.chart')));
  for (let g = 0; g <= 4; g++) { const v = (top / 4) * g; s.appendChild(svg('line', { class: g ? 'grid' : 'axis', x1: padL, x2: W - padR, y1: y(v), y2: y(v) })); s.appendChild(svg('text', { x: padL - 6, y: y(v) + 4, 'text-anchor': 'end' }, shortNum(v))); }
  const root = wrapChart(s, o.label, series.length > 1 ? series.map((z) => z.label) : null);
  series.forEach((sr, si) => {
    const d = sr.values.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(Number(v) || 0).toFixed(1)).join(' ');
    s.appendChild(svg('path', { class: 'line s' + (si % 6), d }));
    sr.values.forEach((v, i) => {
      const c = svg('circle', { class: 'pt s' + (si % 6), cx: x(i), cy: y(Number(v) || 0), r: 3.5 });
      attachTip(root, c, cats[i] + ' · ' + sr.label + ': ' + fmt(Number(v) || 0));
      s.appendChild(c);
    });
  });
  cats.forEach((c, i) => { if (cats.length <= 16 || i % Math.ceil(cats.length / 12) === 0) s.appendChild(svg('text', { x: x(i), y: H - 8, 'text-anchor': 'middle' }, String(c))); });
  return root;
}

/** donutChart({items:[{label, value}], format}) */
export function donutChart(o) {
  const items = (o.items || []).filter((i) => Number(i.value) > 0);
  const total = items.reduce((a, b) => a + Number(b.value), 0);
  const size = 200, r = 78, cx = 100, cy = 100, stroke = 26;
  const s = svg('svg', { viewBox: '0 0 ' + size + ' ' + size, role: 'img', 'aria-label': o.label || t('misc.chart'), style: { maxWidth: '240px', margin: '0 auto' } }, svg('title', null, o.label || t('misc.chart')));
  const root = wrapChart(s, o.label, items.map((i) => i.label + ' ' + fmtNum(i.value)));
  if (!total) { s.appendChild(svg('circle', { cx, cy, r, fill: 'none', class: 'grid', 'stroke-width': stroke })); s.appendChild(svg('text', { x: cx, y: cy + 4, 'text-anchor': 'middle' }, t('misc.no_data'))); return root; }
  const circ = 2 * Math.PI * r; let off = 0;
  items.forEach((it, i) => {
    const frac = Number(it.value) / total;
    const c = svg('circle', { class: 'slice s' + (i % 6), cx, cy, r, fill: 'none', stroke: 'currentColor', 'stroke-width': stroke,
      'stroke-dasharray': (frac * circ).toFixed(2) + ' ' + (circ - frac * circ).toFixed(2), 'stroke-dashoffset': (-off * circ).toFixed(2), transform: 'rotate(-90 ' + cx + ' ' + cy + ')' });
    c.setAttribute('style', 'stroke: var(--' + ['teal', 'amber', 'green', 'muted', 'red', 'ink2'][i % 6] + ')');
    attachTip(root, c, it.label + ': ' + (o.format || fmtNum)(it.value) + ' (' + Math.round(frac * 100) + '%)');
    s.appendChild(c); off += frac;
  });
  s.appendChild(svg('text', { x: cx, y: cy + 6, 'text-anchor': 'middle', style: { fontSize: '20px', fill: 'var(--ink)' } }, fmtNum(total)));
  return root;
}

/** funnelChart({steps:[{label, value}]}) — bars shrink with value; shows % of first. */
export function funnelChart(o) {
  const steps = o.steps || []; const rowH = 34, H = steps.length * rowH + 8, labelW = 150;
  const max = Math.max(1, ...steps.map((s) => Number(s.value) || 0));
  const s = svg('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': o.label || t('misc.chart'), class: 'funnel' }, svg('title', null, o.label || t('misc.chart')));
  const root = wrapChart(s, o.label);
  steps.forEach((st, i) => {
    const v = Number(st.value) || 0; const w = ((W - labelW - 70) * v) / max; const y = 4 + i * rowH;
    s.appendChild(svg('text', { x: labelW - 8, y: y + 20, 'text-anchor': 'end' }, st.label));
    const rect = svg('rect', { x: labelW, y, width: Math.max(2, w), height: rowH - 8, rx: 3, class: 'bar', style: 'fill:var(--teal);opacity:' + (1 - i * 0.12) });
    const pct = steps[0] && Number(steps[0].value) ? Math.round((v / Number(steps[0].value)) * 100) : 0;
    attachTip(root, rect, st.label + ': ' + fmtNum(v) + ' (' + pct + '%)');
    s.appendChild(rect);
    s.appendChild(svg('text', { x: labelW + Math.max(2, w) + 8, y: y + 20, style: { fill: 'var(--ink)' } }, fmtNum(v) + (i ? ' · ' + pct + '%' : '')));
  });
  return root;
}

/** hbarChart({categories, series:[{label, values}], format}) — grouped horizontal bars. */
export function hbarChart(o) {
  const cats = o.categories || [], series = o.series || []; const fmt = o.format || fmtNum;
  const labelW = 150, rowH = series.length > 1 ? 14 * series.length + 10 : 24, H = cats.length * rowH + 8;
  let max = 1; series.forEach((sr) => sr.values.forEach((v) => { max = Math.max(max, Number(v) || 0); }));
  const s = svg('svg', { viewBox: '0 0 ' + W + ' ' + Math.max(H, 40), role: 'img', 'aria-label': o.label || t('misc.chart') }, svg('title', null, o.label || t('misc.chart')));
  const root = wrapChart(s, o.label, series.length > 1 ? series.map((z) => z.label) : null);
  if (!cats.length) { s.appendChild(svg('text', { x: W / 2, y: 24, 'text-anchor': 'middle' }, t('misc.no_data'))); return root; }
  cats.forEach((c, i) => {
    const y0 = 4 + i * rowH;
    s.appendChild(svg('text', { x: labelW - 8, y: y0 + rowH / 2 + 4, 'text-anchor': 'end' }, String(c)));
    series.forEach((sr, si) => {
      const v = Number(sr.values[i]) || 0; const w = ((W - labelW - 60) * v) / max; const bh = series.length > 1 ? 12 : rowH - 8;
      const y = series.length > 1 ? y0 + 4 + si * 14 : y0 + 4;
      const rect = svg('rect', { class: 'bar s' + (si % 6), x: labelW, y, width: Math.max(1, w), height: bh, rx: 2 });
      attachTip(root, rect, c + ' · ' + sr.label + ': ' + fmt(v));
      s.appendChild(rect);
      s.appendChild(svg('text', { x: labelW + Math.max(1, w) + 6, y: y + bh - 2, style: { fill: 'var(--ink)' } }, shortNum(v)));
    });
  });
  return root;
}
