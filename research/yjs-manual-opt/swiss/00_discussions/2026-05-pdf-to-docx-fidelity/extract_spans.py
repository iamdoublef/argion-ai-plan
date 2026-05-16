"""
逐 page 抽取 PDF 的所有 text span，输出 JSON。
比 probe_pdf.py 详细 — 含每个 span 的 (x, y, w, h, font, size, color, text)。
"""
import json
import sys
from pathlib import Path

import fitz


def extract(pdf_path: Path) -> list:
    doc = fitz.open(pdf_path)
    pages = []
    for pno, page in enumerate(doc, start=1):
        spans = []
        text_dict = page.get_text("dict")
        for block in text_dict.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    bbox = span["bbox"]
                    spans.append({
                        "x": round(bbox[0], 1),
                        "y": round(bbox[1], 1),
                        "w": round(bbox[2] - bbox[0], 1),
                        "h": round(bbox[3] - bbox[1], 1),
                        "font": span.get("font", "?"),
                        "size": round(span.get("size", 0), 2),
                        "color": f"#{span.get('color', 0):06X}",
                        "text": span.get("text", "").strip(),
                    })
        # Also extract page-level shapes (lines, rectangles for design elements like borders)
        drawings = []
        for d in page.get_drawings():
            rect = d.get("rect")
            if rect is None:
                continue
            stroke = d.get("color")
            fill = d.get("fill")
            drawings.append({
                "type": d.get("type", "?"),
                "rect": [round(rect[0], 1), round(rect[1], 1), round(rect[2], 1), round(rect[3], 1)],
                "stroke": f"#{int(stroke[0]*255):02X}{int(stroke[1]*255):02X}{int(stroke[2]*255):02X}" if stroke else None,
                "fill": f"#{int(fill[0]*255):02X}{int(fill[1]*255):02X}{int(fill[2]*255):02X}" if fill else None,
                "width": round(d.get("width", 0) or 0, 2),
            })
        # Image positions
        images = []
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                rects = page.get_image_rects(xref)
                for r in rects:
                    images.append({
                        "xref": xref,
                        "rect": [round(r[0], 1), round(r[1], 1), round(r[2], 1), round(r[3], 1)],
                        "size_px": [img_info[2], img_info[3]],
                    })
            except Exception:
                pass

        pages.append({
            "page": pno,
            "size_pt": [round(page.rect.width, 1), round(page.rect.height, 1)],
            "spans": spans,
            "drawings_count": len(drawings),
            "drawings": drawings[:50],  # cap to avoid explosion
            "images": images,
        })
    doc.close()
    return pages


def main():
    if len(sys.argv) != 3:
        print("Usage: extract_spans.py <pdf> <output.json>", file=sys.stderr)
        sys.exit(1)
    pdf = Path(sys.argv[1])
    out = Path(sys.argv[2])
    pages = extract(pdf)
    out.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    total_spans = sum(len(p["spans"]) for p in pages)
    total_drawings = sum(p["drawings_count"] for p in pages)
    print(f"OK: {len(pages)} pages, {total_spans} spans, {total_drawings} drawings → {out}")


if __name__ == "__main__":
    main()
