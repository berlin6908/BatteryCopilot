"""PDF region references, independent of a layout parser's element numbering."""

import hashlib
import re
from contextlib import closing
from threading import Lock

import pypdfium2 as pdfium

from battery_copilot.settings import PDF

# PDFium forbids simultaneous calls even for different documents.
PDF_LOCK = Lock()


def region_uid(digest: str, page: int, bbox: list[float]) -> str:
    coordinates = ",".join(str(round(v * 1_000_000)) for v in bbox)
    return f"pem:{digest}:p{page}:{coordinates}"


def region_text(page, bbox: list[float]) -> str:
    width, height = page.get_size()
    left, top, right, bottom = bbox
    # Half a PDF point avoids clipping glyphs at a rounded layout boundary.
    with closing(page.get_textpage()) as textpage:
        text = textpage.get_text_bounded(
            max(0, left * width - 0.5),
            max(0, (1 - bottom) * height - 0.5),
            min(width, right * width + 0.5),
            min(height, (1 - top) * height + 0.5),
        )
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def read_region(uid: str) -> dict:
    match = re.fullmatch(r"pem:([0-9a-f]{64}):p([1-9]\d*):(\d+,\d+,\d+,\d+)", uid)
    if not match:
        raise ValueError("无效的PDF区域引用。")
    digest, number, coordinates = match.groups()
    bbox = [int(v) / 1_000_000 for v in coordinates.split(",")]
    left, top, right, bottom = bbox
    if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
        raise ValueError("PDF区域超出页面范围。")
    content = PDF.read_bytes()
    if hashlib.sha256(content).hexdigest() != digest:
        raise ValueError("引用的PDF版本与本地文件不同。")
    number = int(number)
    with PDF_LOCK, pdfium.PdfDocument(content) as document:
        if number > len(document):
            raise ValueError("PDF页码超出范围。")
        page = document[number - 1]
        width, height = page.get_size()
        text = region_text(page, bbox)
    return {
        "uid": uid,
        "name": f"PEM · 第 {number} 页原文区域",
        "source_kind": "guide",
        "kind": "pdf_region",
        "source_file": PDF.name,
        "source_sha256": digest,
        "page": number,
        "bbox": bbox,
        "text": text,
        "page_width": width,
        "page_height": height,
        "image_url": f"/api/documents/pem/pages/{number}.png?v={digest}",
    }
