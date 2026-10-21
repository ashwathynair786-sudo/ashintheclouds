// Renders index.html to slide-01..05.png (1080×1350) and carousel.pdf.
// Usage: node render.js   (needs Playwright + Chromium)
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const url = 'file://' + path.join(dir, 'index.html') + '?export';
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  // Fail loudly if any slide's content pushes the footer past the safe area
  const overflow = await page.$$eval('.slide', els => els.map(el => {
    const foot = el.querySelector('.chrome-bottom').getBoundingClientRect();
    const box = el.getBoundingClientRect();
    return box.bottom - foot.bottom < 80 ? el.dataset.n : null;
  }).filter(Boolean));
  if (overflow.length) console.warn('WARNING: content overflows on slide(s)', overflow.join(', '));

  const slides = await page.$$('.slide');
  for (let i = 0; i < slides.length; i++) {
    const file = path.join(dir, `slide-${String(i + 1).padStart(2, '0')}.png`);
    await slides[i].screenshot({ path: file });
    console.log('wrote', path.basename(file));
  }

  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: path.join(dir, 'carousel.pdf'), width: '1080px', height: '1350px', printBackground: true, preferCSSPageSize: true });
  console.log('wrote carousel.pdf');
  await browser.close();
})();
