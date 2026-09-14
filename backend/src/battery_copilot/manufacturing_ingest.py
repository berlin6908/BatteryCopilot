"""Import the pinned KIproBatt RDF archive and its Maccor cycle statistics."""

import argparse
import csv
import hashlib
import io
import json
import zipfile
from collections import Counter
from pathlib import Path

import httpx
from rdflib import RDF, Graph, Namespace, URIRef

from battery_copilot.graph import graph
from battery_copilot.settings import ROOT

VERSION = "kiprobatt-v0.3.2"
SOURCE_URL = "https://zenodo.org/records/11895571"
DOWNLOAD_URL = (
    "https://zenodo.org/api/records/11895571/files/KIproBatt/kiprobatt-dataset-v0.3.2.zip/content"
)
ARCHIVE = ROOT / "data/sources/kiprobatt/dataset-v0.3.2.zip"
ARCHIVE_MD5 = "03dbcb62fcf17f843b90709d07668450"
BASE = "https://kiprobatt.de/id/"
P = Namespace(BASE + "Property-3A")
C = Namespace(BASE + "Category-3A")
KINDS = {
    C["Labprocess-2FInstance"]: "process",
    C.ProcessStepInstance: "step",
    C["LabProcess-2FParameter-2FInstance"]: "parameter",
    C["LabProcess-2FObject"]: "object",
}
RELATIONS = {
    "IsObjectParameterOf": "FOR_OBJECT",
    "IsProcessParameterOf": "FOR_STEP",
    "IsOutputOf": "OUTPUT_OF",
    "IsSubprocessOf": "STEP_OF",
    "HasPredecessor": "SOURCE_OBJECT",
    "HasObject": "HAS_OBJECT",
    "HasOutput": "HAS_OUTPUT",
    "HasInput": "HAS_INPUT",
}


def uid(iri: str) -> str:
    return "ki:" + hashlib.sha256(str(iri).encode()).hexdigest()[:20]


def display(value) -> str:
    """Display only; RDF identifiers are retained unchanged for identity and links."""
    return str(value).removeprefix(BASE).removesuffix("@en").replace("_", " ")


def parse_stats(text: str, file_uid: str) -> dict:
    lines = text.splitlines()
    header = next(i for i, line in enumerate(lines) if line.startswith("Cycle\t"))
    metadata = {}
    for line in lines[:header]:
        key, separator, value = line.partition(":")
        if separator:
            metadata[key.strip()] = value.strip()
    rows = []
    reader = csv.DictReader(io.StringIO("\n".join(lines[header:])), delimiter="\t")
    for number, raw in enumerate(reader, header + 2):
        values = {
            k: float(v.replace(",", ".")) if v.strip() else None
            for k, v in raw.items()
            if k and v is not None
        }
        rows.append(
            {"uid": f"{file_uid}:L{number}", "source_line": number, "values": values, "raw": raw}
        )
    return {"metadata": metadata, "rows": rows}


