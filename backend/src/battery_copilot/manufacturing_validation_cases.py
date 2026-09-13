"""Version 2: explicit output types, failure regressions and previously unasked objects."""

import argparse
import hashlib
import json
from pathlib import Path

from battery_copilot.manufacturing_cases import (
    ARCHIVE_MD5,
    BASE,
    URL,
    SourceArchive,
    evidence_id,
)
from battery_copilot.settings import ROOT

SUITE = ROOT / "data/manufacturing-validation"


def build(path):
    src = SourceArchive(path)
    old = json.loads((ROOT / "data/manufacturing-benchmark/cases.json").read_text(encoding="utf-8"))
    cases = []
    regression_types = {
        "mfg-01": {"chain": "array of object-name strings, upstream first"},
        "mfg-07": {
            "chain": "array of object-name strings, upstream first",
            "unique_processes": "integer count",
        },
        "mfg-09": {"can_count_physical_cells": "boolean", "file_count": "integer count"},
        "mfg-11": {"electrolyte_ml": "number or null"},
        "mfg-18": {"cycle1_ah": "number", "cycle100_ah": "number", "soh_established": "boolean"},
        "mfg-22": {
            "acr_raw": "number or null, never a string",
            "dcir_raw": "number or null, never a string",
        },
        "mfg-30": {"unique_processes": "integer count"},
        "mfg-33": {"mass_field_reviewable": "boolean", "filling_accepted": "boolean or null"},
    }
    for c in old:
        if c["id"] in regression_types:
            cases.append(
                {**c, "split": "dev", "input": {**c["input"], "fields": regression_types[c["id"]]}}
            )

    def cell(batch, number):
        return BASE + "LabObject-3A" + batch + f"-23O{number:04d}"

    def row(c, cycle):
        data, identifier = src.row(c, cycle)
        return {"uid": identifier, "file": "files/" + src.cell_files[c][0], **data}

    def file(c):
        name = src.cell_files[c][0]
        return {
            "uid": evidence_id("files/" + name),
            "file": "files/" + name,
            "row_count": len(src.stats[name]),
            "linked_objects": sorted(src.file_cells[name]),
        }

    def trace(c):
        objects, links = src.trace(c)
        return {
            "uid": "ki:trace:" + evidence_id(c),
            "file": sorted({src.files[o] for o in objects}),
            "objects": objects,
            "predecessor_parameters": [src.source(p) for p in links],
        }

    def quantities(c, fields):
        answer, sources = {}, []
        for key, name, unit in fields:
            value, p = src.quantity(c, name, unit)
            answer[key] = value
            sources.append(src.source(p))
        return answer, sources

    def add(c, category, question, answer, sources, types=None, ordered=()):
        types = types or {k: "number or null" for k in answer}
        cases.append(
            {
                "id": f"new-{len(cases) - len(regression_types) + 1:02d}",
                "split": "test",
                "batch": c.removeprefix(BASE + "LabObject-3A").split("-23")[0],
                "category": category,
                "input": {"cell_uid": evidence_id(c), "question": question, "fields": types},
                "gold": {
                    "answer": answer,
                    "ordered_fields": list(ordered),
                    "required_sources": [s["uid"] for s in sources],
                },
                "sources": sources,
            }
        )

    def cycle_question(c, question, fields):
        evidence = {cycle: row(c, cycle) for _, cycle, _ in fields}
        add(
            c,
            "cycle_lookup",
            question,
            {key: evidence[cycle]["values"][column] for key, cycle, column in fields},
            list(evidence.values()),
        )

    c = cell("OSL0f1dcbc0ddec45608d5272fc38ed5f4a", 10)
    cycle_question(
        c,
        "交接前核对 Cycle 160 的充电容量 charge_ah 和放电容量 discharge_ah，单位Ah。",
        [("charge_ah", 160, "AH-IN"), ("discharge_ah", 160, "AH-OUT")],
    )
    add(
        c,
        "parameters",
        "沿本对象的实际前驱查注液量 electrolyte_ml 与湿质量 wet_g。",
        *quantities(
            c, [("electrolyte_ml", "ElectrolyteVolume10", "ml"), ("wet_g", "WettCellMass10", "g")]
        ),
    )

    c = cell("OSL191ebd16f651496b9c980ad555af2f45", 13)
    cycle_question(
        c,
        "对账 Cycle 250 的放电能量 discharge_wh，使用原始WH-OUT。",
        [("discharge_wh", 250, "WH-OUT")],
    )
    add(
        c,
        "missing_values",
        "复核称重资料：wet_g为湿质量，dry_g为干电芯带支撑质量；未填写则null。",
        *quantities(
            c, [("wet_g", "WettCellMass13", "g"), ("dry_g", "DryCellWithBracingMass13", "g")]
        ),
    )

    c = cell("OSL463655a934d24ff4bd148b2e9cc190e7", 12)
    cycle_question(
        c,
        "先核对测试初始化行 Cycle 0，输出 charge_ah 和 discharge_ah，保留微小非零值。",
        [("charge_ah", 0, "AH-IN"), ("discharge_ah", 0, "AH-OUT")],
    )
    add(
        c,
        "missing_values",
        "称重表中干电芯带支撑质量是否填写？输出 dry_g 和 wet_g，区分记录的0与缺失。",
        *quantities(
            c, [("dry_g", "DryCellWithBracingMass12", "g"), ("wet_g", "WettCellMass12", "g")]
        ),
    )

    c = cell("OSL4ea2d2f3808849239117806bd17894a3", 9)
    cycle_question(
        c,
        "请核对相邻 Cycle 73 和 Cycle 74 的放电容量，输出 cycle73_ah、cycle74_ah。",
        [("cycle73_ah", 73, "AH-OUT"), ("cycle74_ah", 74, "AH-OUT")],
    )
    add(
        c,
        "parameters",
        "报告需要注液压力 injection_mbar 与封口压力 sealing_mbar，分别核对原工序字段。",
        *quantities(
            c,
            [
                ("injection_mbar", "InjectionPressure", "mbar"),
                ("sealing_mbar", "SealingPressure", "mbar"),
            ],
        ),
    )

    c = cell("OSL5fc0a8322ff64454952ef5a31b6e39e4", 12)
    cycle_question(
        c,
        "核对较后段 Cycle 400 的 discharge_ah 和 discharge_wh，不能把Ah当Wh。",
        [("discharge_ah", 400, "AH-OUT"), ("discharge_wh", 400, "WH-OUT")],
    )
    add(
        c,
        "parameters",
        "沿明确前驱读取 electrolyte_ml、dry_g、wet_g；不能按当前对象编号猜注液参数编号。",
        *quantities(
            c,
            [
                ("electrolyte_ml", "ElectrolyteVolume13", "ml"),
                ("dry_g", "DryCellWithBracingMass13", "g"),
                ("wet_g", "WettCellMass13", "g"),
            ],
        ),
    )

    c = cell("OSL618063bc437a4b8285b9aaf52d961b45", 2)
    cycle_question(
        c,
        "交接清单要求 Cycle 220 和 Cycle 221 的放电能量，输出 cycle220_wh、cycle221_wh。",
        [("cycle220_wh", 220, "WH-OUT"), ("cycle221_wh", 221, "WH-OUT")],
    )
    value, p = src.parameter(c, "WettCellMass2")
    add(
        c,
        "source_transcription",
        "为核对异常显示，请把湿质量HasValue的工具显示值原样写入wet_source_value，保留其中编码和单位，不修正数字。",
        {"wet_source_value": value},
        [src.source(p)],
        {"wet_source_value": "string or null"},
    )

    c = cell("OSL6f0a8e17487e4b87806f2d5da185abd1", 4)
    cycle_question(
        c,
        "核查 Cycle 100 的 discharge_ah、discharge_wh，原单位分别为Ah和Wh。",
        [("discharge_ah", 100, "AH-OUT"), ("discharge_wh", 100, "WH-OUT")],
    )
    add(
        c,
        "parameters",
        "核对本对象前驱称重：dry_g、wet_g；同时给出该前驱注液量electrolyte_ml。",
        *quantities(
            c,
            [
                ("dry_g", "DryCellWithBracingMass15", "g"),
                ("wet_g", "WettCellMass15", "g"),
                ("electrolyte_ml", "ElectrolyteVolume15", "ml"),
            ],
        ),
    )

    c = cell("OSL9f61349f3b81400b9f4049ac95e03cd7", 20)
    cycle_question(
        c,
        "在性能资料交接中摘录 Cycle 300 的充放电容量，输出charge_ah、discharge_ah。",
        [("charge_ah", 300, "AH-IN"), ("discharge_ah", 300, "AH-OUT")],
    )
    add(
        c,
        "missing_values",
        "核对末号样品自己的wet_g和electrolyte_ml，不采用同批另一只样品的称重。",
        *quantities(
            c, [("wet_g", "WettCellMass20", "g"), ("electrolyte_ml", "ElectrolyteVolume20", "ml")]
        ),
    )

    c = cell("OSLa7024a3883424ccf8a711c3ac5267ec5", 10)
    cycle_question(
        c,
        "核对 Cycle 239 的放电容量discharge_ah，为归档保留6位小数。",
        [("discharge_ah", 239, "AH-OUT")],
    )
    answer, evidence = quantities(
        c,
        [("injection_pa", "InjectionPressure", "mbar"), ("sealing_pa", "SealingPressure", "mbar")],
    )
    add(
        c,
        "parameters",
        "系统接收Pa：把记录中的注液和封口压力转换成injection_pa、sealing_pa，保留原始引用。",
        {k: v * 100 for k, v in answer.items()},
        evidence,
    )

    c = cell("OSLb4cba0d88fdc49938172c48bf098df6a", 6)
    r = row(c, 10)
    assert not any(r["values"]["Cycle"] == 100 for r in src.stats[src.cell_files[c][0]])
    add(
        c,
        "missing_cycle",
        "分别定位 Cycle 10 和 Cycle 100，输出cycle10_ah、cycle100_ah；不存在的循环返回null。",
        {"cycle10_ah": r["values"]["AH-OUT"], "cycle100_ah": None},
        [r, file(c)],
    )
    add(
        c,
        "missing_values",
        "核对干电芯带支撑质量dry_g与注液量electrolyte_ml：零质量按记录保留，不改成null。",
        *quantities(
            c,
            [
                ("dry_g", "DryCellWithBracingMass6", "g"),
                ("electrolyte_ml", "ElectrolyteVolume6", "ml"),
            ],
        ),
    )

    c = cell("OSLb947c332babc438b9212aac087a68fa8", 10)
    cycle_question(
        c,
        "需要逐行复核 Cycle 200 与 Cycle 201，输出cycle200_ah、cycle201_ah。",
        [("cycle200_ah", 200, "AH-OUT"), ("cycle201_ah", 201, "AH-OUT")],
    )
    objects, _ = src.trace(c)
    add(
        c,
        "lineage",
        "输出从上游到下游的chain名称字符串数组，以及去重后的过程数量process_count。",
        {
            "chain": [src.name(o) for o in objects],
            "process_count": len({p for o in objects for p in src.refs(o, "IsOutputOf")}),
        },
        [trace(c)],
        {"chain": "array of object-name strings, upstream first", "process_count": "integer count"},
        ["chain"],
    )

    c = cell("OSLfdb74e35b39a4ad3ac3e933a90b37b26", 5)
    cycle_question(
        c,
        "核查 Cycle 300 的放电容量discharge_ah及能量discharge_wh，按各自单位摘录。",
        [("discharge_ah", 300, "AH-OUT"), ("discharge_wh", 300, "WH-OUT")],
    )
    assert len(src.trace(c)[0]) == 1 and not any(
        "ElectrolyteVolume" in p for p in src.parameters(c)
    )
    add(
        c,
        "missing_lineage",
        "核对本对象自己的上游注液量electrolyte_ml，明确前驱资料无法提供该数值时返回null并引用查询范围。",
        {"electrolyte_ml": None},
        [trace(c)],
    )

    old_cells = {c["input"]["cell_uid"] for c in old}
    assert not old_cells & {c["input"]["cell_uid"] for c in cases if c["split"] == "test"}
    return cases, src


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    args = parser.parse_args()
    cases, src = build(args.archive)
    SUITE.mkdir(exist_ok=True, parents=True)
    content = json.dumps(cases, ensure_ascii=False, indent=2) + "\n"
    (SUITE / "cases.json").write_text(content, encoding="utf-8")
    manifest = {
        "dataset": "kiprobatt-v0.3.2",
        "source_url": URL,
        "archive_md5": ARCHIVE_MD5,
        "cases": len(cases),
        "dev": 8,
        "test": 24,
        "split_unit": "new objects/files in the SAME 12 previously seen formation batches",
        "annotation": "Developer-assistant tasks and raw-source gold; no external engineer review.",
        "suite_sha256": hashlib.sha256(content.encode()).hexdigest(),
        "source_sha256": src.hashes,
    }
    (SUITE / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps({k: v for k, v in manifest.items() if k != "source_sha256"}, ensure_ascii=False)
    )


if __name__ == "__main__":
    main()
