// Live browser acceptance: five change analyses use the configured model.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

async function checkCases(page, output) {
  const results = [];
  const click = name => page.getByRole('button', { name, exact: true }).click();
  async function mutation(suffix, trigger) {
    const response = page.waitForResponse(r => r.request().method() !== 'GET' && r.url().endsWith(suffix), { timeout: 600000 });
    await trigger();
    const data = await response;
    assert.equal(data.status(), 200, await data.text());
    const value = await data.json();
    await page.getByRole('button', { name: '新建申请', exact: true }).waitFor({ state: 'visible' });
    await page.waitForFunction(() => !document.querySelector('[role="progressbar"]'), null, { timeout: 10000 });
    return value;
  }
  async function analyze() {
    const value = await mutation('/analyze', () => click('分析当前资料'));
    assert.equal(value.analysis_status, 'succeeded', value.last_error);
    assert(value.reports.at(-1).answer.claims.length > 0);
    console.log(JSON.stringify({ case: value.id, title: value.input.title, status: value.status, answer: value.reports.at(-1).answer.run_id }));
    return value;
  }
  for (const [preset, expected] of [['正常示例', 'pass'], ['缺资料示例', 'missing'], ['冲突示例', 'conflict']]) {
    await click('新建申请');
    await click(preset);
    let saved = await mutation('/api/cases', () => click('保存申请'));
    assert.equal(saved.status, 'draft');
    // Reload proves inputs are on the server, independent of Flutter widget state.
    await page.reload();
    await click('变更复核');
    await page.getByText(saved.input.title, { exact: true }).last().waitFor();
    saved = await analyze();
    assert.equal(saved.reports.at(-1).findings[0].status, expected);
    assert.equal(saved.status, expected === 'missing' ? 'awaiting_information' : 'awaiting_review');
    assert.equal(await page.getByRole('button', { name: '完成变更单', exact: true }).isEnabled(), false);
    await page.screenshot({ path: path.join(output, `case-${expected}.png`), fullPage: true });
    const attempts = [saved.reports.at(-1).answer];
    if (expected !== 'pass') {
      await click('补充或修改资料');
      if (expected === 'missing') await page.getByRole('switch', { name: '已提供工具卡', exact: true }).click();
      await page.getByRole('textbox', { name: '支持规格（逗号分隔）', exact: true }).fill('M6, M8');
      await page.getByRole('textbox', { name: '工具卡版次', exact: true }).fill('B');
      saved = await mutation(`/api/cases/${saved.id}`, () => click('保存申请'));
      assert.equal(saved.current_report_id, null);
      saved = await analyze();
      assert.equal(saved.reports.length, 2);
      assert.equal(saved.reports[0].findings[0].status, expected);
      assert(saved.reports.at(-1).findings.every(f => f.status === 'pass'));
      attempts.push(saved.reports.at(-1).answer);
    }
    await page.getByRole('checkbox', { name: `change:${saved.id}:v${saved.input_version}:request 模拟变更申请`, exact: true }).first().click();
    await page.getByText(`${saved.id} / 输入版本 ${saved.input_version}`, { exact: true }).waitFor();
    await click('关闭证据');
    for (const title of ['工具规格适配', '作业指导书同步', '关联对象清单']) {
      await click(`复核${title}`);
      await page.getByRole('textbox', { name: '复核人', exact: true }).fill('演示复核人');
      await page.getByRole('textbox', { name: '复核意见', exact: true }).fill(`已对照当前输入和来源核对${title}。`);
      saved = await mutation('/review', () => click('确认复核'));
    }
    saved = await mutation('/complete', () => click('完成变更单'));
    assert.equal(saved.status, 'completed');
    const downloadEvent = page.waitForEvent('download');
    await click('导出报告');
    const download = await downloadEvent;
    const exportPath = path.join(output, download.suggestedFilename());
    await download.saveAs(exportPath);
    const exported = fs.readFileSync(exportPath, 'utf8');
    assert(exported.includes('状态：已完成') && exported.includes('演示复核人'));
    await page.reload();
    await click('变更复核');
    await page.getByRole('button', { name: '变更单已完成', exact: true }).waitFor();
    await page.screenshot({ path: path.join(output, `case-${expected}-completed.png`), fullPage: true });
    results.push({ id: saved.id, initial_finding: expected, reports: saved.reports.length, completed: true,
      attempts: attempts.map(a => ({ run_id: a.run_id, seconds: a.seconds, usage: a.usage })) });
  }
  return results;
}

module.exports = { checkCases };
