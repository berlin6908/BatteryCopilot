"""Curated manufacturing cases; gold comes directly from the pinned source archive.

No production importer, graph query, tool, or numeric parser is used to compute gold.
Questions and business contrasts below are authored individually, not expanded templates.
"""

import argparse
import csv
import hashlib
import io
import json
import zipfile
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from battery_copilot.settings import ROOT

SUITE = ROOT / "data/manufacturing-benchmark"
BASE = "https://kiprobatt.de/id/"
ARCHIVE_MD5 = "03dbcb62fcf17f843b90709d07668450"
URL = "https://zenodo.org/records/11895571"


def evidence_id(value):
    return "ki:" + hashlib.sha256(value.encode()).hexdigest()[:20]


class SourceArchive:
    def __init__(self, path):
        if hashlib.md5(path.read_bytes()).hexdigest() != ARCHIVE_MD5:
            raise ValueError("Expected KIproBatt v0.3.2 source archive")
        self.nodes, self.contexts, self.files, self.stats, self.hashes = {}, {}, {}, {}, {}
        self.object_params, self.step_params = defaultdict(list), defaultdict(list)
        self.cell_files, self.file_cells = defaultdict(list), defaultdict(list)
        with zipfile.ZipFile(path) as archive:
            for member in sorted(archive.namelist()):
                if "/data/" in member and member.endswith(".jsonld"):
                    data = archive.read(member)
                    doc = json.loads(data.decode("cp1252"))
                    source = "data/" + member.rsplit("/data/", 1)[1]
                    self.hashes[source] = hashlib.sha256(data).hexdigest()
                    for node in doc.get("@graph", [doc]):
                        if "@id" not in node:
                            continue
                        iri = self.expand(node["@id"], doc["@context"])
                        self.nodes[iri], self.contexts[iri], self.files[iri] = (
                            node,
                            doc["@context"],
                            source,
                        )
                elif "/files/" in member and "-STATS-" in member and member.endswith(".txt"):
                    data = archive.read(member)
                    name = member.rsplit("/", 1)[1]
                    self.hashes["files/" + name] = hashlib.sha256(data).hexdigest()
                    lines = data.decode("cp1252").splitlines()
                    start = next(
                        i for i, line in enumerate(lines) if line.split("\t")[0] == "Cycle"
                    )
                    parsed = list(
                        csv.DictReader(io.StringIO("\n".join(lines[start:])), delimiter="\t")
                    )
                    self.stats[name] = [
                        {
                            "line": start + 2 + i,
                            "raw": row,
                            "values": {
                                k: float(Decimal(v.replace(",", "."))) if v else None
                                for k, v in row.items()
                                if k
                            },
                        }
                        for i, row in enumerate(parsed)
                    ]
        for iri in self.nodes:
            for obj in self.refs(iri, "IsObjectParameterOf"):
                self.object_params[obj].append(iri)
                for ref in self.values(iri, "HasFile"):
                    name = ref["@id"].split(":", 1)[1]
                    if name in self.stats:
                        self.cell_files[obj].append(name)
                        self.file_cells[name].append(obj)
            for step in self.refs(iri, "IsProcessParameterOf"):
                self.step_params[step].append(iri)

    @staticmethod
    def expand(value, context):
        prefix, _, rest = value.partition(":")
        if prefix not in context:
            return value
        definition = context[prefix]
        return (definition["@id"] if isinstance(definition, dict) else definition) + rest

    def values(self, iri, key):
        value = self.nodes[iri].get("Property:" + key, [])
        return value if isinstance(value, list) else [value]

    def refs(self, iri, key):
        return [
            self.expand(v["@id"], self.contexts[iri])
            for v in self.values(iri, key)
            if isinstance(v, dict) and "@id" in v
        ]

    def name(self, iri):
        node = self.nodes[iri]
        return node.get("Property:HasName") or node["Property:HasLabel"]["@id"].split(":", 1)[
            1
        ].removesuffix("@en")

    def trace(self, cell):
        found, links = [], []

        def visit(obj):
            if obj in found:
                return
            for p in self.object_params[obj]:
                for previous in self.refs(p, "HasPredecessor"):
                    if previous not in self.nodes:
                        raise ValueError(f"Unresolved raw predecessor in selected case: {previous}")
                    links.append(p)
                    visit(previous)
            found.append(obj)

        visit(cell)
        return found, links

    def parameters(self, cell):
        objects, _ = self.trace(cell)
        processes = {p for obj in objects for p in self.refs(obj, "IsOutputOf")}
        params = {}
        for step in self.step_params:
            if not processes.intersection(self.refs(step, "IsSubprocessOf")):
                continue
            for p in self.step_params[step]:
                targets = set(self.refs(p, "IsObjectParameterOf"))
                if not targets or targets.intersection(objects):
                    params[self.name(p)] = p
        return params

    def parameter(self, cell, name):
        p = self.parameters(cell)[name]
        values = self.values(p, "HasValue")
        value = values[0]["@id"].removeprefix("kiprobatt:").replace("_", " ") if values else None
        return value, p

    def quantity(self, cell, name, unit):
        value, p = self.parameter(cell, name)
        if value is None:
            return None, p
        number, actual_unit = value.rsplit(" ", 1)
        if actual_unit != unit:
            raise ValueError(f"Unexpected source unit: {value}")
        return float(Decimal(number)), p

    def row(self, cell, cycle):
        name = self.cell_files[cell][0]
        row = next(r for r in self.stats[name] if r["values"]["Cycle"] == cycle)
        return row, evidence_id("files/" + name) + f":L{row['line']}"

    def source(self, identity):
        if isinstance(identity, str):
            return {
                "uid": evidence_id(identity),
                "file": self.files[identity],
                "subject": identity,
                "raw_node": self.nodes[identity],
            }
        return identity


