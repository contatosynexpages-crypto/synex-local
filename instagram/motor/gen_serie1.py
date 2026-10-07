# Motor das artes do Instagram da Synex (série "Sinal Costeiro").
# Exemplo completo: as 9 peças da primeira série. Para um lote novo, copie este arquivo,
# mantenha CSS/frame/page/helpers e troque só o dicionário P (uma entrada por post).
# Gera html/<slug>.html; depois: NODE_PATH=$(npm root -g) node render.js  -> out/*.png (1080x1350)
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.abspath(os.path.join(HERE, '..', 'fontes'))
LOGO = open(os.path.join(HERE, 'logo-symbol.svgfrag'), encoding='utf-8').read()
W, H = 1080, 1350
L, R = 90, 990          # margens laterais
TOP, BOT = 112, 1238    # réguas do cabeçalho e do rodapé
RED, INK, AMBER = '#E8283A', '#F3F1EE', '#FFB020'
TOTAL = 9

CSS = """
@font-face{font-family:Shoulders;src:url('FONTS/BigShoulders-Bold.ttf')}
@font-face{font-family:ISerif;font-style:italic;src:url('FONTS/InstrumentSerif-Italic.ttf')}
@font-face{font-family:ISerif;src:url('FONTS/InstrumentSerif-Regular.ttf')}
@font-face{font-family:Mono;src:url('FONTS/GeistMono-Regular.ttf')}
@font-face{font-family:ISans;src:url('FONTS/InstrumentSans-Regular.ttf')}
@font-face{font-family:ISans;font-weight:700;src:url('FONTS/InstrumentSans-Bold.ttf')}
:root{--bg:#0B0B0C;--ink:#F3F1EE;--red:#E8283A;--amber:#FFB020;--i2:rgba(243,241,238,.64);--i3:rgba(243,241,238,.40);--i4:rgba(243,241,238,.15)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;background:var(--bg);overflow:hidden}
body{position:relative;color:var(--ink);-webkit-font-smoothing:antialiased;
  background-image:linear-gradient(rgba(243,241,238,.028) 1px,transparent 1px),linear-gradient(90deg,rgba(243,241,238,.028) 1px,transparent 1px);
  background-size:45px 45px;background-position:0 0}
svg.layer{position:absolute;inset:0;width:1080px;height:1350px}
.t{position:absolute;white-space:nowrap}
.mono{font-family:Mono;font-size:15px;letter-spacing:.17em;text-transform:uppercase;color:var(--i2);line-height:1}
.disp{font-family:Shoulders;font-weight:700;text-transform:uppercase;line-height:.84;letter-spacing:.004em;color:var(--ink)}
.ser{font-family:ISerif;font-style:italic;line-height:1;color:var(--ink);letter-spacing:-.005em}
.sans{font-family:ISans;line-height:1.05;letter-spacing:-.012em}
.red{color:var(--red)} .i2{color:var(--i2)} .i3{color:var(--i3)}
.knock{background:var(--bg);padding:5px 7px;margin:-5px -7px}
.outline{color:transparent;-webkit-text-stroke:1.4px var(--ink)}
"""

def frame(n, coord):
    """cabeçalho, rodapé, réguas e marcas de registro"""
    marks = ''
    for (x, y) in [(L, TOP), (R, TOP), (L, BOT), (R, BOT)]:
        marks += f'<path d="M{x-9} {y}H{x+9}M{x} {y-9}V{y+9}" stroke="{INK}" stroke-opacity=".55" stroke-width="1"/>'
    svg = f'''<line x1="{L+18}" y1="{TOP}" x2="{R-18}" y2="{TOP}" stroke="{INK}" stroke-opacity=".16"/>
<line x1="{L+18}" y1="{BOT}" x2="{R-18}" y2="{BOT}" stroke="{INK}" stroke-opacity=".16"/>{marks}'''
    html = f'''<div class="t mono" style="left:{L}px;top:70px">Synex Local</div>
<div class="t mono i3" style="left:540px;top:70px;transform:translateX(-50%)">{coord}</div>
<div class="t mono" style="right:{W-R}px;top:70px">Nº {n:02d}<span class="i3"> / {TOTAL:02d}</span></div>
<svg class="t" style="left:{L}px;top:1268px" width="168" height="26" viewBox="0 0 644.89 100"><use href="#i-logo"/></svg>
<div class="t mono" style="right:{W-R}px;top:1276px">@synex_pages</div>'''
    return svg, html

