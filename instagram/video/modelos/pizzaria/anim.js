// Linha do tempo determinística: render(t) desenha o quadro do segundo t.
var S = window.SCENES || {s1: 0.5, s2: 5.615, s3: 13.098, s4: 22.373, s5: 30.944, s6: 37.787, s7: 42.774};
var END = window.END || 48.307;
// window.SCENES, window.END e window.CAPTIONS vêm do timeline.js, que o gerar.py cria a partir da narração.
var $ = function (id) { return document.getElementById(id); };
function cl(x) { return Math.max(0, Math.min(1, x)); }
function ez(x) { x = cl(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
function eo(x) { x = cl(x); return 1 - Math.pow(1 - x, 3); }
function p(t, a, b) { return ez((t - a) / (b - a)); }
function po(t, a, b) { return eo((t - a) / (b - a)); }
function scene(t) { var k = 's1'; for (var n in S) if (t >= S[n]) k = n; return k; }

/* ---------- salão em traço ---------- */
var NS = 'http://www.w3.org/2000/svg', art = $('art'), strokes = [];
function el(tag, at) { var e = document.createElementNS(NS, tag); for (var k in at) e.setAttribute(k, at[k]); art.appendChild(e); return e; }
var rays = el('g', {opacity: 0});
[[0, 0, 520, 0, 160, 1400, -200, 1400], [620, 0, 780, 0, 420, 1400, 260, 1400]].forEach(function (q) {
  var r = document.createElementNS(NS, 'polygon'); r.setAttribute('points', q.join(' ')); r.setAttribute('fill', 'rgba(255,214,190,.05)'); rays.appendChild(r); });
var salon = el('g', {});
function stroke(d, w, col, fill) {
  var e = document.createElementNS(NS, 'path'); e.setAttribute('d', d); e.setAttribute('stroke', col || 'rgba(243,241,238,.78)');
  e.setAttribute('stroke-width', w || 3); e.setAttribute('stroke-linecap', 'round'); e.setAttribute('stroke-linejoin', 'round');
  e.setAttribute('fill', fill || 'none'); salon.appendChild(e); strokes.push(e); return e; }
stroke('M120 1340 H960', 2, 'rgba(243,241,238,.35)');                        // chão
stroke('M200 1250 V960 A240 240 0 0 1 680 960 V1250', 3);                     // cúpula do forno
stroke('M330 1250 V1090 A110 110 0 0 1 550 1090 V1250', 2.5);                 // boca do forno
stroke('M400 760 V640 H480 V752', 3);                                         // chaminé
stroke('M215 1130 H320 M560 1130 H665 M228 1010 H318 M562 1010 H652 M290 880 H590', 1.5, 'rgba(243,241,238,.28)'); // tijolos
stroke('M392 1250 Q386 1206 412 1178 Q410 1214 432 1226 Q436 1188 462 1166 Q462 1212 484 1250', 2.5, 'rgba(240,98,45,.95)'); // chama
stroke('M120 1250 H730', 3);                                                  // bancada
stroke('M740 1250 H990', 3);                                                  // prateleira do celular
stroke('M110 1250 V1222 H190 V1250 M114 1222 V1196 H186 V1222 M110 1196 V1170 H190 V1196', 2.5, 'rgba(240,98,45,.8)'); // caixas
stroke('M640 1246 L700 1020', 2.5);                                           // cabo da pá
stroke('M700 1020 Q676 968 702 930 Q728 968 704 1020', 2.5);                  // pá
var lens = strokes.map(function (s) { var L = s.getTotalLength(); s.style.strokeDasharray = L; return L; });
var rings = el('g', {});
for (var i = 0; i < 3; i++) el('circle', {cx: 860, cy: 1100, r: 10, stroke: '#E8283A', 'stroke-width': 3, opacity: 0}).id = 'rg' + i;
['rg0', 'rg1', 'rg2'].forEach(function (id) { rings.appendChild($(id)); });

/* ---------- notificações ---------- */
var NOT = [['Marcos', 'Boa noite! Tão abertos?', S.s1 + 4.4], ['Carol', 'Tem calabresa?', S.s2 + 0.05],
  ['Paulo', 'Quanto é a grande?', S.s2 + 0.9], ['Bia', 'Entrega no Guaraú?', S.s2 + 1.9],
  ['Carol', 'Oi?? Alguém aí?', S.s2 + 3.6], ['Lúcia', 'Vocês aceitam Pix?', S.s2 + 4.6]];
var lock = $('lock');
NOT.forEach(function (n, i) {
  var d = document.createElement('div'); d.className = 'notif'; d.id = 'nt' + i;
  d.innerHTML = '<b>' + n[0] + '</b><span>' + n[1] + '</span><i>agora</i><em class="nr">não respondida</em>'; lock.appendChild(d); });

/* ---------- legendas ---------- */
var CAP = window.CAPTIONS || [
  [S.s1 + 0, 'Sábado, oito da manhã. A Carla abre o salão em Itanhaém...'], [S.s1 + 3.45, '...e o celular <em>não para</em>.'],
  [S.s2 + 0, 'Quanto é a escova? Tem horário hoje?'], [S.s2 + 1.98, 'Faz unha em gel?'],
  [S.s2 + 3.0, 'Ela está com a tesoura na mão,'], [S.s2 + 4.68, 'e as mensagens vão ficando <em>sem resposta</em>.'],
  [S.s3 + 0, 'Do outro lado da cidade, a Júlia procura um salão no Google.'], [S.s3 + 3.6, 'Acha um perfil <em>sem preço, sem horário</em>...'],
  [S.s3 + 6.0, '...e marca com o primeiro que explica tudo direitinho.'],
  [S.s4 + 0, 'Na semana seguinte, a Carla ganha uma <em>página própria</em>:'], [S.s4 + 3.15, 'serviços, preços, fotos dos trabalhos, horários,'],
  [S.s4 + 5.92, 'e um <em>botão direto pro WhatsApp</em>.'],
  [S.s5 + 0, 'A Júlia pesquisa de novo. Agora o <em>Studio Carla</em> aparece.'], [S.s5 + 3.42, 'Ela vê o preço da escova, as fotos... e <em>toca no botão</em>.'],
  [S.s6 + 0, 'A mensagem já chega pronta:'], [S.s6 + 1.54, '“Oi! Vi a página. Quero a escova, sábado às dez.”'],
  [S.s7 + 0, 'A Carla <em>só confirma</em>.'], [S.s7 + 1.54, 'E volta para a cliente que está na cadeira.']];

var STAMP = {s1: 'sex · 19:00 · Peruíbe', s2: 'sex · 19:12 · <b>N</b> sem resposta', s3: 'sex · 19:15 · outro lado da cidade',
  s4: 'uma semana depois', s5: 'sex · 19:02 · Peruíbe', s6: 'sex · 19:03', s7: 'sex · 19:04'};
var WHO = {s1: '', s2: 'celular do Rafa', s3: 'celular do Diego', s4: 'a página nova da pizzaria', s5: 'celular do Diego', s6: 'celular do Rafa', s7: 'celular do Rafa'};

function typeText(t, a, b, txt) { var n = Math.round(cl((t - a) / (b - a)) * txt.length); return txt.slice(0, n); }
function tap(id, t, at, x, y) { var e = $(id), k = (t - at) / .55; e.style.left = x + 'px'; e.style.top = y + 'px';
  e.style.opacity = k < 0 || k > 1 ? 0 : (1 - k); e.style.transform = 'scale(' + (0.6 + k * 0.9) + ')'; }
function show(id, o) { $(id).style.opacity = o; }

function render(t) {
  var sc = scene(t), L = t - S[sc];
  /* textos fixos */
  var st = STAMP[sc]; if (sc === 's7' && L > 1.6) st = 'sex · 19:05 · pedidos de hoje';
  if (sc === 's2') { var c = 0; NOT.forEach(function (n) { if (t >= n[2]) c++; }); st = st.replace('N', c); }
  $('stamp').innerHTML = st; $('stamp').style.opacity = po(L, 0, .4);
  var w = WHO[sc]; $('who').textContent = w; $('who').style.opacity = (w ? po(L, .1, .5) : 0) * (sc === 's7' ? 1 - p(L, 1.4, 1.8) : 1);
  /* legenda */
  var cur = null; CAP.forEach(function (c) { if (t >= c[0]) cur = c; });
  var cap = $('cap'); cap.innerHTML = cur ? '<span>' + cur[1] + '</span>' : ''; cap.style.opacity = cur ? po(t, cur[0], cur[0] + .18) * (1 - p(t, END - .5, END)) : 0;
  cap.style.transform = 'translateY(' + (cur ? (1 - po(t, cur[0], cur[0] + .25)) * 14 : 0) + 'px)';
  /* salão */
  var drawP = t < S.s2 ? 1 : 0;
  strokes.forEach(function (s, i) { var a = .1 + i * .14; s.style.strokeDashoffset = lens[i] * (1 - po(t - S.s1, a, a + 1.1)); });
  var artO = 1 - p(t, S.s2, S.s2 + .6);
  if (sc === 's7') artO = .32 * p(L, 1.6, 2.4);
  salon.setAttribute('opacity', artO); rays.setAttribute('opacity', (sc === 's1' ? po(L, 0, 1.5) : 0) + (sc === 's7' ? .6 * p(L, 1.6, 2.4) : 0));
  ['rg0', 'rg1', 'rg2'].forEach(function (id, i) { var k = ((t - S.s1 - 4.3) / 1.2 + i / 3) % 1, on = sc === 's1' && L > 4.3;
    var r = $(id); r.setAttribute('r', 90 + k * 170); r.setAttribute('opacity', on ? (1 - k) * .7 : 0); });
  /* telefone */
  var ph = $('phone'), g = p(t, S.s2, S.s2 + .7), sx = 320 * (1 - g), sy = 190 * (1 - g), scl = .24 + .76 * g;
  var buzz = sc === 's1' && L > 4.3 ? Math.sin(t * 60) * 3 * (Math.sin(t * 5) > 0 ? 1 : 0) : 0;
  var phO = sc === 's1' ? po(L, 4.0, 4.3) : 1, down = 0;
  if (sc === 's7') { var k7 = p(L, 1.45, 2.2); phO = 1 - k7; down = 260 * k7; }
  ph.style.opacity = phO; ph.style.transform = 'translate(' + (sx + buzz) + 'px,' + (sy + down) + 'px) scale(' + scl + ')';
  /* camadas da tela */
  var lay = {lock: 0, g1: 0, pg: 0, g2: 0, chat: 0};
  if (sc === 's1' || sc === 's2') lay.lock = 1;
  if (sc === 's3') { lay.g1 = p(L, 0, .35); lay.lock = 1 - lay.g1; }
  if (sc === 's4') { lay.pg = p(L, 0, .35); lay.g1 = 1 - lay.pg; }
  if (sc === 's5') { var a5 = p(L, 0, .35), b5 = p(L, 3.6, 3.95); lay.g2 = a5 * (1 - b5); lay.pg = (1 - a5) + b5; }
  if (sc === 's6') { lay.chat = p(L, 0, .35); lay.pg = 1 - lay.chat; }
  if (sc === 's7') lay.chat = 1;
  for (var id in lay) show(id, lay[id]);
  /* bloqueio */
  $('lhora').textContent = t < S.s2 ? '19:00' : '19:12';
  NOT.forEach(function (n, i) { var e = $('nt' + i), rank = 0;
    NOT.forEach(function (m, j) { if (j > i) rank += p(t, m[2], m[2] + .35); });
    e.style.top = (330 + rank * 134) + 'px'; e.style.opacity = po(t, n[2], n[2] + .3) * (1 - .45 * p(t, S.s2 + 4.9, S.s2 + 5.6));
    e.style.transform = 'scale(' + (0.92 + .08 * po(t, n[2], n[2] + .3)) + ')';
    e.querySelector('.nr').style.opacity = p(t, S.s2 + 5.0, S.s2 + 5.6); });
  /* busca 1 */
  if (sc === 's3' || sc === 's4') {
    var L3 = t - S.s3;
    $('q1').textContent = typeText(t, S.s3 + .3, S.s3 + 2.2, 'pizzaria em peruíbe');
    [['r1a', 4.6], ['r1b', 5.2]].forEach(function (r) { var e = $(r[0]); e.style.opacity = po(L3, r[1], r[1] + .35) * (r[0] === 'r1a' ? 1 - .5 * p(L3, 8.5, 8.9) : 1);
      e.style.transform = 'translateY(' + (1 - po(L3, r[1], r[1] + .35)) * 30 + 'px)'; });
    $('r1b').style.outline = L3 > 7.2 ? ('4px solid rgba(19,122,58,' + po(L3, 7.2, 7.6) + ')') : 'none';
    tap('tap1', t, S.s3 + 8.2, 300, 676);
  }
  /* página */
  var B = function (a) { return sc === 's4' ? po(t - S.s4, a, a + .45) : 1; };
  $('b1').style.opacity = B(3.3); $('b2').style.opacity = B(4.8); $('b3').style.opacity = B(5.6);
  ['p1', 'p2', 'p3'].forEach(function (id, i) { var k = B(3.9 + i * .15); $(id).style.opacity = k; $(id).style.transform = 'scale(' + (.6 + .4 * k) + ')'; $(id).style.display = 'inline-block'; });
  [['b1', 3.3], ['b2', 4.8], ['b3', 5.6]].forEach(function (b) { $(b[0]).style.transform = 'translateY(' + (1 - B(b[1])) * 26 + 'px)'; });
  var wk = B(7.4), pulse = sc === 's4' && t - S.s4 > 7.9 ? 1 + .03 * Math.sin((t - S.s4) * 7) : 1;
  $('wab').style.opacity = wk; $('wab').style.transform = 'scale(' + ((.85 + .15 * wk) * pulse) + ')';
  var L5 = t - S.s5, hl = sc === 's5' ? p(L5, 4.1, 4.4) : (sc === 's6' ? 1 : 0);
  $('svEsc').style.outline = hl > 0 ? '4px solid rgba(240,98,45,' + hl + ')' : 'none';
  $('b2').style.filter = sc === 's5' && L5 > 4.9 && L5 < 5.6 ? 'brightness(1.12)' : 'none';
  tap('tap2', t, S.s5 + 6.2, 284, $('wab').offsetTop + 48);
  /* busca 2 */
  if (sc === 's5') {
    $('q2').textContent = typeText(t, S.s5 + .3, S.s5 + 1.4, 'pizzaria peruíbe');
    [['r2a', 2.0], ['r2b', 2.3]].forEach(function (r) { var e = $(r[0]); e.style.opacity = po(L5, r[1], r[1] + .35) * (r[0] === 'r2b' ? .55 : 1);
      e.style.transform = 'translateY(' + (1 - po(L5, r[1], r[1] + .35)) * 30 + 'px)'; });
    tap('tap3', t, S.s5 + 3.3, 300, 362);
  }
  /* conversa */
  var L6 = t - S.s6;
  var ty = sc === 's6' ? p(L6, .4, .6) * (1 - p(L6, 1.5, 1.6)) : 0; $('typ').style.opacity = ty;
  $('typ').querySelectorAll('span').forEach(function (d, i) { d.style.opacity = .4 + .6 * Math.max(0, Math.sin(t * 8 - i)); });
  var m1 = sc === 's6' ? po(L6, 1.6, 1.9) : (sc === 's7' ? 1 : 0);
  $('m1').style.opacity = m1; $('m1').style.transform = 'translateY(' + (1 - m1) * 24 + 'px)';
  var m2 = sc === 's7' ? po(t - S.s7, .3, .6) : 0; $('m2').style.opacity = m2; $('m2').style.transform = 'translateY(' + (1 - m2) * 24 + 'px)';
  /* agenda */
  var ag = sc === 's7' ? po(t - S.s7, 1.8, 2.4) : 0, agEl = $('agenda');
  agEl.style.opacity = ag; agEl.style.transform = 'translateY(' + (1 - ag) * 40 + 'px)';
  var nk = sc === 's7' ? po(t - S.s7, 2.4, 2.8) : 0; $('snew').style.background = 'rgba(240,98,45,' + (.14 * nk) + ')';
  $('snew').style.boxShadow = 'inset 4px 0 0 rgba(240,98,45,' + nk + ')'; $('snew').style.paddingLeft = (nk * 18) + 'px';
  $('snew').querySelector('.chk').style.opacity = sc === 's7' ? po(t - S.s7, 2.8, 3.2) : 0;
  $('glow').style.transform = 'translate(' + Math.sin(t * .25) * 60 + 'px,' + Math.cos(t * .2) * 40 + 'px)';
}
window.render = render;
document.fonts.ready.then(function () { render(0); document.body.dataset.ready = '1'; });
