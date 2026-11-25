// Usage: node render.js [scale]  -> responsibility-post-v2.png
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: Number(process.argv[2] || 1) });
  await p.goto('file://' + path.join(__dirname, 'post.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await (await p.$('.slide')).screenshot({ path: path.join(__dirname, 'responsibility-post-v2.png') });
  await b.close();
})();
