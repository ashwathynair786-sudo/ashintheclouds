const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, out, scale] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1400 }, deviceScaleFactor: Number(scale||1) });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  const fams = await p.evaluate(() => [...document.fonts].map(f => f.family + ':' + f.status));
  console.log(fams.join(', '));
  const n = await p.locator('.slide').count();
  for (let i = 0; i < n; i++) {
    await p.locator('.slide').nth(i).screenshot({ path: path.join(out, `slide-0${i + 1}.png`) });
  }
  await b.close();
})();
