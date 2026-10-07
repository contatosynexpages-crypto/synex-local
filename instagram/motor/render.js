// Renderiza as peças em 2x, reduz para 1080x1350 e confere sobreposição/margens.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const dir = path.join(__dirname, 'html'), out = path.join(__dirname, 'out');
fs.mkdirSync(out, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  const only = process.argv[2];
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html') && (!only || f.startsWith(only))).sort()) {
    const p = await ctx.newPage();
    await p.goto('file://' + path.join(dir, f));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForFunction(() => document.body.dataset.ready === '1');
    await p.waitForTimeout(150);
    const issues = await p.evaluate(() => {
      const els = [...document.querySelectorAll('.t')].filter(e => e.getBoundingClientRect().width > 0 && e.textContent.trim() !== '' || e.tagName === 'svg');
      const R = els.map(e => { const r = e.getBoundingClientRect(); return { e, x0: r.left, y0: r.top, x1: r.right, y1: r.bottom, txt: (e.textContent || 'logo').trim().slice(0, 24) }; });
      const out = [];
      R.forEach(a => { if (a.x0 < 84 || a.x1 > 996 || a.y0 < 60 || a.y1 > 1300) out.push('FORA: ' + a.txt + ` [${a.x0|0},${a.y0|0},${a.x1|0},${a.y1|0}]`); });
      for (let i = 0; i < R.length; i++) for (let j = i + 1; j < R.length; j++) {
        const a = R[i], c = R[j];
        if (a.e.contains(c.e) || c.e.contains(a.e)) continue;
        if (a.x0 < c.x1 - 1 && c.x0 < a.x1 - 1 && a.y0 < c.y1 - 1 && c.y0 < a.y1 - 1) out.push('SOBREPÕE: "' + a.txt + '" x "' + c.txt + '"');
      }
      return out;
    });
    const png = path.join(out, f.replace('.html', '@2x.png'));
    await p.screenshot({ path: png });
    console.log(f, issues.length ? '\n  ' + issues.join('\n  ') : 'ok');
    await p.close();
  }
  await b.close();
})();
