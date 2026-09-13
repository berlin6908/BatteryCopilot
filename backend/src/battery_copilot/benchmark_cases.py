"""Build a source-grounded suite without using the application's graph or rule code."""

import copy
import csv
import hashlib
import json
from collections import Counter, defaultdict

from battery_copilot.settings import DERIVED, RAW, ROOT

SUITE = ROOT / "data/benchmark"
CATEGORIES = {
    "inventory": "台账核对",
    "connections": "连接关系",
    "sequence": "记录顺序",
    "guide": "指南证据定位",
    "scope": "资料边界",
    "workflow": "变更流程",
}


def uid(kind, number):
    return f"kit-v1:{kind}:{number}"


class SourceRows:
    """Independent oracle: raw CSV fields, including original physical line numbers."""

    def __init__(self):
        self.tables = {}
        self.by_uid = {}
        for name, kind in [
            ("battery_catalogue", "battery"),
            ("parts", "part"),
            ("fixations", "fixation"),
            ("operations", "operation"),
        ]:
            with (RAW / f"{name}.csv").open(encoding="utf-8-sig", newline="") as handle:
                rows = [
                    dict(row, source_line=i, source_file=f"{name}.csv", uid=uid(kind, row["id"]))
                    for i, row in enumerate(csv.DictReader(handle), 2)
                ]
            self.tables[kind] = rows
            self.by_uid.update((r["uid"], r) for r in rows)
        self.operations = {r["id"]: r for r in self.tables["operation"]}
        self.removals = defaultdict(list)
        self.previous = {}
        for row in self.tables["operation"]:
            target = (
                uid("part", row["part_id"])
                if row["part_id"]
                else uid("fixation", row["fixation_id"])
            )
            row["target"] = target
            row["battery_id"] = self.by_uid[target]["battery_id"]
            self.removals[target].append(row)
            if row["next_op_id"]:
                self.previous[row["next_op_id"]] = row

    def rows(self, kind, battery):
        return [r for r in self.tables[kind] if int(r.get("battery_id", r["id"])) == battery]

    def refs(self, identifiers):
        return [
            {
                "uid": item,
                "file": "data/sources/kit-battery/" + self.by_uid[item]["source_file"],
                "line": self.by_uid[item]["source_line"],
            }
            for item in dict.fromkeys(identifiers)
        ]

    def chain(self, row, length):
        result = [row]
        while len(result) < length and result[-1]["next_op_id"] in self.operations:
            following = self.operations[result[-1]["next_op_id"]]
            if following in result:
                break
            result.append(following)
        return result


