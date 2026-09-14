# 评测

项目分别评估制造资料核查、工艺指南检索和结构查询。各套题库的任务、划分与评分口径独立，
不合并为单一准确率。题库、来源、运行配置、失败及分项结果一同保留。

## 协议与结果

| 评测 | 范围 | 协议、结果与数据 |
| --- | --- | --- |
| 制造核查 v2 | 8 道回归题与 24 道同批次新对象题；比较无资料、固定查询和 Agent | [协议与修复验证](manufacturing-validation.md) · [题库及结果](../data/manufacturing-validation/) |
| 工艺指南 | 8 道原开发探针及 4 个新增意图的中英德表达，共 20 问；检查页命中、原文区域覆盖与引用稳定性 | [方法与结果](guide-validation.md) · [题库及结果](../data/guide-validation/) |
| 制造核查 v1 | 36 道来源核查案例，覆盖 12 个测试批次 | [协议](manufacturing-benchmark.md) · [结果](manufacturing-results.md) · [题库及结果](../data/manufacturing-benchmark/) |
| 历史综合评测 | 300 道结构、指南及模拟变更案例，60/240 开发测试划分 | [协议](benchmark-300.md) · [结果](benchmark-results.md) · [题库及结果](../data/benchmark/) |

制造 v2 的最终修复重放中，固定查询与 Agent 的字段及预设引用检查均为 24/24；
指南独立解析版本的原 8 问页命中为 8/8，新增 12 问页命中 10/12、原文区域命中 9/12。
这些是已查看问题后的修复验证。数据来源审查还发现过字段评分未捕捉到的归属或摘要错误，
具体运行版本、耗时、失败与限制见对应报告。

历史 300 题的指南成绩依赖原 703 元素解析快照，不能直接用于当前区域引用实现；
当前指南使用独立的页码和原文区域评测。

## 运行指南检索评测

完成 PDF 解析和检索索引后运行，不需要生成模型：

```powershell
$env:PYTHONUTF8 = '1'
uv run python -m battery_copilot.guide_evaluation --output data/runs/guide-validation.json
```

使用新的输出文件保留各次结果。制造评测的版本选择、执行参数和评分细节见[制造验证协议](manufacturing-validation.md)。

## 开发示例

需要完成数据导入和检索索引，模型评测还需要有效的模型配置。

### 示例题与对照

- `data/evaluation/retrieval.json`：8 个中英德检索示例，检查目标页是否进入前 6 条结果。
- `data/evaluation/tasks.json`：20 个结构题，参考答案由原始 CSV 直接计算。
- `data/evaluation/supplement.json`：10 个多跳、指南、资料缺失及模拟变更示例。
- A：固定混合检索；B：相同检索加固定图查询；C：Agent 自主选择领域工具。

这些是开发示例。对照的检索数量和模型调用次数不同，不能当成严格等预算实验。

```powershell
$env:PYTHONUTF8 = '1'
uv run python -m battery_copilot.evaluate --mode retrieval
uv run python -m battery_copilot.evaluate --mode cases
uv run python -m battery_copilot.evaluate --mode models --limit 3
```

默认模型结果写入新的 `data/evaluation/terra-<时间戳>/`，已有目录不会被覆盖。
显式指定任务、方案和目录：

```powershell
uv run python -m battery_copilot.evaluate --mode models --cases data/evaluation/supplement.json --limit 10 --variants C --workers 2 --output data/evaluation/supplement-run
```

### 结果与评分

每次模型运行保存 `manifest.json` 和 `results.jsonl`，包含配置、源文件哈希、实际证据、
工具调用、回答、失败、用量与耗时。生成结果由 Git 忽略。

自动检查区分回答是否返回、引用 ID 是否来自已取回证据、题目要求的对象引用是否覆盖。
引用存在不能证明结论正确；任务完整性和语义支持需要对照原始资料逐项复核。

在运行目录创建 `review.json`，为每个任务和方案填写一项。以下为格式示例，不代表实际评分：

```json
{
  "reviewer": "复核人及方法",
  "items": [
    {
      "case_id": "counts-1",
      "variant": "A",
      "task_pass": false,
      "claims_supported": [true, false],
      "reason": "说明任务完整性，以及逐条结论与证据的对应关系"
    }
  ]
}
```

`claims_supported` 按返回的结论顺序逐条填写；没有返回结论时使用空数组。
必须覆盖全部尝试，包括失败任务，才可生成汇总：

```powershell
uv run python scripts/summarize-evaluation.py data/evaluation/supplement-run
```

程序分别统计任务通过、引用覆盖、结论支持、耗时和用量。失败任务保留在成功率分母，
缺失用量不按零计算。Codex CLI 输入包含自身上下文，不直接等于 API 账单费用。

## 功能检查

`backend/tests/test_cases.py` 使用实际 Neo4j 和替代模型结果，验证正常完成、缺资料后补充、
冲突修正、旧报告失效、过期提交、模型失败后重试，以及迟到分析不覆盖新输入。
`backend/tests/test_agent.py` 通过实际工具循环验证缺失引用收到反馈后补读，以及统计总数的确定性计算。

`LIVE_AGENT=1` 下的浏览器检查使用实际配置的模型，完成三种申请的端到端流程；
缺资料和冲突各包含修改后的第二次分析，并验证人工复核、报告下载和刷新后的持久化。
这是少量场景的功能验收，不能作为业务准确率或跨场景泛化能力的 benchmark。
运行命令见[开发文档](development.md)，已执行的环境与流程见[v0.1.0 验证记录](validation.md)。
