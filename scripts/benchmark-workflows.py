"""Replay the 50 saved-case workflows using actual C answers, without more model calls."""

import argparse
import json
from pathlib import Path

from battery_copilot import cases
from battery_copilot.benchmark_cases import SUITE
from battery_copilot.graph import graph


def must_block(action):
    try:
        action()
    except cases.CaseConflict:
        return
    raise AssertionError("The workflow accepted an operation that should be blocked")


def replay(task, attempt):
    saved = cases.create_case(cases.CaseInput(**task["steps"][0]["input"]))
    case_id = saved["id"]
    snapshots = []
    try:
        for index, (stage, observed) in enumerate(zip(task["steps"], attempt["steps"]), 1):
            if index > 1:
                previous = cases.current_report(saved)
                previous_id = previous["id"]
                saved = cases.update_case(
                    case_id, saved["version"], cases.CaseInput(**stage["input"])
                )
                assert saved["status"] == "draft"
                assert saved["current_report_id"] is None
                must_block(lambda: cases.complete_case(case_id, saved["version"]))
                must_block(
                    lambda: cases.review_finding(
                        case_id,
                        saved["version"],
                        previous_id,
                        "tool-fit",
                        "benchmark simulator",
                        "stale report",
                    )
                )
            started = cases.start_analysis(case_id, saved["version"])
            context = cases.build_context(started)
            # Rebind the identical simulated input's evidence namespace to the new saved-case ID.
            result = json.loads(
                json.dumps(observed["result"]).replace(
                    f"change:{task['id']}:", f"change:{case_id}:"
                )
            )
            saved = cases.finish_analysis(started, context, [result])
            if result["type"] != "answer":
                assert saved["analysis_status"] == "failed"
                return {"status": "model_dependency_failed", "stage": index}
            gold = stage["gold"]["answer"]
            assert saved["status"] == gold["case_status"]
            report = cases.current_report(saved)
            actual = {f["id"]: f["status"] for f in report["findings"]}
            assert actual["tool-fit"] == gold["tool_status"]
            assert actual["instruction-spec"] == gold["instruction_status"]
            assert report["input_version"] == index
            assert report["reviews"] == {}
            must_block(lambda: cases.complete_case(case_id, saved["version"]))
            for finding in report["findings"]:

                def review():
                    return cases.review_finding(
                        case_id,
                        saved["version"],
                        report["id"],
                        finding["id"],
                        "benchmark simulator",
                        "Automated workflow replay; not an engineer sign-off.",
                    )

                if finding["status"] == "pass":
                    saved = review()
                else:
                    must_block(review)
            if gold["ready_for_human_review_completion"]:
                saved = cases.complete_case(case_id, saved["version"])
                assert saved["status"] == "completed"
            else:
                must_block(lambda: cases.complete_case(case_id, saved["version"]))
            assert cases.get_case(case_id) == saved
            exported = cases.export_report(saved)
            assert stage["input"]["target_uid"] in exported
            assert all(e["uid"] in exported for e in report["evidence"])
            snapshots.append({"case": saved, "export": exported})
        return {"status": "passed", "snapshots": snapshots}
    finally:
        # Only remove the fixture created by this invocation, never existing user cases.
        graph().query("MATCH (c:ChangeCase {id:$id}) DETACH DELETE c", id=case_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, type=Path)
    args = parser.parse_args()
    tasks = json.loads((SUITE / "cases.json").read_text(encoding="utf-8"))
    results = []
    for task in tasks:
        if task["category"] != "workflow":
            continue
        attempt = json.loads(
            (args.run / "attempts" / f"{task['id']}-C.json").read_text(encoding="utf-8")
        )
        try:
            outcome = replay(task, attempt)
        except Exception as exc:
            outcome = {"status": "failed", "error": str(exc), "exception": type(exc).__name__}
        results.append({"case_id": task["id"], **outcome})
        print(task["id"], outcome["status"], flush=True)
    (args.run / "workflow-replay.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                s: sum(r["status"] == s for r in results)
                for s in ["passed", "failed", "model_dependency_failed"]
            }
        )
    )


if __name__ == "__main__":
    main()