def load_archive(path: Path):
    if hashlib.md5(path.read_bytes()).hexdigest() != ARCHIVE_MD5:
        raise ValueError("KIproBatt archive checksum differs from the pinned Zenodo release.")
    rdf = Graph()
    sources = {}
    tests = {}
    jsonld_count = 0
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if "/data/" in name and name.endswith(".jsonld"):
                document = json.loads(archive.read(name).decode("cp1252"))
                part = Graph().parse(data=json.dumps(document), format="json-ld")
                rdf += part
                sources.update({s: "data/" + name.split("/data/", 1)[1] for s in part.subjects()})
                jsonld_count += 1
            elif "/files/" in name and "-STATS-" in name and name.endswith(".txt"):
                filename = name.rsplit("/", 1)[-1]
                data = archive.read(name)
                file_uid = uid("files/" + filename)
                tests[filename] = {
                    "uid": file_uid,
                    "name": filename,
                    "kind": "test",
                    "source_file": "files/" + filename,
                    "source_url": SOURCE_URL,
                    "source_kind": "manufacturing",
                    "snapshot": VERSION,
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "data_json": json.dumps(parse_stats(data.decode("cp1252"), file_uid)),
                }
    subjects = {s for s in rdf.subjects() if isinstance(s, URIRef)}
    records, links, test_links = [], [], []
    for subject in sorted(subjects):
        types = set(rdf.objects(subject, RDF.type))
        kind = next((name for category, name in KINDS.items() if category in types), "reference")
        properties = {}
        for predicate, value in rdf.predicate_objects(subject):
            properties.setdefault(str(predicate), []).append(str(value))
        properties = {k: sorted(v) for k, v in sorted(properties.items())}
        names = list(rdf.objects(subject, P.HasName)) or list(rdf.objects(subject, P.HasLabel))
        records.append(
            {
                "uid": uid(subject),
                "iri": str(subject),
                "kind": kind,
                "name": display(names[0]) if names else display(subject),
                "values": sorted(display(v) for v in rdf.objects(subject, P.HasValue)),
                "instance_types": sorted(str(v) for v in rdf.objects(subject, P.IsInstanceOf)),
                "source_file": sources[subject],
                "source_url": SOURCE_URL,
                "source_kind": "manufacturing",
                "snapshot": VERSION,
                "raw_record": json.dumps({"@id": str(subject), **properties}, ensure_ascii=False),
            }
        )
        for predicate, relation in RELATIONS.items():
            for target in rdf.objects(subject, P[predicate]):
                if target in subjects:
                    links.append(
                        {"source": uid(subject), "target": uid(target), "relation": relation}
                    )
        for file_iri in rdf.objects(subject, P.HasFile):
            filename = str(file_iri).rsplit("/", 1)[-1].removeprefix("File-3A")
            if filename in tests:
                for cell in rdf.objects(subject, P.IsObjectParameterOf):
                    if cell in subjects:
                        test_links.append(
                            {
                                "cell": uid(cell),
                                "test": tests[filename]["uid"],
                                "evidence": uid(subject),
                            }
                        )
    counts = dict(Counter(r["kind"] for r in records))
    return (
        records,
        links,
        list(tests.values()),
        test_links,
        {
            "snapshot": VERSION,
            "jsonld_files": jsonld_count,
            "rdf_triples": len(rdf),
            "records": len(records),
            "kinds": counts,
            "stats_files": len(tests),
            "test_linked_objects": len({link["cell"] for link in test_links}),
            "linked_stats_files": len({link["test"] for link in test_links}),
        },
    )


def import_archive(path: Path):
    records, links, tests, test_links, report = load_archive(path)
    db = graph()
    db.query(
        "CREATE CONSTRAINT evidence_uid IF NOT EXISTS FOR (n:Evidence) REQUIRE n.uid IS UNIQUE"
    )
    for label in ("MfgRecord", "MfgTest", "MfgReport"):
        db.query(
            f"CREATE CONSTRAINT {label}_uid IF NOT EXISTS FOR (n:{label}) REQUIRE n.uid IS UNIQUE"
        )
    for label, rows in (("MfgRecord", records), ("MfgTest", tests)):
        for offset in range(0, len(rows), 500):
            db.query(
                f"UNWIND $rows AS row MERGE (n:Evidence:{label} {{uid:row.uid}}) SET n = row",
                rows=rows[offset : offset + 500],
            )
    for relation in RELATIONS.values():
        rows = [r for r in links if r["relation"] == relation]
        for offset in range(0, len(rows), 1000):
            db.query(
                f"""UNWIND $rows AS r
                MATCH (a:MfgRecord {{uid:r.source}}), (b:MfgRecord {{uid:r.target}})
                MERGE (a)-[:{relation}]->(b)""",
                rows=rows[offset : offset + 1000],
            )
    db.query("""MATCH (p:MfgRecord {kind:'parameter'})-[:FOR_OBJECT]->(output:MfgRecord),
                      (p)-[:SOURCE_OBJECT]->(input:MfgRecord)
                MERGE (output)-[:DERIVED_FROM {evidence_uid:p.uid}]->(input)""")
    db.query(
        """UNWIND $rows AS r
        MATCH (cell:MfgRecord {uid:r.cell}), (test:MfgTest {uid:r.test})
        MERGE (cell)-[:HAS_TEST {evidence_uid:r.evidence}]->(test)""",
        rows=test_links,
    )
    db.query(
        "MERGE (d:MfgDataset {uid:$version}) SET d.report=$report",
        version=VERSION,
        report=json.dumps(report),
    )
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=ARCHIVE)
    args = parser.parse_args()
    if not args.archive.exists():
        args.archive.parent.mkdir(parents=True, exist_ok=True)
        with httpx.stream("GET", DOWNLOAD_URL, follow_redirects=True, timeout=120) as response:
            response.raise_for_status()
            with args.archive.open("wb") as output:
                for chunk in response.iter_bytes():
                    output.write(chunk)
    print(json.dumps(import_archive(args.archive), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
