#!/usr/bin/env bash
# Instala o OpenMontage com os ajustes da Synex (voz Kokoro, vídeo vertical,
# legendas com espaço entre palavras, fontes locais).
#
# Uso:  bash instagram/openmontage/instalar.sh [pasta-destino]
# Padrão: ~/OpenMontage. Precisa de git, python3.11+, node 18+ e ffmpeg.
set -euo pipefail

AQUI="$(cd "$(dirname "$0")" && pwd)"
DEST="${1:-$HOME/OpenMontage}"
VERSAO=9327439db69021ab4b0e2776729bf3b58fdb5a87   # versão testada (2026-10-03)

if [ ! -d "$DEST/.git" ]; then
  git clone https://github.com/calesthio/OpenMontage.git "$DEST"
fi
cd "$DEST"
git fetch -q origin "$VERSAO" 2>/dev/null || true
git checkout -q "$VERSAO"
git apply "$AQUI/ajustes-synex.patch"
cp "$AQUI/kokoro_tts.py" tools/audio/
mkdir -p projects/synex-teste && cp "$AQUI/exemplo/produzir.py" projects/synex-teste/

PY=$(command -v python3.11 || command -v python3)
"$PY" -m venv .venv
.venv/bin/python -m pip install -q -r requirements.txt kokoro-onnx soundfile

cd remotion-composer
npm install --silent
npm install --silent --no-save @fontsource/space-grotesk @fontsource/playfair-display
mkdir -p public/fonts
cp node_modules/@fontsource/space-grotesk/files/space-grotesk-latin-*-normal.woff2 \
   node_modules/@fontsource/playfair-display/files/playfair-display-latin-*-normal.woff2 public/fonts/
cd ..
[ -f .env ] || cp .env.example .env

echo
echo "OpenMontage instalado em $DEST"
echo "Teste: KOKORO_MODEL_DIR=<pasta com kokoro-v1.0.onnx e voices-v1.0.bin> \\"
echo "       .venv/bin/python projects/synex-teste/produzir.py"
echo "(Sem Chrome do Remotion disponível, defina REMOTION_BROWSER com o caminho do headless_shell.)"
