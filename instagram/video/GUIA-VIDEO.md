# Guia de vídeo da Synex Local (Reels narrados)

**Regra da Synex: todo vídeo tem narração completa** (voz Alex do começo ao fim), legendas sincronizadas, imagem 1080x1920 limpa e áudio tratado. Vídeo sem narração não sai.

**Vídeos da Synex saem só deste motor.** O OpenMontage está instalado (`instagram/openmontage/`), mas por decisão do Gustavo não é usado para a Synex por enquanto.

Este motor roda na nuvem e no PC. Na nuvem: `cd instagram/video && python3 gerar.py modelos/<nome>` (o modelo de voz, ~350 MB, é baixado sozinho do GitHub do kokoro-onnx na primeira vez; precisa de `pip install --break-system-packages kokoro-onnx soundfile` e Playwright/Chromium, que já existem no ambiente).

## O que é a Synex Local

Cria páginas de vendas para comércios locais de **Itanhaém, Peruíbe e Mongaguá (SP)**. A página mostra serviços, preços, fotos, localização e horários, e tem um botão que leva o cliente direto para o WhatsApp do comércio.

Use só fatos já confirmados:
- página de vendas: R$297, pagamento único;
- bot de atendimento no WhatsApp: opcional, R$49 no primeiro mês e R$99 por mês depois;
- diagnóstico grátis;
- atendimento presencial nas três cidades.

Não prometa prazo de entrega, "sem mensalidade de hospedagem", "API oficial do WhatsApp" nem resultados, porque isso ainda não foi confirmado.

## Regras do vídeo

1. **Formato:** vertical 1080x1920, 30 fps, **45 a 60 segundos**.
2. **Voz:** Kokoro `pm_alex` (Alex), português do Brasil, velocidade 1.0.
3. **História em 5 a 7 cenas:**
   - um comerciante fictício da região num dia normal;
   - o problema: cliente sem resposta ou cliente que não acha o negócio no Google e vai para o concorrente;
   - a virada: o comércio ganha uma página própria;
   - a cliente acha a página, vê o preço e toca no botão do WhatsApp;
   - a mensagem chega pronta e o comerciante só confirma.
4. **Final:** termina na última cena da história. **Sem logo, sem telefone e sem chamada no fim.** A chamada vai na legenda do post.
5. **Nomes e preços** de comércio e de clientes são inventados e plausíveis para a região. Nunca use nome de comércio real.
6. **Legendas:** frases curtas sincronizadas com a narração, com 1 ou 2 palavras-chave em destaque (`*assim*` no roteiro).

## Estilo visual (manter igual ao modelo do salão)

- **Fundo:** preto `#0B0B0C` com grade fina e um brilho rosa/vinho suave que se move devagar.
- **Cores:**
  - vermelho Synex `#E8283A` para destaques pequenos (ponto final de títulos, alertas);
  - rosa `#D9467A` para palavras-chave da legenda;
  - verde WhatsApp `#25D366` só no botão e no ícone.
- **Fontes** (pasta `fontes`):
  - Instrument Sans para legendas e interface;
  - Instrument Serif itálico para o rótulo "celular da Carla";
  - Geist Mono para o carimbo de hora/lugar no topo (ex.: `SÁB · 08:14 · ITANHAÉM`);
  - Big Shoulders para títulos grandes.
- **Composição:**
  - carimbo de hora no topo;
  - rótulo itálico dizendo de quem é o celular;
  - celular no centro (600x1220), com as telas mudando por cena: notificações, busca no Google, página de vendas, conversa do WhatsApp;
  - legenda grande embaixo.
- **Abertura:** desenho em traço fino do lugar (no salão: espelho, cadeira e bancada) que se desenha sozinho. Termina numa cena-resumo (no salão: a agenda de sábado com o horário novo confirmado).
- **Movimento:**
  - entradas suaves de baixo para cima;
  - notificações empilhando;
  - texto digitando na busca;
  - círculo de toque onde o dedo "toca";
  - "digitando..." antes da mensagem chegar.

## Como criar um modelo novo

1. Copie a pasta `modelos/salao-de-beleza` para `modelos/<novo-segmento>`. Apague o `exemplo-pronto.mp4` e a pasta `voz`.
2. Escreva o `roteiro.json`:
   - `cenas`, com `id`, `texto` e `legendas`;
   - `efeitos`, com sons de `pop`, `toque`, `mensagem` e `enviada`, cada um com a cena e os segundos dentro dela;
   - `arquivo_final`.
3. Adapte o `cena.html` e o `anim.js` ao segmento. Por exemplo, para pizzaria: cardápio e pedido no lugar de serviços e agenda.
   - A função `render(t)` desenha o quadro do segundo `t` e precisa ser determinística (sem timers, só cálculo a partir de `t`).
   - Use `S.s1`…`S.sN` (início de cada cena) e `END`, que o `gerar.py` define no `timeline.js` a partir da duração real da narração.
   - Os horários dentro de cada cena são relativos ao início dela.
   - As legendas vêm do `roteiro.json`. Não as coloque no `anim.js`.
4. Rode `python3 gerar.py modelos/<novo-segmento>`. Ele gera a voz, desenha os quadros, mistura o áudio e salva o MP4.
5. Confira quadros soltos antes de entregar: textos sem sobrepor, nada cortado e legenda batendo com a fala.

## Legenda do post (modelo)

> [Gancho com a dor do segmento, em 1 linha]
> Com uma página de vendas, o cliente já chega sabendo o preço e chama no WhatsApp pronto pra [pedir/agendar/comprar].
> Diagnóstico grátis: link na bio.
> #itanhaem #peruibe #mongagua #litoralsul #comerciolocal #paginadevendas #[segmento]

## Qualidade (conferir antes de publicar)

- **Áudio:**
  - narração tratada pelo motor (filtro de graves, compressão leve, presença e loudnorm a -14 LUFS);
  - confira se a voz pronuncia bem os nomes. Se uma palavra sair estranha, reescreva o texto (por exemplo, número por extenso) e gere de novo.
- **Imagem:**
  - extraia 6 a 8 quadros do MP4 (`ffmpeg -ss <t> -i video.mp4 -frames:v 1 q.png`) e olhe cada um;
  - nada sobreposto, nada cortado, legenda legível, sem tela vazia por mais de 1 s.
- **Duração:** 45 a 60 s. Se passar, enxugue o roteiro; não acelere a voz.
- **Publicação:**
  - MP4 em `social/AAAA-MM-DD-<tema>.mp4` (push, esperar o deploy);
  - no Metricool use `instagramData.type` "REEL", `showReelOnFeed` true e `isAiGenerated` true (a voz é sintética);
  - `videoCoverMilliseconds` num quadro forte, o gancho.
