# Gerador de vídeos da Synex: narração (Kokoro, voz Alex) + animação (HTML) + legendas + efeitos -> MP4 vertical.
# Roda no Windows (kit) e na nuvem (Linux). O modelo de voz é baixado sozinho na primeira vez.
# Uso:  python gerar.py modelos\salao-de-beleza            (gera voz nova e o vídeo)
#       python gerar.py modelos\salao-de-beleza --sem-voz  (reaproveita a voz que já está na pasta voz\)
import json, os, re, shutil, subprocess, sys

KIT = os.path.dirname(os.path.abspath(__file__))
MODELO = os.environ.get('SYNEX_KOKORO', os.path.join(KIT, 'modelo'))
URL_MODELO = 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/'
LEAD, GAP, HOLD, FPS = 0.5, 0.55, 1.8, 30


def ffmpeg_bin(nome):
    achado = shutil.which(nome)
    if achado:
        return achado
    for raiz in [os.environ.get('LOCALAPPDATA', ''), r'C:\ffmpeg', r'C:\Program Files\ffmpeg']:
        for pasta, _, arqs in os.walk(raiz) if raiz and os.path.isdir(raiz) else []:
            if nome + '.exe' in arqs and 'bin' in pasta.lower():
                return os.path.join(pasta, nome + '.exe')
    sys.exit('Não achei o %s. Rode o 1-INSTALAR.bat de novo.' % nome)


FFMPEG = ffmpeg_bin('ffmpeg')


def duracao(wav):
    import soundfile as sf
    info = sf.info(wav)
    return info.frames / info.samplerate


def gerar_voz(rot, pasta_voz):
    from kokoro_onnx import Kokoro
    import soundfile as sf
    import urllib.request
    os.makedirs(MODELO, exist_ok=True)
    for arq in ('kokoro-v1.0.onnx', 'voices-v1.0.bin'):
        dest = os.path.join(MODELO, arq)
        if not os.path.exists(dest) or os.path.getsize(dest) < 1000000:
            print('  baixando', arq, '(só na primeira vez)...')
            urllib.request.urlretrieve(URL_MODELO + arq, dest)
    k = Kokoro(os.path.join(MODELO, 'kokoro-v1.0.onnx'), os.path.join(MODELO, 'voices-v1.0.bin'))
    os.makedirs(pasta_voz, exist_ok=True)
    for c in rot['cenas']:
        audio, sr = k.create(c['texto'], voice=c.get('voz', rot.get('voz', 'pm_alex')),
                             speed=c.get('velocidade', rot.get('velocidade', 1.0)), lang='pt-br')
        sf.write(os.path.join(pasta_voz, c['id'] + '.wav'), audio, sr)
        print('  voz', c['id'], round(len(audio) / sr, 1), 's')


