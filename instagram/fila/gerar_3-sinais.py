"""Gera os posts do Instagram da Synex Local (filosofia: Sinal Costeiro)."""
import math, random, pathlib, base64
from playwright.sync_api import sync_playwright

FONTS = "/mnt/skills/examples/canvas-design/canvas-fonts"
OUT = pathlib.Path(__file__).parent / "posts"
OUT.mkdir(exist_ok=True)

BG, INK, RED, GRAPH, MUTED = "#0B0B0C", "#F2EEE6", "#E8283A", "#38383E", "#8C8A86"

def F(n): return "data:font/ttf;base64," + base64.b64encode(open(f"{FONTS}/{n}","rb").read()).decode()
CSS = f"""
@font-face{{font-family:Shoulders;src:url({F("BigShoulders-Bold.ttf")})}}
@font-face{{font-family:ShouldersR;src:url({F("BigShoulders-Regular.ttf")})}}
@font-face{{font-family:Sans;src:url({F("InstrumentSans-Regular.ttf")})}}
@font-face{{font-family:SansB;src:url({F("InstrumentSans-Bold.ttf")})}}
@font-face{{font-family:SerifI;src:url({F("InstrumentSerif-Italic.ttf")})}}
@font-face{{font-family:Mono;src:url({F("GeistMono-Regular.ttf")})}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:{BG}}}
.c{{position:relative;overflow:hidden;background:{BG};color:{INK}}}
.abs{{position:absolute}}
.mono{{font-family:Mono;font-size:19px;letter-spacing:.14em;text-transform:uppercase;color:{MUTED}}}
.disp{{font-family:Shoulders;text-transform:uppercase;line-height:.86;letter-spacing:-.005em;color:{INK}}}
.serif{{font-family:SerifI;color:{INK}}}
.body{{font-family:Sans;font-size:36px;line-height:1.38;color:#CFCBC4}}
.red{{color:{RED}}}
.wm{{font-family:Shoulders;font-size:46px;letter-spacing:.06em;line-height:1}}
.wm span.l{{font-family:ShouldersR;color:{MUTED};margin-left:.28em}}
"""

def contours(w, h, top, bottom, seed, n=None, gap=15, amp=1.0, fade_up=True):
    rnd = random.Random(seed)
    f1, f2, f3 = rnd.uniform(.0028,.0042), rnd.uniform(.007,.011), rnd.uniform(.0012,.002)
    p1, p2, p3 = rnd.uniform(0,6.28), rnd.uniform(0,6.28), rnd.uniform(0,6.28)
    lines = []
    count = n or int((bottom - top) / gap)
    for i in range(count):
        y0 = top + i * gap
        pts = []
        for x in range(-20, w + 21, 12):
            y = (y0
                 + amp * 26 * math.sin(x * f1 + p1 + i * .11)
                 + amp * 9 * math.sin(x * f2 + p2 - i * .23)
                 + amp * 38 * math.sin(x * f3 + p3 + i * .045))
            pts.append(f"{x},{y:.1f}")
        t = i / max(count - 1, 1)
        op = (.25 + .75 * t) if fade_up else (1 - .7 * t)
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{GRAPH}" '
                     f'stroke-width="1.3" stroke-opacity="{op:.2f}"/>')
    return "\n".join(lines)

def signal(cx, cy, r=9, rings=4, step=26, solid=True):
    s = []
    for k in range(rings, 0, -1):
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r + k*step}" fill="none" stroke="{RED}" '
                 f'stroke-width="1.4" stroke-opacity="{.75 - k*.15:.2f}"/>')
    if solid:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{RED}"/>')
    else:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    return "\n".join(s)

def frame(w, h, m=60):
    """Marcas de registro nos cantos e régua lateral."""
    s, L = [], 16
    for x, y in [(m, m), (w-m, m), (m, h-m), (w-m, h-m)]:
        s.append(f'<line x1="{x-L}" y1="{y}" x2="{x+L}" y2="{y}" stroke="{MUTED}" stroke-width="1" stroke-opacity=".55"/>')
        s.append(f'<line x1="{x}" y1="{y-L}" x2="{x}" y2="{y+L}" stroke="{MUTED}" stroke-width="1" stroke-opacity=".55"/>')
    for i, y in enumerate(range(m + 60, h - m - 40, 24)):
        ln = 12 if i % 5 == 0 else 6
        s.append(f'<line x1="{w-m}" y1="{y}" x2="{w-m-ln}" y2="{y}" stroke="{MUTED}" stroke-width="1" stroke-opacity=".35"/>')
    return "\n".join(s)

def page(w, h, svg, html):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="c" style="width:{w}px;height:{h}px">'
            f'<svg class="abs" style="left:0;top:0" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svg}</svg>'
            f'{html}</div></body></html>')

def header(idx, total, right="24°11′S · 46°47′W", w=1080):
    return (f'<div class="abs mono" style="left:96px;top:92px">Synex Local — {idx:02d}/{total:02d}</div>'
            f'<div class="abs mono" style="right:96px;top:92px">{right}</div>')

