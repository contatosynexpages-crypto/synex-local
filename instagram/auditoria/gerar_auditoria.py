# Auditoria do Instagram @synexpages (12/10/2026). Gera auditoria.html e, com Playwright, o PDF A4.
# Dados: Meta Business Suite (Insights > Instagram, últimos 28 dias: 14/09 a 11/10/2026) e o perfil público em 12/10.
import os, json, subprocess, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.abspath(os.path.join(HERE, '..', 'fontes'))

# ---------- dados (como o Meta mostrou; None = sem dado) ----------
INICIO = dt.date(2026, 9, 14)
VIEWS_DIA = [0,0,0,0,4,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,1,0,0]
ALCANCE_DIA = [0,0,0,0,2,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0]
TOTAL = dict(views=14, alcance=4, alc_seg=0, alc_nseg=4, interacoes=0, conversas=0, pedidos=0, seguidores=0, seguindo=0, posts=4)
POSTS = [  # data, tipo, título, views, alcance, interações, tempo total, tempo médio
    ('06/10 19:10', 'Reel', 'Seu cliente procurou você (vídeo do Gustavo)', 0, 1, 0, '1 min 36 s', '16 s'),
    ('07/10 10:03', 'Foto', '01 · Seu comércio, encontrado', 2, 1, 0, None, None),
    ('08/10 18:04', 'Reel', 'Pizzaria em Peruíbe (narrado, voz Alex)', 1, 1, 0, '24 s', '6 s'),
    ('09/10 10:03', 'Foto', '02 · Procuraram por você, acharam o concorrente', 0, None, 0, None, None),
]

def fonte(nome):
    return 'file://' + os.path.join(FONTES, nome)

