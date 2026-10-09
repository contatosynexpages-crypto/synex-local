// Anúncio de captação da Synex Local. render(t) desenha o quadro do segundo t (determinístico).
// window.SCENES, window.END e window.CAPTIONS vêm do timeline.js, que o gerar.py cria a partir da narração.
var S = window.SCENES || {s1: 0.5, s2: 7.19, s3: 13.03, s4: 19.52, s5: 23.27, s6: 30.51, s7: 37.66, s8: 42.52, s9: 45.6};
var END = window.END || 46.88;
var $ = function (id) { return document.getElementById(id); };
function cl(x) { return Math.max(0, Math.min(1, x)); }
function ez(x) { x = cl(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
function eo(x) { x = cl(x); return 1 - Math.pow(1 - x, 3); }
function p(t, a, b) { return ez((t - a) / (b - a)); }
function po(t, a, b) { return eo((t - a) / (b - a)); }
function scene(t) { var k = 's1'; for (var n in S) if (t >= S[n]) k = n; return k; }

/* ---------- ofícios em traço (gancho) ---------- */
var NS = 'http://www.w3.org/2000/svg', art = $('art'), strokes = [];
var trades = document.createElementNS(NS, 'g'); art.appendChild(trades);
function stroke(d, w, col) {
  var e = document.createElementNS(NS, 'path'); e.setAttribute('d', d); e.setAttribute('stroke', col || 'rgba(243,241,238,.8)');
  e.setAttribute('stroke-width', w || 4); e.setAttribute('stroke-linecap', 'round'); e.setAttribute('stroke-linejoin', 'round');
  e.setAttribute('fill', 'none'); trades.appendChild(e); strokes.push(e); return e; }
stroke('M120 1330 H960', 2, 'rgba(243,241,238,.25)');                                             // linha de base
// tesoura (salão / barbearia)
stroke('M150 1268 m-24 0 a24 24 0 1 0 48 0 a24 24 0 1 0 -48 0 M216 1268 m-24 0 a24 24 0 1 0 48 0 a24 24 0 1 0 -48 0');
stroke('M162 1248 L228 1130 M204 1248 L138 1130');
// chave inglesa (oficina)
stroke('M392 1290 L470 1180 M470 1180 a38 38 0 1 1 30 -62 l-22 26 l8 22 l24 4 l20 -26 a38 38 0 0 1 -60 36');
// fatia de pizza (lanchonete / pizzaria)
stroke('M622 1150 Q680 1118 738 1150 L680 1290 Z');
stroke('M664 1180 m-12 0 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0 M696 1214 m-10 0 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0', 3, 'rgba(232,40,58,.95)');
// raio (eletricista / serviços)
stroke('M928 1130 L882 1215 H926 L896 1292 L966 1196 H922 L956 1130 Z', 4, 'rgba(232,40,58,.95)');
var lens = strokes.map(function (s) { var L = s.getTotalLength(); s.style.strokeDasharray = L; return L; });

/* ---------- legendas e rótulos ---------- */
var CAP = window.CAPTIONS || [];
var STAMP = {s1: 'comércio local · litoral sul', s2: 'qui · 10:14 · Itanhaém', s3: 'qui · 10:14 · Itanhaém', s4: 'qui · 10:14 · o seu negócio',
  s5: 'com a Synex Local', s6: 'com a Synex Local', s7: 'qui · 10:20 · Itanhaém', s8: 'qui · 10:22', s9: 'Synex Local · Itanhaém · Peruíbe · Mongaguá'};
var WHO = {s1: '', s2: 'celular do cliente', s3: 'celular do cliente', s4: 'o seu celular', s5: 'exemplo de página', s6: 'exemplo de página',
  s7: 'celular da Renata', s8: 'o seu celular', s9: ''};

function typeText(t, a, b, txt) { var n = Math.round(cl((t - a) / (b - a)) * txt.length); return txt.slice(0, n); }
function tap(id, t, at, x, y) { var e = $(id), k = (t - at) / .55; e.style.left = x + 'px'; e.style.top = y + 'px';
  e.style.opacity = k < 0 || k > 1 ? 0 : (1 - k); e.style.transform = 'scale(' + (0.6 + k * 0.9) + ')'; }
function show(id, o) { $(id).style.opacity = o; }
function rise(id, k, dy) { var e = $(id); e.style.opacity = k; e.style.transform = 'translateY(' + (1 - k) * (dy || 30) + 'px)'; }

function render(t) {
  var sc = scene(t), L = t - S[sc];
  /* topo */
  var st = STAMP[sc]; $('stamp').innerHTML = st; $('stamp').style.opacity = sc === 's1' ? 1 : po(L, 0, .4);
  var w = WHO[sc]; if (sc === 's7' && L > 2.4) w = 'o seu celular';
  $('who').textContent = w; $('who').style.opacity = (w ? po(L, .1, .5) : 0) * (sc === 's8' ? 1 - p(L, 1.3, 1.7) : 1);
  /* legenda */
  var cur = null; CAP.forEach(function (c) { if (t >= c[0]) cur = c; });
  var cap = $('cap'); cap.innerHTML = cur ? '<span>' + cur[1] + '</span>' : '';
  cap.style.opacity = cur ? po(t, cur[0], cur[0] + .18) * (1 - p(t, END - .5, END)) : 0;
  cap.style.transform = 'translateY(' + (cur ? (1 - po(t, cur[0], cur[0] + .25)) * 14 : 0) + 'px)';

  /* gancho: título já visível no primeiro quadro (vira a capa) */
  var L1 = t - S.s1, hk = $('hook');
  var hkIn = t < S.s1 ? 1 : 1, hkOut = p(t, S.s2 - .45, S.s2 + .1);
  var punch = 1 + .035 * Math.sin(Math.min(L1, 5) * 2.2) * (L1 > 0 ? 1 : 0);
  var att = sc === 's1' && L1 > 5.2 ? po(L1, 5.2, 5.6) : 0;          // "Presta atenção": aperta e acende
  hk.style.opacity = hkIn * (1 - hkOut);
  hk.style.transform = 'translateY(' + (-40 * hkOut) + 'px) scale(' + (punch * (1 + .06 * att)) + ')';
  hk.querySelector('em').style.textShadow = att ? '0 0 ' + (40 * att) + 'px rgba(232,40,58,.8)' : 'none';
  strokes.forEach(function (s, i) { var a = .15 + i * .32; s.style.strokeDashoffset = lens[i] * (1 - po(t - S.s1, a, a + .9)); });
  trades.setAttribute('opacity', 1 - p(t, S.s2 - .45, S.s2 + .1));

  /* telefone */
  var ph = $('phone'), g = p(t, S.s2, S.s2 + .7);
  var phO = t < S.s2 ? 0 : po(t, S.s2, S.s2 + .35), dim = 1, down = 0, scl = .7 + .3 * g;
  if (sc === 's6') dim = 1 - .62 * p(L, 3.1, 3.5);
  if (sc === 's7') dim = 1;
  if (sc === 's8') { var k8 = p(L, 1.35, 2.1); phO = 1 - k8; down = 260 * k8; }
  if (sc === 's9') { phO = 0; }
  ph.style.opacity = phO * dim; ph.style.transform = 'translateY(' + ((1 - g) * 180 + down) + 'px) scale(' + scl + ')';

  /* camadas da tela */
  var lay = {g1: 0, lock: 0, pg: 0, g2: 0, chat: 0};
  if (sc === 's2' || sc === 's3') lay.g1 = 1;
  if (sc === 's4') { lay.lock = p(L, 0, .35); lay.g1 = 1 - lay.lock; }
  if (sc === 's5') { lay.pg = p(L, 0, .35); lay.lock = 1 - lay.pg; }
  if (sc === 's6') lay.pg = 1;
  if (sc === 's7') { var a7 = p(L, 0, .35), b7 = p(L, 2.3, 2.6); lay.g2 = a7 * (1 - b7); lay.pg = 1 - a7; lay.chat = b7; }
  if (sc === 's8' || sc === 's9') lay.chat = 1;
  for (var id in lay) show(id, lay[id]);

  /* busca do cliente */
  if (sc === 's2' || sc === 's3' || sc === 's4') {
    $('q1').textContent = typeText(t, S.s2 + .8, S.s2 + 3.0, 'eletricista em itanhaém');
    var L3 = t - S.s3;
    [['r1', .1], ['r2', .35], ['r3', .6]].forEach(function (r) { rise(r[0], t < S.s3 ? 0 : po(L3, r[1], r[1] + .35)); });
    var gh = t < S.s3 ? 0 : po(L3, 1.2, 1.55); rise('r4', gh, 20);
    $('r4').style.transform += ' scale(' + (1 + .04 * Math.sin(Math.max(0, L3 - 1.2) * 9) * (1 - p(L3, 1.2, 2.2))) + ')';
    var hl = t < S.s3 ? 0 : po(L3, 2.4, 2.8);
    $('r1').style.outline = hl ? '4px solid rgba(19,122,58,' + hl + ')' : 'none';
    tap('tap1', t, S.s3 + 3.2, 300, 360);
    $('dn1').style.opacity = t < S.s3 ? 0 : po(L3, 4.8, 5.2);
    $('r2').style.opacity = t >= S.s3 ? po(L3, .35, .7) * (1 - .45 * p(L3, 4.8, 5.2)) : 0;
    $('r3').style.opacity = t >= S.s3 ? po(L3, .6, .95) * (1 - .45 * p(L3, 4.8, 5.2)) : 0;
  }

  /* página de exemplo */
  var B = function (a) { return sc === 's5' ? po(t - S.s5, a, a + .45) : (t > S.s5 ? 1 : 0); };
  [['b1', 2.7], ['b2', 3.9], ['b3', 4.9]].forEach(function (b) { rise(b[0], B(b[1]), 26); });
  ['p1', 'p2', 'p3'].forEach(function (id, i) { var k = B(3.1 + i * .15); $(id).style.opacity = k; $(id).style.transform = 'scale(' + (.6 + .4 * k) + ')'; });
  var wk = sc === 's6' ? po(t - S.s6, .3, .75) : (t > S.s6 ? 1 : 0);
  var pulse = sc === 's6' && t - S.s6 > .8 ? 1 + .035 * Math.sin((t - S.s6) * 7) : 1;
  $('wab').style.opacity = wk; $('wab').style.transform = 'scale(' + ((.85 + .15 * wk) * pulse) + ')';

  /* preço */
  var pr = sc === 's6' ? po(L, 3.2, 3.6) : 0, prOut = sc === 's7' ? 1 - p(L, 0, .3) : 1;
  if (sc === 's7') pr = 1;
  $('price').style.opacity = pr * prOut * (sc === 's6' || sc === 's7' ? 1 : 0);
  $('price').style.transform = 'translateY(' + (1 - pr) * 40 + 'px) scale(' + (.94 + .06 * pr) + ')';

  /* busca de novo */
  if (sc === 's7') {
    $('q2').textContent = typeText(t, S.s7 + .2, S.s7 + 1.0, 'eletricista itanhaém');
    rise('s1r', po(L, 1.05, 1.4)); rise('s2r', po(L, 1.25, 1.6)); $('s2r').style.opacity = po(L, 1.25, 1.6) * .55;
    tap('tap3', t, S.s7 + 2.0, 300, 360);
  }
  /* conversa */
  var L7 = t - S.s7;
  var ty = sc === 's7' ? p(L7, 2.55, 2.7) * (1 - p(L7, 3.0, 3.1)) : 0; $('typ').style.opacity = ty;
  $('typ').querySelectorAll('span').forEach(function (d, i) { d.style.opacity = .4 + .6 * Math.max(0, Math.sin(t * 8 - i)); });
  var m1 = sc === 's7' ? po(L7, 3.05, 3.35) : (sc === 's8' ? 1 : 0); rise('m1', m1, 24);
  var m2 = sc === 's8' ? po(t - S.s8, .2, .5) : (sc === 's9' ? 1 : 0); rise('m2', m2, 24);

  /* agenda final */
  var ag = sc === 's8' ? po(t - S.s8, 1.75, 2.35) : (sc === 's9' ? 1 - p(L, 0, .4) : 0); rise('agenda', ag, 40);
  var ct = sc === 's9' ? po(L, .35, .8) : 0; rise('cta', ct, 40);
  var bp = sc === 's9' && L > 1.6 ? 1 + .04 * Math.sin((L - 1.6) * 6) : 1; $('ctabtn').style.transform = 'scale(' + bp + ')';
  var nk = sc === 's8' ? po(t - S.s8, 2.35, 2.75) : (sc === 's9' ? 1 : 0); $('snew').style.background = 'rgba(232,40,58,' + (.14 * nk) + ')';
  $('snew').style.boxShadow = 'inset 4px 0 0 rgba(232,40,58,' + nk + ')'; $('snew').style.paddingLeft = (nk * 18) + 'px';
  $('snew').querySelector('.chk').style.opacity = sc === 's8' ? po(t - S.s8, 2.75, 3.15) : (sc === 's9' ? 1 : 0);

  $('glow').style.transform = 'translate(' + Math.sin(t * .25) * 60 + 'px,' + Math.cos(t * .2) * 40 + 'px)';
}
window.render = render;
document.fonts.ready.then(function () { render(0); document.body.dataset.ready = '1'; });