def wordmark(left=96, bottom=96, extra="synexpages.net"):
    return (f'<div class="abs wm" style="left:{left}px;bottom:{bottom}px">SYNE<span class="red">X</span><span class="l">LOCAL</span></div>'
            f'<div class="abs mono" style="right:96px;bottom:{bottom+8}px">{extra}</div>')

W, H = 1080, 1350
posts = {}

# ---------------- 01 · Manifesto ----------------
svg = contours(W, H, 760, 1160, seed=7) + signal(820, 930) + frame(W, H)
html = header(1, 1, "Itanhaém · Peruíbe · Mongaguá") + f"""
<div class="abs disp" style="left:90px;top:200px;font-size:196px;white-space:nowrap">Seu negócio<br>aberto <span class="red">24h.</span></div>
<div class="abs serif" style="left:96px;top:590px;font-size:68px">Mesmo com a porta fechada.</div>
<div class="abs body" style="left:96px;top:1078px;width:560px;font-size:28px;color:{MUTED}">Página de vendas e atendimento automático para o comércio do litoral.</div>
""" + wordmark()
posts["01-manifesto"] = page(W, H, svg, html)

# ---------------- 02–06 · Carrossel "3 sinais" ----------------
T = 5
svg = contours(W, H, 900, 1180, seed=21, amp=.8) + signal(900, 1010, rings=3) + frame(W, H)
html = header(1, T) + f"""
<div class="abs mono red" style="left:96px;top:210px;color:{RED}">Diagnóstico · leia até o fim</div>
<div class="abs disp" style="left:92px;top:270px;font-size:150px">3 sinais de que<br>seu cliente<br>está indo pro<br><span class="red">concorrente.</span></div>
<div class="abs mono" style="left:96px;bottom:104px">Arrasta para o lado &nbsp;→</div>
"""
posts["02-carrossel-1-capa"] = page(W, H, svg, html)

sinais = [
    ("01", "Te procuram<br>no Google e<br>não te acham.",
     "Quem pesquisa “lanche em Itanhaém” às 22h escolhe quem aparece primeiro — com endereço, cardápio e botão de WhatsApp.", 31),
    ("02", "Seu WhatsApp<br>responde<br>horas depois.",
     "Pedido que espera, esfria. Com o atendimento automático, o cliente recebe resposta e preço na hora — até de madrugada.", 43),
    ("03", "Seu cardápio<br>é uma foto<br>no Instagram.",
     "Preço desatualizado, imagem cortada, nenhum link. Uma página própria organiza tudo e leva o cliente direto pro pedido.", 57),
]
for k, (num, title, body, seed) in enumerate(sinais, start=2):
    svg = contours(W, H, 1090, 1250, seed=seed, amp=.6, gap=16) + frame(W, H)
    html = header(k, T) + f"""
<div class="abs disp red" style="left:88px;top:170px;font-size:300px;line-height:.8">{num}</div>
<div class="abs disp" style="left:92px;top:450px;font-size:128px">{title}</div>
<div class="abs" style="left:96px;top:858px;width:72px;height:3px;background:{RED}"></div>
<div class="abs body" style="left:96px;top:892px;width:820px">{body}</div>
""" + wordmark(extra="@synexpages")
    posts[f"0{k+1}-carrossel-{k}"] = page(W, H, svg, html)

svg = contours(W, H, 640, 1010, seed=88) + signal(820, 860, r=12, rings=5, step=30) + frame(W, H)
html = header(5, T) + f"""
<div class="abs disp" style="left:92px;top:190px;font-size:176px">Todo sinal<br>tem<br><span class="red">conserto.</span></div>
<div class="abs body" style="left:96px;top:1030px;width:880px;font-size:34px">Faça o diagnóstico do seu negócio em <span style="font-family:SansB;color:{INK}">synexpages.net</span><br>ou chame no WhatsApp <span style="font-family:SansB;color:{INK}">(13) 98881-1950</span>.</div>
""" + wordmark(extra="@synexpages")
posts["06-carrossel-5-cta"] = page(W, H, svg, html)

# ---------------- 07 · Oferta ----------------
svg = contours(W, H, 1040, 1200, seed=5, amp=.5, gap=16) + frame(W, H)
html = header(1, 1, "Valor de lançamento") + f"""
<div class="abs mono" style="left:96px;top:190px">Página de vendas completa</div>
<div class="abs disp" style="left:88px;top:262px;font-size:300px;line-height:.82">R$<span class="red">297</span></div>
<div class="abs serif" style="left:96px;top:520px;font-size:58px">pagamento único.</div>
<div class="abs" style="left:96px;top:660px;width:888px;height:1px;background:{GRAPH}"></div>
<div class="abs mono" style="left:96px;top:700px">+ opcional</div>
<div class="abs disp" style="left:94px;top:745px;font-size:86px">Atendimento automático<br>no WhatsApp</div>
<div class="abs body" style="left:96px;top:945px;width:880px">R$49 no 1º mês · depois R$99/mês.</div>
""" + wordmark(extra="Novos clientes")
posts["07-oferta"] = page(W, H, svg, html)

