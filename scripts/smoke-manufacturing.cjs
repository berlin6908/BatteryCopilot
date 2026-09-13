const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const page = await browser.newPage({ viewport: { width: 1512, height: 1100 } });
  page.setDefaultTimeout(30000);
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  const output = path.join(__dirname, '../data/runs/browser');
  fs.mkdirSync(output, { recursive: true });
  await page.goto(process.env.BASE_URL || 'http://127.0.0.1:8000');
  await page.getByText('1 · 制造履历', { exact: true }).waitFor();
  await page.getByText('2 · 循环测试记录', { exact: true }).waitFor();
  await page.waitForTimeout(1200);
  await page.screenshot({ path: path.join(output, 'manufacturing-workbench.png') });
  await page.getByRole('button', { name: '第 10 行', exact: true }).click();
  await page.getByText('来源属性 / 测试原始行', { exact: true }).waitFor();
  await page.screenshot({ path: path.join(output, 'manufacturing-source.png') });
  await page.getByRole('button', { name: '关闭证据' }).click();
  await page.getByRole('button', { name: '下一页循环', exact: true }).click();
  await page.getByRole('button', { name: '上一页循环', exact: true }).click();
  const result = { flows: ['cell selection', 'manufacturing trace', 'original cycle row', 'cycle paging'], errors };
  if (process.env.LIVE_AGENT === '1') {
    const response = page.waitForResponse(r => r.url().endsWith('/api/manufacturing/reports') &&
      r.request().method() === 'POST', { timeout: 600000 });
    await page.getByRole('button', { name: '生成制造复核报告', exact: true }).click();
    const events = (await (await response).text()).trim().split('\n').map(JSON.parse);
    const answer = events.find(e => e.type === 'answer');
    if (!answer?.report_id) throw new Error(JSON.stringify(events.at(-1)));
    fs.writeFileSync(path.join(output, 'manufacturing-agent-events.json'), JSON.stringify(events, null, 2));
    await page.getByText('人工复核', { exact: true }).waitFor();
    await page.reload();
    await page.getByText('1 · 制造履历', { exact: true }).waitFor();
    // A saved report is selected through the same history control the user uses.
    await page.getByRole('button', { name: '已保存报告', exact: true }).click();
    await page.getByRole('menuitem').filter({ hasText: answer.summary }).first().click();
    await page.getByText('人工复核', { exact: true }).waitFor();
    if (process.env.TEST_REVIEW === '1') {
      await page.getByRole('textbox', { name: '复核人', exact: true }).fill('automated browser test');
      await page.getByRole('textbox', { name: '复核意见', exact: true }).fill('自动化流程验收：需补测试条件，不构成工程师验收。');
      await page.getByRole('button', { name: '保存人工复核', exact: true }).click();
      await page.getByText('自动化流程验收：需补测试条件，不构成工程师验收。', { exact: false }).waitFor();
      result.flows.push('test-labelled manual review form');
    }
    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('button', { name: '导出含来源的 Markdown 报告', exact: true }).click();
    const download = await downloadPromise;
    await download.saveAs(path.join(output, 'manufacturing-report.md'));
    const markdown = fs.readFileSync(path.join(output, 'manufacturing-report.md'), 'utf8');
    if (!markdown.includes('来源快照') || !markdown.includes('AH-OUT')) throw new Error('Incomplete export');
    result.flows.push('live Agent report', 'report persistence', 'source snapshot export');
    await page.mouse.move(1050, 850);
    await page.mouse.wheel(0, 2300);
    await page.waitForTimeout(900);
    await page.screenshot({ path: path.join(output, 'manufacturing-report.png') });
    result.agent = { report_id: answer.report_id, seconds: answer.seconds, usage: answer.usage };
  }
  fs.writeFileSync(path.join(output, 'manufacturing-check.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result));
  await browser.close();
  if (errors.length) process.exitCode = 1;
})().catch(e => { console.error(e); process.exit(1); });
