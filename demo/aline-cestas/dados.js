/* Dados compartilhados da loja e do painel da Aline Cestas (prévia).
   Na versão real, isto vem do banco de dados e a Aline edita pelo painel. */
window.CJ = (function () {
  'use strict';
  const PRODUTOS = [
    { id: 'cafe-simples', cat: 'cafe', nome: 'Café da manhã clássico', desc: 'Pães, bolo caseiro, frios, frutas, suco e café na cesta de vime.', ilus: 'cafe',
      opcoes: [{ id: '1', nome: 'Para 1 pessoa', preco: 139 }, { id: '2', nome: 'Para 2 pessoas', preco: 199 }] },
    { id: 'cafe-completo', cat: 'cafe', nome: 'Café da manhã completo', desc: 'O clássico com croissant, iogurte, granola, geleias e chocolate.', ilus: 'cafe',
      opcoes: [{ id: '2', nome: 'Para 2 pessoas', preco: 259 }, { id: '4', nome: 'Para 4 pessoas', preco: 369 }] },
    { id: 'cafe-flores', cat: 'cafe', nome: 'Café da manhã com flores', desc: 'Café completo para 2 com mini buquê de rosas.', ilus: 'flores',
      opcoes: [{ id: 'u', nome: 'Para 2 pessoas', preco: 299 }] },
    { id: 'aniversario', cat: 'datas', nome: 'Cesta de aniversário', desc: 'Bolo de pote, docinhos, espumante sem álcool e balão.', ilus: 'aniversario',
      opcoes: [{ id: 'u', nome: 'Completa', preco: 189 }] },
    { id: 'romantica', cat: 'datas', nome: 'Cesta romântica', desc: 'Espumante, taças, chocolates finos e pelúcia.', ilus: 'romantica',
      opcoes: [{ id: 'u', nome: 'Completa', preco: 239 }] },
    { id: 'maternidade', cat: 'datas', nome: 'Cesta maternidade', desc: 'Mimos para a mamãe e o bebê, com lembrança personalizada.', ilus: 'maternidade',
      opcoes: [{ id: 'u', nome: 'Completa', preco: 219 }] },
    { id: 'chocolates', cat: 'chocolates', nome: 'Cesta de chocolates', desc: 'Bombons, barras e trufas selecionados.', ilus: 'chocolate',
      opcoes: [{ id: 'p', nome: 'Pequena', preco: 129 }, { id: 'g', nome: 'Grande', preco: 199 }] },
    { id: 'caneca', cat: 'chocolates', nome: 'Caneca recheada', desc: 'Caneca com bombons e cartãozinho. Mimo rápido e certeiro.', ilus: 'caneca',
      opcoes: [{ id: 'u', nome: 'Caneca 300 ml', preco: 69 }] },
    { id: 'happy', cat: 'happy', nome: 'Cesta happy hour', desc: 'Cervejas especiais, petiscos e amendoim. Ideal para eles.', ilus: 'happy',
      opcoes: [{ id: 'u', nome: 'Completa', preco: 179 }] },
    { id: 'happy-vinho', cat: 'happy', nome: 'Kit vinho & queijos', desc: 'Vinho tinto, queijos, torradas e tábua de madeira.', ilus: 'vinho',
      opcoes: [{ id: 'u', nome: 'Completo', preco: 229 }] },
  ];
  const EXTRAS = [
    { id: 'balao', nome: 'Balão metalizado', preco: 25 },
    { id: 'pelucia', nome: 'Pelúcia de urso', preco: 49 },
    { id: 'buque', nome: 'Mini buquê de rosas', preco: 45 },
  ];
  const CATEGORIAS = [
    { id: 'todos', nome: 'Tudo' }, { id: 'cafe', nome: 'Café da manhã' }, { id: 'datas', nome: 'Datas especiais' },
    { id: 'chocolates', nome: 'Chocolates' }, { id: 'happy', nome: 'Happy hour' },
  ];
  // taxas de exemplo (a loja define as reais no painel)
  const BAIRROS = [
    { nome: 'Jardim Ribamar', taxa: 8 }, { nome: 'Centro', taxa: 10 }, { nome: 'Cidade Nova Peruíbe', taxa: 10 },
    { nome: 'Jardim Peruíbe', taxa: 10 }, { nome: 'Stella Maris', taxa: 12 }, { nome: 'Oásis', taxa: 15 },
    { nome: 'Balneário Três Marias', taxa: 15 }, { nome: 'Caraguava', taxa: 18 }, { nome: 'Guaraú', taxa: 25 },
  ];
  // corte = até que hora dá para pedir para o mesmo dia (null = só a partir de amanhã) · sabado = existe no sábado
  const PERIODOS = [
    { id: 'cedo', nome: 'Bem cedinho', faixa: '7h às 9h', corte: null, sabado: true },
    { id: 'manha', nome: 'Manhã', faixa: '9h às 12h', corte: 8, sabado: true },
    { id: 'tarde', nome: 'Tarde', faixa: '13h às 18h30', corte: 14, sabado: false },
  ];
  const LOJA = { nome: 'Aline Cestas & Presentes', endereco: 'R. Rui Barbosa, 1619 · Jardim Ribamar', whats: '5513997101930' };

  const brl = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  const ler = (k, padrao) => { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : padrao; } catch (e) { return padrao; } };
  const gravar = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* sem armazenamento: segue só na memória */ } };
  function agoraSP() {
    const p = Object.fromEntries(new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo', year: 'numeric', month: '2-digit', day: '2-digit', hour: 'numeric', minute: 'numeric', hourCycle: 'h23' }).formatToParts(new Date()).map((x) => [x.type, x.value]));
    return { data: `${p.year}-${p.month}-${p.day}`, hora: Number(p.hour) + Number(p.minute) / 60 };
  }
  const somarDias = (iso, n) => { const d = new Date(iso + 'T12:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
  const diaSemana = (iso) => new Date(iso + 'T12:00:00Z').getUTCDay();

  return { PRODUTOS, EXTRAS, CATEGORIAS, BAIRROS, PERIODOS, LOJA, brl, ler, gravar, agoraSP, somarDias, diaSemana,
    CHAVE_PEDIDOS: 'al-pedidos', CHAVE_ESGOTADOS: 'al-esgotados', CHAVE_SACOLA: 'al-sacola' };
})();

/* Ilustrações próprias das cestas (substituídas pelas fotos reais na versão final) */
(function () {
  const cesta = (dentro) => `<ellipse cx="60" cy="108" rx="44" ry="6" fill="rgba(58,42,32,.12)"/><path d="M28 56c0-30 64-30 64 0" stroke="#8E6A48" stroke-width="5" fill="none"/>${dentro}<path d="M18 64h84l-10 42H28z" fill="#C9A27E"/><path d="M22 74h76M25 86h70M27 98h66" stroke="#A9825E" stroke-width="2.5"/><path d="M40 64v42M60 64v42M80 64v42" stroke="#B48F6A" stroke-width="1.5" opacity=".7"/><rect x="14" y="60" width="92" height="8" rx="4" fill="#B48F6A"/><path d="M56 64c-8-8-18-6-16 0s10 6 16 0c6 6 14 6 16 0s-8-8-16 0" fill="#8E2441"/>`;
  const garrafa = (x, c, tampa = '#C9A027') => `<rect x="${x}" y="24" width="12" height="40" rx="4" fill="${c}"/><rect x="${x + 3}" y="16" width="6" height="10" fill="${tampa}"/>`;
  const rosa = (x, y, r, c) => `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/><path d="M${x - r / 2} ${y}a${r / 2} ${r / 2} 0 1 1 ${r} 0" fill="none" stroke="rgba(110,26,50,.35)" stroke-width="1.5"/>`;
  const S = {
    cafe: cesta(`${garrafa(70, '#F2A33A')}<path d="M30 60c2-12 22-12 24 0Z" fill="#E3B26B"/><path d="M34 58c4-4 12-4 16 0" stroke="#C8904A" stroke-width="2" fill="none"/><circle cx="58" cy="54" r="8" fill="#D9473B"/><circle cx="89" cy="56" r="7" fill="#F5C531"/><rect x="44" y="40" width="14" height="22" rx="3" fill="#FFF9F1" stroke="#C9A27E"/><path d="M58 46h4a4 4 0 0 1 0 8h-4" stroke="#C9A27E" stroke-width="2" fill="none"/>`),
    flores: cesta(`${rosa(40, 44, 9, '#E05A6A')}${rosa(54, 36, 10, '#EF7A86')}${rosa(46, 56, 8, '#C9455A')}<path d="M32 50c-8-2-10-10-6-14 6 2 8 8 6 14Z" fill="#4E6E44"/>${garrafa(74, '#F2A33A')}<path d="M62 60c2-10 16-10 18 0Z" fill="#E3B26B"/>`),
    aniversario: cesta(`<rect x="34" y="40" width="22" height="22" rx="3" fill="#FBE3E3" stroke="#E8A9A6"/><path d="M34 48h22" stroke="#8E2441" stroke-width="3"/><path d="M45 40v-8" stroke="#3A2A20" stroke-width="2"/><path d="M45 26c-3 3-3 6 0 7 3-1 3-4 0-7Z" fill="#F5A623"/>${garrafa(62, '#F7E7B4', '#B8B8B8')}<ellipse cx="88" cy="22" rx="12" ry="14" fill="#E05A6A"/><path d="M88 36c-2 8 4 14 0 24" stroke="#8E6A48" stroke-width="1.5" fill="none"/>`),
    romantica: cesta(`${garrafa(40, '#2F4A35')}<path d="M58 30h12l-2 14a4 4 0 0 1-8 0Z" fill="#FFF9F1" stroke="#C9A27E"/><path d="M64 48v12" stroke="#C9A27E" stroke-width="2"/><path d="M84 40c-6-8-16-2-10 6l10 10 10-10c6-8-4-14-10-6Z" fill="#8E2441"/><circle cx="30" cy="58" r="6" fill="#6B4423"/>`),
    maternidade: cesta(`<path d="M34 34h20l6 8-6 4v18H34V46l-6-4Z" fill="#CFE3F2"/><circle cx="76" cy="44" r="9" fill="#C9A27E"/><circle cx="70" cy="36" r="4" fill="#C9A27E"/><circle cx="82" cy="36" r="4" fill="#C9A27E"/><ellipse cx="76" cy="58" rx="11" ry="8" fill="#C9A27E"/><circle cx="73" cy="43" r="1.3" fill="#3A2A20"/><circle cx="79" cy="43" r="1.3" fill="#3A2A20"/>`),
    chocolate: cesta(`<rect x="30" y="36" width="26" height="26" rx="3" fill="#6B4423" transform="rotate(-8 43 49)"/><path d="M34 44h20M34 52h20" stroke="#8B5A33" stroke-width="2" transform="rotate(-8 43 49)"/><rect x="60" y="30" width="30" height="34" rx="4" fill="#8E2441"/><path d="M60 46h30M75 30v34" stroke="#C9A027" stroke-width="3"/><circle cx="40" cy="62" r="5" fill="#C9A027"/><circle cx="52" cy="62" r="5" fill="#6B4423"/>`),
    caneca: `<ellipse cx="60" cy="106" rx="34" ry="6" fill="rgba(58,42,32,.12)"/><circle cx="48" cy="40" r="8" fill="#C9A027"/><circle cx="62" cy="36" r="8" fill="#6B4423"/><circle cx="74" cy="42" r="8" fill="#8E2441"/><path d="M34 46h52v48a10 10 0 0 1-10 10H44a10 10 0 0 1-10-10Z" fill="#FFF9F1" stroke="#C9A27E" stroke-width="2"/><path d="M86 56h6a10 10 0 0 1 0 20h-6" stroke="#C9A27E" stroke-width="5" fill="none"/><path d="M60 82c-4-5-11-1-7 4l7 6 7-6c4-5-3-9-7-4Z" fill="#E05A6A"/>`,
    happy: cesta(`${garrafa(32, '#8E5A1F')}${garrafa(48, '#6E4416')}${garrafa(64, '#8E5A1F')}<path d="M80 62c0-12 20-12 20 0Z" fill="#E3B26B"/><circle cx="86" cy="54" r="2" fill="#B87C3A"/><circle cx="93" cy="56" r="2" fill="#B87C3A"/>`),
    vinho: cesta(`<rect x="34" y="18" width="13" height="46" rx="5" fill="#5A1428"/><rect x="37" y="10" width="7" height="10" fill="#3A2A20"/><rect x="34" y="38" width="13" height="12" fill="#FBF3E8"/><path d="M56 50h26l4 10H52Z" fill="#F2C94C"/><circle cx="64" cy="55" r="2" fill="#E0B23A"/><path d="M84 40l14 2-2 18-14-2Z" fill="#B48F6A"/>`),
  };
  window.CJ.SPRITE = `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>${Object.entries(S).map(([k, v]) => `<symbol id="il-${k}" viewBox="0 0 120 120">${v}</symbol>`).join('')}</defs></svg>`;
})();