# ---------------- 08 · Portfólio (mapa) ----------------
coast = []
for x in range(-20, W + 21, 10):
    y = 1180 - x * .52 + 22 * math.sin(x * .011) + 9 * math.sin(x * .031)
    coast.append(f"{x},{y:.1f}")
coast_line = f'<polyline points="{" ".join(coast)}" fill="none" stroke="{INK}" stroke-width="2" stroke-opacity=".55"/>'
def coast_y(x): return 1180 - x * .52 + 22 * math.sin(x * .011) + 9 * math.sin(x * .031)
# linhas de "mar" paralelas à costa
sea = []
for i in range(1, 22):
    pts = []
    for x in range(-20, W + 21, 12):
        y = coast_y(x) + i * 15 + 6 * math.sin(x * .02 + i * .4)
        pts.append(f"{x},{y:.1f}")
    sea.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{GRAPH}" stroke-width="1.2" stroke-opacity="{1 - i*.04:.2f}"/>')
pins = [(820, "Beatrice Confeitaria", "Mongaguá", True),
        (520, "Dogão Lanches", "Guapura · Itanhaém", True),
        (210, "Seu negócio", "Peruíbe · em breve", False)]
pin_svg, pin_html = [], []
for x, name, place, solid in pins:
    y = coast_y(x) - 4
    pin_svg.append(signal(x, round(y), r=8, rings=2, step=18, solid=solid))
    pin_svg.append(f'<line x1="{x}" y1="{y-50}" x2="{x}" y2="{y-150}" stroke="{MUTED}" stroke-width="1" stroke-opacity=".6"/>')
    color = INK if solid else RED
    pos = f"right:{W-x-6}px;text-align:right" if x > W*0.6 else f"left:{x-6}px"
    pin_html.append(f'<div class="abs" style="{pos};top:{y-262:.0f}px;width:340px">'
                    f'<div style="font-family:SansB;font-size:30px;color:{color};line-height:1.15">{name}</div>'
                    f'<div class="mono" style="margin-top:8px;font-size:17px">{place}</div></div>')
svg = "\n".join(sea) + coast_line + "\n".join(pin_svg) + frame(W, H)
html = header(1, 1, "Feito aqui no litoral") + f"""
<div class="abs disp" style="left:92px;top:190px;font-size:158px">Quem já<br>está <span class="red">no ar.</span></div>
""" + "".join(pin_html) + wordmark(extra="O próximo pin é seu?")
posts["08-portfolio"] = page(W, H, svg, html)

# ---------------- Capas de destaques (1080x1920) ----------------
HW, HH = 1080, 1920
cx, cy = 540, 960
def cover(label, glyph):
    svg = (f'<circle cx="{cx}" cy="{cy}" r="300" fill="none" stroke="{GRAPH}" stroke-width="2"/>' + glyph)
    html = f'<div class="abs mono" style="left:0;width:{HW}px;text-align:center;top:1320px;font-size:30px;color:{INK}">{label}</div>'
    return page(HW, HH, svg, html)

g_sobre = signal(cx, cy, r=22, rings=3, step=46)
g_preco = (f'<text x="{cx}" y="{cy+70}" text-anchor="middle" font-family="Shoulders" font-size="230" fill="{RED}">R$</text>')
g_port = "".join(f'<rect x="{cx-120+dx}" y="{cy-120+dy}" width="104" height="104" fill="{RED if (dx,dy)==(136,136) else "none"}" stroke="{RED}" stroke-width="5"/>'
                 for dx in (0, 136) for dy in (0, 136))
g_como = "".join([f'<circle cx="{cx-150+i*150}" cy="{cy}" r="{20 if i<2 else 30}" fill="{RED if i==2 else "none"}" stroke="{RED}" stroke-width="5"/>' for i in range(3)]
                 + [f'<line x1="{cx-150+i*150+28}" y1="{cy}" x2="{cx+i*150-28 - (8 if i==1 else 0)}" y2="{cy}" stroke="{RED}" stroke-width="5"/>' for i in range(2)])
posts["destaque-sobre"] = cover("Sobre", g_sobre)
posts["destaque-precos"] = cover("Preços", g_preco)
posts["destaque-portfolio"] = cover("Portfólio", g_port)
posts["destaque-como-funciona"] = cover("Como funciona", g_como)

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, doc in posts.items():
        tall = name.startswith("destaque")
        pg = b.new_page(viewport={"width": HW if tall else W, "height": HH if tall else H})
        pg.set_content(doc)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(250)
        pg.screenshot(path=str(OUT / f"{name}.png"))
        pg.close()
    b.close()
print("\n".join(sorted(x.name for x in OUT.iterdir())))
