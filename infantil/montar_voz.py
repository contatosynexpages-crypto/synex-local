# Gera a narração em partes, com pausas controladas, e salva marcas de tempo (marks.js) e as legendas no roteiro.
import json, sys, os, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
pasta = sys.argv[1]
M = os.environ['SYNEX_KOKORO']
k = Kokoro(os.path.join(M, 'kokoro-v1.0.onnx'), os.path.join(M, 'voices-v1.0.bin'))
partes = json.load(open(os.path.join(pasta, 'partes.json'), encoding='utf-8'))
rot = json.load(open(os.path.join(pasta, 'roteiro.json'), encoding='utf-8'))
marks = {}
os.makedirs(os.path.join(pasta, 'voz'), exist_ok=True)
for c in rot['cenas']:
    sid = c['id']; trechos = []; t = 0.0; marks[sid] = []
    for texto, pausa in partes[sid]:
        a, sr = k.create(texto, voice=rot['voz'], speed=rot['velocidade'], lang='pt-br')
        # corta silêncio das pontas
        idx = np.where(np.abs(a) > 0.01)[0]
        a = a[max(0, idx[0] - 240): idx[-1] + 480]
        marks[sid].append([round(t, 3), round(t + len(a) / sr, 3), texto])
        trechos.append(a); t += len(a) / sr
        if pausa:
            trechos.append(np.zeros(int(pausa * sr), dtype=a.dtype)); t += pausa
    sf.write(os.path.join(pasta, 'voz', sid + '.wav'), np.concatenate(trechos), sr)
    c['texto'] = ' '.join(p[0] for p in partes[sid])
    print(sid, round(t, 2), 's')
json.dump(rot, open(os.path.join(pasta, 'roteiro.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
open(os.path.join(pasta, 'marks.js'), 'w', encoding='utf-8').write('window.MARKS = ' + json.dumps(marks, ensure_ascii=False) + ';\n')
