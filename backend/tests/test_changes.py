import pytest
from battery_copilot.changes import assess_tool_fit


@pytest.mark.parametrize(
    ("new_spec", "supported", "expected"),
    [("M8", ["M6"], "conflict"), ("M6", ["M6"], "compatible"), ("M8", [], "unknown")],
)
def test_tool_fit_distinguishes_conflict_from_missing_information(new_spec, supported, expected):
    assert assess_tool_fit(new_spec, supported)["status"] == expected
