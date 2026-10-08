// Contando até 5 com as frutinhas: render(t) desenha o quadro do segundo t (determinístico).
var S = window.SCENES, END = window.END, MK = window.MARKS, CAP = window.CAPTIONS || [];
var NS = 'http://www.w3.org/2000/svg';
function $(id) { return document.getElementById(id); }
function cl(x) { return Math.max(0, Math.min(1, x)); }
function eo(x) { x = cl(x); return 1 - Math.pow(1 - x, 3); }
function ez(x) { x = cl(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
function back(x) { x = cl(x); var c = 2.2; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); } // passa do ponto e volta
function el(tag, at, pai) { var e = document.createElementNS(NS, tag); for (var k in at) e.setAttribute(k, at[k]); (pai || $('mundo')).appendChild(e); return e; }
function scene(t) { var k = 's1'; for (var n in S) if (t >= S[n]) k = n; return k; }
function rnd(i) { var x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }

/* ---------- cenário ---------- */
for (var i = 0; i < 12; i++) el('path', {d: 'M0 -112 L14 -150 L-14 -150 Z', fill: '#FFD23F', transform: 'rotate(' + i * 30 + ')'}, $('raios'));
var NUV = [[160, 330, 1.0, 12], [620, 520, .8, 8], [-60, 760, .7, 10]];
NUV.forEach(function (n, i) {
  var g = el('g', {id: 'nv' + i}, $('nuvens'));
  [[0, 0, 70], [70, -30, 85], [150, 0, 70], [75, 20, 80]].forEach(function (c) { el('circle', {cx: c[0], cy: c[1], r: c[2], fill: '#fff'}, g); });
});
for (var f = 0; f < 14; f++) {
  var fx = 40 + rnd(f) * 1000, fy = 1480 + rnd(f + 9) * 380, cor = ['#ff7eb6', '#fff', '#FFD23F', '#ff9f43'][f % 4];
  var g = el('g', {transform: 'translate(' + fx + ' ' + fy + ')'}, $('flores'));
  for (var p = 0; p < 5; p++) el('circle', {cx: Math.cos(p * 1.2566) * 14, cy: Math.sin(p * 1.2566) * 14, r: 11, fill: cor}, g);
  el('circle', {r: 9, fill: '#F7A400'}, g);
}

/* ---------- frutinhas (viewBox 200x200, base em y=190) ---------- */
var CORPO = {
  maca: '<path d="M100 44 C60 22 18 52 24 108 C30 162 70 192 100 176 C130 192 170 162 176 108 C182 52 140 22 100 44Z" fill="#EF3B3B" stroke="#2b2f6b" stroke-width="7"/><ellipse cx="62" cy="80" rx="14" ry="22" fill="#fff" opacity=".35" transform="rotate(25 62 80)"/><path d="M100 46 Q97 24 108 10" stroke="#6b3b1f" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M107 26 Q132 4 156 18 Q132 40 107 26Z" fill="#4fbf47" stroke="#2b2f6b" stroke-width="5"/>',
  banana: '<path d="M24 52 Q30 176 168 178 Q192 176 184 160 Q92 150 64 46 Q58 30 42 34 Q22 38 24 52Z" fill="#FFD93B" stroke="#2b2f6b" stroke-width="7"/><path d="M40 60 Q52 140 140 160" stroke="#F2B705" stroke-width="7" fill="none" stroke-linecap="round" opacity=".7"/><path d="M178 158 L192 166" stroke="#6b3b1f" stroke-width="9" stroke-linecap="round"/>',
  laranja: '<circle cx="100" cy="110" r="78" fill="#FF9F1C" stroke="#2b2f6b" stroke-width="7"/><circle cx="70" cy="80" r="4" fill="#ffc46b"/><circle cx="132" cy="92" r="4" fill="#ffc46b"/><circle cx="84" cy="150" r="4" fill="#ffc46b"/><circle cx="140" cy="140" r="4" fill="#ffc46b"/><ellipse cx="66" cy="84" rx="12" ry="20" fill="#fff" opacity=".3" transform="rotate(25 66 84)"/><path d="M100 34 Q122 10 146 20 Q126 42 100 34Z" fill="#4fbf47" stroke="#2b2f6b" stroke-width="5"/>',
  uva: '<circle cx="100" cy="116" r="72" fill="#8E44AD" stroke="#2b2f6b" stroke-width="7"/><ellipse cx="70" cy="88" rx="14" ry="20" fill="#fff" opacity=".35" transform="rotate(25 70 88)"/><path d="M100 46 Q104 26 118 18" stroke="#6b3b1f" stroke-width="8" fill="none" stroke-linecap="round"/>',
  morango: '<path d="M100 184 C52 164 22 112 32 76 C42 44 74 44 100 56 C126 44 158 44 168 76 C178 112 148 164 100 184Z" fill="#FF4D6D" stroke="#2b2f6b" stroke-width="7"/><g fill="#FFE08A"><ellipse cx="60" cy="96" rx="4" ry="6"/><ellipse cx="140" cy="96" rx="4" ry="6"/><ellipse cx="72" cy="140" rx="4" ry="6"/><ellipse cx="128" cy="140" rx="4" ry="6"/><ellipse cx="100" cy="162" rx="4" ry="6"/></g><path d="M56 56 L76 34 L88 52 L100 26 L112 52 L124 34 L144 56 Q100 76 56 56Z" fill="#4fbf47" stroke="#2b2f6b" stroke-width="5" stroke-linejoin="round"/>'
};
var ROSTO = {maca: [100, 112], banana: [104, 128], laranja: [100, 114], uva: [100, 118], morango: [100, 112]};
function fruta(tipo, pai) {
  var g = el('g', {}, pai), corpo = el('g', {}, g);
  corpo.innerHTML = CORPO[tipo];
  var r = ROSTO[tipo], face = el('g', {transform: 'translate(' + r[0] + ' ' + r[1] + ')'}, corpo);
  var olhos = el('g', {}, face);
  [-22, 22].forEach(function (x) {
    el('ellipse', {cx: x, cy: -8, rx: 13, ry: 16, fill: '#fff', stroke: '#2b2f6b', 'stroke-width': 4}, olhos);
    el('circle', {cx: x + 2, cy: -6, r: 7, fill: '#2b2f6b'}, olhos);
    el('circle', {cx: x + 5, cy: -10, r: 2.6, fill: '#fff'}, olhos);
  });
  el('ellipse', {cx: -38, cy: 16, rx: 11, ry: 7, fill: '#ff8fb0', opacity: .75}, face);
  el('ellipse', {cx: 38, cy: 16, rx: 11, ry: 7, fill: '#ff8fb0', opacity: .75}, face);
  el('path', {d: 'M-16 16 Q0 32 16 16', stroke: '#2b2f6b', 'stroke-width': 5, fill: 'none', 'stroke-linecap': 'round'}, face);
  return {g: g, corpo: corpo, olhos: olhos};
}

/* ---------- cenas ---------- */
var CENAS = {
  s2: {n: 1, tipo: 'maca', palavra: '1 maçã', cor: '#EF3B3B'},
  s3: {n: 2, tipo: 'banana', palavra: '2 bananas', cor: '#F2B705'},
  s4: {n: 3, tipo: 'laranja', palavra: '3 laranjas', cor: '#FF8A00'},
  s5: {n: 4, tipo: 'uva', palavra: '4 uvinhas', cor: '#8E44AD'},
  s6: {n: 5, tipo: 'morango', palavra: '5 morangos', cor: '#FF4D6D'}
};
var TAM = {1: 470, 2: 370, 3: 300, 4: 238, 5: 192};
var palco = $('palco');
for (var sid in CENAS) {
  var c = CENAS[sid]; c.grupo = el('g', {}, palco); c.itens = [];
  var tam = TAM[c.n], larg = c.n * tam * .98, x0 = 540 - larg / 2;
  for (var k = 0; k < c.n; k++) {
    var fr = fruta(c.tipo, c.grupo); fr.x = x0 + k * tam * .98 + tam / 2; fr.y = 1400; fr.s = tam / 200; c.itens.push(fr);
  }
}
var turma = {grupo: el('g', {}, palco), itens: []};
['maca', 'banana', 'laranja', 'uva', 'morango'].forEach(function (tp, k) {
  var fr = fruta(tp, turma.grupo); fr.x = 140 + k * 200; fr.y = 1400; fr.s = 1.0; turma.itens.push(fr);
});
var CONF = [];
for (var q = 0; q < 70; q++) CONF.push(el('rect', {width: 18, height: 30, rx: 4, fill: ['#FF4D6D', '#FFD23F', '#4fbf47', '#5cc2ff', '#8E44AD', '#FF9F1C'][q % 6], opacity: 0}, $('confete')));

function poe(fr, x, y, sx, sy, rot) {
  fr.g.setAttribute('transform', 'translate(' + x + ' ' + y + ') rotate(' + (rot || 0) + ') scale(' + (fr.s * sx) + ' ' + (fr.s * sy) + ') translate(-100 -190)');
}
function pisca(fr, t, i) { var k = ((t + i * .37) % 3.1); fr.olhos.setAttribute('transform', 'translate(0 ' + (k < .12 ? -6 : 0) + ') scale(1 ' + (k < .12 ? .15 : 1) + ')'); }

function render(t) {
  var sc = scene(t), L = t - S[sc];
  var prox = {s1: 's2', s2: 's3', s3: 's4', s4: 's5', s5: 's6', s6: 's7', s7: null}[sc];
  var saida = prox ? cl((S[prox] - t) / .35) : 1;           // some nos últimos 0,35 s da cena
  var entra = eo(L / .35);
  /* cenário vivo */
  $('raios').setAttribute('transform', 'rotate(' + t * 12 + ')');
  $('sol').setAttribute('transform', 'translate(900 ' + (210 + Math.sin(t * 1.6) * 8) + ')');
  NUV.forEach(function (n, i) { var x = ((n[0] + t * n[3]) % 1300) - 120; $('nv' + i).setAttribute('transform', 'translate(' + x + ' ' + n[1] + ') scale(' + n[2] + ')'); });
  /* legenda */
  var cur = null; CAP.forEach(function (c) { if (t >= c[0]) cur = c; });
  $('capin').innerHTML = cur ? cur[1] : ''; $('cap').style.opacity = cur ? eo((t - cur[0]) / .15) * cl((END - t) / .5) : 0;
  $('cap').style.transform = 'scale(' + (cur ? .9 + .1 * back((t - cur[0]) / .3) : 1) + ')';
  /* esconde tudo e mostra a cena atual */
  for (var k in CENAS) CENAS[k].grupo.setAttribute('opacity', 0);
  turma.grupo.setAttribute('opacity', 0);
  CONF.forEach(function (c) { c.setAttribute('opacity', 0); });
  var tit = $('titulo'), num = $('numero');
  tit.style.opacity = 0; num.style.opacity = 0;

  if (sc === 's1' || sc === 's7') {
    var m = MK[sc];
    turma.grupo.setAttribute('opacity', 1);
    turma.itens.forEach(function (fr, i) {
      var t0 = sc === 's1' ? .3 + i * .25 : 0, k = (L - t0) / .5, y = fr.y - (1 - back(k)) * 0 - (k < 1 ? (1 - eo(k)) * 500 : 0);
      var pulo = sc === 's1' ? (L > m[2][0] ? Math.abs(Math.sin((L - m[2][0]) * 6 + i * .6)) * 60 * cl(1 - (L - m[2][0]) / 1.6) : 0)
                             : Math.abs(Math.sin(L * 5 + i * .7)) * 40;
      var bob = Math.sin(t * 3 + i) * 5, sq = k < 1.2 && k > .8 ? 1 - Math.sin((k - .8) * 7.8) * .12 : 1;
      var rot = sc === 's7' && L > m[2][0] ? Math.sin(L * 9 + i) * 12 : 0;
      poe(fr, fr.x, y - pulo + bob, 1 / sq, sq, rot); fr.g.setAttribute('opacity', k > 0 ? 1 : 0); pisca(fr, t, i);
    });
    turma.grupo.setAttribute('opacity', sc === 's1' ? saida : entra);
    var txt = sc === 's1' ? 'Vamos contar!' : 'Muito bem!';
    tit.innerHTML = txt.split('').map(function (ch, i) {
      var y = Math.sin(t * 5 + i * .5) * 10; return '<span style="transform:translateY(' + y + 'px)">' + (ch === ' ' ? '&nbsp;' : ch) + '</span>'; }).join('');
    tit.style.top = '560px'; tit.style.fontSize = '128px';
    tit.style.opacity = (sc === 's1' ? eo((L - .2) / .4) * saida : entra);
    tit.style.transform = 'scale(' + (.7 + .3 * back((L - (sc === 's1' ? .2 : 0)) / .5)) + ')';
    if (sc === 's7') {
      CONF.forEach(function (c, i) {
        var t0 = rnd(i) * 1.2, k = L - t0; if (k < 0) return;
        var x = rnd(i + 50) * 1080 + Math.sin(k * 3 + i) * 40, y = -40 + k * (260 + rnd(i + 99) * 220);
        c.setAttribute('opacity', y < 1500 ? 1 : 0); c.setAttribute('transform', 'translate(' + x + ' ' + y + ') rotate(' + (k * 300 * (rnd(i + 7) - .5)) + ')');
      });
    }
    return;
  }
  /* cenas de contagem */
  var c = CENAS[sc], m = MK[sc], g = c.grupo; g.setAttribute('opacity', entra * saida);
  tit.style.top = '330px'; tit.style.fontSize = '118px';
  tit.innerHTML = '<span style="color:' + c.cor + '">' + c.palavra + '</span>';
  tit.style.opacity = entra * saida; tit.style.transform = 'scale(' + (.8 + .2 * back(L / .45)) + ')';
  var conta = 0, ultimo = 0;
  c.itens.forEach(function (fr, i) {
    var tc = m[c.n === 1 ? 1 : i + 1][0];                     // momento em que essa fruta é contada
    var k = (L - tc) / .45, cheio = L >= tc;
    if (cheio) { conta = i + 1; ultimo = tc; }
    var drop = k < 1 ? (1 - eo(k)) * 70 : 0;
    var sq = k > 0 && k < 1 ? 1 + Math.sin(k * Math.PI) * .18 : 1;
    var festa = L > m[m.length - 1][0] + .3 ? Math.abs(Math.sin((L - m[m.length - 1][0]) * 7 + i * .8)) * 34 : 0;
    poe(fr, fr.x, fr.y - drop - festa + Math.sin(t * 3 + i) * 4, 1 / sq, sq, 0);
    fr.g.setAttribute('opacity', cheio ? 1 : .22);
    fr.corpo.setAttribute('filter', cheio ? '' : 'grayscale(1)');
    fr.corpo.style.filter = cheio ? 'none' : 'grayscale(1) brightness(1.4)';
    pisca(fr, t, i);
  });
  if (conta > 0) {
    num.textContent = conta; num.style.opacity = entra * saida;
    num.style.transform = 'scale(' + (.55 + .45 * back((L - ultimo) / .4)) + ') rotate(' + (Math.sin(t * 2) * 3) + 'deg)';
    num.style.color = conta === c.n ? '#FFD23F' : '#fff';
  }
}
window.render = render;
document.fonts.ready.then(function () { render(0); document.body.dataset.ready = '1'; });