def falas(wav, dur):
    """Trechos com fala (início, fim) detectados pelas pausas da narração."""
    out = subprocess.run([FFMPEG, '-hide_banner', '-i', wav, '-af', 'silencedetect=noise=-35dB:d=0.18', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]
    fim = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
    trechos, cursor = [], 0.0
    for a, b in zip(ini, fim + [dur] * (len(ini) - len(fim))):
        if a - cursor > 0.15:
            trechos.append((cursor, a))
        cursor = b
    if dur - cursor > 0.15:
        trechos.append((cursor, dur))
    return trechos


def tempos_legenda(frases, trechos, dur):
    if len(frases) == len(trechos):
        return [t[0] for t in trechos]
    # proporcional ao tamanho do texto
    total = sum(len(f) for f in frases) or 1
    t, out = 0.0, []
    for f in frases:
        out.append(t)
        t += dur * len(f) / total
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit('Uso: python gerar.py modelos\\nome-do-modelo [--sem-voz]')
    pasta = os.path.abspath(sys.argv[1])
    rot = json.load(open(os.path.join(pasta, 'roteiro.json'), encoding='utf-8'))
    pasta_voz = os.path.join(pasta, 'voz')
    faltando = [c['id'] for c in rot['cenas'] if not os.path.exists(os.path.join(pasta_voz, c['id'] + '.wav'))]
    if '--sem-voz' not in sys.argv or faltando:
        print('1/4 Gerando a narração...')
        gerar_voz(rot, pasta_voz)
    else:
        print('1/4 Reaproveitando a narração da pasta voz')

    print('2/4 Montando a linha do tempo...')
    S, CAP, t = {}, [], LEAD
    durs = {}
    for c in rot['cenas']:
        wav = os.path.join(pasta_voz, c['id'] + '.wav')
        d = duracao(wav)
        durs[c['id']] = d
        S[c['id']] = round(t, 3)
        frases = c.get('legendas') or [c['texto']]
        for ini, f in zip(tempos_legenda(frases, falas(wav, d), d), frases):
            CAP.append([round(t + ini, 3), re.sub(r'\*(.+?)\*', r'<em>\1</em>', f)])
        t += d + GAP
    ultimo = rot['cenas'][-1]['id']
    END = round(S[ultimo] + durs[ultimo] + HOLD, 3)
    with open(os.path.join(pasta, 'timeline.js'), 'w', encoding='utf-8') as fp:
        fp.write('window.SCENES = %s;\nwindow.END = %s;\nwindow.CAPTIONS = %s;\n' %
                 (json.dumps(S), END, json.dumps(CAP, ensure_ascii=False)))
    print('   duração total: %.1f s' % END)

    print('3/4 Desenhando os quadros (demora alguns minutos)...')
    from playwright.sync_api import sync_playwright
    quadros = os.path.join(pasta, 'quadros')
    shutil.rmtree(quadros, ignore_errors=True)
    os.makedirs(quadros)
    n = int(END * FPS + 0.999)
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={'width': 1080, 'height': 1920})
        pg.on('pageerror', lambda e: print('   ERRO na animação:', e))
        pg.goto('file:///' + os.path.join(pasta, 'cena.html').replace('\\', '/'))
        pg.wait_for_function("document.body.dataset.ready === '1'", timeout=30000)
        for i in range(n):
            pg.evaluate('t => render(t)', i / FPS)
            pg.screenshot(path=os.path.join(quadros, '%05d.jpg' % i), type='jpeg', quality=92)
            if i % 150 == 0:
                print('   quadro %d de %d' % (i, n))
        nav.close()

    print('4/4 Juntando áudio e vídeo...')
    ids = [c['id'] for c in rot['cenas']]
    entradas, filtros, rotulos = [], [], []
    for i, cid in enumerate(ids):
        ms = int(S[cid] * 1000)
        entradas += ['-i', os.path.join(pasta_voz, cid + '.wav')]
        filtros.append('[%d:a]aresample=48000:resampler=soxr,highpass=f=70,lowpass=f=15000,equalizer=f=3000:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,adelay=%d|%d[v%d]' % (i, ms, ms, i))
        rotulos.append('[v%d]' % i)
    som = {'pop': ("0.18*sin(2*PI*(880+220*exp(-30*t))*t)*exp(-22*t)", 0.25),
           'toque': ("0.20*sin(2*PI*1600*t)*exp(-90*t)", 0.08),
           'mensagem': ("0.16*(sin(2*PI*660*t)*lt(t\\,0.09)+sin(2*PI*990*t)*gte(t\\,0.09)*exp(-12*(t-0.09)))", 0.35),
           'enviada': ("0.12*sin(2*PI*1200*t)*exp(-28*t)", 0.18),
           'boing': ("0.16*sin(2*PI*(260+520*exp(-14*t))*t)*exp(-9*t)", 0.35),
           'plim': ("0.11*(sin(2*PI*1568*t)+0.5*sin(2*PI*2349*t)+0.25*sin(2*PI*3136*t))*exp(-7*t)", 0.7),
           'tada': ("0.10*(sin(2*PI*523*t)*lt(t\\,0.11)+sin(2*PI*659*t)*gte(t\\,0.11)*lt(t\\,0.22)+sin(2*PI*784*t)*gte(t\\,0.22)*lt(t\\,0.33)+(sin(2*PI*1047*t)+0.5*sin(2*PI*1319*t))*gte(t\\,0.33)*exp(-2.2*(t-0.33)))", 1.6)}
    for j, (cid, off, tipo) in enumerate(rot.get('efeitos', [])):
        e, d = som[tipo]
        ms = int((S[cid] + off) * 1000)
        filtros.append('aevalsrc=%s:s=48000:d=%s[e%d];[e%d]adelay=%d|%d[f%d]' % (e, d, j, j, ms, ms, j))
        rotulos.append('[f%d]' % j)
    musica = os.path.join(pasta, 'musica.wav')
    if os.path.exists(musica):
        entradas += ['-i', musica]
        mi = len(ids)
        filtros.append(''.join(rotulos) + 'amix=inputs=%d:normalize=0,apad=whole_dur=%s[vf]' % (len(rotulos), END))
        filtros.append('[vf]asplit=2[vfa][vfb]')
        filtros.append('[%d:a]aresample=48000,lowpass=f=5000,volume=0.22,atrim=0:%s[mus]' % (mi, END))
        filtros.append('[mus][vfb]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=350[mducked]')
        filtros.append('[vfa][mducked]amix=inputs=2:normalize=0[m];[m]loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[out]')
    else:
        filtros.append(''.join(rotulos) + 'amix=inputs=%d:normalize=0,apad=whole_dur=%s[m];[m]loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[out]' % (len(rotulos), END))
    audio = os.path.join(pasta, 'audio.wav')
    subprocess.run([FFMPEG, '-y', '-hide_banner', '-loglevel', 'error'] + entradas +
                   ['-filter_complex', ';'.join(filtros), '-map', '[out]', '-ac', '2', '-t', str(END), audio], check=True)
    final = os.path.join(pasta, rot.get('arquivo_final', 'video-synex.mp4'))
    subprocess.run([FFMPEG, '-y', '-hide_banner', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(quadros, '%05d.jpg'),
                    '-i', audio, '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-profile:v', 'high', '-r', str(FPS), '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', final], check=True)
    shutil.rmtree(quadros, ignore_errors=True)
    print('\nPRONTO: ' + final)


if __name__ == '__main__':
    main()