def page(n, coord, svg, html):
    fsvg, fhtml = frame(n, coord)
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS.replace('FONTS', 'file://' + FONTS)}</style></head>
<body><svg width="0" height="0" style="position:absolute">{LOGO}</svg>
<svg class="layer" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" fill="none">{fsvg}{svg}</svg>
{fhtml}
{html}
<script>
document.querySelectorAll('[data-fit]').forEach(function(el){{var max=+el.dataset.fit,fs=parseFloat(getComputedStyle(el).fontSize);while(el.getBoundingClientRect().width>max&&fs>10){{fs-=1;el.style.fontSize=fs+'px';}}}});
document.body.dataset.ready='1';
</script></body></html>'''

def catmull(pts, closed=False):
    """caminho suave passando pelos pontos"""
    d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f' C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d

def rings(cx, cy, step, count, color=RED, o0=.85, sw=1.3, clip=None):
    out = ''
    for i in range(1, count + 1):
        o = o0 * (1 - (i - 1) / count) ** 1.35
        out += f'<circle cx="{cx}" cy="{cy}" r="{i*step}" stroke="{color}" stroke-opacity="{o:.3f}" stroke-width="{sw}"/>'
    if clip:
        return f'<g clip-path="url(#{clip})">{out}</g>'
    return out

def clip(id_, x, y, w, h):
    return f'<defs><clipPath id="{id_}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath></defs>'

P = {}
COORD = {'pe': '24°19′S 47°00′W', 'it': '24°11′S 46°47′W', 'mo': '24°06′S 46°37′W'}

# ---------- 01 · Encontrado ----------
coast = [(60, 760), (250, 668), (560, 520), (790, 404), (1020, 286)]
svg = clip('c1', L, TOP + 1, R - L, 650)
svg += f'<path d="{catmull(coast)}" stroke="{INK}" stroke-opacity=".5" stroke-width="1.2"/>'
for k in range(1, 4):
    off = [(x + 10 * k, y + 22 * k) for x, y in coast]
    svg += f'<path d="{catmull(off)}" stroke="{INK}" stroke-opacity="{.16 - k*.04:.2f}" stroke-dasharray="2 7" clip-path="url(#c1)"/>'
svg += rings(560, 520, 34, 13, clip='c1')
svg += f'<circle cx="560" cy="520" r="7" fill="{RED}"/>'
for (x, y) in [(250, 668), (790, 404)]:
    svg += f'<circle cx="{x}" cy="{y}" r="4" fill="{INK}" fill-opacity=".8"/>'
html = f'''
<div class="t mono knock" style="left:268px;top:688px">Peruíbe</div>
<div class="t mono knock" style="left:808px;top:424px">Mongaguá</div>
<div class="t mono red knock" style="left:582px;top:540px">Itanhaém</div>
<div class="t ser" style="left:{L-4}px;top:818px;font-size:80px">Seu comércio,</div>
<div class="t disp" data-fit="904" style="left:{L-6}px;top:912px;font-size:232px">Encontrado<span class="red">.</span></div>
<div class="t mono" style="left:{L}px;top:1146px">Páginas de vendas para o comércio local</div>
<div class="t mono i3" style="right:{W-R}px;top:1146px">Itanhaém · Peruíbe · Mongaguá</div>'''
P[1] = ('01-encontrado', COORD['it'], svg, html)

# ---------- 02 · Procuraram por você ----------
svg = f'<rect x="{L}" y="616" width="{R-L}" height="76" rx="38" stroke="{INK}" stroke-opacity=".28"/>'
svg += f'<circle cx="{L+42}" cy="652" r="11" stroke="{INK}" stroke-opacity=".6" stroke-width="1.6"/><path d="M{L+50} 660l9 9" stroke="{INK}" stroke-opacity=".6" stroke-width="1.6"/>'
rows = [(744, False), (900, False), (1056, True)]
for i, (y, you) in enumerate(rows):
    if you:
        svg += f'<rect x="196" y="{y-14}" width="{R-196}" height="136" rx="6" stroke="{RED}" stroke-width="1.3" stroke-dasharray="6 6"/>'
        svg += f'<rect x="222" y="{y+40}" width="300" height="14" rx="3" fill="{INK}" fill-opacity=".14"/>'
        svg += f'<rect x="222" y="{y+70}" width="520" height="8" rx="3" fill="{INK}" fill-opacity=".07"/>'
        svg += f'<rect x="222" y="{y+90}" width="410" height="8" rx="3" fill="{INK}" fill-opacity=".07"/>'
    else:
        svg += f'<rect x="222" y="{y+6}" width="{[430, 360][i]}" height="16" rx="3" fill="{INK}" fill-opacity=".72"/>'
        svg += f'<rect x="222" y="{y+40}" width="{[640, 600][i]}" height="9" rx="3" fill="{INK}" fill-opacity=".22"/>'
        svg += f'<rect x="222" y="{y+62}" width="{[540, 470][i]}" height="9" rx="3" fill="{INK}" fill-opacity=".22"/>'
        svg += f'<line x1="222" y1="{y+108}" x2="{R}" y2="{y+108}" stroke="{INK}" stroke-opacity=".08"/>'
html = f'''
<div class="t ser" style="left:{L-3}px;top:150px;font-size:80px">Procuraram por você.</div>
<div class="t disp" data-fit="904" style="left:{L-5}px;top:252px;font-size:178px">Acharam o</div>
<div class="t disp" data-fit="904" style="left:{L-5}px;top:404px;font-size:178px">concorrente<span class="red">.</span></div>
<div class="t mono" style="left:{L+76}px;top:645px;font-size:20px;letter-spacing:.06em;text-transform:none;color:var(--ink)">pizzaria em peruíbe<span style="display:inline-block;width:3px;height:26px;background:var(--red);vertical-align:-6px;margin-left:6px"></span></div>
<div class="t disp i3" style="left:{L}px;top:742px;font-size:66px">01</div>
<div class="t disp i3" style="left:{L}px;top:898px;font-size:66px">02</div>
<div class="t disp red" style="left:{L}px;top:1054px;font-size:66px">03</div>
<div class="t mono red" style="left:222px;top:1062px">Você · perfil parado há 5 meses</div>'''
P[2] = ('02-procuraram', COORD['pe'], svg, html)

# ---------- 03 · O caminho ----------
xs = [150, 440, 730]
svg = ''
# rota sem página
ya, yb = 300, 600
svg += f'<line x1="{xs[0]}" y1="{ya}" x2="{xs[1]}" y2="{ya}" stroke="{INK}" stroke-opacity=".4" stroke-width="1.2"/>'
for k in range(12):
    x = xs[1] + 22 + k * 22
    svg += f'<line x1="{x}" y1="{ya}" x2="{x+9}" y2="{ya}" stroke="{INK}" stroke-opacity="{.4*(1-k/12):.3f}" stroke-width="1.2"/>'
for x in xs[:2]:
    svg += f'<circle cx="{x}" cy="{ya}" r="9" fill="#0B0B0C" stroke="{INK}" stroke-opacity=".6" stroke-width="1.3"/>'
svg += f'<path d="M{R-40} {ya-8}l16 16M{R-40} {ya+8}l16 -16" stroke="{INK}" stroke-opacity=".35" stroke-width="1.3"/>'
# rota com página
svg += f'<line x1="{xs[0]}" y1="{yb}" x2="{xs[2]}" y2="{yb}" stroke="{INK}" stroke-opacity=".75" stroke-width="1.4"/>'
svg += f'<line x1="{xs[2]}" y1="{yb}" x2="{R-60}" y2="{yb}" stroke="{RED}" stroke-width="1.6"/>'
for x in xs:
    svg += f'<circle cx="{x}" cy="{yb}" r="9" fill="#0B0B0C" stroke="{INK}" stroke-width="1.4"/>'
svg += rings(R - 60, yb, 16, 6)
svg += f'<circle cx="{R-60}" cy="{yb}" r="9" fill="{RED}"/>'
svg += f'<line x1="{L}" y1="430" x2="{R}" y2="430" stroke="{INK}" stroke-opacity=".08"/>'
lab = lambda x, y, t, c='': f'<div class="t mono {c}" style="left:{x}px;top:{y}px;transform:translateX(-50%)">{t}</div>'
html = f'''
<div class="t mono i3" style="left:{L}px;top:{ya-62}px">A · Sem página</div>
<div class="t mono" style="left:{L}px;top:{yb-62}px">B · Com página</div>
{lab(xs[0], ya+34, 'Busca')}{lab(xs[1], ya+34, 'Perfil')}<div class="t mono i3" style="right:{W-R}px;top:{ya+34}px">Desistiu</div>
{lab(xs[0], yb+34, 'Busca')}{lab(xs[1], yb+34, 'Página')}{lab(xs[2], yb+34, 'Botão')}{lab(R-60, yb+120, 'WhatsApp', 'red')}
<div class="t ser" style="left:{L-3}px;top:812px;font-size:76px">Todo cliente faz um caminho</div>
<div class="t disp" data-fit="904" style="left:{L-5}px;top:910px;font-size:168px">até o seu</div>
<div class="t disp" data-fit="904" style="left:{L-5}px;top:1052px;font-size:168px">WhatsApp<span class="red">.</span></div>'''
P[3] = ('03-caminho', COORD['mo'], svg, html)

# ---------- 04 · Três passos ----------
rowsy = [548, 812, 1076]
NX = L + 46
svg = f'<line x1="{NX}" y1="{rowsy[0]}" x2="{NX}" y2="{rowsy[2]}" stroke="{INK}" stroke-opacity=".3" stroke-width="1.2"/>'
for i, y in enumerate(rowsy):
    if i < 2:
        svg += f'<circle cx="{NX}" cy="{y}" r="9" fill="#0B0B0C" stroke="{INK}" stroke-width="1.4"/>'
    else:
        svg += rings(NX, y, 15, 3) + f'<circle cx="{NX}" cy="{y}" r="9" fill="{RED}"/>'
    if i < 2:
        svg += f'<line x1="{L+110}" y1="{y+132}" x2="{R}" y2="{y+132}" stroke="{INK}" stroke-opacity=".08"/>'
steps = [('Diagnóstico grátis', 'Uma conversa sobre o seu negócio'),
         ('A gente monta a sua página', 'Textos, fotos e a cara do seu comércio'),
         ('O cliente chama no WhatsApp', 'Um toque e a conversa começa')]
html = f'''
<div class="t ser" style="left:{L-3}px;top:150px;font-size:80px">Como funciona</div>
<div class="t disp" data-fit="904" style="left:{L-6}px;top:244px;font-size:218px">Três passos<span class="red">.</span></div>'''
for i, (y, (a, b)) in enumerate(zip(rowsy, steps)):
    html += f'''
