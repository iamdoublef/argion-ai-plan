"""Inspect W27 docx structure: paragraph spacing, table borders, fonts, etc.

Goal: produce data-grounded findings for the audit prose. Read the docx as zip+XML,
walk paragraphs/tables, and report:
  - per-style table border widths
  - paragraph spacing (space_before / space_after / line_spacing) per style
  - any pattern of pPr.pBdr (paragraph borders, used for CAUTION/NOTICE boxes)
  - cell shading and borders in each table
  - font run sizes used per style
"""
from __future__ import annotations
import zipfile, json, re, sys
from pathlib import Path
from xml.etree import ElementTree as ET

DOCX = Path(r"D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/final/imt050-wevac-eu-cn.docx")
OUT = Path(r"D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/design-iter-34/path-design-audit/_work/docx_inspect.json")

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def qn(tag):
    return f"{{{W}}}{tag}"


def main():
    z = zipfile.ZipFile(DOCX)
    doc_xml = z.read("word/document.xml").decode("utf-8", "replace")
    styles_xml = z.read("word/styles.xml").decode("utf-8", "replace")

    doc = ET.fromstring(doc_xml)
    styles = ET.fromstring(styles_xml)

    out = {
        "paragraph_borders": [],
        "tables": [],
        "table_styles": {},
        "para_spacing_by_style": {},
        "run_sizes_by_style": {},
        "numbered_lists": [],
        "section": {},
    }

    # 1. Paragraph borders (for CAUTION/NOTICE box detection)
    for p in doc.iter(qn("p")):
        pPr = p.find(qn("pPr"))
        if pPr is None:
            continue
        pBdr = pPr.find(qn("pBdr"))
        pStyle = pPr.find(qn("pStyle"))
        style_id = pStyle.get(qn("val")) if pStyle is not None else None
        if pBdr is not None:
            sides = {}
            for side in ("top", "left", "bottom", "right"):
                el = pBdr.find(qn(side))
                if el is not None:
                    sides[side] = {
                        "sz": el.get(qn("sz")),
                        "color": el.get(qn("color")),
                        "val": el.get(qn("val")),
                    }
            # Snippet of paragraph text for context
            txt = "".join(t.text or "" for t in p.iter(qn("t")))[:60]
            out["paragraph_borders"].append({"style": style_id, "text": txt, "sides": sides})

    # 2. Paragraph spacing per style
    for s in styles.findall(qn("style")):
        sid = s.get(qn("styleId"))
        pPr = s.find(qn("pPr"))
        if pPr is None:
            continue
        spacing = pPr.find(qn("spacing"))
        if spacing is not None:
            out["para_spacing_by_style"][sid] = {
                "before": spacing.get(qn("before")),
                "after": spacing.get(qn("after")),
                "line": spacing.get(qn("line")),
                "lineRule": spacing.get(qn("lineRule")),
            }
        rPr = s.find(qn("rPr"))
        if rPr is not None:
            sz = rPr.find(qn("sz"))
            if sz is not None:
                out["run_sizes_by_style"][sid] = {"sz_half_pt": sz.get(qn("val"))}

    # 3. Table-level: borders, cells with shading
    for ti, tbl in enumerate(doc.iter(qn("tbl"))):
        rec = {"index": ti, "rows": 0, "tblBorders": None, "row_heights": [], "cell_shades": [], "cell_borders_top": [], "first_cell_text": ""}
        tblPr = tbl.find(qn("tblPr"))
        if tblPr is not None:
            bds = tblPr.find(qn("tblBorders"))
            if bds is not None:
                rec["tblBorders"] = {}
                for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
                    el = bds.find(qn(side))
                    if el is not None:
                        rec["tblBorders"][side] = {"sz": el.get(qn("sz")), "color": el.get(qn("color")), "val": el.get(qn("val"))}
        rows = list(tbl.iter(qn("tr")))
        rec["rows"] = len(rows)
        for r in rows[:8]:  # sample first 8 rows
            trPr = r.find(qn("trPr"))
            h = None
            if trPr is not None:
                hel = trPr.find(qn("trHeight"))
                if hel is not None:
                    h = {"val": hel.get(qn("val")), "rule": hel.get(qn("hRule"))}
            rec["row_heights"].append(h)
            shades = []
            top_borders = []
            for tc in r.iter(qn("tc")):
                tcPr = tc.find(qn("tcPr"))
                if tcPr is None:
                    shades.append(None); top_borders.append(None); continue
                shd = tcPr.find(qn("shd"))
                shades.append(shd.get(qn("fill")) if shd is not None else None)
                tcBorders = tcPr.find(qn("tcBorders"))
                if tcBorders is not None:
                    top = tcBorders.find(qn("top"))
                    top_borders.append({"sz": top.get(qn("sz")), "color": top.get(qn("color")), "val": top.get(qn("val"))} if top is not None else None)
                else:
                    top_borders.append(None)
            rec["cell_shades"].append(shades)
            rec["cell_borders_top"].append(top_borders)
        # First cell text snippet
        first_cell_t = []
        first_row = rows[0] if rows else None
        if first_row is not None:
            for tc in first_row.iter(qn("tc")):
                first_cell_t.append("".join(t.text or "" for t in tc.iter(qn("t"))))
        rec["first_cell_text"] = " | ".join(first_cell_t)[:200]
        out["tables"].append(rec)

    # 4. Page sectPr (margins)
    for sect in doc.iter(qn("sectPr")):
        pgMar = sect.find(qn("pgMar"))
        pgSz = sect.find(qn("pgSz"))
        out["section"] = {
            "pgMar": {a.split("}", 1)[-1]: pgMar.get(a) for a in pgMar.attrib} if pgMar is not None else None,
            "pgSz": {a.split("}", 1)[-1]: pgSz.get(a) for a in pgSz.attrib} if pgSz is not None else None,
        }
        break

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("borders:", len(out["paragraph_borders"]), " tables:", len(out["tables"]))


if __name__ == "__main__":
    main()
