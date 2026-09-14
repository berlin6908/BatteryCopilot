"""Parse the local guide with Docling; preserve page and element provenance."""

import argparse
import hashlib
import json
import time
from contextlib import closing

import pypdfium2 as pdfium

from battery_copilot.document_sources import region_text, region_uid
from battery_copilot.graph import graph
from battery_copilot.settings import DERIVED, PDF


def project_regions(doc, pdf, digest):
    from docling_core.types.doc import PictureItem, TableItem

    rows, page_titles, headers = [], {}, {}
    for item, _ in doc.iterate_items():
        if getattr(item, "label", None) in ("section_header", "title") and item.prov:
            for prov in item.prov:
                box = prov.bbox.to_top_left_origin(doc.pages[prov.page_no].size.height)
                headers.setdefault(prov.page_no, []).append((item.text, box))
                page_titles.setdefault(prov.page_no, item.text)
    for item, _ in doc.iterate_items():
        if not getattr(item, "prov", None):
            continue
        label = item.label.value
        for prov in item.prov:
            page = doc.pages[prov.page_no]
            title = page_titles.get(prov.page_no, PDF.stem)
            box = prov.bbox.to_top_left_origin(page.size.height)
            bbox = [
                box.l / page.size.width,
                box.t / page.size.height,
                box.r / page.size.width,
                box.b / page.size.height,
            ]
            text = getattr(item, "text", "")
            if isinstance(item, TableItem):
                text = item.export_to_markdown(doc=doc)
            if isinstance(item, PictureItem):
                with closing(pdf[prov.page_no - 1]) as source_page:
                    text = region_text(source_page, bbox)
                text = f"Figure on page {prov.page_no}. Embedded PDF text:\n{text}"
            if not text.strip():
                continue
            # ponytail: nearest overlapping heading; nested layouts need visual review.
            candidates = [
                (name, b)
                for name, b in headers.get(prov.page_no, [])
                if b.b <= box.t + 1 and b.l < box.r and b.r > box.l
            ]
            heading = (
                min(candidates, key=lambda h: (round((box.t - h[1].b) / 6), abs(box.l - h[1].l)))[0]
                if candidates
                else title
            )
            if label in ("section_header", "title"):
                heading = text
            rows.append(
                {
                    "uid": region_uid(digest, prov.page_no, bbox),
                    "kind": label,
                    "source_kind": "guide",
                    "source_file": PDF.name,
                    "source_sha256": digest,
                    "page": prov.page_no,
                    "name": f"{title} / {heading}" if heading != title else title,
                    "text": "\n".join(dict.fromkeys([title, heading, text])),
                    "element_ref": item.self_ref,
                    "bbox": bbox,
                    "page_width": page.size.width,
                    "page_height": page.size.height,
                    "image_url": f"/api/documents/pem/pages/{prov.page_no}.png?v={digest}",
                }
            )
    return rows


def main():
    from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling_core.types.doc import DoclingDocument

    started = time.perf_counter()
    output = DERIVED / "pem"
    output.mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--reuse-parsed", action="store_true", help="Reindex existing Docling JSON")
    args = parser.parse_args()
    options = PdfPipelineOptions()
    options.do_ocr = False  # This source is a born-digital PDF with an embedded text layer.
    options.generate_page_images = True
    options.generate_picture_images = True
    options.images_scale = 1.5
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=options, backend=PyPdfiumDocumentBackend
            )
        }
    )
    if args.reuse_parsed:
        doc = DoclingDocument.load_from_json(output / "docling.json")
    else:
        doc = converter.convert(PDF).document
        doc.save_as_json(output / "docling.json")
    digest = hashlib.sha256(PDF.read_bytes()).hexdigest()
    with pdfium.PdfDocument(PDF) as pdf:
        rows = project_regions(doc, pdf, digest)
    for page_no, page in doc.pages.items():
        page.image.pil_image.save(output / f"page-{page_no}.png")
    (output / "elements.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    db = graph()
    # These are derived index entries; reports retain their own evidence snapshots.
    db.query("MATCH (n:Guide) DETACH DELETE n")
    db.query(
        "UNWIND $rows AS row MERGE (n:Evidence:Guide {uid:row.uid}) SET n += row,n.embedding=null",
        rows=rows,
    )
    db.query(
        "MERGE (d:Document {uid:'pem'}) SET d.name=$name,d.source_kind='guide' "
        "WITH d MATCH (e:Guide) MERGE (d)-[:HAS_EVIDENCE]->(e)",
        name=PDF.name,
    )
    report = {
        "pages": len(doc.pages),
        "elements": len(rows),
        "seconds": round(time.perf_counter() - started, 2),
        "parser": "Docling StandardPdfPipeline",
        "backend": "PyPdfiumDocumentBackend",
        "reused_parsed_document": args.reuse_parsed,
        "ocr": False,
        "source_sha256": digest,
    }
    (output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report))
    db.driver.close()


if __name__ == "__main__":
    main()