<div class="t disp outline" style="left:{L+100}px;top:{y-46}px;font-size:112px;{'-webkit-text-stroke-color:var(--red)' if i == 2 else ''}">0{i+1}</div>
<div class="t sans" style="left:{L+282}px;top:{y-38}px;font-size:44px">{a}</div>
<div class="t mono i2" style="left:{L+284}px;top:{y+26}px">{b}</div>'''
P[4] = ('04-tres-passos', COORD['it'], svg, html)

# ---------- 05 · 297 ----------
svg = ''
y0 = 1168
for k in range(0, 101):
    x = L + k * (R - L) / 100
    h = 26 if k % 10 == 0 else (16 if k % 5 == 0 else 9)
    svg += f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0+h}" stroke="{INK}" stroke-opacity="{.5 if k%10==0 else .22}" stroke-width="1"/>'
svg += f'<line x1="{L}" y1="{y0}" x2="{R}" y2="{y0}" stroke="{INK}" stroke-opacity=".3"/>'
svg += f'<path d="M{L+297*(R-L)/1000:.1f} {y0-14}l-7 -12h14z" fill="{RED}"/>'
svg += f'<line x1="{L}" y1="902" x2="{R}" y2="902" stroke="{INK}" stroke-opacity=".16"/>'
items = ['Página de vendas completa', 'Pronta pro celular', 'Botão direto pro seu WhatsApp']
html = f'''
<div class="t mono" style="left:{L}px;top:160px">Investimento</div>
<div class="t mono i3" style="right:{W-R}px;top:160px">Página de vendas</div>
<div class="t ser i2" style="left:{L}px;top:262px;font-size:64px">R$</div>
<div class="t disp" style="left:{L+92}px;top:236px;font-size:560px;letter-spacing:-.01em">297</div>
<div class="t ser" style="left:{L-3}px;top:760px;font-size:96px">pagamento <span class="red">único.</span></div>'''
for i, t in enumerate(items):
    html += f'<div class="t mono" style="left:{L+26}px;top:{940+i*44}px"><span class="red" style="position:absolute;left:-26px">●</span>{t}</div>'
P[5] = ('05-preco', COORD['pe'], svg, html)

# ---------- 06 · Cada ofício ----------
cells = [('A', 'Salão|& estética'), ('B', 'Restaurante|& delivery'), ('C', 'Revenda|de veículos'), ('D', 'Prestador|de serviço')]
cw, chh, gap = 435, 336, 30
x0s, y0s = [L, L + cw + gap], [496, 496 + chh + gap]
svg = ''
html = f'''
<div class="t ser" style="left:{L-3}px;top:150px;font-size:80px">Uma página para</div>
<div class="t disp" data-fit="904" style="left:{L-6}px;top:244px;font-size:200px">cada ofício<span class="red">.</span></div>'''
def glyph(k, cx, cy):
    s = f'stroke="{INK}" stroke-opacity=".7" stroke-width="1.4"'
    if k == 0:   # tesoura
        return f'<circle cx="{cx-14}" cy="{cy+18}" r="9" {s}/><circle cx="{cx+14}" cy="{cy+18}" r="9" {s}/><path d="M{cx-8} {cy+11}L{cx+16} {cy-26}M{cx+8} {cy+11}L{cx-16} {cy-26}" {s}/>'
    if k == 1:   # prato e talheres
        return f'<circle cx="{cx}" cy="{cy}" r="22" {s}/><circle cx="{cx}" cy="{cy}" r="13" {s} stroke-opacity=".35"/><path d="M{cx-36} {cy-24}V{cy+26}M{cx+36} {cy-24}V{cy+26}M{cx-41} {cy-24}V{cy-10}M{cx-31} {cy-24}V{cy-10}" {s}/>'
    if k == 2:   # carro: rodas e linha
        return f'<circle cx="{cx-22}" cy="{cy+14}" r="10" {s}/><circle cx="{cx+22}" cy="{cy+14}" r="10" {s}/><path d="M{cx-44} {cy+14}V{cy-2}L{cx-26} {cy-18}H{cx+18}L{cx+40} {cy-2}H{cx+44}V{cy+14}" {s}/>'
    return f'<path d="M{cx+6} {cy-30}L{cx-14} {cy+4}H{cx+2}L{cx-6} {cy+30}L{cx+16} {cy-6}H{cx}Z" {s}/>'   # raio
for k, (idx, name) in enumerate(cells):
    x, y = x0s[k % 2], y0s[k // 2]
    svg += f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" stroke="{INK}" stroke-opacity=".14"/>'
    # mini página
    px, py, pw, ph = x + 28, y + 28, 142, chh - 56
    svg += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16" stroke="{INK}" stroke-opacity=".5" stroke-width="1.2"/>'
    svg += f'<rect x="{px+14}" y="{py+18}" width="40" height="7" rx="2" fill="{INK}" fill-opacity=".6"/>'
    svg += f'<rect x="{px+14}" y="{py+40}" width="{pw-28}" height="74" rx="6" fill="{INK}" fill-opacity=".07"/>'
    svg += f'<rect x="{px+24}" y="{py+56}" width="80" height="9" rx="2" fill="{INK}" fill-opacity=".7"/><rect x="{px+24}" y="{py+72}" width="60" height="9" rx="2" fill="{INK}" fill-opacity=".7"/>'
    svg += f'<rect x="{px+24}" y="{py+92}" width="58" height="12" rx="3" fill="{RED}"/>'
    for j in range(3):
        svg += f'<rect x="{px+14+j*40}" y="{py+128}" width="34" height="34" rx="5" stroke="{INK}" stroke-opacity=".22"/>'
    for j in range(3):
        svg += f'<rect x="{px+14}" y="{py+178+j*16}" width="{pw-28-j*18}" height="6" rx="2" fill="{INK}" fill-opacity=".14"/>'
    svg += f'<circle cx="{px+pw-20}" cy="{py+ph-20}" r="9" fill="#25D366" fill-opacity=".9"/>'
    svg += glyph(k, x + 302, y + 120)
    nm = name.split('|')
    html += f'<div class="t mono i3" style="left:{x+210}px;top:{y+30}px">{idx}</div>'
    html += f'<div class="t sans" style="left:{x+210}px;top:{y+chh-104}px;font-size:28px;line-height:1.12">{nm[0]}<br><span class=i2>{nm[1].replace("&", "&amp;")}</span></div>'
P[6] = ('06-oficios', COORD['mo'], svg, html)

# ---------- 07 · Daqui ----------
coast = [(60, 1212), (330, 1044), (592, 884), (836, 736), (1030, 616)]
cities = [(330, 1044, 'Peruíbe', COORD['pe']), (592, 884, 'Itanhaém', COORD['it']), (836, 736, 'Mongaguá', COORD['mo'])]
svg = clip('c7', L, 500, R - L, BOT - 500 - 1)
land = catmull(coast) + f' L1030 500 L60 500 Z'
svg += f'<defs><clipPath id="land"><path d="{land}"/></clipPath><pattern id="hatch" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="12" stroke="{INK}" stroke-opacity=".07" stroke-width="1"/></pattern></defs>'
svg += f'<g clip-path="url(#c7)"><rect x="0" y="500" width="{W}" height="800" fill="url(#hatch)" clip-path="url(#land)"/></g>'
svg += f'<path d="{catmull(coast)}" stroke="{INK}" stroke-opacity=".7" stroke-width="1.3" clip-path="url(#c7)"/>'
for k in range(1, 5):
    off = [(x + 14 * k, y + 26 * k) for x, y in coast]
    svg += f'<path d="{catmull(off)}" stroke="{INK}" stroke-opacity="{.2 - k*.04:.2f}" stroke-dasharray="2 8" clip-path="url(#c7)"/>'
for (x, y, n, c) in cities:
    svg += rings(x, y, 14, 5, clip='c7') + f'<circle cx="{x}" cy="{y}" r="6" fill="{RED}"/>'
html = f'''
<div class="t disp" data-fit="904" style="left:{L-3}px;top:150px;font-size:268px">Daqui<span class="red">.</span></div>
<div class="t ser" style="left:{L-3}px;top:388px;font-size:80px">Pra quem é daqui.</div>
<div class="t mono" style="left:{L}px;top:540px">Atendimento presencial</div>
<div class="t ser i3" style="right:{W-R}px;top:1168px;font-size:30px">Oceano Atlântico</div>'''
for (x, y, n, c) in cities:
    html += f'<div class="t mono knock" style="right:{W-x+22}px;top:{y-66}px;color:var(--ink)">{n}</div>'
    html += f'<div class="t mono i3 knock" style="right:{W-x+22}px;top:{y-40}px;font-size:13px">{c}</div>'
P[7] = ('07-daqui', COORD['it'], svg, html)

# ---------- 08 · O bot responde ----------
cx, cy, r = 540, 440, 238
svg = f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{INK}" stroke-opacity=".3" stroke-width="1.2"/>'
def ang(hh):  # 00h no topo, sentido horário
    return math.radians(hh / 24 * 360 - 90)
# faixa do horário comercial (9h-18h)
a0, a1 = ang(9), ang(18)
rr = r - 22
svg += f'<path d="M{cx+rr*math.cos(a0):.1f} {cy+rr*math.sin(a0):.1f} A{rr} {rr} 0 0 1 {cx+rr*math.cos(a1):.1f} {cy+rr*math.sin(a1):.1f}" stroke="{INK}" stroke-opacity=".12" stroke-width="16"/>'
for m in range(96):
    a = ang(m / 4)
    l = 22 if m % 24 == 0 else (14 if m % 4 == 0 else 6)
    o = .7 if m % 24 == 0 else (.42 if m % 4 == 0 else .2)
    svg += f'<line x1="{cx+(r-l)*math.cos(a):.1f}" y1="{cy+(r-l)*math.sin(a):.1f}" x2="{cx+r*math.cos(a):.1f}" y2="{cy+r*math.sin(a):.1f}" stroke="{INK}" stroke-opacity="{o}" stroke-width="1"/>'
msgs = [(22 + 47/60, '22:47'), (6 + 12/60, '06:12'), (12 + 31/60, '12:31'), (19 + 5/60, '19:05')]
labels = ''
for hh, t in msgs:
    a = ang(hh)
    svg += f'<line x1="{cx+(r-60)*math.cos(a):.1f}" y1="{cy+(r-60)*math.sin(a):.1f}" x2="{cx+(r+16)*math.cos(a):.1f}" y2="{cy+(r+16)*math.sin(a):.1f}" stroke="{RED}" stroke-width="1.6"/>'
    svg += f'<circle cx="{cx+r*math.cos(a):.1f}" cy="{cy+r*math.sin(a):.1f}" r="5" fill="{RED}"/>'
    lx, ly = cx + (r + 52) * math.cos(a), cy + (r + 44) * math.sin(a)
    labels += f'<div class="t mono red" style="left:{lx:.0f}px;top:{ly-7:.0f}px;transform:translateX(-50%)">{t}</div>'
for hh, t in [(0, '00'), (6, '06'), (12, '12'), (18, '18')]:
    a = ang(hh)
    labels += f'<div class="t mono i3" style="left:{cx+(r-50)*math.cos(a):.0f}px;top:{cy+(r-50)*math.sin(a)-7:.0f}px;transform:translateX(-50%)">{t}</div>'
html = f'''{labels}
<div class="t disp" style="left:{cx}px;top:{cy-46}px;transform:translateX(-50%);font-size:108px">24<span class="i3" style="font-size:.5em">h</span></div>
<div class="t ser" style="left:{L-3}px;top:790px;font-size:76px">Enquanto você atende,</div>
<div class="t disp" data-fit="904" style="left:{L-5}px;top:884px;font-size:168px">o bot</div>
<div class="t disp" data-fit="904" style="left:{L-5}px;top:1026px;font-size:168px">responde<span class="red">.</span></div>
<div class="t mono" style="right:{W-R}px;top:1044px;text-align:right;line-height:1.75">Bot no WhatsApp<br><span class="i3">Opcional</span></div>
<div class="t mono" style="right:{W-R}px;top:1110px;text-align:right;line-height:1.75">R$49 no 1º mês<br><span class="i3">depois R$99/mês</span></div>'''
P[8] = ('08-bot', COORD['pe'], svg, html)

# ---------- 09 · Diagnóstico grátis ----------
svg = clip('c9', L, 250, R - L, 520)
svg += rings(540, 510, 30, 15, clip='c9', o0=.9)
svg += f'<circle cx="540" cy="510" r="11" fill="{RED}"/>'
svg += f'<path d="M{L} 510H500M580 510H{R}" stroke="{INK}" stroke-opacity=".14" stroke-dasharray="3 6"/>'
svg += f'<path d="M540 250V470M540 550V770" stroke="{INK}" stroke-opacity=".14" stroke-dasharray="3 6"/>'
html = f'''
<div class="t ser" style="left:540px;top:150px;font-size:80px;transform:translateX(-50%)">Chama a gente.</div>
<div class="t disp" data-fit="904" style="left:540px;top:820px;font-size:190px;transform:translateX(-50%)">Diagnóstico</div>
<div class="t disp" data-fit="904" style="left:540px;top:980px;font-size:190px;transform:translateX(-50%)">grátis<span class="red">.</span></div>
<div class="t mono" style="left:540px;top:1176px;transform:translateX(-50%);color:var(--ink);font-size:17px">WhatsApp (13) 98881-1950 <span class="i3">· link na bio</span></div>'''
P[9] = ('09-diagnostico', COORD['it'], svg, html)

os.makedirs(os.path.join(HERE, 'html'), exist_ok=True)
for n, (slug, coord, svg, html) in P.items():
    open(os.path.join(HERE, 'html', slug + '.html'), 'w', encoding='utf-8').write(page(n, coord, svg, html))
print('ok', len(P))
