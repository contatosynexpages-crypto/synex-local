# Stories e capas dos destaques do @synexpages (Como funciona, Preço, Dúvidas), no estilo "Sinal Costeiro".
# Uso: python3 gerar.py  ->  out/*.png (stories 1080x1920 e capas 1080x1920 com ícone central)
# Textos tirados do site (FAQ e oferta): não inventar prazo, preço ou depoimento.
import os, subprocess, json

HERE = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.abspath(os.path.join(HERE, '..', 'fontes'))
OUT = os.path.join(HERE, 'out'); HTML = os.path.join(HERE, 'html')
os.makedirs(OUT, exist_ok=True); os.makedirs(HTML, exist_ok=True)
F = lambda n: 'file://' + os.path.join(FONTES, n)

CSS = f"""
@font-face{{font-family:Shoulders;src:url('{F('BigShoulders-Bold.ttf')}')}}
@font-face{{font-family:Mono;src:url('{F('GeistMono-Regular.ttf')}')}}
@font-face{{font-family:ISans;src:url('{F('InstrumentSans-Regular.ttf')}')}}
@font-face{{font-family:ISans;font-weight:700;src:url('{F('InstrumentSans-Bold.ttf')}')}}
@font-face{{font-family:ISerif;font-style:italic;src:url('{F('InstrumentSerif-Italic.ttf')}')}}
:root{{--bg:#0B0B0C;--ink:#F3F1EE;--red:#E8283A;--amber:#FFB020;--i2:rgba(243,241,238,.70);--i3:rgba(243,241,238,.42);--i4:rgba(243,241,238,.15)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;background:var(--bg);color:var(--ink);overflow:hidden;-webkit-font-smoothing:antialiased;font-family:ISans,sans-serif}}
body{{background-image:linear-gradient(rgba(243,241,238,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(243,241,238,.03) 1px,transparent 1px);background-size:45px 45px}}
.wrap{{position:absolute;left:96px;right:96px;top:260px;bottom:330px;display:flex;flex-direction:column;gap:46px}}
.mono{{font-family:Mono,monospace;font-size:24px;letter-spacing:.17em;text-transform:uppercase;color:var(--i3)}}
.red{{color:var(--red)}}
h1{{font-family:Shoulders,sans-serif;text-transform:uppercase;font-size:136px;line-height:.86;letter-spacing:.005em}}
.lede{{font-family:ISerif,serif;font-style:italic;font-size:46px;line-height:1.2;color:var(--ink)}}
.steps{{display:flex;flex-direction:column;gap:40px}}
.step{{display:grid;grid-template-columns:96px 1fr;gap:26px;align-items:start}}
.step .n{{font-family:Shoulders,sans-serif;font-size:110px;line-height:.8;color:var(--red)}}
.step b{{display:block;font-size:44px;line-height:1.1;margin-bottom:10px}}
.step p{{font-size:33px;line-height:1.35;color:var(--i2)}}
.price{{font-family:Shoulders,sans-serif;font-size:330px;line-height:.8;color:var(--ink)}}
.price small{{font-size:120px;color:var(--red);vertical-align:top;margin-right:10px}}
.rule{{height:2px;background:var(--i4)}}
.item{{font-size:36px;line-height:1.35;color:var(--i2)}} .item b{{color:var(--ink)}}
.qa{{display:flex;flex-direction:column;gap:12px}}
.qa b{{font-size:42px;line-height:1.15}} .qa p{{font-size:33px;line-height:1.35;color:var(--i2)}}
.foot{{position:absolute;left:96px;right:96px;bottom:200px;display:flex;justify-content:space-between;border-top:2px solid var(--i4);padding-top:26px}}
.cover{{position:absolute;inset:0;display:grid;place-items:center}}
.ring{{width:620px;height:620px;border-radius:50%;border:6px solid var(--red);display:grid;place-items:center;position:relative}}
.ring span{{font-family:Shoulders,sans-serif;font-size:300px;line-height:1;color:var(--ink)}}
"""

