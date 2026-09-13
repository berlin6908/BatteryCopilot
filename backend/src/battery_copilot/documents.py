"""Parse the local guide with Docling; preserve page and element provenance."""

import argparse
import json
import time

from battery_copilot.graph import graph
from battery_copilot.settings import DERIVED, PDF


def main():
    from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling_core.types.doc import DoclingDocument, PictureItem, TableItem

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
    rows, page_titles, headers = [], {}, {}
    for item, _ in doc.iterate_items():
        if getattr(item, "label", None) in ("section_header", "title") and item.prov:
            for prov in item.prov:
                box = prov.bbox.to_top_left_origin(doc.pages[prov.page_no].size.height)
                headers.setdefault(prov.page_no, []).append((item.text, box))
                page_titles.setdefault(prov.page_no, item.text)
    for index, (item, _) in enumerate(doc.iterate_items()):
        if not hasattr(item, "prov") or not item.prov:
            continue
        label = str(item.label.value)
        text = getattr(item, "text", "")
        if isinstance(item, TableItem):
            text = item.export_to_markdown(doc=doc)
        if isinstance(item, PictureItem):
            text = f"Figure on page {item.prov[0].page_no}; inspect the highlighted source region."
        if not text.strip():
            continue
        for prov_index, prov in enumerate(item.prov):
            page = doc.pages[prov.page_no]
            title = page_titles.get(prov.page_no, PDF.stem)
            box = prov.bbox.to_top_left_origin(page.size.height)
            # ponytail: same-page column geometry; nested layouts still need visual review.
            candidates = [
                (name, b)
                for name, b in headers.get(prov.page_no, [])
                if b.b <= box.t + 1 and b.l <= box.l + 12
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
                    "uid": f"pem:p{prov.page_no}:e{index}:{prov_index}",
                    "kind": label,
                    "source_kind": "guide",
                    "source_file": PDF.name,
                    "page": prov.page_no,
                    "name": f"{title} / {heading}" if heading != title else title,
                    "text": "\n".join(dict.fromkeys([title, heading, text])),
                    "element_ref": item.self_ref,
                    "bbox": [
                        box.l / page.size.width,
                        box.t / page.size.height,
                        box.r / page.size.width,
                        box.b / page.size.height,
                    ],
                    "page_width": page.size.width,
                    "page_height": page.size.height,
                    "image_url": f"/api/documents/pem/pages/{prov.page_no}.png",
                }
            )
    for page_no, page in doc.pages.items():
        page.image.pil_image.save(output / f"page-{page_no}.png")
    (output / "elements.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    db = graph()
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
    }
    (output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report))
    db.driver.close()


if __name__ == "__main__":
    main()