def build(path):
    src = SourceArchive(path)
    cases = []
    roots = {
        "march": "OSL9f61349f3b81400b9f4049ac95e03cd7",
        "nov": "OSL618063bc437a4b8285b9aaf52d961b45",
        "shared": "OSL5fc0a8322ff64454952ef5a31b6e39e4",
        "gap": "OSLfdb74e35b39a4ad3ac3e933a90b37b26",
        "short": "OSLb4cba0d88fdc49938172c48bf098df6a",
        "lowvol": "OSLb947c332babc438b9212aac087a68fa8",
        "pulse": "OSL4ea2d2f3808849239117806bd17894a3",
        "feb6": "OSLa7024a3883424ccf8a711c3ac5267ec5",
        "feb7": "OSL0f1dcbc0ddec45608d5272fc38ed5f4a",
        "filename": "OSL463655a934d24ff4bd148b2e9cc190e7",
        "mass": "OSL191ebd16f651496b9c980ad555af2f45",
        "nov22": "OSL6f0a8e17487e4b87806f2d5da185abd1",
    }

    def cell(group, number=1):
        return BASE + "LabObject-3A" + roots[group] + f"-23O{number:04d}"

    def add(group, number, category, question, answer, sources, *, obj=1, ordered=()):
        c = cell(group, obj)
        actual_sources = [src.source(s) for s in sources]
        cases.append(
            {
                "id": f"mfg-{len(cases) + 1:02d}",
                "scenario": f"{group}-{number}",
                "split": "dev" if group in ("march", "nov") else "test",
                "batch": roots[group],
                "category": category,
                "input": {"cell_uid": evidence_id(c), "question": question},
                "gold": {
                    "answer": answer,
                    "ordered_fields": list(ordered),
                    "required_sources": [s["uid"] for s in actual_sources],
                },
                "sources": actual_sources,
            }
        )

    def chain_source(c):
        objects, links = src.trace(c)
        return {
            "uid": "ki:trace:" + evidence_id(c),
            "file": sorted({src.files[o] for o in objects}),
            "basis": "Direct traversal of original object"
                     "-specific predecessor parameters",
            "objects": objects,
            "predecessor_parameters": [src.source(p) for p in links],
        }

    def file_source(c):
        name = src.cell_files[c][0]
        return {
            "uid": evidence_id("files/" + name),
            "file": "files/" + name,
            "row_count": len(src.stats[name]),
            "linked_objects": sorted(src.file_cells[name]),
        }

    def row_source(c, cycle):
        row, identifier = src.row(c, cycle)
        return {
            "uid": identifier,
            "file": "files/" + src.cell_files[c][0],
            "line": row["line"],
            "raw_row": row["raw"],
        }

    def val(c, cycle, field):
        value = src.row(c, cycle)[0]["values"][field]
        return round(value, 6) if value is not None else None

    c = cell("march")
    add(
        "march",
        1,
        "lineage",
        "准备履历交接：列出明确对象链的名称，从最上游到当前对象，输出 chai"
        "n。不要根据工序常识补链。",
        {"chain": [src.name(o) for o in src.trace(c)[0]]},
        [chain_source(c)],
        ordered=["chain"],
    )
    v, p = src.quantity(c, "ElectrolyteVolume1", "ml")
    pressure, missing = src.quantity(c, "CompactingPressure1", "kPa")
    add(
        "march",
        2,
        "parameters",
        "核对注液与化成的交接资料：输出 electrolyte_ml（本电芯注"
        "液量）、compacting_kpa（压实压力；未填时null）。",
        {"electrolyte_ml": v, "compacting_kpa": pressure},
        [p, missing],
    )
    add(
        "march",
        3,
        "missing_values",
        "有人把空白一律填成零。核对 Cycle 0：输出 charge_ah、"
        "dcir_raw，保留缺失值，数值保留6位小数。",
        {"charge_ah": val(c, 0, "AH-IN"), "dcir_raw": val(c, 0, "DCIR")},
        [row_source(c, 0)],
    )

    c = cell("nov")
    add(
        "nov",
        1,
        "cycle_lookup",
        "复核中段记录：输出 Cycle 120 的 discharge_ah，"
        "保留6位小数；不能用首尾循环替代。",
        {"discharge_ah": val(c, 120, "AH-OUT")},
        [row_source(c, 120)],
    )
    a, pa = src.quantity(c, "InjectionPressure", "mbar")
    b, pb = src.quantity(c, "SealingPressure", "mbar")
    add(
        "nov",
        2,
        "parameters",
        "核对注入与封口压力差异：输出 injection_mbar、seali"
        "ng_mbar、difference_mbar（前者减后者）。",
        {"injection_mbar": a, "sealing_mbar": b, "difference_mbar": a - b},
        [pa, pb],
    )
    records = src.stats[src.cell_files[c][0]]
    add(
        "nov",
        3,
        "cycle_lookup",
        "做文件交接清点：输出 row_count（数据行数，不含文件头）与 l"
        "ast_cycle（最后一行Cycle）。",
        {"row_count": len(records), "last_cycle": records[-1]["values"]["Cycle"]},
        [file_source(c), row_source(c, records[-1]["values"]["Cycle"])],
    )

    c = cell("shared", 54)
    objects = src.trace(c)[0]
    add(
        "shared",
        1,
        "lineage",
        "该对象经过化成后又被记录为已测试。输出按上游到下游的 chain，以及"
        "不同来源过程的 unique_processes。不要把对象状态数当成"
        "不同工序数。",
        {
            "chain": [src.name(o) for o in objects],
            "unique_processes": len({p for o in objects for p in src.refs(o, "IsOutputOf")}),
        },
        [chain_source(c)],
        obj=54,
        ordered=["chain"],
    )
    add(
        "shared",
        2,
        "identity",
        "这份测试文件可能重复挂接。输出 linked_object_count"
        " 与 linked_names（所有引用该文件的对象名称），不要只数当"
        "前选中项。",
        {
            "linked_object_count": len(src.file_cells[src.cell_files[c][0]]),
            "linked_names": [src.name(o) for o in src.file_cells[src.cell_files[c][0]]],
        },
        [file_source(c)],
        obj=54,
    )
    add(
        "shared",
        3,
        "identity",
        "仅根据此文件被多少图谱对象引用，能否把该数量直接当成独立物理电芯数量？"
        "输出 can_count_ph"
        "ysical_cells（布尔）和 file_count（当前对象所绑"
        "定的不同循环统计文件数）。",
        {"can_count_physical_cells": False, "file_count": len(set(src.cell_files[c]))},
        [file_source(c)],
        obj=54,
    )

    c = cell("gap")
    add(
        "gap",
        1,
        "lineage",
        "履历审计发现可能断链。输出 chain 中实际可追溯的对象名称，以及 "
        "upstream_record_found（当前对象是否有明确更上游对"
        "象）。",
        {
            "chain": [src.name(o) for o in src.trace(c)[0]],
            "upstream_record_found": len(src.trace(c)[0]) > 1,
        },
        [chain_source(c)],
        ordered=["chain"],
    )
    add(
        "gap",
        2,
        "missing_values",
        "采购同事想沿用上一批的注液量。当前电芯履历是否提供自己的注液量？输出 "
        "electrolyte_ml；资料没有给出则null，不能借用别的批次"
        "。",
        {"electrolyte_ml": None},
        [chain_source(c)],
    )
    add(
        "gap",
        3,
        "cycle_lookup",
        "尽管制造履历不完整，仍需核对测试末段：输出 Cycle 365 的 c"
        "harge_ah 与 discharge_ah，保留6位小数。",
        {"charge_ah": val(c, 365, "AH-IN"), "discharge_ah": val(c, 365, "AH-OUT")},
        [row_source(c, 365)],
    )

    c = cell("short")
    records = src.stats[src.cell_files[c][0]]
    add(
        "short",
        1,
        "cycle_lookup",
        "有人要求提取 Cycle 100。先核实这个短测试文件：输出 row_"
        "count 和 cycle100_discharge_ah（不存在则n"
        "ull）。",
        {"row_count": len(records), "cycle100_discharge_ah": None},
        [file_source(c)],
    )
    v, p = src.quantity(c, "ElectrolyteVolume1", "ml")
    add(
        "short",
        2,
        "parameters",
        "量具交接采用微升。读取本电芯注液记录，输出 electrolyte_m"
        "l 与 electrolyte_ul（1 ml=1000 µl），不能"
        "用通用电芯配方。",
        {"electrolyte_ml": v, "electrolyte_ul": v * 1000},
        [p],
    )
    add(
        "short",
        3,
        "decision_boundary",
        "导出数据交接要求包含Cycle 10。输出 cycle10_present；"
        "另外输出 lifetime_established，说明记录数量是否已经证明电芯寿命。",
        {"cycle10_present": any(r["values"]["Cycle"] == 10 for r in records),
         "lifetime_established": False},
        [file_source(c), row_source(c, 10)],
    )

    c = cell("lowvol")
    v, p = src.quantity(c, "ElectrolyteVolume1", "ml")
    add(
        "lowvol",
        1,
        "parameters",
        "工艺卡转录草稿写着“本电芯注液2.1 ml”。与当前对象的实际参数核对"
        "，输出 recorded_ml 和 draft_matches（布尔）"
        "。草稿不是原始制造证据。",
        {"recorded_ml": v, "draft_matches": v == 2.1},
        [p],
    )
    last = src.stats[src.cell_files[c][0]][-1]["values"]["Cycle"]
    add(
        "lowvol",
        2,
        "cycle_lookup",
        "核查长循环文件最后一行：输出 last_cycle 和 dischar"
        "ge_ah，容量保留6位小数。",
        {"last_cycle": last, "discharge_ah": val(c, last, "AH-OUT")},
        [row_source(c, last)],
    )
    add(
        "lowvol",
        3,
        "decision_boundary",
        "有人想仅凭同一文件的 Cycle 1 和 Cycle 100 容量就报"
        "告健康度下降。输出 cycle"
        "1_ah、cycle100_ah（6位小数）和 soh_establi"
        "shed（这些资料是否足以确定"
        "SOH）。",
        {
            "cycle1_ah": val(c, 1, "AH-OUT"),
            "cycle100_ah": val(c, 100, "AH-OUT"),
            "soh_established": False,
        },
        [row_source(c, 1), row_source(c, 100)],
    )

    c = cell("pulse")
    add(
        "pulse",
        1,
        "decision_boundary",
        "复核Cycle 1：输出 discharge_ah，保留原始精度，可用科学计数法；"
        "输出 exactly_zero（是否严格等于零）、failure_established（是否足以判定制造失败）。",
        {"discharge_ah": src.row(c, 1)[0]["values"]["AH-OUT"],
         "exactly_zero": src.row(c, 1)[0]["values"]["AH-OUT"] == 0,
         "failure_established": False},
        [row_source(c, 1)],
    )
    add(
        "pulse",
        2,
        "cycle_lookup",
        "工程师需要核对 Cycle 50 与 Cycle 51 的交接数据，输"
        "出 cycle50_ah、cycle51_ah，均保留6位小数。",
        {"cycle50_ah": val(c, 50, "AH-OUT"), "cycle51_ah": val(c, 51, "AH-OUT")},
        [row_source(c, 50), row_source(c, 51)],
    )
    temperature, p = src.quantity(c, "FormationTemperature", "°C")
    add(
        "pulse",
        3,
        "parameters",
        "表单要求填写已记录的化成温度。输出 formation_c；这里问的是"
        "该工序参数，不是推测所有循环都在相同温度下进行。",
        {"formation_c": temperature},
        [p],
    )

    c = cell("feb6")
    add(
        "feb6",
        1,
        "missing_values",
        "不要把电阻字段中的数值零误当空值。核对 Cycle 1，输出 acr_"
        "raw、dcir_raw；不推定单位。",
        {"acr_raw": val(c, 1, "ACR"), "dcir_raw": val(c, 1, "DCIR")},
        [row_source(c, 1)],
    )
    add(
        "feb6",
        2,
        "cycle_lookup",
        "定位 Cycle 180 的统计行，输出 discharge_ah 与"
        " discharge_wh，均保留6位小数。",
        {"discharge_ah": val(c, 180, "AH-OUT"), "discharge_wh": val(c, 180, "WH-OUT")},
        [row_source(c, 180)],
    )
    value, p = src.parameter(c, "CompactingPressure1")
    add(
        "feb6",
        3,
        "missing_values",
        "复核压实压力字段：是否有字段但没填值？输出 parameter_pre"
        "sent 和 compacting_kpa；不要把未填写解释成零压力。",
        {"parameter_present": True, "compacting_kpa": None},
        [p],
    )

    c = cell("feb7")
    add(
        "feb7",
        1,
        "cycle_lookup",
        "生产记录与检验交接时需要中段点位。输出 Cycle 200 的 cha"
        "rge_ah、discharge_ah，保留6位小数。",
        {"charge_ah": val(c, 200, "AH-IN"), "discharge_ah": val(c, 200, "AH-OUT")},
        [row_source(c, 200)],
    )
    foreign = src.cell_files[cell("march")][0]
    add(
        "feb7",
        2,
        "identity",
        f"交接单误贴了 {foreign}。输出 attached_to_selected_cell，"
        "说明这个文件是否是当前选中对象的关联循环文件。",
        {"attached_to_selected_cell": False},
        [chain_source(c)],
    )
    count, p = src.parameter(c, "ElectrodeCount")
    add(
        "feb7",
        3,
        "parameters",
        "读取已记录的叠片 ElectrodeCount，输出 electrod"
        "e_count。不要用对象上 HasNumberOfEntities "
        "的占位值代替工序参数。",
        {"electrode_count": int(count)},
        [p],
    )

    c = cell("filename", 10)
    add(
        "filename",
        1,
        "identity",
        "导出文件命名多了一个连字符。请返回当前对象绑定的 filename，严"
        "格保留原始文件名。",
        {"filename": src.cell_files[c][0]},
        [file_source(c)],
        obj=10,
    )
    add(
        "filename",
        2,
        "cycle_lookup",
        "检查这个非常规命名文件仍能定位到 Cycle 15，输出 charge"
        "_ah、discharge_ah（6位小数）。",
        {"charge_ah": val(c, 15, "AH-IN"), "discharge_ah": val(c, 15, "AH-OUT")},
        [row_source(c, 15)],
        obj=10,
    )
    add(
        "filename",
        3,
        "lineage",
        "文件命名不同不代表工艺链不同。输出当前对象明确履历中不同来源过程的数量"
        " unique_processes。",
        {"unique_processes": len({p for o in src.trace(c)[0] for p in src.refs(o, "IsOutputOf")})},
        [chain_source(c)],
        obj=10,
    )

    c = cell("mass", 2)
    wet, pw = src.quantity(c, "WettCellMass2", "g")
    dry, pd = src.quantity(c, "DryCellWithBracingMass2", "g")
    add(
        "mass",
        1,
        "missing_values",
        "质量差计算前先核对输入。输出 wet_g、dry_with_braci"
        "ng_g、can_compute_mass_difference；缺失"
        "质量不得补零。",
        {
            "wet_g": wet,
            "dry_with_bracing_g": dry,
            "can_compute_mass_difference": wet is not None and dry is not None,
        },
        [pw, pd],
        obj=2,
    )
    add(
        "mass",
        2,
        "parameters",
        "称量记录要转成SI单位。读取当前电芯湿质量，输出 wet_g 与 we"
        "t_kg（1 g=0.001 kg），不要混淆归一化值和显示单位。",
        {"wet_g": wet, "wet_kg": float(Decimal(str(wet)) / 1000)},
        [pw],
        obj=2,
    )
    add(
        "mass",
        3,
        "decision_boundary",
        "资料表要求湿质量可追溯。输出 mass_field_reviewable（是否有可核查的值）；"
        "另输出 filling_accepted，缺少注液质量判据时返回null并说明缺口。",
        {"mass_field_reviewable": wet is not None, "filling_accepted": None},
        [pw],
        obj=2,
    )

    c = cell("nov22")
    add(
        "nov22",
        1,
        "cycle_lookup",
        "需要在记录交接前核对 Cycle 150 与 Cycle 151 的放"
        "电能量：输出 cycle150_wh、cycle151_wh，保留6位"
        "小数。",
        {"cycle150_wh": val(c, 150, "WH-OUT"), "cycle151_wh": val(c, 151, "WH-OUT")},
        [row_source(c, 150), row_source(c, 151)],
    )
    v, p = src.parameter(c, "ElectrolyteSelection")
    add(
        "nov22",
        2,
        "missing_values",
        "核对电解液选择字段：输出 electrolyte_selection，"
        "字段没有填值则null，不能根据电芯名称猜配方。",
        {"electrolyte_selection": v},
        [p],
    )
    add(
        "nov22",
        3,
        "decision_boundary",
        "盘点当前可核查的不同制造过程数量，输出 process_count。"
        "另输出 complete_history_proven，现有记录是否证明了完整制造履历？",
        {"process_count": len({p for o in src.trace(c)[0] for p in src.refs(o, "IsOutputOf")}),
         "complete_history_proven": False},
        [chain_source(c)],
    )

    assert len(cases) == 36
    return cases, src


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    cases, src = build(args.archive)
    SUITE.mkdir(parents=True, exist_ok=True)
    content = json.dumps(cases, ensure_ascii=False, indent=2) + "\n"
    (SUITE / "cases.json").write_text(content, encoding="utf-8")
    manifest = {
        "dataset": "kiprobatt-v0.3.2",
        "source_url": URL,
        "archive_md5": ARCHIVE_MD5,
        "cases": 36,
        "dev": 6,
        "test": 30,
        "batches": 12,
        "suite_sha256": hashlib.sha256(content.encode()).hexdigest(),
        "source_sha256": src.hashes,
        "annotation": "Questions and business contrasts au"
                      "thored by devel"
        "opment assistant; answers checked a"
        "gainst raw expo"
        "rts. No external engineer review.",
    }
    (SUITE / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps({k: v for k, v in manifest.items() if k != "source_sha256"}, ensure_ascii=False)
    )


if __name__ == "__main__":
    main()