FOOT = '<div class="foot"><span class="mono">Diagnóstico grátis · (13) 98881-1950</span><span class="mono red">@synexpages</span></div>'

STORIES = {
  'como-funciona': f'''<div class="wrap"><span class="mono">Synex Local · como funciona</span>
<h1>Do primeiro oi<br>à página <span class="red">no ar</span></h1>
<div class="steps">
<div class="step"><span class="n">1</span><div><b>Diagnóstico grátis</b><p>Você chama no WhatsApp e a gente mostra como o seu negócio aparece hoje para quem procura.</p></div></div>
<div class="step"><span class="n">2</span><div><b>A gente monta com você</b><p>Não precisa ter texto pronto: usamos as fotos do seu celular, o cardápio ou a lista de serviços.</p></div></div>
<div class="step"><span class="n">3</span><div><b>Página no ar em poucos dias</b><p>Rápida no celular, com preços, fotos, localização e um botão direto pro seu WhatsApp.</p></div></div>
</div></div>{FOOT}''',
  'preco': f'''<div class="wrap"><span class="mono">Synex Local · preço</span>
<div><div class="price"><small>R$</small>297</div><p class="lede" style="margin-top:18px">pagamento único pela página de vendas</p></div>
<div class="rule"></div>
<p class="item"><b>Publicação inclusa.</b> Sem mensalidade de hospedagem.</p>
<p class="item"><b>Domínio próprio é opcional.</b> Se quiser um seunegocio.com.br, ele fica no seu nome.</p>
<p class="item"><b>Bot de atendimento no WhatsApp, se quiser:</b> R$49 no primeiro mês e R$99 por mês depois.</p>
</div>{FOOT}''',
  'duvidas': f'''<div class="wrap"><span class="mono">Synex Local · dúvidas</span>
<h1>Perguntas<br>que todo<br>mundo <span class="red">faz</span></h1>
<div class="qa"><b>Preciso ter fotos e textos prontos?</b><p>Não. A gente levanta o que você já tem e monta o texto junto com você.</p></div>
<div class="qa"><b>Tem mensalidade pra manter no ar?</b><p>Não. Mensalidade só existe se você contratar o bot de atendimento.</p></div>
<div class="qa"><b>Atendem só Itanhaém, Peruíbe e Mongaguá?</b><p>O atendimento presencial é nessas três cidades. De outra cidade? Chama no WhatsApp.</p></div>
</div>{FOOT}''',
}
COVERS = {'capa-como-funciona': '1·2·3', 'capa-preco': 'R$', 'capa-duvidas': '?'}

def page(body):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'

jobs = []
for k, b in STORIES.items():
    p = os.path.join(HTML, k + '.html'); open(p, 'w', encoding='utf-8').write(page(b)); jobs.append((p, os.path.join(OUT, k + '.png')))
for k, sym in COVERS.items():
    size = '210px' if len(sym) > 2 else '300px'
    b = f'<div class="cover"><div class="ring"><span style="font-size:{size}">{sym}</span></div></div>'
    p = os.path.join(HTML, k + '.html'); open(p, 'w', encoding='utf-8').write(page(b)); jobs.append((p, os.path.join(OUT, k + '.png')))

JS = """const {chromium}=require('playwright');(async()=>{const jobs=JSON.parse(process.argv[2]);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const [h,o] of jobs){await p.goto('file://'+h);await p.evaluate(()=>document.fonts.ready);
const bad=await p.evaluate(()=>{const w=document.querySelector('.wrap');return w?w.scrollHeight>w.clientHeight+2:false});if(bad)console.log('ESTOURO',h);
await p.screenshot({path:o});console.log('ok',o)}await b.close()})();"""
js = os.path.join(HTML, 'render.js'); open(js, 'w').write(JS)
npm_root = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
subprocess.run(['node', js, json.dumps(jobs)], check=True, env={**os.environ, 'NODE_PATH': npm_root})
