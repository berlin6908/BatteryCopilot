"""Explicit mapping of the KIT release, including record-level provenance."""

import csv
import json
from dataclasses import dataclass
from pathlib import Path

SNAPSHOT = "kit-v1"


def uid(kind: str, raw_id: str | int) -> str:
    return f"{SNAPSHOT}:{kind.lower()}:{raw_id}"


@dataclass
class KitGraph:
    nodes: list[dict]
    edges: list[tuple[str, str, str]]


def load_kit(directory: Path) -> KitGraph:
    nodes: dict[str, dict] = {}
    edges: list[tuple[str, str, str]] = []
    tables = {
        "battery_catalogue.csv": "Battery",
        "parts.csv": "Part",
        "fixations.csv": "Fixation",
        "operations.csv": "Operation",
    }
    for filename, kind in tables.items():
        with (directory / filename).open(encoding="utf-8-sig", newline="") as handle:
            for line, row in enumerate(csv.DictReader(handle), 2):
                node = {
                    "uid": uid(kind, row["id"]),
                    "kind": kind,
                    "raw_id": int(row["id"]),
                    "snapshot_id": SNAPSHOT,
                    "source_kind": "record",
                    "source_file": filename,
                    "source_line": line,
                    "raw_record": json.dumps(row, ensure_ascii=False),
                    "name": row.get("name") or row.get("class") or row.get("skill_id"),
                    "details": row.get("details", ""),
                }
                if kind == "Battery":
                    node.update(
                        battery_id=int(row["id"]),
                        year=row["year"],
                        source_urls=[v.strip() for v in row["info;"].split(";") if v.strip()],
                    )
                elif kind in ("Part", "Fixation"):
                    node["battery_id"] = int(row["battery_id"])
                    edges.append((uid("Battery", row["battery_id"]), "CONTAINS", node["uid"]))
                    if kind == "Part":
                        node.update(
                            part_no=row["part_no"], visible_parts=row["visible_parts"].split("+")
                        )
                    else:
                        edges.extend(
                            [
                                (uid("Part", row["fromPartID"]), "FROM_PART", node["uid"]),
                                (node["uid"], "TO_PART", uid("Part", row["toPartID"])),
                            ]
                        )
                else:
                    target = (
                        uid("Part", row["part_id"])
                        if row["part_id"]
                        else uid("Fixation", row["fixation_id"])
                    )
                    node.update(target_uid=target, battery_id=nodes[target]["battery_id"])
                    edges.append((target, "REMOVED_BY", node["uid"]))
                    if row["next_op_id"]:
                        edges.append((node["uid"], "NEXT", uid("Operation", row["next_op_id"])))
                nodes[node["uid"]] = node

    successors = {a: b for a, rel, b in edges if rel == "NEXT"}
    has_previous = set(successors.values())
    for head in [
        n for n in nodes.values() if n["kind"] == "Operation" and n["uid"] not in has_previous
    ]:
        current, position = head["uid"], 1
        while current:
            if "sequence_index" in nodes[current]:
                raise ValueError(f"Repeated operation in recorded sequence: {current}")
            nodes[current]["sequence_index"] = position
            current, position = successors.get(current), position + 1

    adjacent: dict[str, list[str]] = {key: [] for key in nodes}
    for source, relation, target in edges:
        adjacent[source].append(f"{relation} -> {target}")
        adjacent[target].append(f"{relation} <- {source}")
    for node in nodes.values():
        battery = nodes[uid("Battery", node["battery_id"])]
        node["text"] = (
            f"{battery['name']} | {node['kind']} {node['raw_id']}: {node['name']}. "
            f"{node['details']} {node.get('part_no', '')}. " + "; ".join(adjacent[node["uid"]])
        )
    return KitGraph(list(nodes.values()), edges)
