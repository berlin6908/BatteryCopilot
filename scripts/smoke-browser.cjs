const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const page = await browser.newPage({ viewport: { width: 1512, height: 1100 } });
  const errors = [];
  page.on('pageerror', error => { errors.push(error.message); console.error(error.message); });
  page.on('console', message => { if (message.type() === 'error') { errors.push(message.text()); console.error(message.text()); } });
  const output = path.join(__dirname, '../data/runs/browser');
  fs.mkdirSync(output, { recursive: true });
  await page.goto('http://127.0.0.1:8000');
  await page.getByRole('button', { name: '结构与记录', exact: true }).click();
  await page.getByRole('button', { name: '查看当前对象证据', exact: true }).waitFor();
  await page.getByRole('button', { name: /^screw 1000/ }).waitFor();
  await page.waitForTimeout(1200);
  console.log('Graph node bounds:', await page.getByRole('button', { name: /^screw 1000/ }).boundingBox());
  await page.screenshot({ path: path.join(output, 'workbench-final.png') });
  await page.getByRole('button', { name: /^screw 1000/ }).click();
  await page.getByText('原始 CSV 行', { exact: true }).waitFor();
  await page.waitForTimeout(350);
  await page.screenshot({ path: path.join(output, 'csv-evidence.png') });
  await page.getByRole('button', { name: '关闭证据' }).click();
  await page.getByRole('button', { name: '工艺证据', exact: true }).click();
  await page.getByRole('button', { name: /第 18 页.*Mounting the modules/ }).first().waitFor();
  await page.getByRole('button', { name: /第 18 页.*Mounting the modules/ }).first().click();
  await page.getByRole('button', { name: '关闭证据' }).waitFor();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(output, 'pdf-evidence.png') });
  await page.getByRole('button', { name: '关闭证据' }).click();
  await page.getByRole('button', { name: '变更复核', exact: true }).click();
  await page.getByRole('button', { name: '新建申请', exact: true }).waitFor();
  const result = { browser: 'Edge', viewport: '1512x1100',
    flows: ['graph overview', 'CSV provenance', 'PDF page/bbox', 'saved change workbench'], errors };
  if (process.env.LIVE_AGENT === '1') {
    const { checkCases } = require('./smoke-cases.cjs');
    result.cases = await checkCases(page, output);
    await page.getByRole('button', { name: '结构与记录', exact: true }).click();
    await page.getByRole('button', { name: '螺钉 1000 连接哪些部件，如何拆除？', exact: true }).click();
    const response = page.waitForResponse(r => r.url().endsWith('/api/agent/run'));
    await page.getByRole('button', { name: '运行', exact: true }).click();
    const events = (await (await response).text()).trim().split('\n').map(JSON.parse);
    const answer = events.find(e => e.type === 'answer');
    if (!answer) throw new Error(JSON.stringify(events));
    if (!answer.claims.flatMap(c => c.evidence_ids).includes('kit-v1:fixation:1000')) {
      throw new Error('Missing screw citation');
    }
    const citation = page.getByLabel('kit-v1:fixation:1000', { exact: true }).first();
    await citation.scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(output, 'agent-answer.png') });
    await citation.click();
    await page.getByText('原始 CSV 行', { exact: true }).waitFor();
    await page.waitForTimeout(350);
    await page.screenshot({ path: path.join(output, 'agent-citation.png') });
    result.flows.push('live Agent tool loop', 'answer citation opens CSV');
    result.agent = { run_id: answer.run_id, seconds: answer.seconds, usage: answer.usage };
  }
  fs.writeFileSync(path.join(output, 'browser-check.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result));
  await browser.close();
  if (errors.length) process.exitCode = 1;
})().catch(error => { console.error(error); process.exit(1); });
