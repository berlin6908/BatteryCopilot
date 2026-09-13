import pytest
from battery_copilot.api import app
from battery_copilot.graph import graph
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def test_real_graph_api_and_scenarios_keep_evidence_and_product_scope():
    with TestClient(app) as client:
        counts = client.get("/api/overview").json()["counts"]
        assert counts == {"Battery": 10, "Part": 563, "Fixation": 1896, "Operation": 2281}
        local = client.get("/api/graph/kit-v1:fixation:1000?battery_id=1").json()
        assert {n["uid"] for n in local["nodes"]} == {
            "kit-v1:fixation:1000",
            "kit-v1:part:1000",
            "kit-v1:part:1001",
            "kit-v1:operation:1000",
        }
        assert client.get("/api/graph/kit-v1:fixation:1000?battery_id=2").status_code == 400
        sequence = client.get("/api/sequence?battery_id=1&target_uid=kit-v1:fixation:1000").json()
        assert sequence["total"] == 375
        assert sequence["items"][0]["uid"] == "kit-v1:operation:1000"
        old = client.get("/api/evidence/kit-v1:fixation:1000?battery_id=1").json()
        conflict = client.get("/api/scenarios/demo-change-01/report?battery_id=1").json()
        resolved = client.get("/api/scenarios/demo-change-02/report?battery_id=1").json()
        assert conflict["check"]["status"] == "conflict"
        assert resolved["check"]["status"] == "compatible"
        assert client.get("/api/scenarios/demo-change-01/report?battery_id=2").status_code == 400
        assert old == client.get("/api/evidence/kit-v1:fixation:1000?battery_id=1").json()
        pages = client.get("/api/documents/pem/elements?page=18").json()
        assert any("Mounting the modules" in e["text"] for e in pages)
        left = next(e for e in pages if "Correct alignment of the modules" in e["text"])
        right = next(e for e in pages if "Positioning accuracy of the cooling" in e["text"])
        assert "Process parameters & requirements" in left["name"]
        assert "Quality parameters" in right["name"]
        assert all(e["page"] == 18 and len(e["bbox"]) == 4 for e in pages)
        assert client.get("/api/documents/pem/pages/18.png").headers["content-type"] == "image/png"
    graph.cache_clear()
