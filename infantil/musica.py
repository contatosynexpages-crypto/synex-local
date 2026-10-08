# Trilha original simples: violão "pluck" (Karplus-Strong) em C-G-Am-F + baixo suave. Uso: python3 musica.py saida.wav segundos
import sys, numpy as np, soundfile as sf
SR = 48000; dur = float(sys.argv[2]); bpm = 104; beat = 60 / bpm
rng = np.random.default_rng(7)
def pluck(freq, secs, decay=0.996, bright=0.5):
    n = int(SR * secs); p = int(SR / freq)
    buf = rng.uniform(-1, 1, p) * bright; out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = decay * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return out
def note(m): return 440 * 2 ** ((m - 69) / 12)
acordes = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60]]   # C G Am F
padrao = [0, 2, 1, 2, 0, 2, 1, 2]                                       # arpejo em colcheias
total = np.zeros(int(SR * (dur + 2)))
cache = {}
t = 0.0; compasso = 0
while t < dur:
    ac = acordes[compasso % 4]
    for k, idx in enumerate(padrao):
        m = ac[idx] + 12
        if m not in cache: cache[m] = pluck(note(m), 1.2, 0.995, 0.6)
        i0 = int((t + k * beat / 2) * SR); s = cache[m]
        total[i0:i0 + len(s)] += s[:len(total) - i0] * (0.55 if k % 2 else 0.75)
    for k in (0, 2):  # baixo
        m = ac[0] - 12
        if ('b', m) not in cache: cache[('b', m)] = pluck(note(m), 1.6, 0.997, 0.9)
        i0 = int((t + k * beat) * SR); s = cache[('b', m)]
        total[i0:i0 + len(s)] += s[:len(total) - i0] * 0.9
    t += 4 * beat; compasso += 1
total = total[:int(SR * dur)]
fade = int(SR * 1.5); total[-fade:] *= np.linspace(1, 0, fade); total[:int(SR*.3)] *= np.linspace(0, 1, int(SR*.3))
total /= np.max(np.abs(total)) + 1e-9
st = np.stack([total * 0.9, np.roll(total, 240) * 0.9], axis=1)  # leve abertura estéreo
sf.write(sys.argv[1], st.astype(np.float32), SR)
print('ok', dur)
