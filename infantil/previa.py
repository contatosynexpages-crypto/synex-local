# Gera timeline.js (como o gerar.py) e tira quadros soltos: python3 previa.py pasta t1 t2 ...
import sys, os, json, re, importlib.util
spec = importlib.util.spec_from_file_location('g', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gerar.py')); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
pasta = os.path.abspath(sys.argv[1]); rot = json.load(open(os.path.join(pasta, 'roteiro.json'), encoding='utf-8'))
S, CAP, t, durs = {}, [], g.LEAD, {}
for c in rot['cenas']:
    wav = os.path.join(pasta, 'voz', c['id'] + '.wav'); d = g.duracao(wav); durs[c['id']] = d; S[c['id']] = round(t, 3)
    frases = c.get('legendas') or [c['texto']]
    for ini, f in zip(g.tempos_legenda(frases, g.falas(wav, d), d), frases):
        CAP.append([round(t + ini, 3), re.sub(r'\*(.+?)\*', r'<em>\1</em>', f)])
    t += d + g.GAP
u = rot['cenas'][-1]['id']; END = round(S[u] + durs[u] + g.HOLD, 3)
open(os.path.join(pasta, 'timeline.js'), 'w', encoding='utf-8').write('window.SCENES = %s;\nwindow.END = %s;\nwindow.CAPTIONS = %s;\n' % (json.dumps(S), END, json.dumps(CAP, ensure_ascii=False)))
print('SCENES', S, 'END', END)
from playwright.sync_api import sync_playwright
os.makedirs(os.path.join(pasta, 'prev'), exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.on('pageerror', lambda e: print('ERRO', e))
    pg.goto('file://' + os.path.join(pasta, 'cena.html')); pg.wait_for_function("document.body.dataset.ready === '1'", timeout=20000)
    for tt in sys.argv[2:]:
        pg.evaluate('t => render(t)', float(tt)); pg.screenshot(path=os.path.join(pasta, 'prev', 't%05.2f.png' % float(tt)))
    b.close()
