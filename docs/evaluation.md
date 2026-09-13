# 评测执行说明

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
