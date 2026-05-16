from __future__ import annotations

import argparse
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = NS["w"]
ET.register_namespace("w", W)


def qn(name: str) -> str:
    prefix, local = name.split(":")
    return f"{{{NS[prefix]}}}{local}"


def ensure(parent: ET.Element, tag: str, first: bool = False) -> ET.Element:
    node = parent.find(tag, NS)
    if node is None:
        node = ET.Element(qn(tag))
        if first:
            parent.insert(0, node)
        else:
            parent.append(node)
    return node


def paragraph_text(p: ET.Element) -> str:
    return "".join(t.text or "" for t in p.findall(".//w:t", NS))


def iter_blocks(body: ET.Element):
    page = 1
    p_idx = 0
    t_idx = 0
    for child in list(body):
        local = child.tag.rsplit("}", 1)[-1]
        if local == "p":
            p_idx += 1
            yield "p", page, p_idx, child
            if child.find(".//w:sectPr", NS) is not None:
                page += 1
        elif local == "tbl":
            t_idx += 1
            yield "tbl", page, t_idx, child


def set_exact_spacing(p: ET.Element, line: int = 240) -> None:
    p_pr = ensure(p, "w:pPr", first=True)
    spacing = ensure(p_pr, "w:spacing")
    spacing.set(qn("w:line"), str(line))
    spacing.set(qn("w:lineRule"), "exact")


def set_auto_spacing_off(p: ET.Element) -> None:
    p_pr = ensure(p, "w:pPr", first=True)
    for name in ("w:autoSpaceDE", "w:autoSpaceDN"):
        node = ensure(p_pr, name)
        node.set(qn("w:val"), "0")


def set_kerning(r: ET.Element, val: int = 14) -> None:
    r_pr = ensure(r, "w:rPr", first=True)
    kern = ensure(r_pr, "w:kern")
    kern.set(qn("w:val"), str(val))


def add_tblp_pr(tbl: ET.Element, *, x: int = 0, y: int = 0) -> None:
    tbl_pr = ensure(tbl, "w:tblPr", first=True)
    tblp = tbl_pr.find("w:tblpPr", NS)
    if tblp is None:
        tblp = ET.Element(qn("w:tblpPr"))
        tbl_pr.insert(0, tblp)
    tblp.set(qn("w:leftFromText"), "0")
    tblp.set(qn("w:rightFromText"), "0")
    tblp.set(qn("w:topFromText"), "0")
    tblp.set(qn("w:bottomFromText"), "0")
    tblp.set(qn("w:vertAnchor"), "text")
    tblp.set(qn("w:horzAnchor"), "margin")
    tblp.set(qn("w:tblpXSpec"), "center")
    tblp.set(qn("w:tblpX"), str(x))
    tblp.set(qn("w:tblpY"), str(y))


def patch_document(path: Path, variant: str) -> dict[str, int]:
    tree = ET.parse(path)
    root = tree.getroot()
    body = root.find("w:body", NS)
    if body is None:
        raise RuntimeError("word/document.xml has no body")

    counts: dict[str, int] = {}
    def bump(name: str) -> None:
        counts[name] = counts.get(name, 0) + 1

    blocks = list(iter_blocks(body))
    if variant == "p14_exact_240":
        for kind, page, _, node in blocks:
            if kind == "p" and page == 14 and paragraph_text(node).strip():
                set_exact_spacing(node, 240)
                bump("paragraph_exact_240")
            elif kind == "tbl" and page == 14:
                for p in node.findall(".//w:p", NS):
                    if paragraph_text(p).strip():
                        set_exact_spacing(p, 240)
                        bump("table_paragraph_exact_240")
    elif variant == "autospace_off_all":
        for _, _, _, node in blocks:
            for p in ([node] if node.tag == qn("w:p") else node.findall(".//w:p", NS)):
                set_auto_spacing_off(p)
                bump("paragraph_autospace_off")
    elif variant == "kern_all":
        for r in root.findall(".//w:r", NS):
            text = paragraph_text(r)
            if text.strip():
                set_kerning(r, 14)
                bump("runs_kern_14")
    elif variant == "p14_tbl_float":
        for kind, page, idx, node in blocks:
            if kind == "tbl" and page == 14 and idx in (15, 16):
                add_tblp_pr(node)
                bump("tables_floating")
    elif variant == "p11_exact_220_autospace":
        for kind, page, _, node in blocks:
            if kind == "p" and page == 11 and paragraph_text(node).strip():
                set_exact_spacing(node, 220)
                set_auto_spacing_off(node)
                bump("paragraph_exact_220_autospace")
            elif kind == "tbl" and page == 11:
                for p in node.findall(".//w:p", NS):
                    if paragraph_text(p).strip():
                        set_exact_spacing(p, 220)
                        set_auto_spacing_off(p)
                        bump("table_paragraph_exact_220_autospace")
    else:
        raise ValueError(f"unknown variant: {variant}")

    tree.write(path, encoding="utf-8", xml_declaration=True)
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("unpacked", type=Path)
    parser.add_argument("variant")
    args = parser.parse_args()
    path = args.unpacked / "word" / "document.xml"
    counts = patch_document(path, args.variant)
    print(counts)


if __name__ == "__main__":
    main()
