"""Walk target PDF and pull font sizes / vertical positions per page for hard pages.

Goal: ground-truth comparison so we can say 'target uses 9pt body, W27 uses 8pt' etc.
"""
from __future__ import annotations
import json
from pathlib import Path
import fitz

PDF = Path(r"D:/work/private/yjsplan/research/yjs-manual-opt/swiss/output/imt050-wevac-eu-cn.pdf")
OUT = Path(r"D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/design-iter-34/path-design-audit/_work/target_pdf_inspect.json")

PAGES = [1, 3, 4, 7, 8, 9, 11, 14]


def main():
    doc = fitz.open(PDF)
    out = {}
    for p in PAGES:
        page = doc[p - 1]
        d = page.get_text("dict")
        spans = []
        for b in d.get("blocks", []):
            for line in b.get("lines", []):
                for s in line.get("spans", []):
                    spans.append({
                        "size": round(s.get("size", 0), 2),
                        "font": s.get("font"),
                        "color": s.get("color"),
                        "bbox": [round(x, 1) for x in s.get("bbox", [])],
                        "text": (s.get("text", "") or "")[:80],
                    })
        # Group by size+font
        from collections import Counter
        sf = Counter((sp["size"], sp["font"]) for sp in spans)
        out[p] = {
            "size_font_histogram": [{"size": s, "font": f, "count": c} for (s, f), c in sf.most_common(15)],
            "span_samples": spans[:8],
            "span_count": len(spans),
            "page_size": [round(page.rect.width, 1), round(page.rect.height, 1)],
            "drawings_count": len(page.get_drawings()),
        }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("pages:", list(out.keys()))


if __name__ == "__main__":
    main()
