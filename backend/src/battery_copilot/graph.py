"""Small, parameterized domain queries shared by API and Agent tools."""

from functools import lru_cache

from neo4j import GraphDatabase

from battery_copilot.settings import SNAPSHOT, settings

NODE = "n{.*, embedding: null, raw_record: null}"


class Graph:
    def __init__(self):
        config = settings()
        self.driver = GraphDatabase.driver(
            config.neo4j_uri, auth=(config.neo4j_user, config.neo4j_password)
        )

    def query(self, cypher: str, **params) -> list[dict]:
        records, _, _ = self.driver.execute_query(
            cypher, parameters_={"snapshot": SNAPSHOT, **params}, database_="neo4j"
        )
        return [r.data() for r in records]

    def overview(self) -> dict:
        counts = self.query(
            "MATCH (n:Record {snapshot_id:$snapshot}) RETURN n.kind AS kind, count(*) AS count"
        )
        evidence = self.query("MATCH (n:Evidence {source_kind:'guide'}) RETURN count(n) AS count")
        return {
            "counts": {r["kind"]: r["count"] for r in counts},
            "document_elements": evidence[0]["count"],
            "snapshot_id": SNAPSHOT,
        }

    def batteries(self) -> list[dict]:
        return self.query(
            "MATCH (n:Battery {snapshot_id:$snapshot}) "
            "OPTIONAL MATCH (n)-[:CONTAINS]->(p:Part) "
            "WITH n,count(p) AS parts "
            "OPTIONAL MATCH (n)-[:CONTAINS]->(f:Fixation) "
            "WITH n,parts,count(f) AS fixations "
            "RETURN n{.*,embedding:null,raw_record:null} AS battery,parts,fixations "
            "ORDER BY n.raw_id"
        )

    def entities(
        self, battery_id: int, query: str = "", kind: str = "Part", limit: int = 40
    ) -> list:
        return [
            r["node"]
            for r in self.query(
                "MATCH (n:Record {snapshot_id:$snapshot,battery_id:$battery_id}) "
                "WHERE ($kind = '' OR n.kind = $kind) AND "
                "(toLower(n.name) CONTAINS toLower($q) OR toString(n.raw_id) = $q "
                "OR toLower(coalesce(n.part_no,'')) CONTAINS toLower($q)) "
                f"RETURN {NODE} AS node ORDER BY n.raw_id LIMIT $limit",
                battery_id=battery_id,
                q=query,
                kind=kind,
                limit=limit,
            )
        ]

    def record(self, uid: str, battery_id: int | None = None) -> dict:
        rows = self.query(
            "MATCH (n:Evidence {uid:$uid}) "
            "WHERE $battery_id IS NULL OR n.battery_id=$battery_id OR n.source_kind='guide' "
            "RETURN n{.*,embedding:null} AS node",
            uid=uid,
            battery_id=battery_id,
        )
        if not rows:
            raise ValueError("当前产品中找不到该证据。")
        return rows[0]["node"]

    def neighborhood(self, uid: str, battery_id: int) -> dict:
        center = self.record(uid, battery_id)
        rows = self.query(
            "MATCH (n:Record {uid:$uid,battery_id:$battery_id,snapshot_id:$snapshot}) "
            "MATCH (n)-[r:FROM_PART|TO_PART|REMOVED_BY]-(m:Record) "
            "RETURN m{.*,embedding:null,raw_record:null} AS node, "
            "startNode(r).uid AS source,type(r) AS relation,endNode(r).uid AS target "
            "ORDER BY m.raw_id LIMIT 40",
            uid=uid,
            battery_id=battery_id,
        )
        # ponytail: one-hop, at most 40 neighbors; paginate only when larger neighborhoods matter.
        return {
            "nodes": [center] + [r["node"] for r in rows],
            "edges": [{k: r[k] for k in ("source", "relation", "target")} for r in rows],
        }

    def sequence(
        self, battery_id: int, offset: int = 0, limit: int = 25, target_uid: str = ""
    ) -> dict:
        if target_uid:
            rows = self.query(
                "MATCH (n:Record {uid:$uid,battery_id:$battery_id}) "
                "OPTIONAL MATCH (n)-[:REMOVED_BY]->(o:Operation) "
                "RETURN coalesce(o.sequence_index,n.sequence_index) AS position "
                "ORDER BY position LIMIT 1",
                uid=target_uid,
                battery_id=battery_id,
            )
            if not rows or rows[0]["position"] is None:
                raise ValueError("该对象没有已记录的拆解操作。")
            offset = max(0, rows[0]["position"] - 4)
        rows = self.query(
            "MATCH (n:Operation {snapshot_id:$snapshot,battery_id:$battery_id}) "
            f"RETURN {NODE} AS node ORDER BY n.sequence_index SKIP $offset LIMIT $limit",
            battery_id=battery_id,
            offset=offset,
            limit=limit,
        )
        total = self.query(
            "MATCH (n:Operation {snapshot_id:$snapshot,battery_id:$battery_id}) "
            "RETURN count(n) AS total",
            battery_id=battery_id,
        )[0]["total"]
        return {
            "items": [r["node"] for r in rows],
            "total": total,
            "offset": offset,
            "scope": "recorded_disassembly_sequence",
        }

    def composition(self, battery_id: int) -> list:
        return self.query(
            "MATCH (n:Record {snapshot_id:$snapshot,battery_id:$battery_id}) "
            "WHERE n.kind IN ['Part','Fixation','Operation'] "
            "RETURN n.kind AS kind,n.name AS name,count(n) AS count "
            "ORDER BY kind,count DESC,name",
            battery_id=battery_id,
        )


@lru_cache
def graph() -> Graph:
    return Graph()
