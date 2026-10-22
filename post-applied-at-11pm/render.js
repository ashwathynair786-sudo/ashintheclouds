// Renders index.html to post.png (1080×1350) and post@2x.png (2160×2700).
// Usage: node render.js   (needs Playwright + Chromium)
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const url = 'file://' + path.join(dir, 'index.html') + '?export';
  const browser = await chromium.launch();
  for (const [scale, name] of [[1, 'post.png'], [2, 'post@2x.png']]) {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: scale });
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await (await page.$('.post')).screenshot({ path: path.join(dir, name) });
    console.log('wrote', name);
    await page.close();
  }
  await browser.close();
})();
