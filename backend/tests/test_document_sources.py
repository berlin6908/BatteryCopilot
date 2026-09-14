import hashlib

import pypdfium2 as pdfium
import pytest
from battery_copilot.agent import read_evidence
from battery_copilot.document_sources import region_uid
from battery_copilot.documents import project_regions
from battery_copilot.guide_evaluation import coverage
from battery_copilot.settings import PDF
from docling_core.types.doc import BoundingBox, DoclingDocument, ProvenanceItem, Size


def test_region_scoring_accepts_split_evidence_without_double_counting_overlap():
    target = [0, 0, 1, 1]
    half = [0, 0, 1, 0.5]
    assert coverage(target, [half, half]) == 0.5
    assert coverage(target, [half, [0, 0.5, 1, 1]]) == 1
    assert coverage(target, [[2, 2, 3, 3]]) == 0


@pytest.mark.integration
def test_pdf_reference_survives_reordering_and_splitting_with_embedded_figure_text():
    """Use the real guide; parser changes must not destroy an existing region citation."""
    digest = hashlib.sha256(PDF.read_bytes()).hexdigest()
    with pdfium.PdfDocument(PDF) as pdf:
        width, height = pdf[23].get_size()

        def provenance(bbox):
            left, top, right, bottom = bbox
            return ProvenanceItem(
                page_no=24,
                charspan=(0, 0),
                bbox=BoundingBox(
                    l=left * width, t=top * height, r=right * width, b=bottom * height
                ),
            )

        doc = DoclingDocument(name="layout-regression")
        doc.add_page(page_no=24, size=Size(width=width, height=height))
        doc.add_text(
            label="section_header",
            text="Layout planning",
            prov=provenance([0.42, 0.462, 0.58, 0.476]),
        )
        picture = doc.add_picture(prov=provenance([0.059919, 0.491448, 0.938376, 0.896832]))
        original = next(r for r in project_regions(doc, pdf, digest) if r["kind"] == "picture")
        assert "Buffer zones" in original["text"] and "Rework stations" in original["text"]
        assert original["name"] == "Layout planning"

        # Insert an unrelated element before the figure: traversal indexes change.
        doc.add_text(label="text", text="unrelated", prov=provenance([0.1, 0.1, 0.3, 0.12]))
        doc.body.children.insert(0, doc.body.children.pop())
        reordered = next(r for r in project_regions(doc, pdf, digest) if r["kind"] == "picture")
        assert reordered["uid"] == original["uid"]

        # A future parser splits the original figure in two.
        picture.prov = [provenance([0.059919, 0.491448, 0.938376, 0.7])]
        doc.add_picture(prov=provenance([0.059919, 0.7, 0.938376, 0.896832]))
        assert original["uid"] not in {r["uid"] for r in project_regions(doc, pdf, digest)}

    # Source resolution needs neither the current parser output nor Neo4j.
    source = read_evidence(original["uid"], 1)
    assert "Buffer zones" in source["text"] and "Rework stations" in source["text"]
    assert source["bbox"] == pytest.approx(original["bbox"], abs=1e-6)
    wrong_version = region_uid("0" * 64, 24, original["bbox"])
    with pytest.raises(ValueError, match="PDF版本"):
        read_evidence(wrong_version, 1)
