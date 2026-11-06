/* Dados compartilhados da loja e do painel (prévia).
   Na versão real, isto vem do banco de dados e a loja edita pelo painel. */
window.CJ = (function () {
  'use strict';
  const PRODUTOS = [
    { id: 'rosas', cat: 'buques', nome: 'Buquê de rosas', desc: 'Rosas colombianas embaladas em papel de seda, com folhagens.', ilus: 'rosas',
      opcoes: [{ id: 'p', nome: '6 rosas', preco: 89 }, { id: 'm', nome: '12 rosas', preco: 149 }, { id: 'g', nome: '24 rosas', preco: 259 }] },
    { id: 'campo', cat: 'buques', nome: 'Buquê do campo', desc: 'Mix de flores da estação: lisianthus, astromélias e mosquitinho.', ilus: 'campo',
      opcoes: [{ id: 'p', nome: 'Pequeno', preco: 99 }, { id: 'g', nome: 'Grande', preco: 159 }] },
    { id: 'girassol', cat: 'buques', nome: 'Buquê de girassóis', desc: 'Três ou seis girassóis com eucalipto. Alegria pura.', ilus: 'girassol',
      opcoes: [{ id: 'p', nome: '3 girassóis', preco: 79 }, { id: 'g', nome: '6 girassóis', preco: 129 }] },
    { id: 'caixa', cat: 'arranjos', nome: 'Rosas na caixa', desc: 'Caixa redonda com rosas e espaço para bombons.', ilus: 'caixa',
      opcoes: [{ id: 'u', nome: 'Caixa média', preco: 179 }] },
    { id: 'orquidea', cat: 'arranjos', nome: 'Orquídea plantada', desc: 'Phalaenopsis em cachepô de cerâmica. A flor dura semanas.', ilus: 'orquidea',
      opcoes: [{ id: '1', nome: '1 haste', preco: 129 }, { id: '2', nome: '2 hastes', preco: 189 }] },
    { id: 'suculentas', cat: 'arranjos', nome: 'Mini jardim de suculentas', desc: 'Suculentas variadas em vaso baixo, com pedrinhas.', ilus: 'suculentas',
      opcoes: [{ id: 'u', nome: 'Vaso 20 cm', preco: 79 }] },
    { id: 'cafe', cat: 'cestas', nome: 'Cesta café com flores', desc: 'Café da manhã completo com mini buquê de rosas.', ilus: 'cesta',
      opcoes: [{ id: 'u', nome: 'Para 2 pessoas', preco: 219 }] },
    { id: 'romantica', cat: 'cestas', nome: 'Cesta romântica', desc: 'Espumante, chocolates, pelúcia e rosas.', ilus: 'cesta',
      opcoes: [{ id: 'u', nome: 'Completa', preco: 249 }] },
    { id: 'zamio', cat: 'plantas', nome: 'Zamioculca', desc: 'Aguenta pouca luz e rega a cada 15 dias. Vaso de cerâmica.', ilus: 'folhagem',
      opcoes: [{ id: 'm', nome: 'Média', preco: 89 }, { id: 'g', nome: 'Grande', preco: 139 }] },
    { id: 'costela', cat: 'plantas', nome: 'Costela-de-adão', desc: 'Folhas grandes e recortadas para sala ou varanda.', ilus: 'folhagem',
      opcoes: [{ id: 'u', nome: 'Vaso 25 cm', preco: 119 }] },
    { id: 'lirio', cat: 'plantas', nome: 'Lírio-da-paz', desc: 'Flores brancas e folhas brilhantes. Fácil de cuidar.', ilus: 'lirio',
      opcoes: [{ id: 'u', nome: 'Vaso 17 cm', preco: 69 }] },
  ];
  const EXTRAS = [
    { id: 'chocolate', nome: 'Bombons (caixa 8 un.)', preco: 39 },
    { id: 'balao', nome: 'Balão metalizado de coração', preco: 25 },
    { id: 'pelucia', nome: 'Pelúcia de urso', preco: 49 },
  ];
  const CATEGORIAS = [
    { id: 'todos', nome: 'Tudo' }, { id: 'buques', nome: 'Buquês' }, { id: 'arranjos', nome: 'Arranjos' },
    { id: 'cestas', nome: 'Cestas' }, { id: 'plantas', nome: 'Plantas' },
  ];
  // taxas de exemplo (a loja define as reais no painel)
  const BAIRROS = [
    { nome: 'Cidade Nova Peruíbe', taxa: 8 }, { nome: 'Centro', taxa: 10 }, { nome: 'Jardim Peruíbe', taxa: 10 },
    { nome: 'Stella Maris', taxa: 12 }, { nome: 'Jardim Ribamar', taxa: 12 }, { nome: 'Oásis', taxa: 15 },
    { nome: 'Balneário Três Marias', taxa: 15 }, { nome: 'Caraguava', taxa: 18 }, { nome: 'Guaraú', taxa: 25 },
  ];
  const PERIODOS = [
    { id: 'manha', nome: 'Manhã', faixa: '8h30 às 12h', fim: 12 },
    { id: 'tarde', nome: 'Tarde', faixa: '13h às 17h30', fim: 17.5 },
  ];

  const brl = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  const ler = (k, padrao) => { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : padrao; } catch (e) { return padrao; } };
  const gravar = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* sem armazenamento: segue só na memória */ } };

  // agora em Peruíbe (horário de Brasília)
  function agoraSP() {
    const p = Object.fromEntries(new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo', year: 'numeric', month: '2-digit', day: '2-digit', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' }).formatToParts(new Date()).map((x) => [x.type, x.value]));
    return { data: `${p.year}-${p.month}-${p.day}`, hora: Number(p.hour) + Number(p.minute) / 60 };
  }
  const somarDias = (iso, n) => { const d = new Date(iso + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
  const diaSemana = (iso) => new Date(iso + 'T12:00:00Z').getUTCDay();

  return { PRODUTOS, EXTRAS, CATEGORIAS, BAIRROS, PERIODOS, brl, ler, gravar, agoraSP, somarDias, diaSemana,
    CHAVE_PEDIDOS: 'cj-pedidos', CHAVE_ESGOTADOS: 'cj-esgotados' };
})();

