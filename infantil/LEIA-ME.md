# Vídeos infantis (YouTube Shorts e TikTok)

Motor de vídeo infantil, derivado do motor da Synex: personagens em SVG, voz Kokoro, música e efeitos próprios, legendas e vídeo vertical 1080x1920. Tudo é original: personagens, música e sons são gerados aqui, então não há risco de direitos autorais.

## Como gerar um episódio

```bash
cd infantil
export SYNEX_KOKORO=<pasta com kokoro-v1.0.onnx e voices-v1.0.bin>
python3 montar_voz.py modelos/<ep>                   # narração com pausas, marks.js e legendas
python3 musica.py modelos/<ep>/musica.wav <segundos>  # trilha original (duração do vídeo + 2 s)
python3 previa.py modelos/<ep>                       # fotos de conferência em prev/
python3 gerar.py modelos/<ep> --sem-voz              # vídeo final (usa as vozes já montadas)
```

Cada episódio é uma pasta em `modelos/`, com estes arquivos:
- `partes.json`: as falas de cada cena, com a pausa depois de cada uma;
- `roteiro.json`: voz, velocidade, nome do arquivo final, legendas e efeitos sonoros;
- `cena.html` e `anim.js`: o cenário e a animação.

Use `contar-frutas` como modelo.

## Regras

- **Voz:** `pf_dora`, velocidade 0.88. Falas curtas, com pausas para a criança responder ou contar junto.
- **Conteúdo:** de 30 a 60 s, um tema por vídeo (contar, cores, formas, animais, letras). Linguagem simples e positiva, sem marcas, personagens conhecidos ou músicas de terceiros.
- **Áudio:** a música abaixa sozinha quando a voz fala. O volume final fica em torno de −14 a −16 LUFS.
- **No YouTube:** marcar **"Conteúdo para crianças"**, obrigatório (COPPA). Com isso os comentários ficam desligados e os anúncios são limitados.
- **No TikTok:** a plataforma é para maiores de 13 anos. Lá o público é de pais e familiares, então a legenda deve falar com os pais ("pra assistir com os pequenos").
