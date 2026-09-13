"""Publish compact verdicts and a report only after all scheduled attempts are present."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from battery_copilot.benchmark import summarize
from battery_copilot.benchmark_cases import CATEGORIES, SUITE


def percentage(count, total):
    return f"{count}/{total} ({count / total:.1%})"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    tasks = json.loads((SUITE / "cases.json").read_text(encoding="utf-8"))
    paths = sorted((args.run / "attempts").glob("*.json"))
    rows = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
    expected = {(t["id"], v) for t in tasks for v in "ABC"}
    actual = {(r["case_id"], r["variant"]) for r in rows}
    if actual != expected or len(rows) != 900:
        raise ValueError(f"Expected 900 unique attempts; missing {len(expected - actual)}")
    if sum(len(row["steps"]) for row in rows) != 1035:
        raise ValueError("Expected 1,035 analysis stages")
    replay = json.loads((args.run / "workflow-replay.json").read_text(encoding="utf-8"))
    if {r["case_id"] for r in replay} != {t["id"] for t in tasks if t["category"] == "workflow"}:
        raise ValueError("Missing workflow replays")
    manifest = json.loads((args.run / "manifest.json").read_text(encoding="utf-8"))
    summary = summarize(args.run)
    paired = {}
    by_key = {(r["case_id"], r["variant"]): r for r in rows}
    for other in "AB":
        outcomes = Counter()
        for task in tasks:
            if task["split"] == "test":
                c = by_key[task["id"], "C"]["grounded_task_pass"]
                b = by_key[task["id"], other]["grounded_task_pass"]
                outcomes[
                    "both_pass"
                    if c and b
                    else "C_only"
                    if c
                    else "control_only"
                    if b
                    else "both_fail"
                ] += 1
        paired[f"C_vs_{other}"] = dict(outcomes)
    consumption = {}
    for variant in "ABC":
        stages = [
            s for r in rows if r["split"] == "test" and r["variant"] == variant for s in r["steps"]
        ]
        consumption[variant] = {
            "stages": len(stages),
            "completed_tool_calls": sum(
                e.get("type") == "tool" and e.get("status") == "completed"
                for s in stages
                for e in s["trace"]
            ),
            "retrieved_uid_citation_errors": sum(
                bool(s["score"]["unresolved_citations"]) for s in stages
            ),
        }
    compact = []
    for row, path in zip(rows, paths):
        compact.append(
            {
                **{
                    k: row[k]
                    for k in [
                        "case_id",
                        "category",
                        "family",
                        "split",
                        "variant",
                        "returned_answer",
                        "answer_correct",
                        "grounded_task_pass",
                        "seconds",
                    ]
                },
                "attempt_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "stages": [
                    {
                        "answer_correct": s["score"]["answer_correct"],
                        "grounded_task_pass": s["score"]["grounded_task_pass"],
                        "field_correct": s["score"]["field_correct"],
                        "error": s["result"].get("message")
                        if s["result"]["type"] == "error"
                        else None,
                    }
                    for s in row["steps"]
                ],
            }
        )
    published = {
        "frozen_commit": args.commit,
        "suite": json.loads((SUITE / "manifest.json").read_text(encoding="utf-8")),
        "run_manifest": manifest,
        "summary": summary,
        "test_paired": paired,
        "test_consumption": consumption,
        "workflow_replay": {
            s: sum(r["status"] == s for r in replay)
            for s in ["passed", "failed", "model_dependency_failed"]
        },
        "verdicts": compact,
    }
    (SUITE / "results.json").write_text(
        json.dumps(published, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    lines = [
        "# 300 案例实测结果",
        "",
        f"冻结源码：`{args.commit}`。模型：`{manifest['config']['model']}`，"
        f"并发 {manifest['config']['workers']}。",
        "",
        "完整执行 900 个案例尝试、1,035 个分析阶段。每题每方案一次；失败保留在分母。",
        "开发集 60 题；下面的主要比较使用 240 题测试集。",
        "",
        "| 方案 | 返回完整答案 | 答案正确 | 答案及引用通过 | 中位耗时 | P95 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    names = {"A": "固定 RAG", "B": "固定图查询与规则", "C": "生产 Agent"}
    for v in "ABC":
        r = summary["by_split"]["test"][v]
        lines.append(
            f"| {v} {names[v]} | {percentage(r['answers'], 240)} | "
            f"{percentage(r['answer_correct'], 240)} | "
            f"{percentage(r['grounded_task_pass'], 240)} | "
            f"{r['median_seconds']} s | {r['p95_seconds']} s |"
        )
    lines += [
        "",
        "## 按业务类别",
        "",
        "下表为答案与引用同时通过的案例数。",
        "",
        "| 类别 | A / 40 | B / 40 | C / 40 |",
        "| --- | ---: | ---: | ---: |",
    ]
    for category, title in CATEGORIES.items():
        scores = [
            summary["by_split"]["test"][v]["categories"][category]["grounded_task_pass"]
            for v in "ABC"
        ]
        lines.append(f"| {title} | {scores[0]} | {scores[1]} | {scores[2]} |")
    lines += [
        "",
        "## 实际调用与失败",
        "",
        "| 方案 | 模型调用 | 工具调用 | 已观测输入 token | 输出 token | 缓存输入 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for v in "ABC":
        u = summary["by_split"]["test"][v]["observed_usage"]
        lines.append(
            f"| {v} | {u['model_calls']} | {consumption[v]['completed_tool_calls']} | "
            f"{u['input_tokens']:,} | {u['output_tokens']:,} | {u['cached_input_tokens']:,} |"
        )
    lines += [
        "",
        "实际调用量并不相等；B 可读指定整页，C 使用生产检索工具。"
        "输入 token 含 CLI 上下文，不能换算成 API 账单费用。",
        "",
    ]
    for v in "ABC":
        r = summary["by_split"]["test"][v]
        lines.append(
            f"- {v}：{r['steps_with_usage']}/{r['steps']} 阶段返回 usage；"
            f"错误分布：`{json.dumps(r['errors'], ensure_ascii=False)}`。"
        )
    lines += ["", "## 同题比较与流程验证", ""]
    for comparison, counts in paired.items():
        lines.append(
            f"- {comparison}：同时通过 {counts.get('both_pass', 0)}；"
            f"仅 C 通过 {counts.get('C_only', 0)}；"
            f"仅对照通过 {counts.get('control_only', 0)}；"
            f"同时失败 {counts.get('both_fail', 0)}。"
        )
    counts = published["workflow_replay"]
    lines += [
        "",
        f"50 个保存流程重放：通过 {counts['passed']}，实现检查失败 {counts['failed']}，"
        f"因模型未返回答案而未走完 {counts['model_dependency_failed']}。",
        "重放复用实际 C 回答并重新绑定证据命名空间，不再调用模型；自动模拟复核人的 API 操作，"
        "检查修订使旧报告失效、缺失/冲突禁止完成、复核后完成、持久化及报告导出。"
        "该结果独立于模型答题分数，不是工程师试用或人工签字。",
        "",
        "## 解读范围",
        "",
        "300 个案例来自 41 种题型或流程；同产品及同页案例有关联。"
        "测试集的产品/页面与开发集分离，但部分题型共享。",
        "指南题只自动评分条目定位与覆盖；引用存在检查不等于每句解释的语义正确。"
        "变更规格为模拟资料，不能据此声称工业可用性。",
        "",
        "10 个开发案例另做过管线试跑，未并入上述分母；试跑后澄清两处输出格式，"
        "正式运行期间没有改题、调 Agent 或挑选重试结果。",
        "",
        "[协议](benchmark-300.md) · [逐案例判定及完整统计](../data/benchmark/results.json) · "
        "[题目、答案与来源](../data/benchmark/catalogue.md)",
        "",
    ]
    (Path("docs") / "benchmark-results.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )


if __name__ == "__main__":
    main()
