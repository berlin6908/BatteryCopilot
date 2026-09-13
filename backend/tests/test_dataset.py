from pathlib import Path

from battery_copilot.dataset import load_kit

RAW = Path(__file__).resolve().parents[2] / "data/sources/kit-battery"


def test_real_kit_mapping_keeps_typed_ids_and_original_direction():
    graph = load_kit(RAW)
    assert len(graph.nodes) == 4750
    assert len(graph.edges) == 10803
    nodes = {node["uid"]: node for node in graph.nodes}
    assert nodes["kit-v1:part:1000"]["name"] == "housing cover"
    assert nodes["kit-v1:fixation:1000"]["name"] == "screw"
    assert ("kit-v1:part:1000", "FROM_PART", "kit-v1:fixation:1000") in graph.edges
    assert ("kit-v1:fixation:1000", "TO_PART", "kit-v1:part:1001") in graph.edges
    assert nodes["kit-v1:part:1000"]["source_line"] == 2
    assert nodes["kit-v1:part:1000"]["visible_parts"] == ["housing cover"]
    assert nodes["kit-v1:battery:6"]["source_urls"] == []


def test_all_ten_recorded_sequences_preserve_csv_successors():
    graph = load_kit(RAW)
    nodes = {node["uid"]: node for node in graph.nodes}
    operations = [n for n in graph.nodes if n["kind"] == "Operation"]
    assert len(operations) == 2281
    expected_counts = [375, 168, 387, 158, 167, 211, 131, 328, 183, 173]
    for battery_id, expected in enumerate(expected_counts, 1):
        sequence = sorted(
            [n for n in operations if n["battery_id"] == battery_id],
            key=lambda n: n["sequence_index"],
        )
        assert len(sequence) == expected
        assert [n["sequence_index"] for n in sequence] == list(range(1, expected + 1))
        for left, right in zip(sequence, sequence[1:]):
            assert (left["uid"], "NEXT", right["uid"]) in graph.edges
    for source, relation, target in graph.edges:
        assert source in nodes and target in nodes
        assert nodes[source]["battery_id"] == nodes[target]["battery_id"]
