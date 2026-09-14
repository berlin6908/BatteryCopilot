# 评测执行说明

完整题库及三方案测试使用 [300 案例协议](benchmark-300.md)。下列命令保留为开发示例检查。

需要完成数据导入和检索索引，模型评测还需要有效的模型配置。

## 示例题与对照

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

## 结果与评分

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

## 业务流程验收

`backend/tests/test_cases.py` 使用实际 Neo4j 和替代模型结果，验证正常完成、缺资料后补充、
冲突修正、旧报告失效、过期提交、模型失败后重试，以及迟到分析不覆盖新输入。
`backend/tests/test_agent.py` 通过实际工具循环验证缺失引用收到反馈后补读，以及统计总数的确定性计算。

`LIVE_AGENT=1` 下的浏览器检查使用实际配置的模型，完成三种申请的端到端流程；
缺资料和冲突各包含修改后的第二次分析，并验证人工复核、报告下载和刷新后的持久化。
这是少量场景的功能验收，不能作为业务准确率或跨场景泛化能力的 benchmark。
