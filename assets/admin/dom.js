/* dom.js — build DOM without innerHTML. el(tag, attrs, ...children):
   attrs may hold class, dataset, style, on<Event> handlers, aria-* and
   any attribute; children are strings (text nodes), nodes, arrays, or
   null/false (skipped). Untrusted data never touches innerHTML. */

const SVG_NS = 'http://www.w3.org/2000/svg';

function apply(node, attrs, isSvg) {
  if (!attrs) return;
  for (const k of Object.keys(attrs)) {
    const v = attrs[k];
    if (v == null || v === false) continue;
    if (k === 'class' || k === 'className') node.setAttribute('class', v);
    else if (k === 'text') node.textContent = String(v);
    else if (k === 'dataset') for (const d of Object.keys(v)) node.dataset[d] = v[d];
    else if (k === 'style' && typeof v === 'object') Object.assign(node.style, v);
    else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2).toLowerCase(), v);
    else if (!isSvg && (k === 'value' || k === 'checked' || k === 'disabled' || k === 'selected' || k === 'readOnly' || k === 'indeterminate')) node[k] = v;
    else if (v === true) node.setAttribute(k, '');
    else node.setAttribute(k, String(v));
  }
}

function append(node, child) {
  if (child == null || child === false) return;
  if (Array.isArray(child)) { child.forEach((c) => append(node, c)); return; }
  if (child instanceof Node) { node.appendChild(child); return; }
  node.appendChild(document.createTextNode(String(child)));
}

export function el(tag, attrs, ...children) {
  const node = document.createElement(tag);
  apply(node, attrs, false);
  children.forEach((c) => append(node, c));
  return node;
}

export function svg(tag, attrs, ...children) {
  const node = document.createElementNS(SVG_NS, tag);
  apply(node, attrs, true);
  children.forEach((c) => append(node, c));
  return node;
}

export function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); return node; }
export function mount(node, ...children) { clear(node); children.forEach((c) => append(node, c)); return node; }
export function frag(...children) { const f = document.createDocumentFragment(); children.forEach((c) => append(f, c)); return f; }

/* A few line glyphs for controls that need one (no decorative icons). */
const PATHS = {
  search: 'M11 4a7 7 0 1 1 0 14a7 7 0 0 1 0-14zM20 20l-4-4',
  sun: 'M12 4v2M12 18v2M4 12h2M18 12h2M6.3 6.3l1.4 1.4M16.3 16.3l1.4 1.4M6.3 17.7l1.4-1.4M16.3 7.7l1.4-1.4M12 8a4 4 0 1 0 0 8a4 4 0 0 0 0-8z',
  moon: 'M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z',
  close: 'M6 6l12 12M18 6L6 18',
  chevL: 'M14 6l-6 6l6 6', chevR: 'M10 6l6 6l-6 6', chevD: 'M6 10l6 6l6-6',
  home: 'M4 11l8-7l8 7v9a1 1 0 0 1-1 1h-5v-6h-4v6H5a1 1 0 0 1-1-1z',
  inbox: 'M4 13V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v7M4 13h5l1 2h4l1-2h5M4 13v5a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5',
  cart: 'M4 5h2l2 10h10l2-7H7M9 20a1 1 0 1 0 0-2a1 1 0 0 0 0 2zM17 20a1 1 0 1 0 0-2a1 1 0 0 0 0 2z',
  people: 'M16 19v-1a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v1M9.5 11a3.5 3.5 0 1 0 0-7a3.5 3.5 0 0 0 0 7zM21 19v-1a4 4 0 0 0-3-3.9M16 4.1a3.5 3.5 0 0 1 0 6.8',
  dots: 'M5 12h.01M12 12h.01M19 12h.01',
  check: 'M5 12l5 5l9-10',
  print: 'M6 9V3h12v6M6 18H4a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1h-2M6 14h12v7H6z',
};
export function glyph(name, size) {
  const s = size || 18;
  return svg('svg', { width: s, height: s, viewBox: '0 0 24 24', 'aria-hidden': 'true', focusable: 'false',
    fill: 'none', stroke: 'currentColor', 'stroke-width': '1.7', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' },
    svg('path', { d: PATHS[name] || PATHS.dots }));
}

/** Small helpers used everywhere. */
export function link(href, text, attrs) { return el('a', Object.assign({ href }, attrs || {}), text); }
export function btn(text, onClick, cls, attrs) {
  return el('button', Object.assign({ type: 'button', class: 'btn' + (cls ? ' ' + cls : ''), onClick }, attrs || {}), text);
}
export function debounce(fn, ms) {
  let t = 0;
  return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
}
