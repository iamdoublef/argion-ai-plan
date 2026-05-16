from __future__ import annotations

import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "seed-output.docx"
TARGET = Path(r"D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf")
TARGET_PNGS = ROOT.parent.parent / "baseline" / "target_png"
SCORE = ROOT.parent.parent / "score_candidate.py"

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = NS["w"]
ET.register_namespace("w", W)

HARD_PAGES = {3, 9, 11, 14}


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


def text(node: ET.Element) -> str:
    return "".join(t.text or "" for t in node.findall(".//w:t", NS))


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


def unpack_docx(docx: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    with zipfile.ZipFile(docx) as zf:
        zf.extractall(dst)


def pack_docx(src: Path, docx: Path) -> None:
    if docx.exists():
        docx.unlink()
    with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(src.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(src).as_posix())


def load_tree(unpacked: Path) -> tuple[ET.ElementTree, ET.Element]:
    tree = ET.parse(unpacked / "word" / "document.xml")
    root = tree.getroot()
    body = root.find("w:body", NS)
    if body is None:
        raise RuntimeError("word/document.xml has no body")
    return tree, body


def set_auto_spacing_off(p: ET.Element) -> None:
    p_pr = ensure(p, "w:pPr", first=True)
    for name in ("w:autoSpaceDE", "w:autoSpaceDN"):
        node = ensure(p_pr, name)
        node.set(qn("w:val"), "0")


def all_paragraphs(node: ET.Element):
    if node.tag == qn("w:p"):
        yield node
    else:
        yield from node.findall(".//w:p", NS)


def apply_baseline_autospace(body: ET.Element) -> int:
    count = 0
    for _, _, _, node in iter_blocks(body):
        for p in all_paragraphs(node):
            set_auto_spacing_off(p)
            count += 1
    return count


def add_numbering(unpacked: Path, *, indent: int = 181, hanging: int = 181) -> tuple[int, int]:
    """Use real w:numPr bullets and remove the literal leading bullet run."""
    tree, body = load_tree(unpacked)
    num_path = unpacked / "word" / "numbering.xml"
    num_tree = ET.parse(num_path)
    num_root = num_tree.getroot()

    abstract_ids = [
        int(n.get(qn("w:abstractNumId"), "0"))
        for n in num_root.findall("w:abstractNum", NS)
    ]
    num_ids = [int(n.get(qn("w:numId"), "0")) for n in num_root.findall("w:num", NS)]
    abstract_id = max(abstract_ids or [0]) + 1
    num_id = max(num_ids or [0]) + 1

    abstract = ET.Element(qn("w:abstractNum"))
    abstract.set(qn("w:abstractNumId"), str(abstract_id))
    lvl = ET.SubElement(abstract, qn("w:lvl"))
    lvl.set(qn("w:ilvl"), "0")
    ET.SubElement(lvl, qn("w:start")).set(qn("w:val"), "1")
    ET.SubElement(lvl, qn("w:numFmt")).set(qn("w:val"), "bullet")
    ET.SubElement(lvl, qn("w:lvlText")).set(qn("w:val"), "\u2022")
    ET.SubElement(lvl, qn("w:lvlJc")).set(qn("w:val"), "left")
    p_pr = ET.SubElement(lvl, qn("w:pPr"))
    ind = ET.SubElement(p_pr, qn("w:ind"))
    ind.set(qn("w:left"), str(indent))
    ind.set(qn("w:hanging"), str(hanging))
    r_pr = ET.SubElement(lvl, qn("w:rPr"))
    r_fonts = ET.SubElement(r_pr, qn("w:rFonts"))
    r_fonts.set(qn("w:ascii"), "Arial")
    r_fonts.set(qn("w:hAnsi"), "Arial")
    r_fonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    ET.SubElement(r_pr, qn("w:color")).set(qn("w:val"), "E63946")
    ET.SubElement(r_pr, qn("w:sz")).set(qn("w:val"), "12")
    ET.SubElement(r_pr, qn("w:szCs")).set(qn("w:val"), "12")
    num_root.append(abstract)

    num = ET.Element(qn("w:num"))
    num.set(qn("w:numId"), str(num_id))
    ET.SubElement(num, qn("w:abstractNumId")).set(qn("w:val"), str(abstract_id))
    num_root.append(num)

    touched = 0
    removed_runs = 0
    for kind, page, _, node in iter_blocks(body):
        if page not in HARD_PAGES:
            continue
        for p in all_paragraphs(node):
            stripped = text(p).lstrip()
            if not stripped.startswith("\u2022"):
                continue
            p_pr = ensure(p, "w:pPr", first=True)
            num_pr = ensure(p_pr, "w:numPr")
            ensure(num_pr, "w:ilvl", first=True).set(qn("w:val"), "0")
            ensure(num_pr, "w:numId").set(qn("w:val"), str(num_id))
            ind_node = ensure(p_pr, "w:ind")
            ind_node.set(qn("w:left"), str(indent))
            ind_node.set(qn("w:hanging"), str(hanging))
            for r in list(p.findall("w:r", NS)):
                r_text = text(r)
                if "\u2022" in r_text:
                    p.remove(r)
                    removed_runs += 1
                    break
            touched += 1

    tree.write(unpacked / "word" / "document.xml", encoding="utf-8", xml_declaration=True)
    num_tree.write(num_path, encoding="utf-8", xml_declaration=True)
    return touched, removed_runs


def patch_text_alignment(unpacked: Path, value: str = "auto") -> int:
    tree, body = load_tree(unpacked)
    count = apply_baseline_autospace(body)
    touched = 0
    for _, page, _, node in iter_blocks(body):
        if page not in HARD_PAGES:
            continue
        for p in all_paragraphs(node):
            if not text(p).strip():
                continue
            p_pr = ensure(p, "w:pPr", first=True)
            align = ensure(p_pr, "w:textAlignment")
            align.set(qn("w:val"), value)
            touched += 1
    tree.write(unpacked / "word" / "document.xml", encoding="utf-8", xml_declaration=True)
    return count + touched


def patch_run_position(unpacked: Path, val: int) -> int:
    tree, body = load_tree(unpacked)
    apply_baseline_autospace(body)
    touched = 0
    for _, page, _, node in iter_blocks(body):
        if page not in HARD_PAGES:
            continue
        for r in node.findall(".//w:r", NS):
            if not text(r).strip():
                continue
            r_pr = ensure(r, "w:rPr", first=True)
            pos = ensure(r_pr, "w:position")
            pos.set(qn("w:val"), str(val))
            touched += 1
    tree.write(unpacked / "word" / "document.xml", encoding="utf-8", xml_declaration=True)
    return touched


def patch_szcs(unpacked: Path, delta: int = 0) -> int:
    tree, body = load_tree(unpacked)
    apply_baseline_autospace(body)
    touched = 0
    for _, page, _, node in iter_blocks(body):
        if page not in HARD_PAGES:
            continue
        for r in node.findall(".//w:r", NS):
            if not text(r).strip():
                continue
            r_pr = ensure(r, "w:rPr", first=True)
            sz = r_pr.find("w:sz", NS)
            if sz is None:
                continue
            val = max(2, int(sz.get(qn("w:val"), "14")) + delta)
            szcs = ensure(r_pr, "w:szCs")
            szcs.set(qn("w:val"), str(val))
            touched += 1
    tree.write(unpacked / "word" / "document.xml", encoding="utf-8", xml_declaration=True)
    return touched


def patch_nowrap_tables(unpacked: Path) -> int:
    tree, body = load_tree(unpacked)
    apply_baseline_autospace(body)
    touched = 0
    for kind, page, _, node in iter_blocks(body):
        if kind != "tbl" or page not in {11, 14}:
            continue
        for tc in node.findall(".//w:tc", NS):
            tc_pr = ensure(tc, "w:tcPr", first=True)
            ensure(tc_pr, "w:noWrap")
            touched += 1
    tree.write(unpacked / "word" / "document.xml", encoding="utf-8", xml_declaration=True)
    return touched


def patch_page_margins(unpacked: Path) -> int:
    tree, body = load_tree(unpacked)
    apply_baseline_autospace(body)
    # sectPr for page N is at the end of page N-1 except the final section.
    margin_by_page = {
        3: {"top": 568, "bottom": 552},
        9: {"top": 552, "bottom": 568},
        11: {"top": 552, "bottom": 568},
        14: {"top": 552, "bottom": 568},
    }
    touched = 0
    current_page = 1
    for child in list(body):
        if child.tag.rsplit("}", 1)[-1] != "p":
            continue
        sect = child.find(".//w:sectPr", NS)
        if sect is not None:
            next_page = current_page + 1
            if next_page in margin_by_page:
                pg_mar = ensure(sect, "w:pgMar")
                for key, value in margin_by_page[next_page].items():
                    pg_mar.set(qn(f"w:{key}"), str(value))
                touched += 1
            current_page = next_page
    tree.write(unpacked / "word" / "document.xml", encoding="utf-8", xml_declaration=True)
    return touched


def patch_framepr_headers(unpacked: Path) -> int:
    tree, body = load_tree(unpacked)
    apply_baseline_autospace(body)
    touched = 0
    for _, page, _, node in iter_blocks(body):
        if page not in HARD_PAGES or node.tag != qn("w:p"):
            continue
        content = text(node).strip()
        if not content or not (content.startswith("威富可CH.") or content[:2].isdigit()):
            continue
        p_pr = ensure(node, "w:pPr", first=True)
        frame = ensure(p_pr, "w:framePr", first=True)
        frame.set(qn("w:w"), "7258")
        frame.set(qn("w:h"), "1")
        frame.set(qn("w:hRule"), "atLeast")
        frame.set(qn("w:xAlign"), "left")
        frame.set(qn("w:y"), "1")
        frame.set(qn("w:hAnchor"), "margin")
        frame.set(qn("w:vAnchor"), "text")
        frame.set(qn("w:wrap"), "notBeside")
        touched += 1
    tree.write(unpacked / "word" / "document.xml", encoding="utf-8", xml_declaration=True)
    return touched


VARIANTS = [
    ("iter-1-numpr-bullets", lambda d: add_numbering(d, indent=181, hanging=181)),
    ("iter-2-textAlignment-auto", lambda d: patch_text_alignment(d, "auto")),
    ("iter-3-run-position-minus1", lambda d: patch_run_position(d, -1)),
    ("iter-4-szCs-match", lambda d: patch_szcs(d, 0)),
    ("iter-5-nowrap-p11-p14-tables", patch_nowrap_tables),
    ("iter-6-page-margin-overrides", patch_page_margins),
    # Extra framePr implementation is kept for manual testing if a seventh probe is needed.
]


def score_docx(docx: Path) -> dict:
    cmd = [
        sys.executable,
        str(SCORE),
        str(docx),
        "--target",
        str(TARGET),
        "--baseline-pngs",
        str(TARGET_PNGS),
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)
    return json.loads(docx.with_suffix(".score.json").read_text(encoding="utf-8"))


def main() -> None:
    if not BASE.exists():
        raise SystemExit(f"missing {BASE}")

    baseline = json.loads((ROOT / "seed-output.score.json").read_text(encoding="utf-8")) if (ROOT / "seed-output.score.json").exists() else score_docx(BASE)
    best_score = baseline["visual"]["overall_mean_diff"]
    best_max = baseline["visual"]["max_page_diff"]
    best_path = BASE
    rows = []

    for name, patcher in VARIANTS:
        out_dir = ROOT / name
        out_dir.mkdir(exist_ok=True)
        docx = out_dir / "output.docx"
        unpacked = out_dir / "unpacked"
        unpack_docx(BASE, unpacked)
        patch_counts = patcher(unpacked)
        pack_docx(unpacked, docx)
        result = score_docx(docx)
        overall = result["visual"]["overall_mean_diff"]
        max_page = result["visual"]["max_page_diff"]
        rows.append((name, patch_counts, overall, max_page, result["visual"]["per_page_mean_diff"], result["pass"]))
        if result["pass"]["overall"] and (overall < best_score or (overall == best_score and max_page < best_max)):
            best_score = overall
            best_max = max_page
            best_path = docx

    shutil.copy2(best_path, ROOT / "output.docx")
    final = score_docx(ROOT / "output.docx")
    (ROOT / "experiment-summary.json").write_text(json.dumps({
        "baseline": baseline,
        "rows": [
            {
                "name": n,
                "patch_counts": c,
                "overall": o,
                "max": m,
                "per_page": p,
                "pass": passed,
            }
            for n, c, o, m, p, passed in rows
        ],
        "selected": str(best_path),
        "final": final,
    }, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
