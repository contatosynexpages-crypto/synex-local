"""Teste Synex no OpenMontage: narração Kokoro (Alex) + composição Remotion Explainer em 1080x1920.

Uso (na raiz do OpenMontage):  .venv/bin/python projects/synex-teste/produzir.py
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.tool_registry import registry  # noqa: E402

AQUI = Path(__file__).resolve().parent
COMPOSER = ROOT / "remotion-composer"
PUB = COMPOSER / "public" / "synex"
PUB.mkdir(parents=True, exist_ok=True)

VERMELHO, PRETO, BRANCO, CINZA = "#E8283A", "#0B0B0C", "#F5F5F2", "#9A9A96"

# Cada cena: frases da narração + como ela aparece na tela.
CENAS = [
    (["O Jorge tem uma oficina mecânica em Peruíbe.", "O serviço é bom, e quem conhece, indica."],
     {"type": "hero_title", "text": "Oficina do Jorge", "subtitle": "PERUÍBE · LITORAL SUL", "scale": 1.15}),
    (["Mas quem procura mecânico pelo celular não acha a oficina dele.",
      "E quando acha, não sabe o horário, o preço nem onde fica."],
     {"type": "callout", "callout_type": "warning", "title": "O cliente procurou e…", "scale": 1.5,
      "text": "Não achou o horário. Não achou o preço. Não achou o endereço."}),
    (["Com uma página de vendas da Synex, tudo isso fica num lugar só.",
      "Serviços, fotos, localização e um botão que abre direto o WhatsApp."],
     {"type": "callout", "callout_type": "tip", "title": "Tudo num lugar só", "scale": 1.5,
      "text": "Serviços · Fotos · Localização · Botão direto pro WhatsApp"}),
    (["A página custa duzentos e noventa e sete reais, pagamento único."],
     {"type": "stat_card", "stat": "R$297", "subtitle": "pagamento único"}),
    (["Antes, o cliente perguntava e sumia.", "Agora, ele já chega sabendo o que quer."],
     {"type": "comparison", "title": "A diferença", "leftLabel": "Antes", "leftValue": "Pergunta e some",
      "rightLabel": "Agora", "rightValue": "Chega sabendo", "scale": 1.0}),
    (["E o Jorge passa o dia fazendo o que sabe: consertando carro."],
     {"type": "text_card", "text": "Consertando carro.", "subtitle": ""}),
]


def main() -> None:
    registry.discover()
    tts = registry.get("kokoro_tts")
    texto = " ".join(f for frases, _ in CENAS for f in frases)
    bruto = AQUI / "narracao_bruta.wav"
    r = tts.execute({"text": texto, "voice": "pm_alex", "lang": "pt-br", "speed": 1.0,
                     "sentence_pause": 0.4, "output_path": str(bruto)})
    if not r.success:
        sys.exit(r.error)
    frases = r.data["sentences"]

    # tratamento da voz (mesma cadeia do motor da Synex) + normalização -14 LUFS
    final_wav = PUB / "narracao.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(bruto), "-af",
                    "highpass=f=80,lowpass=f=12000,equalizer=f=3000:t=q:w=1.2:g=2,"
                    "acompressor=threshold=-20dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=7",
                    "-ar", "48000", str(final_wav)], check=True)

    cuts, i, inicio = [], 0, 0.0
    for n, (fs, visual) in enumerate(CENAS):
        fim_fala = frases[i + len(fs) - 1]["end"]
        i += len(fs)
        fim = fim_fala + (0.9 if n == len(CENAS) - 1 else 0.35)
        cuts.append({"id": f"c{n+1}", "source": "", "in_seconds": round(inicio, 2),
                     "out_seconds": round(fim, 2), "backgroundColor": PRETO, "accentColor": VERMELHO,
                     "color": BRANCO, **visual})
        inicio = fim

    props = {
        "themeConfig": {
            "primaryColor": VERMELHO, "accentColor": VERMELHO, "backgroundColor": PRETO,
            "surfaceColor": "#18181A", "textColor": BRANCO, "mutedTextColor": CINZA,
            "chartColors": [VERMELHO, BRANCO, CINZA, "#FF6B78"],
            "captionHighlightColor": VERMELHO, "captionBackgroundColor": "rgba(0,0,0,0.75)",
        },
        "cuts": cuts,
        "overlays": [{"type": "section_title", "in_seconds": 0.3, "out_seconds": cuts[-1]["out_seconds"],
                      "text": "SYNEX LOCAL", "subtitle": "páginas de vendas", "accentColor": VERMELHO,
                      "position": "top-left"}],
        "captions": r.data["captions"],
        "audio": {"narration": {"src": "synex/narracao.wav", "volume": 1}},
    }
    props_path = AQUI / "props.json"
    props_path.write_text(json.dumps(props, ensure_ascii=False, indent=2), encoding="utf-8")

    saida = AQUI / "synex-oficina-openmontage.mp4"
    cmd = ["npx", "remotion", "render", "src/index.tsx", "Explainer", str(saida), "--props", str(props_path),
           "--codec", "h264", "--crf", "18", "--audio-codec", "aac", "--audio-bitrate", "192k",
           "--width", "1080", "--height", "1920"]
    hs = os.environ.get("REMOTION_BROWSER")
    if hs:
        cmd += ["--browser-executable", hs]
    subprocess.run(cmd, cwd=COMPOSER, check=True)
    print("PRONTO:", saida, "duração da fala:", r.data["duration_seconds"], "s")


if __name__ == "__main__":
    main()
