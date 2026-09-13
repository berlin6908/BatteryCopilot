"""Run: uv run python -m battery_copilot.ingest"""

import json

from battery_copilot.dataset import load_kit
from battery_copilot.graph import graph
from battery_copilot.settings import DERIVED, RAW


def main():
    data = load_kit(RAW)
    db = graph()
    db.query("CREATE INDEX record_uid IF NOT EXISTS FOR (n:Record) ON (n.uid)")
    db.query(
        "CREATE CONSTRAINT evidence_uid IF NOT EXISTS FOR (n:Evidence) REQUIRE n.uid IS UNIQUE"
    )
    db.query(
        "CREATE INDEX record_scope IF NOT EXISTS FOR (n:Record) ON (n.snapshot_id,n.battery_id)"
    )
    for kind in ("Battery", "Part", "Fixation", "Operation"):
        db.query(
            f"UNWIND $rows AS row MERGE (n:Evidence:Record:{kind} {{uid:row.uid}}) SET n += row",
            rows=[n for n in data.nodes if n["kind"] == kind],
        )
    for relation in ("CONTAINS", "FROM_PART", "TO_PART", "REMOVED_BY", "NEXT"):
        db.query(
            "UNWIND $rows AS row MATCH (a:Record {uid:row.source}),(b:Record {uid:row.target}) "
            f"MERGE (a)-[:{relation}]->(b)",
            rows=[{"source": a, "target": b} for a, rel, b in data.edges if rel == relation],
        )
    report = db.overview()
    report["relationships"] = db.query(
        "MATCH (:Record {snapshot_id:$snapshot})-[r]->(:Record {snapshot_id:$snapshot}) "
        "RETURN count(r) AS count"
    )[0]["count"]
    DERIVED.mkdir(parents=True, exist_ok=True)
    (DERIVED / "import-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    db.driver.close()


if __name__ == "__main__":
    main()
