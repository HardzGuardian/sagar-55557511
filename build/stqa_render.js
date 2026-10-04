const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const pg = await b.newPage();
  await pg.goto('file://' + __dirname + '/stqa_guide.html');
  await pg.pdf({ path: __dirname + '/../STQA_Exam_Answer_Guide.pdf', format: 'A4', printBackground: true,
    margin: { top: '16mm', bottom: '16mm', left: '14mm', right: '14mm' }, displayHeaderFooter: true,
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#777"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    headerTemplate: '<div style="font-size:9px;width:100%;text-align:right;color:#555;padding-right:14mm;font-family:Helvetica,Arial,sans-serif">Sagar Salunkhe</div>' });
  await b.close();
})();
