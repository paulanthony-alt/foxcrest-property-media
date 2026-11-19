// Renders the jobs written by build_brand.py into PNG/PDF files using Playwright.
const fs = require("fs");
const { chromium } = require("playwright");

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const browser = await chromium.launch();
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w || 2400, height: j.h || 1400 } });
    await page.setContent(j.html, { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    if (j.type === "pdf") {
      await page.pdf({ path: j.out, printBackground: true, preferCSSPageSize: true });
    } else if (j.selector) {
      await page.locator(j.selector).screenshot({ path: j.out, omitBackground: !!j.transparent });
    } else {
      await page.screenshot({ path: j.out, clip: { x: 0, y: 0, width: j.w, height: j.h } });
    }
    await page.close();
    console.log("wrote", j.out.split("/brand/")[1]);
  }
  await browser.close();
})();
