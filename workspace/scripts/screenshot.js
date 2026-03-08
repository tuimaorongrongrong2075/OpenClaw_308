const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto(process.argv[2] || 'http://127.0.0.1:8888/kanban.html', { waitUntil: 'networkidle0' });
  await page.screenshot({ path: process.argv[3] || '/root/.openclaw/workspace/screenshot.png' });
  await browser.close();
  console.log('Screenshot saved!');
})();
