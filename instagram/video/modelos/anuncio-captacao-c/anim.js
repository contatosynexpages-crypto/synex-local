// Anúncio C (curto, oferta, salão). render(t) desenha o quadro do segundo t (determinístico).
var S = window.SCENES || {s1: 0.5, s2: 5.32, s3: 9.32, s4: 13.58, s5: 16.87};
var END = window.END || 23.51;
var $ = function (id) { return document.getElementById(id); };
function cl(x) { return Math.max(0, Math.min(1, x)); }
function ez(x) { x = cl(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
function eo(x) { x = cl(x); return 1 - Math.pow(1 - x, 3); }
function p(t, a, b) { return ez((t - a) / (b - a)); }
function po(t, a, b) { return eo((t - a) / (b - a)); }
function scene(t) { var k = 's1'; for (var n in S) if (t >= S[n]) k = n; return k; }
function typeText(t, a, b, txt) { var n = Math.round(cl((t - a) / (b - a)) * txt.length); return txt.slice(0, n); }
function tap(id, t, at, x, y) { var e = $(id), k = (t - at) / .55; e.style.left = x + 'px'; e.style.top = y + 'px';
  e.style.opacity = k < 0 || k > 1 ? 0 : (1 - k); e.style.transform = 'scale(' + (0.6 + k * 0.9) + ')'; }
function rise(id, k, dy) { var e = $(id); e.style.opacity = k; e.style.transform = 'translateY(' + (1 - k) * (dy || 30) + 'px)'; }

var CAP = window.CAPTIONS || [];
var STAMP = {s1: 'qui · 21:10 · Peruíbe', s2: 'com a Synex Local', s3: 'com a Synex Local', s4: 'qui · 21:12 · Peruíbe', s5: 'Synex Local · página de vendas'};

function render(t) {
  var sc = scene(t), L = t - S[sc], L1 = t - S.s1;
  /* topo */
  $('stamp').innerHTML = STAMP[sc]; $('stamp').style.opacity = sc === 's1' ? 1 : po(L, 0, .4);
  var w = '';
  if (sc === 's1' && L1 > 1.6) w = 'celular da Júlia';
  if (sc === 's2' || sc === 's3') w = 'exemplo de página';
  if (sc === 's4') w = L < 1.9 ? 'exemplo de página' : 'o seu celular';
  $('who').textContent = w; $('who').style.opacity = w ? (sc === 's1' ? po(L1, 1.6, 2.0) : po(L, .1, .5)) : 0;
  /* legenda */
  var cur = null; CAP.forEach(function (c) { if (t >= c[0]) cur = c; });
  var cap = $('cap'); cap.innerHTML = cur ? '<span>' + cur[1] + '</span>' : '';
  cap.style.opacity = cur ? po(t, cur[0], cur[0] + .18) * (1 - p(t, END - .5, END)) : 0;
  cap.style.transform = 'translateY(' + (cur ? (1 - po(t, cur[0], cur[0] + .25)) * 14 : 0) + 'px)';

  /* gancho: visível no primeiro quadro (capa) */
  var hkOut = p(t, S.s1 + 1.2, S.s1 + 1.7), hk = $('hook');
  hk.style.opacity = 1 - hkOut;
  hk.style.transform = 'translateY(' + (-40 * hkOut) + 'px) scale(' + (1 + .03 * Math.sin(Math.max(0, L1) * 3)) + ')';

  /* telefone */
  var ph = $('phone'), g = p(t, S.s1 + 1.4, S.s1 + 2.0), dim = 1;
  if (sc === 's5') dim = 1 - .62 * p(L, .1, .45);
  ph.style.opacity = po(t, S.s1 + 1.4, S.s1 + 1.7) * dim;
  ph.style.transform = 'translateY(' + (1 - g) * 180 + 'px) scale(' + (.7 + .3 * g) + ')';

  /* camadas */
  var lay = {g1: 0, pg: 0, chat: 0};
  if (sc === 's1') lay.g1 = 1;
  if (sc === 's2') { lay.pg = p(L, 0, .35); lay.g1 = 1 - lay.pg; }
  if (sc === 's3') lay.pg = 1;
  if (sc === 's4') { lay.chat = p(L, 1.9, 2.2); lay.pg = 1 - lay.chat; }
  if (sc === 's5') lay.chat = 1;
  for (var id in lay) $(id).style.opacity = lay[id];

  /* busca */
  if (sc === 's1' || sc === 's2') {
    $('q1').textContent = typeText(t, S.s1 + 1.9, S.s1 + 2.6, 'salão em peruíbe');
    rise('r1', po(L1, 2.6, 2.95)); rise('r2', po(L1, 2.8, 3.15));
    var gh = po(L1, 3.1, 3.45); rise('r4', gh, 20);
    $('r4').style.transform += ' scale(' + (1 + .05 * Math.sin(Math.max(0, L1 - 3.1) * 9) * (1 - p(L1, 3.1, 4.2))) + ')';
  }

  /* página */
  var B = function (a) { return sc === 's3' ? po(t - S.s3, a, a + .4) : (t > S.s3 ? 1 : 0); };
  [['b1', .1], ['b2', 1.3], ['b3', 2.6]].forEach(function (b) {
    var k = B(b[1]); rise(b[0], k, 26);
    var on = sc === 's3' && t - S.s3 >= b[1] && t - S.s3 < b[1] + 1.25;
    $(b[0]).style.outline = on ? '4px solid rgba(217,70,122,' + (1 - p(t - S.s3, b[1] + .9, b[1] + 1.25)) + ')' : 'none';
    $(b[0]).style.outlineOffset = '6px'; $(b[0]).style.borderRadius = '18px'; });
  ['p1', 'p2', 'p3'].forEach(function (id, i) { var k = B(.4 + i * .12); $(id).style.opacity = k; $(id).style.transform = 'scale(' + (.6 + .4 * k) + ')'; });
  var wk = t > S.s3 + 2.9 ? po(t, S.s3 + 2.9, S.s3 + 3.3) : 0;
  var pulse = sc === 's4' ? 1 + .035 * Math.sin(L * 7) : 1;
  $('wab').style.opacity = wk; $('wab').style.transform = 'scale(' + ((.85 + .15 * wk) * pulse) + ')';
  tap('tap2', t, S.s4 + 1.6, 284, $('wab').offsetTop + 48);

  /* conversa */
  var ty = sc === 's4' ? p(L, 2.0, 2.1) * (1 - p(L, 2.25, 2.3)) : 0; $('typ').style.opacity = ty;
  $('typ').querySelectorAll('span').forEach(function (d, i) { d.style.opacity = .4 + .6 * Math.max(0, Math.sin(t * 8 - i)); });
  var m1 = sc === 's4' ? po(L, 2.3, 2.55) : (sc === 's5' ? 1 : 0); rise('m1', m1, 24);

  /* preço */
  var pr = sc === 's5' ? po(L, .2, .6) : 0;
  $('price').style.opacity = pr; $('price').style.transform = 'translateY(' + (1 - pr) * 40 + 'px) scale(' + (.94 + .06 * pr) + ')';
  var pd = sc === 's5' ? po(L, 3.2, 3.6) : 0; $('pdiag').style.opacity = pd;
  $('pdiag').style.transform = 'translateY(' + (1 - pd) * 16 + 'px)';

  $('glow').style.transform = 'translate(' + Math.sin(t * .25) * 60 + 'px,' + Math.cos(t * .2) * 40 + 'px)';
}
window.render = render;
document.fonts.ready.then(function () { render(0); document.body.dataset.ready = '1'; });