def diverse(rows, signature, count):
    """Prefer different source structures, then deterministic spread within each group."""
    groups = defaultdict(list)
    for row in rows:
        groups[str(signature(row))].append(row)
    selected = []
    ordered = sorted(groups)
    while len(selected) < count:
        progressed = False
        for key in ordered:
            if groups[key]:
                selected.append(groups[key].pop(len(groups[key]) // 2))
                progressed = True
                if len(selected) == count:
                    return selected
        if not progressed:
            raise ValueError(f"Only {len(selected)} eligible source objects for {count} cases")
    return selected


def build():
    oracle = SourceRows()
    tasks = []

    def add(
        category,
        family,
        bid,
        question,
        expected,
        anchors=(),
        sources=(),
        *,
        split=None,
        query=None,
        ordered=(),
        intent=None,
        steps=None,
        page=None,
    ):
        number = sum(t["category"] == category for t in tasks) + 1
        task_id = f"{category}-{number:03d}"
        task = {
            "id": task_id,
            "category": category,
            "family": family,
            "split": split or ("dev" if bid <= 2 else "test"),
            "group": f"pem-page-{page}" if page else f"battery-{bid}",
            "business_intent": intent or CATEGORIES[category],
            "input": {
                "battery_id": bid,
                "question": question,
                "anchors": list(anchors),
                "search_query": query or question,
                "guide_page": page,
            },
            "gold": {
                "answer": expected,
                "required_sources": list(dict.fromkeys(sources)),
                "ordered_fields": list(ordered),
                "basis": "原始 CSV 字段独立计算",
            },
            "sources": oracle.refs(sources),
        }
        if steps is not None:
            task["steps"] = steps
            task["gold"]["basis"] = "预先声明的模拟输入、独立状态表及原始 CSV 关联"
        tasks.append(task)
        return task

    for bid in range(1, 11):
        parts, fixes, ops = (oracle.rows(kind, bid) for kind in ("part", "fixation", "operation"))
        battery = oracle.by_uid[uid("battery", bid)]
        name = battery["name"]
        # Three different inventory decisions, with actual per-product distributions.
        for kind, key, title in [
            ("part", "class", "部件备查"),
            ("fixation", "class", "连接方式清点"),
            ("operation", "skill_id", "拆解技能工作量"),
        ]:
            rows = oracle.rows(kind, bid)
            counts = Counter(r[key] for r in rows)
            labels = [label for label, _ in counts.most_common(3)]
            selected = [r["uid"] for r in rows if r[key] in labels]
            task = add(
                "inventory",
                f"{kind}_class_counts",
                bid,
                f"为{name}准备{title}：分别统计 {', '.join(labels)} 的记录条数。"
                "返回以原始英文类别为键、整数数量为值的对象。",
                {label: counts[label] for label in labels},
                query=f"{name} {kind} {' '.join(labels)}",
            )
            task["sources"] = oracle.refs(selected)
            task["gold"]["required_sources"] = [f"summary:{bid}"]
            task["gold"]["source_alternatives"] = {f"summary:{bid}": selected}
        selected_parts = diverse([p for p in parts if p["part_no"]], lambda p: p["class"], 2)
        add(
            "inventory",
            "part_identification",
            bid,
            f"采购核对：{selected_parts[0]['uid']} 与 {selected_parts[1]['uid']} "
            "的原始部件编号分别是什么？"
            '返回 {"part_numbers":{"UID":"原始 part_no 字符串"}} 格式的对象。',
            {"part_numbers": {p["uid"]: p["part_no"] for p in selected_parts}},
            [p["uid"] for p in selected_parts],
            [p["uid"] for p in selected_parts],
        )
        common = [p for p in parts if uid("fixation", p["id"]) in oracle.by_uid]
        p = diverse(common, lambda p: p["class"], 1)[0]
        f = oracle.by_uid[uid("fixation", p["id"])]
        add(
            "inventory",
            "typed_id_collision",
            bid,
            f"台账中数字编号 {p['id']} 同时用于部件和连接件。核对 {p['uid']} 与 {f['uid']} 的类别，"
            "返回 part_class 和 fixation_class，保留原始英文类别。",
            {"part_class": p["class"], "fixation_class": f["class"]},
            [p["uid"], f["uid"]],
            [p["uid"], f["uid"]],
        )

        chosen = diverse(
            fixes[5:],
            lambda f: (
                f["class"],
                oracle.by_uid[uid("part", f["fromPartID"])]["class"],
                oracle.by_uid[uid("part", f["toPartID"])]["class"],
            ),
            8,
        )
        f = chosen[0]
        add(
            "connections",
            "fastener_endpoints",
            bid,
            f"变更前核对 {f['uid']} 的两端："
            "返回 from_part、to_part（UID）和 removal_operations（对应操作 UID 列表）。",
            {
                "from_part": uid("part", f["fromPartID"]),
                "to_part": uid("part", f["toPartID"]),
                "removal_operations": [r["uid"] for r in oracle.removals[f["uid"]]],
            },
            [f["uid"]],
            [f["uid"]] + [r["uid"] for r in oracle.removals[f["uid"]]],
        )
        f = chosen[1]
        endpoints = [oracle.by_uid[uid("part", f[k])] for k in ["fromPartID", "toPartID"]]
        add(
            "connections",
            "endpoint_classification",
            bid,
            f"评估 {f['uid']} 的关联范围：读取其两端部件，"
            "返回 from_class、to_class（英文类别）和 same_class（布尔值）。",
            {
                "from_class": endpoints[0]["class"],
                "to_class": endpoints[1]["class"],
                "same_class": endpoints[0]["class"] == endpoints[1]["class"],
            },
            [f["uid"]],
            [f["uid"]] + [p["uid"] for p in endpoints],
        )
        f1, f2 = chosen[2:4]
        ends1 = {uid("part", f1[k]) for k in ["fromPartID", "toPartID"]}
        ends2 = {uid("part", f2[k]) for k in ["fromPartID", "toPartID"]}
        add(
            "connections",
            "shared_endpoints",
            bid,
            f"两个连接件 {f1['uid']}、{f2['uid']} 是否涉及共同部件？"
            "返回 shared_parts（共有部件 UID 列表，若无则空列表）。",
            {"shared_parts": sorted(ends1 & ends2)},
            [f1["uid"], f2["uid"]],
            [f1["uid"], f2["uid"]],
        )
        p = diverse([p for p in parts if oracle.removals[p["uid"]]], lambda p: p["class"], 1)[0]
        removals = oracle.removals[p["uid"]]
        add(
            "connections",
            "part_removal_method",
            bid,
            f"为复核清单补充 {p['uid']} 的已记录移除方法："
            "返回 operation_uids（UID 列表）和 skills（英文技能去重列表）。",
            {
                "operation_uids": [o["uid"] for o in removals],
                "skills": sorted({o["skill_id"] for o in removals}),
            },
            [p["uid"]],
            [p["uid"]] + [o["uid"] for o in removals],
        )
        op = diverse(ops[5:], lambda o: (o["skill_id"], o["target"].split(":")[1]), 1)[0]
        target = oracle.by_uid[op["target"]]
        add(
            "connections",
            "operation_target",
            bid,
            f"审查 {op['uid']} 的操作对象："
            "返回 target_uid、target_kind（part 或 fixation）和 target_class（英文类别）。",
            {
                "target_uid": op["target"],
                "target_kind": op["target"].split(":")[1],
                "target_class": target["class"],
            },
            [op["uid"]],
            [op["uid"], target["uid"]],
        )

        starts = diverse(
            [o for o in ops[6:] if len(oracle.chain(o, 5)) == 5],
            lambda o: [(v["skill_id"], v["target"].split(":")[1]) for v in oracle.chain(o, 5)],
            5,
        )
        for index, family in enumerate(
            ["next_target", "two_successors", "predecessor", "skill_window", "transition"]
        ):
            op = starts[index]
            chain = oracle.chain(op, 5)
            anchors = [op["uid"]]
            if family == "next_target":
                nxt = chain[1]
                target = oracle.by_uid[nxt["target"]]
                question = (
                    f"完成记录操作 {op['uid']} 后，NEXT 紧接的操作及对象是什么？"
                    "返回 next_operation（操作 UID）、target_uid、target_class（英文类别）。"
                )
                expected = {
                    "next_operation": nxt["uid"],
                    "target_uid": nxt["target"],
                    "target_class": target["class"],
                }
                sources = [op["uid"], nxt["uid"], target["uid"]]
            elif family == "two_successors":
                question = (
                    f"按 NEXT 从 {op['uid']} 向后追踪两步（不含当前操作），"
                    "返回 operation_uids 和 target_uids 两个按记录顺序排列的列表。"
                )
                expected = {
                    "operation_uids": [o["uid"] for o in chain[1:3]],
                    "target_uids": [o["target"] for o in chain[1:3]],
                }
                sources = [o["uid"] for o in chain[:3]]
            elif family == "predecessor":
                op = chain[2]
                prev = oracle.previous[op["id"]]
                anchors = [op["uid"]]
                question = (
                    f"检查记录操作 {op['uid']} 的紧邻前序记录，"
                    "返回 previous_operation 和 previous_target（UID）。这里只问已记录顺序。"
                )
                expected = {"previous_operation": prev["uid"], "previous_target": prev["target"]}
                sources = [op["uid"], prev["uid"]]
            elif family == "skill_window":
                question = (
                    f"从 {op['uid']} 起沿 NEXT 取连续四条操作（含当前操作），"
                    "返回 operation_uids 和 skills，两个列表均保持顺序且不去重。"
                )
                expected = {
                    "operation_uids": [o["uid"] for o in chain[:4]],
                    "skills": [o["skill_id"] for o in chain[:4]],
                }
                sources = [o["uid"] for o in chain[:4]]
            else:
                question = (
                    f"{op['uid']} 与其 NEXT 后继是否作用于同一个对象？"
                    "返回 same_target（布尔值）、current_target 和 next_target（UID）。"
                )
                expected = {
                    "same_target": op["target"] == chain[1]["target"],
                    "current_target": op["target"],
                    "next_target": chain[1]["target"],
                }
                sources = [op["uid"], chain[1]["uid"]]
            add(
                "sequence",
                family,
                bid,
                question,
                expected,
                anchors,
                sources,
                ordered=["operation_uids", "target_uids", "skills"],
            )

        f = chosen[4]
        add(
            "scope",
            "torque_absence",
            bid,
            f"仅根据 {f['uid']} 的原始 CSV 行，该行是否给出了拧紧扭矩？"
            "返回 documented（布尔值）和 torque_nm（没有就为 null）。",
            {"documented": False, "torque_nm": None},
            [f["uid"]],
            [f["uid"]],
        )
        year = battery["year"]
        add(
            "scope",
            "catalogue_year_availability",
            bid,
            f"{name} 的电池目录是否记录年份？"
            "返回 documented 和 year，year 为整数；NA 表示未知，此时返回 null。",
            {"documented": year != "NA", "year": int(year) if year != "NA" else None},
            [battery["uid"]],
            [battery["uid"]],
        )
        other_bid = 2 if bid == 1 else 1
        wrong = oracle.rows("fixation", other_bid)[7]
        absence = add(
            "scope",
            "wrong_product",
            bid,
            f"当前产品是{name}。查找连接件原始编号 {wrong['id']}，不要切换产品。"
            "返回 found_in_current_product（布尔值）。",
            {"found_in_current_product": False},
            query=f"{name} fixation {wrong['id']}",
        )
        # Absence is checked against every fixation row in the selected product.
        absence["sources"] = oracle.refs([row["uid"] for row in fixes])
        absence["gold"]["basis"] = "原始 CSV 中当前产品全部连接件均不含所查询的编号"
        op = starts[0]
        add(
            "scope",
            "sequence_not_assembly",
            bid,
            f"查阅 {op['uid']} 后判断：是否能仅把 NEXT 记录倒序就认定为该车型的装配工艺？"
            "返回 can_infer_assembly（布尔值）和 source_scope"
            "（recorded_disassembly 或 manufacturing_plan）。",
            {"can_infer_assembly": False, "source_scope": "recorded_disassembly"},
            [op["uid"]],
            [op["uid"]],
        )
        p = diverse(parts[3:], lambda p: bool(p["part_no"]), 1)[0]
        add(
            "scope",
            "part_number_availability",
            bid,
            f"仅核对 {p['uid']} 的原始 part_no 字段是否有值。"
            "返回 documented 和 part_no；空字段用 null，非空保留原始字符串。",
            {"documented": bool(p["part_no"]), "part_no": p["part_no"] or None},
            [p["uid"]],
            [p["uid"]],
        )

    add_guides(tasks)
    add_workflows(tasks, oracle)
    return tasks


def add_guides(tasks):
    rows = json.loads((DERIVED / "pem/elements.json").read_text(encoding="utf-8"))
    annotations = json.loads((SUITE / "guide-annotations.json").read_text(encoding="utf-8"))
    lookup = {r["uid"]: r for r in rows}
    for index, annotation in enumerate(annotations, 1):
        sources = annotation["evidence_ids"]
        for source in sources:
            assert lookup[source]["page"] == annotation["page"]
        tasks.append(
            {
                "id": f"guide-{index:03d}",
                "category": "guide",
                "family": annotation["family"],
                "split": annotation["split"],
                "group": f"pem-page-{annotation['page']}",
                "business_intent": annotation["intent"],
                "input": {
                    "battery_id": 1,
                    "question": annotation["question"]
                    + " 返回 evidence_uids（覆盖所求全部条目的 UID 列表），"
                    "在 claims 中说明条目内容。",
                    "anchors": [],
                    "search_query": annotation["query"],
                    "guide_page": annotation["page"],
                },
                "gold": {
                    "answer": {"evidence_uids": sources},
                    "required_sources": sources,
                    "ordered_fields": [],
                    "basis": "对照原始 PDF 页及版面选定条目，按 UID 评分定位覆盖",
                },
                "sources": [
                    {
                        "uid": source,
                        "file": "data/sources/pem-module-pack-guide.pdf",
                        "page": annotation["page"],
                        "bbox": lookup[source]["bbox"],
                        "url": "https://publications.rwth-aachen.de/record/973056/",
                    }
                    for source in sources
                ],
            }
        )


def workflow_gold(values):
    """Independent truth table; never calls the application's rule implementation."""
    card, instruction = values["tool_card"], values["instruction"]
    tool_status = (
        "missing"
        if not card or not card["supported_specs"]
        else ("pass" if values["new_spec"] in card["supported_specs"] else "conflict")
    )
    instruction_status = (
        "missing"
        if not instruction
        else ("pass" if instruction["spec"] == values["new_spec"] else "conflict")
    )
    return {
        "tool_status": tool_status,
        "instruction_status": instruction_status,
        "case_status": "awaiting_information"
        if "missing" in (tool_status, instruction_status)
        else "awaiting_review",
        "ready_for_human_review_completion": tool_status == instruction_status == "pass",
        "new_spec": values["new_spec"],
    }


def add_workflows(tasks, oracle):
    names = [
        "正常核对",
        "补充工具卡",
        "补充指导书",
        "纠正工具冲突",
        "更新指导书规格",
        "部分补齐资料",
        "部分解决冲突",
        "变更目标再修订",
        "撤回指导书",
        "修订未解决问题",
    ]
    for family, name in enumerate(names):
        products = [1 + family % 2] + [3 + (family + j * 2) % 8 for j in range(4)]
        for bid in products:
            candidates = [f for f in oracle.rows("fixation", bid) if f["class"] == "screw"]
            target = diverse(
                candidates, lambda f: (f["class"], f["fromPartID"], f["toPartID"]), 10
            )[family]
            task_id = f"workflow-{sum(t['category'] == 'workflow' for t in tasks) + 1:03d}"
            initial = {
                "title": f"{name} · {target['uid']}",
                "battery_id": bid,
                "target_uid": target["uid"],
                "reason": f"模拟业务：{name}；核对连接对象、工具和作业资料。",
                "old_spec": "M6",
                "new_spec": "M8",
                "tool_card": {
                    "id": f"TOOL-{bid}",
                    "revision": "B",
                    "supported_specs": ["M6", "M8"],
                },
                "instruction": {"id": f"WI-{bid}", "revision": "B", "spec": "M8"},
            }
            if family in [1, 5]:
                initial["tool_card"] = None
            if family in [2, 5]:
                initial["instruction"] = None
            if family in [3, 6, 9]:
                initial["tool_card"].update(revision="A", supported_specs=["M6"])
            if family in [4, 6]:
                initial["instruction"].update(revision="A", spec="M6")
            revised = copy.deepcopy(initial)
            if family in [1, 3, 5, 6]:
                revised["tool_card"] = {
                    "id": f"TOOL-{bid}",
                    "revision": "C",
                    "supported_specs": ["M8"],
                }
            if family in [2, 4]:
                revised["instruction"] = {"id": f"WI-{bid}", "revision": "C", "spec": "M8"}
            if family == 7:
                revised["new_spec"] = "M10"
            if family == 8:
                revised["instruction"] = None
            if family == 9:
                revised["tool_card"].update(revision="B", supported_specs=["M4", "M6"])
            values = [initial] if family == 0 else [initial, revised]
            steps = []
            for version, value in enumerate(values, 1):
                expected = workflow_gold(value)
                prefix = f"change:{task_id}:v{version}"
                required = [f"{prefix}:request"]
                if value["tool_card"]:
                    required.append(f"{prefix}:tool-card")
                if value["instruction"]:
                    required.append(f"{prefix}:instruction")
                steps.append(
                    {
                        "input": value,
                        "gold": {
                            "answer": expected,
                            "required_sources": required,
                            "ordered_fields": [],
                        },
                    }
                )
            tasks.append(
                {
                    "id": task_id,
                    "category": "workflow",
                    "family": f"workflow_{family + 1:02d}",
                    "split": "dev" if bid <= 2 else "test",
                    "group": f"battery-{bid}",
                    "business_intent": name,
                    "steps": steps,
                    "input": {
                        "battery_id": bid,
                        "anchors": [target["uid"]],
                        "guide_page": None,
                        "search_query": f"{target['uid']} change tool card instruction",
                        "question": "按当前变更资料评估工具卡、指导书及资料状态。"
                        "返回 tool_status 和 instruction_status"
                        "（pass/conflict/missing）、case_status（awaiting_information/awaiting_review）、"
                        "ready_for_human_review_completion（全部规则通过且可在人工复核后完成，"
                        "布尔值）和 new_spec。",
                    },
                    "gold": {
                        "basis": "独立模拟状态表；正常情形一轮，其余情形修订后第二轮，"
                        "两轮共同构成一个案例"
                    },
                    "sources": oracle.refs(
                        [
                            target["uid"],
                            uid("part", target["fromPartID"]),
                            uid("part", target["toPartID"]),
                        ]
                    ),
                }
            )


def write_suite():
    tasks = build()
    assert len(tasks) == 300 and len({t["id"] for t in tasks}) == 300
    counts = Counter((t["category"], t["split"]) for t in tasks)
    assert all(counts[c, "dev"] == 10 and counts[c, "test"] == 40 for c in CATEGORIES), counts
    groups = defaultdict(set)
    for task in tasks:
        groups[task["group"]].add(task["split"])
    assert all(len(splits) == 1 for splits in groups.values()), groups
    SUITE.mkdir(exist_ok=True)
    payload = json.dumps(tasks, ensure_ascii=False, indent=2) + "\n"
    (SUITE / "cases.json").write_text(payload, encoding="utf-8")
    manifest = {
        "cases": len(tasks),
        "splits": dict(Counter(t["split"] for t in tasks)),
        "families": len({t["family"] for t in tasks}),
        "category_families": {
            c: len({t["family"] for t in tasks if t["category"] == c}) for c in CATEGORIES
        },
        "sha256": hashlib.sha256(payload.encode()).hexdigest(),
        "source_sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [
                *RAW.glob("*.csv"),
                SUITE / "guide-annotations.json",
                ROOT / "data/sources/pem-module-pack-guide.pdf",
            ]
        },
    }
    (SUITE / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# BatteryCopilot 300 案例目录",
        "",
        "开发集 60；测试集 240。完整答案、输入和来源见 cases.json。",
        "",
    ]
    for category, title in CATEGORIES.items():
        lines += [f"## {title}", ""]
        for task in tasks:
            if task["category"] != category:
                continue
            lines += [
                f"### {task['id']} · {task['split']} · {task['business_intent']}",
                "",
                task["input"]["question"],
                "",
            ]
            gold = (
                [s["gold"]["answer"] for s in task["steps"]]
                if "steps" in task
                else task["gold"]["answer"]
            )
            lines += [
                "答案：`" + json.dumps(gold, ensure_ascii=False) + "`",
                "",
                "来源："
                + "; ".join(
                    f"{s['file']}:{s.get('line', s.get('page'))}" for s in task["sources"][:6]
                ),
                "",
            ]
    (SUITE / "catalogue.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    write_suite()
