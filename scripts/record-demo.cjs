// Run against an isolated demo database: this creates a real report and demo review.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const base = process.env.BASE_URL || 'http://127.0.0.1:18000';
  const fast = process.env.DEMO_FAST === '1';
  const output = path.resolve('data/runs/demo');
  fs.mkdirSync(output, { recursive: true });
  const question = '用三条结论追溯当前电芯的明确前驱和制造工序，核对 Cycle 1 的充放电容量，说明缺失哪些资料、现在能否作质量判定。每条结论给出来源。';
  let events;
  const eventsFile = path.join(output, 'agent-events.json');
  if (process.env.DEMO_REUSE_REPORT === '1') {
    events = JSON.parse(fs.readFileSync(eventsFile, 'utf8'));
  } else {
    const catalogue = await (await fetch(`${base}/api/manufacturing/cells`)).json();
    const response = await fetch(`${base}/api/manufacturing/reports`, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ cell_uid: catalogue.cells[0].cell.uid, question }),
    });
    events = (await response.text()).trim().split('\n').map(JSON.parse);
    fs.writeFileSync(eventsFile, JSON.stringify(events, null, 2));
  }
  const answer = events.find(e => e.type === 'answer');
  if (!answer?.report_id) throw new Error(JSON.stringify(events.at(-1)));
  console.log(JSON.stringify({ report_id: answer.report_id, generation_seconds: answer.seconds }));

  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    recordVideo: { dir: output, size: { width: 1440, height: 900 } },
  });
  const page = await context.newPage();
  page.setDefaultTimeout(30000);
  const errors = [], chapters = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  const start = Date.now();
  const elapsed = () => (Date.now() - start) / 1000;
  async function chapter(at, text) {
    if (!fast) await page.waitForTimeout(Math.max(0, at * 1000 - (Date.now() - start)));
    chapters.push({ start: elapsed(), text });
    console.log(text);
  }
  async function focus(locator) {
    await page.mouse.move(1100, 600);
    for (let attempt = 0; attempt < 20; attempt++) {
      const box = await locator.boundingBox();
      if (!box) throw new Error('Demo target is absent');
      if (box.y >= 70 && box.y + box.height < 895) return;
      await page.mouse.wheel(0, Math.max(-900, Math.min(900, box.y - 350)));
      await page.waitForTimeout(250);
    }
    await page.screenshot({ path: path.join(output, 'scroll-failure.png') });
    throw new Error(`Could not scroll to ${locator}: ${JSON.stringify(await locator.boundingBox())}`);
  }
  await page.goto(base);
  await page.getByText('1 · 制造履历', { exact: true }).waitFor();
  await chapter(0, 'Battery Engineering Copilot｜制造资料复核 Agent\n公开 KIproBatt 实验室数据；演示对象有原始制造和循环记录');
  await chapter(15, '01 / 追溯制造履历\n展开工序，核对属于当前对象的参数与明确前驱');
  const filling = page.getByRole('button', { name: /Filling Protocol.*→/ }).first();
  await focus(filling);
  await filling.click();
  await page.screenshot({ path: path.join(output, 'trace.png') });
  await chapter(35, '02 / 回到原始测试行\nCycle 1 的放电容量 0.438290374336 Ah，来自文件第 11 行');
  const cycleSource = page.getByRole('button', { name: '第 11 行', exact: true });
  await focus(cycleSource);
  await cycleSource.click();
  await page.getByText('来源属性 / 测试原始行', { exact: true }).waitFor();
  await page.screenshot({ path: path.join(output, 'cycle-source.png') });
  await chapter(55, '03 / 查看真实 Agent 报告\n此报告在录屏前通过模型生成；录屏展示保存结果，不展示生成耗时');
  await page.getByRole('button', { name: '关闭证据' }).click();
  await focus(page.getByRole('button', { name: '已保存报告', exact: true }));
  await page.getByRole('button', { name: '已保存报告', exact: true }).click();
  await page.getByRole('menuitem', { name: answer.summary }).first().click();
  await chapter(75, 'Agent 按问题选择履历、参数和循环查询\n结论带来源；对象范围、原始数值由领域工具提供');
  await focus(page.getByRole('button', { name: '来源 1', exact: true }).first());
  await page.screenshot({ path: path.join(output, 'report.png') });
  await chapter(98, '04 / 核对结论引用\n打开报告保存时的来源快照，检查证据是否支持结论');
  await page.getByRole('button', { name: '来源 1', exact: true }).first().click();
  await page.getByText('来源属性 / 测试原始行', { exact: true }).waitFor();
  await chapter(116, '05 / 明确资料缺口\n追溯终点不等于制造起点；缺少测试条件和验收标准时保留判断');
  await page.getByRole('button', { name: '关闭证据' }).click();
  await focus(page.getByText('待补充资料', { exact: true }));
  await chapter(136, '06 / 保存人工复核意见\n这里填写“演示复核人”，结论为需补充资料');
  await focus(page.getByRole('textbox', { name: '复核人', exact: true }));
  await page.getByRole('textbox', { name: '复核人', exact: true }).fill('演示复核人');
  await page.getByRole('textbox', { name: '复核意见', exact: true }).fill('演示流程：已核对 Cycle 1 原始行，需补充测试条件与验收标准。此意见不是工程师验收。');
  const reviewButton = page.getByRole('button', { name: '保存人工复核', exact: true });
  await focus(reviewButton);
  const reviewResponse = page.waitForResponse(r => r.url().endsWith('/review') && r.request().method() === 'POST');
  await reviewButton.click();
  if (!(await reviewResponse).ok()) throw new Error('Review was not saved');
  await page.screenshot({ path: path.join(output, 'review.png') });
  await chapter(155, '07 / 刷新后继续处理\n从历史记录恢复报告与复核意见，资料不会随页面关闭丢失');
  await page.reload();
  await page.getByText('1 · 制造履历', { exact: true }).waitFor();
  await focus(page.getByRole('button', { name: '已保存报告', exact: true }));
  await page.getByRole('button', { name: '已保存报告', exact: true }).click();
  await page.getByRole('menuitem', { name: answer.summary }).first().click();
  await focus(page.getByText('人工复核', { exact: true }));
  await chapter(170, '08 / 导出复核报告与来源快照\n数据：KIproBatt v0.3.2，CC BY 4.0；完整作者署名与评测见仓库');
  const pendingDownload = page.waitForEvent('download');
  const exportButton = page.getByRole('button', { name: '导出含来源的 Markdown 报告', exact: true });
  await focus(exportButton);
  await exportButton.click();
  await (await pendingDownload).saveAs(path.join(output, 'report.md'));
  const markdown = fs.readFileSync(path.join(output, 'report.md'), 'utf8');
  if (!markdown.includes('AH-OUT') || !markdown.includes('演示复核人')) throw new Error('Incomplete report export');
  if (!fast) await page.waitForTimeout(Math.max(0, 180000 - (Date.now() - start)));
  await context.close();
  const video = await page.video().path();
  await browser.close();
  fs.writeFileSync(path.join(output, 'recording.json'), JSON.stringify({
    video, chapters, seconds: elapsed(), report_id: answer.report_id,
    generation_seconds: answer.seconds, errors,
  }, null, 2));
  if (errors.length) throw new Error(JSON.stringify(errors));
  console.log(JSON.stringify({ video, errors }));
})().catch(e => { console.error(e); process.exit(1); });
