// Renders each .slide in carousel.html to slide-0N.png. Usage: node render.js [scale]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = __dirname;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1400 }, deviceScaleFactor: Number(process.argv[2] || 1) });
  await p.goto('file://' + path.join(dir, 'carousel.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  const s = await p.$$('.slide');
  for (let i = 0; i < s.length; i++) await s[i].screenshot({ path: path.join(dir, `slide-0${i + 1}.png`) });
  await b.close();
})();
