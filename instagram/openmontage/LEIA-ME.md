# OpenMontage (instalado, fora de uso na Synex)

**Decisão do Gustavo (2026-10-08):** o OpenMontage fica instalado, mas **não é usado para a Synex por enquanto**. Todo vídeo da Synex continua saindo do nosso motor (`instagram/video/`, ver `GUIA-VIDEO.md`).

## O que é

[OpenMontage](https://github.com/calesthio/OpenMontage) é um sistema aberto de produção de vídeo guiado por agente. A licença é AGPL-3.0: usar para gerar vídeos é livre; só redistribuir o código modificado exige publicar as mudanças.

- **Sem chave de API:** monta vídeos de texto, números e gráficos (cartões, comparações, R$, legendas), via Remotion.
- **Com chaves:** clipes e imagens de IA (Kling, Veo, fal.ai…, pagos), vídeos de banco de imagens (Pexels e Pixabay, chave grátis) e música. Na nuvem do Claude esses sites são bloqueados; no PC funcionam.

## Ajustes da Synex (`ajustes-synex.patch` + `kokoro_tts.py`)

Testado na versão `9327439` (2026-10-03).

1. **Voz Kokoro** (`tools/audio/kokoro_tts.py`): pm_alex, pf_dora, grátis e offline, com legendas palavra a palavra estimadas. O OpenMontage não trazia nenhuma voz grátis em português que funcionasse.
   - Inclui uma correção: o espeak falha quando a pasta do venv tem um caminho muito longo.
2. **Vertical 1080x1920:** as cenas são escaladas (padrão 1,8x; ajustável por cena com `"scale"`), e as legendas ficam maiores e acima da interface do Reels.
3. **Legendas:** corrigido um bug que grudava as palavras ("Comumapágina").
4. **Comparação:** as cores seguem o tema, em vez de azul e verde fixos.
5. **Fontes locais:** troca o download do Google Fonts por arquivos locais, porque a nuvem bloqueia o Google Fonts.

## Instalar

```bash
bash instagram/openmontage/instalar.sh            # instala em ~/OpenMontage
```

Exemplo de produção: `exemplo/produzir.py` (Reel "Oficina do Jorge", narração Alex, 38 s). Na nuvem, renderize com `REMOTION_BROWSER=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`.