/* Ilustrações próprias dos produtos (substituídas pelas fotos reais na versão final) */
(function () {
  const rosa = (x, y, r, c) => `<g transform="translate(${x} ${y})"><circle r="${r}" fill="${c}"/><path d="M${-r * .5} 0a${r * .5} ${r * .5} 0 1 1 ${r} 0" fill="none" stroke="rgba(120,30,40,.35)" stroke-width="1.6"/><path d="M${-r * .25} ${-r * .1}a${r * .25} ${r * .25} 0 1 0 ${r * .5} 0" fill="none" stroke="rgba(120,30,40,.35)" stroke-width="1.4"/></g>`;
  const papel = (c1, c2) => `<path d="M30 58 60 112 90 58Z" fill="${c1}"/><path d="M30 58 48 70 60 112Z" fill="${c2}"/><path d="M52 92h16l-3 6h-10z" fill="#A9512F"/><path d="M60 94c-8-6-14-4-14 0s6 6 14 0c8 6 14 4 14 0s-6-6-14 0" fill="#C0392B" opacity=".85"/>`;
  const folhas = `<g fill="#5E8A5A"><path d="M34 58c-10-6-12-18-6-24 8 4 10 14 6 24Z"/><path d="M86 58c10-6 12-18 6-24-8 4-10 14-6 24Z"/></g>`;
  const vaso = (c) => `<path d="M38 82h44l-6 32H44z" fill="${c}"/><rect x="34" y="76" width="52" height="10" rx="3" fill="${c}" opacity=".85"/>`;
  const S = {
    rosas: folhas + rosa(48, 46, 11, '#E05A6A') + rosa(72, 46, 11, '#D94E60') + rosa(60, 34, 12, '#EF7A86') + rosa(60, 56, 10, '#C9455A') + papel('#F3E3D3', '#E6CDB5'),
    campo: folhas + '<g>' + [[44, 40, '#C9A7E8'], [60, 30, '#F8F2EA'], [76, 40, '#F2B5C4'], [52, 54, '#F7D774'], [70, 54, '#C9A7E8']].map(([x, y, c]) => `<g transform="translate(${x} ${y})">${[0, 72, 144, 216, 288].map((a) => `<ellipse cx="0" cy="-6" rx="4" ry="7" fill="${c}" transform="rotate(${a})"/>`).join('')}<circle r="3" fill="#B07F27"/></g>`).join('') + '</g>' + papel('#DDE8D6', '#C6D7BC'),
    girassol: folhas + [[44, 44], [76, 44], [60, 30]].map(([x, y]) => `<g transform="translate(${x} ${y})">${Array.from({ length: 12 }, (_, i) => `<ellipse cy="-10" rx="3.5" ry="7" fill="#F5C531" transform="rotate(${i * 30})"/>`).join('')}<circle r="7" fill="#6B4423"/></g>`).join('') + papel('#EADBC4', '#D9C3A3'),
    caixa: `<ellipse cx="60" cy="98" rx="38" ry="10" fill="#1F2B25"/><rect x="22" y="62" width="76" height="36" fill="#2A3A31"/><ellipse cx="60" cy="62" rx="38" ry="10" fill="#344A3D"/>` + rosa(44, 56, 10, '#E05A6A') + rosa(64, 54, 10, '#EF7A86') + rosa(82, 58, 9, '#D94E60') + rosa(54, 66, 9, '#C9455A') + rosa(74, 66, 9, '#E05A6A') + `<path d="M22 78h76" stroke="#C99A3C" stroke-width="3"/>`,
    orquidea: vaso('#F2EDE4') + `<path d="M60 78C58 50 66 36 80 30" stroke="#3E6046" stroke-width="2.5" fill="none"/><path d="M50 80c-14-2-20-10-18-16 10 0 16 6 18 16Zm20 0c14-2 20-10 18-16-10 0-16 6-18 16Z" fill="#4E7A4C"/>` + [[66, 44], [76, 34], [86, 30]].map(([x, y]) => `<g transform="translate(${x} ${y})">${[0, 72, 144, 216, 288].map((a) => `<ellipse cy="-5" rx="4.5" ry="6" fill="#F4F0FA" stroke="#D8C7EA" transform="rotate(${a})"/>`).join('')}<circle r="2.5" fill="#D9539A"/></g>`).join(''),
    suculentas: `<path d="M24 86h72l-4 26H28z" fill="#A9512F"/><rect x="20" y="80" width="80" height="9" rx="3" fill="#BF6440"/>` + [[38, 72, '#8DB59A'], [60, 68, '#A8C9B0'], [82, 72, '#9DBF8E']].map(([x, y, c]) => `<g transform="translate(${x} ${y})">${[0, 60, 120, 180, 240, 300].map((a) => `<ellipse cy="-7" rx="4" ry="8" fill="${c}" transform="rotate(${a})"/>`).join('')}<circle r="3" fill="#C7DFC9"/></g>`).join(''),
    cesta: `<path d="M24 66h72l-8 44H32z" fill="#C49A6C"/><path d="M28 74h64M30 86h60M32 98h56" stroke="#A67C4E" stroke-width="2"/><path d="M34 66c0-30 52-30 52 0" stroke="#A67C4E" stroke-width="4" fill="none"/>` + rosa(46, 58, 9, '#E05A6A') + rosa(62, 54, 10, '#EF7A86') + `<rect x="70" y="40" width="10" height="26" rx="3" fill="#2F4A35"/><rect x="72" y="34" width="6" height="8" fill="#C99A3C"/><circle cx="84" cy="60" r="6" fill="#6B4423"/>`,
    folhagem: vaso('#A9512F') + `<path d="M60 78V30M60 78C56 58 46 46 34 40M60 78c4-20 14-32 26-38" stroke="#2F4A35" stroke-width="2.5" fill="none"/><path d="M34 40c-12 2-16 14-12 22 10-2 14-12 12-22Zm52 0c12 2 16 14 12 22-10-2-14-12-12-22ZM60 30c-10-6-10-16 0-20 10 4 10 14 0 20Z" fill="#5E8A5A"/><path d="M50 62c-14 0-18 8-16 14 10 0 14-6 16-14Zm20 0c14 0 18 8 16 14-10 0-14-6-16-14Z" fill="#4E7A4C"/>`,
    lirio: vaso('#F2EDE4') + `<path d="M48 80c-12-8-16-24-10-32 8 6 12 18 10 32Zm24 0c12-8 16-24 10-32-8 6-12 18-10 32ZM60 80c-6-14-6-28 0-36 6 8 6 22 0 36Z" fill="#3E6046"/><path d="M60 46V26" stroke="#3E6046" stroke-width="2"/><path d="M60 14c-9 6-9 18 0 22 9-4 9-16 0-22Z" fill="#FBFBF7" stroke="#DCDCD0"/><rect x="58.5" y="20" width="3" height="12" rx="1.5" fill="#F2D27A"/>`,
  };
  window.CJ.SPRITE = `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>${Object.entries(S).map(([k, v]) => `<symbol id="il-${k}" viewBox="0 0 120 120">${v}</symbol>`).join('')}</defs></svg>`;
})();