def barras_diarias(vals, w=680, h=200):
    n = len(vals); pad_l, pad_b, pad_t = 6, 34, 26
    bw = (w - pad_l) / n; mx = max(vals) or 1; out = []
    for i, v in enumerate(vals):
        x = pad_l + i * bw + bw * 0.18; bwid = bw * 0.64
        bh = (h - pad_b - pad_t) * v / mx
        y = h - pad_b - bh
        if v:
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bwid:.1f}" height="{bh:.1f}" rx="4" fill="var(--red)"/>')
            out.append(f'<text x="{x+bwid/2:.1f}" y="{y-7:.1f}" class="v" text-anchor="middle">{v}</text>')
        else:
            out.append(f'<rect x="{x:.1f}" y="{h-pad_b-3:.1f}" width="{bwid:.1f}" height="3" rx="1.5" fill="var(--i4)"/>')
        d = INICIO + dt.timedelta(days=i)
        if i % 7 == 0 or i == n - 1:
            out.append(f'<text x="{x+bwid/2:.1f}" y="{h-12}" class="ax" text-anchor="middle">{d.day:02d}/{d.month:02d}</text>')
    marco = 22  # 06/10, primeiro post da Synex
    mxp = pad_l + marco * bw + bw * 0.5
    out.append(f'<line x1="{mxp:.1f}" x2="{mxp:.1f}" y1="{pad_t-14}" y2="{h-pad_b}" stroke="var(--amber)" stroke-dasharray="3 4"/>')
    out.append(f'<text x="{mxp-6:.1f}" y="{pad_t-4}" class="ax amb" text-anchor="end">1º post da série · 06/10</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Visualizações por dia">{"".join(out)}</svg>'

def barras_posts(w=680, h=230):
    grupos = POSTS; n = len(grupos); pad_b, pad_t = 56, 24; gw = w / n
    mx = max(max(p[3] or 0, p[4] or 0) for p in grupos) or 1; out = []
    for i, p in enumerate(grupos):
        for j, (val, cor, rot) in enumerate([(p[3], 'var(--red)', 'visualizações'), (p[4], 'var(--amber)', 'alcance')]):
            bw = gw * 0.22; x = i * gw + gw * 0.25 + j * (bw + 8)
            if val is None:
                out.append(f'<text x="{x+bw/2:.1f}" y="{h-pad_b-8}" class="v mut" text-anchor="middle">s/ dado</text>'); continue
            bh = (h - pad_b - pad_t) * val / mx; y = h - pad_b - bh
            if val:
                out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="5" fill="{cor}"/>')
            else:
                out.append(f'<rect x="{x:.1f}" y="{h-pad_b-3}" width="{bw:.1f}" height="3" rx="1.5" fill="var(--i4)"/>')
            out.append(f'<text x="{x+bw/2:.1f}" y="{(y if val else h-pad_b)-8:.1f}" class="v" text-anchor="middle">{val}</text>')
        out.append(f'<text x="{i*gw+gw/2:.1f}" y="{h-30}" class="ax" text-anchor="middle">{p[1]} · {p[0][:5]}</text>')
    out.append(f'<g class="ax"><rect x="{w-250}" y="0" width="12" height="12" rx="3" fill="var(--red)"/><text x="{w-232}" y="10">visualizações</text>'
               f'<rect x="{w-130}" y="0" width="12" height="12" rx="3" fill="var(--amber)"/><text x="{w-112}" y="10">alcance</text></g>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="Visualizações e alcance por post">{"".join(out)}</svg>'

def linhas_posts():
    tr = []
    for p in POSTS:
        f = lambda v: '<span class="mut">sem dado</span>' if v is None else str(v)
        tr.append(f'<tr><td class="mono">{p[0]}</td><td>{p[1]}</td><td>{p[2]}</td><td class="n">{f(p[3])}</td><td class="n">{f(p[4])}</td><td class="n">{p[5]}</td><td class="n">{f(p[7]) if p[1]=="Reel" else "—"}</td></tr>')
    return ''.join(tr)

def pagina(num, titulo, corpo, kicker=''):
    return f'''<section class="page"><header class="ph"><span class="mono">@synexpages · auditoria · {num:02d}</span><span class="mono">14/09 – 11/10/2026</span></header>
<div class="body">{f'<div class="kick mono">{kicker}</div>' if kicker else ''}<h2>{titulo}</h2>{corpo}</div>
<footer class="pf mono"><span>Synex Local</span><span>{num:02d}</span></footer></section>'''

CSS = f'''
@font-face{{font-family:Shoulders;src:url('{fonte("BigShoulders-Bold.ttf")}')}}
@font-face{{font-family:Mono;src:url('{fonte("GeistMono-Regular.ttf")}')}}
@font-face{{font-family:ISans;src:url('{fonte("InstrumentSans-Regular.ttf")}')}}
@font-face{{font-family:ISans;font-weight:700;src:url('{fonte("InstrumentSans-Bold.ttf")}')}}
@font-face{{font-family:ISerif;font-style:italic;src:url('{fonte("InstrumentSerif-Italic.ttf")}')}}
@page{{size:A4;margin:0}}
:root{{--bg:#0B0B0C;--card:#151517;--ink:#F3F1EE;--red:#E8283A;--amber:#FFB020;--i2:rgba(243,241,238,.68);--i3:rgba(243,241,238,.42);--i4:rgba(243,241,238,.16);--line:rgba(243,241,238,.14)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:var(--bg);color:var(--ink);font-family:ISans,Helvetica,Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:210mm;height:297mm;padding:16mm 17mm 14mm;display:flex;flex-direction:column;page-break-after:always;position:relative;overflow:hidden;
  background-image:linear-gradient(rgba(243,241,238,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(243,241,238,.03) 1px,transparent 1px);background-size:9mm 9mm}}
.page:last-child{{page-break-after:auto}}
.mono{{font-family:Mono,monospace;font-size:8.6pt;letter-spacing:.14em;text-transform:uppercase;color:var(--i3)}}
.ph,.pf{{display:flex;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:3mm}}
.pf{{border-bottom:0;border-top:1px solid var(--line);padding:3mm 0 0;margin-top:auto}}
.body{{flex:1;display:flex;flex-direction:column;gap:6mm;padding-top:9mm}}
.kick{{color:var(--red)}}
h1,h2{{font-family:Shoulders,Impact,sans-serif;text-transform:uppercase;line-height:.88;letter-spacing:.005em}}
h2{{font-size:40pt}}
p{{font-size:11pt;line-height:1.5;color:var(--i2);max-width:150mm}}
p b,li b{{color:var(--ink)}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:5mm}}
.grid4{{display:grid;grid-template-columns:1fr 1fr;gap:5mm}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:5mm;padding:5mm 6mm;display:flex;flex-direction:column;gap:2mm}}
.big{{font-family:Shoulders,Impact,sans-serif;font-size:58pt;line-height:.85}}
.big small{{font-size:22pt;color:var(--i3)}}
.lab{{font-size:10pt;color:var(--i2);line-height:1.4}}
.red{{color:var(--red)}} .amb{{color:var(--amber)}}
svg text{{font-family:Mono,monospace}} svg .v{{font-size:12px;fill:var(--ink)}} svg .ax{{font-size:10.5px;fill:var(--i3);letter-spacing:.06em}} svg .amb{{fill:var(--amber)}} svg .mut{{fill:var(--i3);font-size:10px}}
table{{width:100%;border-collapse:collapse;font-size:9.6pt}}
th{{text-align:left;font-family:Mono,monospace;font-weight:400;font-size:7.6pt;letter-spacing:.12em;text-transform:uppercase;color:var(--i3);padding:0 2mm 2.5mm;border-bottom:1px solid var(--line)}}
td{{padding:3mm 2mm;border-bottom:1px solid var(--line);color:var(--i2);vertical-align:top}}
td.n{{text-align:right;font-variant-numeric:tabular-nums;color:var(--ink)}} th.n{{text-align:right}}
td.mono{{font-size:8pt;letter-spacing:.06em;color:var(--i3)}}
.mut{{color:var(--i3)}}
ul.lista{{list-style:none;display:flex;flex-direction:column;gap:3.4mm}}
ul.lista li{{font-size:10.6pt;line-height:1.45;color:var(--i2);padding-left:7mm;position:relative}}
ul.lista li::before{{content:"";position:absolute;left:0;top:2.1mm;width:3mm;height:3mm;border-radius:1mm;background:var(--red)}}
ol.passos{{list-style:none;counter-reset:p;display:flex;flex-direction:column;gap:4mm}}
ol.passos li{{counter-increment:p;display:grid;grid-template-columns:13mm 1fr;gap:3mm;font-size:10.6pt;line-height:1.45;color:var(--i2)}}
ol.passos li::before{{content:counter(p);font-family:Shoulders,Impact,sans-serif;font-size:30pt;line-height:.9;color:var(--red)}}
ol.passos b{{color:var(--ink);display:block;font-size:12pt;margin-bottom:1mm}}
.bar{{height:9mm;border-radius:3mm;background:var(--i4);position:relative;overflow:hidden}}
.bar i{{position:absolute;inset:0 auto 0 0;border-radius:3mm;background:var(--red)}}
.quote{{font-family:ISerif,serif;font-style:italic;font-size:15pt;line-height:1.35;color:var(--ink)}}
.cover{{justify-content:space-between}}
.cover h1{{font-size:88pt}}
.tag{{display:inline-block;border:1px solid var(--line);border-radius:99px;padding:1.2mm 3.4mm;font-family:Mono,monospace;font-size:7.6pt;letter-spacing:.12em;text-transform:uppercase;color:var(--i2)}}
'''

capa = f'''<section class="page cover">
<header class="ph"><span class="mono">Synex Local · auditoria de Instagram</span><span class="mono">12/10/2026</span></header>
<div style="display:flex;flex-direction:column;gap:7mm;padding-top:14mm">
  <span class="mono red">@synexpages · 14/09 a 11/10/2026</span>
  <h1>O conteúdo<br>está no ar.<br><span class="red">Falta gente</span><br>vendo.</h1>
  <p class="quote" style="max-width:160mm">Em 28 dias, a conta alcançou 4 pessoas. O problema agora não é a qualidade dos posts: é que eles ainda não chegam a ninguém.</p>
</div>
<div class="grid4">
  <div class="card"><span class="mono">Seguidores</span><div class="big">0 <small>±0</small></div><span class="lab">Nenhum seguidor ganho ou perdido no período.</span></div>
  <div class="card"><span class="mono">Contas alcançadas</span><div class="big">4</div><span class="lab">100% não seguidores · 14 visualizações no total.</span></div>
  <div class="card"><span class="mono">Reels</span><div class="big">0–1 <small>visualizações</small></div><span class="lab">Com 2 Reels e quase nenhuma exibição, ainda não dá para medir um “normal”.</span></div>
  <div class="card"><span class="mono">Melhor conteúdo</span><div class="big">2 <small>visualizações</small></div><span class="lab">Post 01 “Seu comércio, encontrado” (07/10). Interações: 0 em todos.</span></div>
</div>
<footer class="pf mono"><span>Fonte: Meta Business Suite + perfil público</span><span>01</span></footer></section>'''

p_cresc = pagina(2, 'Crescimento', f'''
<p>A conta tem <b>0 seguidores</b> e segue <b>0 perfis</b>. No período, o Meta registrou 0 novos seguidores e 0 que deixaram de seguir, então ainda não há curva para comparar a última semana com as anteriores.</p>
<div class="grid2">
  <div class="card"><span class="mono">Seguiram</span><div class="big">0</div></div>
  <div class="card"><span class="mono">Deixaram de seguir</span><div class="big">0</div></div>
</div>
<div class="card"><span class="mono">O que isso quer dizer</span>
<p>Com zero seguidores, todo post depende de o Instagram mostrar para quem não conhece a conta. Isso acontece principalmente com Reels, e só começa depois que os primeiros vídeos ganham alguma tração. Por isso a primeira meta não é “viralizar”: é chegar aos <b>primeiros 100 seguidores locais</b>, que é também quando o Meta começa a mostrar dados de público.</p></div>
''', 'Seguidores')

p_alcance = pagina(3, 'Alcance e descoberta', f'''
<div class="card"><span class="mono">Visualizações por dia · 14/09 a 11/10</span>{barras_diarias(VIEWS_DIA)}
<span class="lab">As 6 visualizações de setembro vieram antes da série da Synex (conteúdo antigo da conta). Desde o 1º post, em 06/10: <b>8 visualizações</b>.</span></div>
<div class="grid2">
  <div class="card"><span class="mono">Alcance: seguidores × não seguidores</span>
    <div class="lab">Não seguidores · 4</div><div class="bar"><i style="width:100%"></i></div>
    <div class="lab">Seguidores · 0</div><div class="bar"><i style="width:0"></i></div></div>
  <div class="card"><span class="mono">Por tipo de conteúdo</span>
    <p><b>Fotos:</b> 2 visualizações, 1 conta alcançada (o post 02 não tem dado de alcance).<br><b>Reels:</b> 1 visualização, 2 contas alcançadas.</p>
    <p><b>Anúncios:</b> nenhum alcance pago no período. A campanha “CAMPANHA DE ENGAJAMENTO SYNEX” aparece <b>ativa desde 10/10</b>, mas sem gasto nem exibições registradas até agora.</p></div>
</div>''', 'Visualizações e alcance')

p_perfil = pagina(4, 'O perfil', '''
<div class="card"><span class="mono">Como está hoje</span>
<p><b>Nome:</b> Synex Pages | Sites &amp; automação<br><b>Bio:</b> “Seu negócio pode estar perdendo vendas. Criamos páginas que transformam visitas em clientes. Automação para vender mais. Fale conosco”<br><b>Link:</b> local.synexpages.net · <b>Destaques:</b> nenhum · <b>Posts:</b> 4 (2 Reels, 2 fotos)</p></div>
<ul class="lista">
<li><b>As artes mostram um @ que não existe.</b> O rodapé dos posts da série diz “@SYNEX_PAGES”, mas a conta é <b>@synexpages</b>. Quem digitar o que vê na arte cai em “página não disponível”.</li>
<li><b>A bio não diz onde nem quanto.</b> Não cita Itanhaém, Peruíbe e Mongaguá, nem a oferta (página de vendas, diagnóstico grátis). Quem chega por um Reel não entende em 3 segundos se é para ele.</li>
<li><b>Nome sem a palavra que as pessoas buscam.</b> A busca do Instagram lê o campo nome. “Página de vendas · Litoral Sul” ajuda mais do que “Sites &amp; automação”.</li>
<li><b>Sem destaques.</b> Faltam respostas fixas para quem visita o perfil: como funciona, preço, exemplos prontos.</li>
<li><b>Um Reel some do perfil.</b> O Reel do salão de beleza (marcado como publicado em 06/10) não aparece na grade, e o post 03 (previsto para 13/10) ainda não saiu.</li>
</ul>''', 'Primeira impressão')

p_reels = pagina(5, 'Reels', f'''
<p>Com 2 Reels e no máximo 1 visualização cada, não existe um “normal” da conta ainda. Os números abaixo servem como ponto de partida, não como veredito sobre os vídeos.</p>
<table><thead><tr><th>Data</th><th>Tipo</th><th>Post</th><th class="n">Visual.</th><th class="n">Alcance</th><th class="n">Interações</th><th class="n">Tempo médio</th></tr></thead>
<tbody>{''.join(r+'</tr>' for r in linhas_posts().split('</tr>') if '<td>Reel</td>' in r)}</tbody></table>
<div class="grid2">
  <div class="card"><span class="mono">Seu cliente procurou você · 06/10</span>
  <p>Segurou <b>16 s em média</b>, o melhor tempo da conta. <b>Ajuste:</b> é longo (o tempo total visto foi 1 min 36 s). Corte para 25–30 s e coloque a frase “Seu cliente procurou você. Achou o concorrente.” escrita na tela já no 1º segundo.</p></div>
  <div class="card"><span class="mono">Pizzaria em Peruíbe · 08/10</span>
  <p><b>6 s em média</b> para 1 visualização. <b>Ajuste:</b> abrir com a dor (“Sexta, 21h, o WhatsApp não para”) antes de mostrar a solução, e testar uma versão de 20 s.</p></div>
</div>
<p class="mut" style="font-size:9.5pt">Taxa de pulo e compartilhamentos por curtida: sem dado (o Meta não mostra com esse volume; nenhuma curtida no período).</p>
''', 'Vídeos')

p_posts = pagina(6, 'Posts e carrosséis', f'''
<div class="card"><span class="mono">Visualizações e alcance por post</span>{barras_posts()}</div>
<table><thead><tr><th>Data</th><th>Tipo</th><th>Post</th><th class="n">Visual.</th><th class="n">Alcance</th><th class="n">Interações</th><th class="n">Tempo médio</th></tr></thead><tbody>{linhas_posts()}</tbody></table>
<p><b>Salvamentos, compartilhamentos e cliques no link: 0</b> em todos os posts. Ainda não há “ímã de salvamento”. Carrossel: nenhum publicado, então não há comparação foto × carrossel. Vale testar um: “3 sinais de que seu negócio está perdendo cliente no Google”.</p>
''', 'Imagens')

p_publico = pagina(7, 'Público', '''
<div class="card"><span class="mono">Idade, gênero, cidades</span>
<p><b>Sem dados.</b> O Meta só mostra o público de contas com pelo menos 100 seguidores, e as 4 contas alcançadas são poucas demais para qualquer recorte.</p></div>
<div class="card"><span class="mono">Quem a Synex precisa alcançar</span>
<p>Donos de comércio e prestadores de serviço de <b>Itanhaém, Peruíbe e Mongaguá</b>. Quando a conta passar de 100 seguidores, o primeiro número a conferir é a fatia de seguidores nessas três cidades. Se ela for baixa, o conteúdo está atraindo gente de fora e precisa de mais referência local (bairros, ruas, comércios conhecidos).</p></div>''', 'Quem vê')

p_horarios = pagina(8, 'Horários', '''
<div class="card"><span class="mono">Quando seus seguidores estão online</span><p><b>Sem dados.</b> Sem seguidores, o Instagram não calcula esse gráfico.</p></div>
<div class="card"><span class="mono">Janela para testar nas próximas 2 semanas</span>
<p>Manter o que já está no calendário e medir: <b>posts às 10h</b> (terça a sexta) e <b>Reels às 18h</b> (terça a quinta), que é quando dono de comércio costuma olhar o celular antes do movimento da noite. Isso é um teste, não uma descoberta: depois de 100 seguidores, trocar pelo horário que o Instagram mostrar.</p></div>''', 'Quando postar')

p_perguntas = pagina(9, 'O que perguntam', '''
<div class="card"><span class="mono">Perguntas nos comentários</span><p><b>Nenhum comentário</b> nos 4 posts, então ainda não há perguntas do público.</p></div>
<p>Enquanto isso, dá para usar as dúvidas que aparecem nas conversas de venda da Synex Local. Cada uma vira um post:</p>
<ul class="lista">
<li><b>“Já tenho Instagram, preciso de página?”</b> → Reel: o cliente pesquisando no Google e não achando o perfil.</li>
<li><b>“Quanto custa?”</b> → post do preço (05 da série) com o que vem incluso, em vez de só o número.</li>
<li><b>“Demora quanto pra ficar pronto?”</b> → carrossel “do primeiro contato à página no ar”.</li>
<li><b>“E se eu quiser mudar o cardápio depois?”</b> → Reel curto mostrando uma alteração sendo feita.</li>
</ul>''', 'Ideias de post')

p_plano = pagina(10, 'O plano da semana', '''
<ol class="passos">
<li><div><b>Arrumar a vitrine (hoje, 30 min)</b>Trocar “@SYNEX_PAGES” por “@synexpages” nas artes que ainda vão sair. Reescrever a bio com cidade, oferta e chamada: “Páginas de vendas para o comércio de Itanhaém, Peruíbe e Mongaguá · Diagnóstico grátis no WhatsApp”. Mudar o nome para “Synex · Página de vendas Litoral Sul”. Criar 3 destaques: Como funciona, Preço, Exemplos.</div></li>
<li><div><b>Dar o primeiro empurrão de alcance</b>Cada post vai para os stories da Synex e para o status do WhatsApp do Gustavo. 15 min por dia seguindo e comentando de verdade em perfis de comércios locais (eles são o público). Se for usar a campanha ativa, apontar para o melhor Reel, só para o Litoral Sul, e com orçamento aprovado antes.</div></li>
<li><div><b>Mais Reels, mais curtos</b>Dois Reels por semana, de 20 a 30 s, com a frase-gancho escrita na tela no 1º segundo. Os posts de imagem continuam, mas quem traz gente nova são os Reels.</div></li>
</ol>
<div class="grid2">
  <div class="card"><span class="mono">Remakes</span><p><b>1.</b> “Seu cliente procurou você” em 30 s.<br><b>2.</b> Pizzaria abrindo pela dor de sexta à noite.</p><p class="mut" style="font-size:9.5pt">Sequência quente de 48 h: nenhuma em aberto.</p></div>
  <div class="card"><span class="mono">3 números para conferir na próxima semana</span><p><b>Contas alcançadas</b> (hoje: 4)<br><b>Visitas ao perfil</b><br><b>Toques no link / WhatsApp</b></p></div>
</div>''', 'Prioridades')

p_metodo = pagina(11, 'Como foi medido', '''
<ul class="lista">
<li><b>Período:</b> últimos 28 dias do Meta Business Suite, de 14/09 a 11/10/2026. Perfil conferido em 12/10/2026.</li>
<li><b>Fonte:</b> Insights do Instagram no Meta Business Suite (visão geral e tabela de conteúdo) e o perfil público @synexpages. Os números são os que o Meta mostrou, sem estimativa.</li>
<li><b>“Normal” da conta:</b> não calculado. Com 2 Reels e no máximo 1 visualização cada, uma mediana não diria nada. Na próxima auditoria, com mais Reels, cada vídeo passa a ser comparado com a mediana da própria conta.</li>
<li><b>Dados que faltaram:</b> taxa de pulo dos Reels, compartilhamentos por curtida, público (idade, gênero, cidades) e horários dos seguidores. O Meta não mostra esses dados para contas com tão pouco volume ou com menos de 100 seguidores. “Sem dado” não quer dizer zero.</li>
<li><b>Anúncios:</b> nenhum alcance pago entrou nos números acima.</li>
<li><b>Ferramenta:</b> a conexão da Buzzfy não estava disponível nesta sessão, então os dados vieram direto do Meta Business Suite.</li>
</ul>''', 'Método')

html = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Auditoria Instagram @synexpages</title><style>{CSS}</style></head><body>' + \
    ''.join([capa, p_cresc, p_alcance, p_perfil, p_reels, p_posts, p_publico, p_horarios, p_perguntas, p_plano, p_metodo]) + '</body></html>'
caminho = os.path.join(HERE, 'auditoria.html')
open(caminho, 'w', encoding='utf-8').write(html)
print(caminho)
