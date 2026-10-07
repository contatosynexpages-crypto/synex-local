# Instagram da Synex: guia de gestão

O Claude cuida do Instagram **@synex_pages** por delegação do Gustavo (dono da Synex): cria as peças e agenda no Metricool, com **pelo menos 1 post a cada 3 dias**. Este guia é a referência de cada rodada.

## Conta e ferramentas

- **Metricool:** marca `synex_pages`, `blogId` **7026216**, fuso **America/Sao_Paulo**. Só o Instagram está conectado.
- **Melhores horários (dados do Metricool):**
  - pico às **10h**, de terça a sexta (quarta, quinta e sexta são os mais fortes);
  - segundo pico às **18h**;
  - sábado e domingo rendem cerca de metade.
  - Padrão: **10h00** nos dias úteis. Evite feriados nacionais.
- **Mídia:** o Metricool precisa de URL pública. Salve as imagens e vídeos em `social/` deste repositório e dê push na `main`. A Cloudflare publica em `https://synexpages.net/social/<arquivo>` em cerca de 2 minutos; confira o deploy pelo check-run "Workers Builds" do commit (`gh api repos/contatosynexpages-crypto/synex-local/commits/<sha>/check-runs`) antes de criar o post.
- **Histórico:** `instagram/historico.json`. Registre todo post criado, com data, tipo, tema, mídia e status, para não repetir tema.

## O que é a Synex Local (só fatos confirmados)

- Cria **páginas de vendas** para comércios locais de **Itanhaém, Peruíbe e Mongaguá (SP)**: serviços/cardápio, preços, fotos, localização, horários e botão direto para o WhatsApp.
- Página: **R$297, pagamento único**.
- **Bot de atendimento no WhatsApp:** opcional, **R$49 no 1º mês e R$99/mês** depois.
- **Diagnóstico grátis.** Atendimento presencial nas três cidades.
- **WhatsApp:** (13) 98881-1950. **Site:** synexpages.net.

**Nunca afirmar** (ainda não confirmado): prazo de entrega, "sem mensalidade de hospedagem", "API oficial do WhatsApp", garantia, número de clientes, resultados ("vende X% mais") ou depoimentos. Não citar comércios reais nem pessoas reais. Nomes de exemplo são inventados (Studio Carla, Sabor da Praia…).

## Linha editorial

O público são donos de comércio e prestadores de serviço do litoral sul (salão, barbearia, lanchonete, pizzaria, açaí, oficina, revenda de carros, eletricista, pet shop, loja). O tom é direto e local, em português do Brasil coloquial ("pra", "a gente"), sem jargão de marketing.

Pilares, alternados para não repetir o mesmo dois posts seguidos:

1. **Dor do cliente:** não é achado no Google, perfil parado, mensagem sem resposta, cliente pergunta preço e some.
2. **Como funciona:** passo a passo, o que tem na página, o diagnóstico grátis.
3. **Segmento:** um ofício por post, com a página que faria sentido para ele (salão, pizzaria, oficina...).
4. **Local:** as três cidades, temporada vs. morador, busca por "perto de mim".
5. **Oferta:** preço da página, bot opcional, diagnóstico grátis. No máximo 1 a cada 4 posts.
6. **Dica útil:** algo que o comerciante aplica sozinho (foto do cardápio, horário atualizado, responder rápido). Gera alcance e confiança.

## Formatos

- **Post estático 1080x1350** no estilo da série "Sinal Costeiro" (ver `filosofia-sinal-costeiro.md`):
  - fundo preto com grade fina e vermelho `#E8283A` só no essencial;
  - fontes Big Shoulders (títulos), Instrument Serif itálico (frase de apoio), Geist Mono (rótulos) e Instrument Sans;
  - cabeçalho com "SYNEX LOCAL", coordenadas e numeração; rodapé com o logo e @synex_pages;
  - margens de 90 px, nada sobreposto, texto curto.
- **Carrossel** (3 a 6 telas no mesmo estilo) para passo a passo e dicas. No Metricool são várias imagens em `media`.
- **Reels narrados:** **todo vídeo da Synex tem narração completa com a voz Alex**, legendas e áudio tratado. Use o motor de `instagram/video/`, que roda aqui na nuvem, e siga `instagram/video/GUIA-VIDEO.md`. Meta: **1 Reels por semana**, com segmento novo a cada vez (pizzaria, barbearia, oficina, açaí, pet shop, revenda de carros, eletricista…). Parta do modelo `salao-de-beleza` e crie as cenas do segmento. Vídeo com voz sintética vai com `isAiGenerated: true`. Vídeo enviado pelo Gustavo sem narração: pergunte antes se deve ganhar narração.

### Como gerar as artes

1. Copie `instagram/motor/gen_serie1.py` para um arquivo novo do lote, por exemplo `gen_2026-11.py`.
   - Mantenha CSS, `frame`, `page` e os helpers.
   - Troque o dicionário `P`: cada post tem slug, coordenada do cabeçalho, SVG da arte e HTML do texto.
   - Ajuste `TOTAL` e a numeração. Numeração nova por série, ou tire o "Nº" se for avulso.
2. Rode `python3 gen_<lote>.py`, depois `NODE_PATH=$(npm root -g) node render.js` (a saída aponta sobreposição ou texto fora da margem; corrija até sair tudo "ok") e por fim `python3 finalizar.py`.
3. Olhe cada PNG (contact sheet) antes de publicar. Se não estiver impecável, refaça.
4. Copie os PNGs finais (sem `@2x`) para `social/` com nome datado, por exemplo `social/2026-11-03-dica-fotos.png`, faça commit e push.

## Legenda

- Primeira linha forte (gancho), 2 a 4 linhas curtas, chamada no fim: "Diagnóstico grátis: link na bio" ou "Chama no WhatsApp (13) 98881-1950".
- 6 a 8 hashtags: sempre `#itanhaem #peruibe #mongagua #litoralsul #comerciolocal #paginadevendas` mais 1 ou 2 do segmento.
- Texto alternativo (`mediaAltText`) descrevendo a imagem.

## Rotina de cada rodada

1. `getScheduledPosts` dos próximos 10 dias e o `historico.json`.
2. Se em algum trecho dos próximos 7 dias houver mais de 3 dias sem post agendado, crie posts para cobrir, pensando nos dias úteis às 10h. Se já estiver coberto, não crie nada.
   - Se não houver Reels narrado publicado ou agendado nos últimos 7 dias nem nos próximos 7, produza um (segmento ainda não usado no `historico.json`) e agende para terça, quarta ou quinta às 18h00. O Reels conta como post para a regra dos 3 dias.
3. Gere as artes, revise, publique a mídia no site, crie os posts no Metricool (`createScheduledPost`, `autoPublish: true`, `draft: false`, `instagramData.type` POST ou REEL) e atualize o `historico.json` (commit e push).
4. Se houver dados, olhe o desempenho dos últimos posts (`getAnalyticsDataByMetrics`) e prefira os pilares e formatos que tiveram mais alcance e salvamentos.
5. Termine com um resumo curto para o Gustavo: o que foi agendado (data, tema), o que publicou e qualquer problema.
