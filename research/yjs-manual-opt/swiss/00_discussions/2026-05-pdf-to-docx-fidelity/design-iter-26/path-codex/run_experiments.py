from __future__ import annotations

import json
import shutil
import subprocess
import sys
import zipfile
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "seed-output.docx"
TARGET = Path(r"D:\work\private\yjsplan\research\yjs-manual-opt\swiss\output\imt050-wevac-eu-cn.pdf")
TARGET_PNGS = ROOT.parent.parent / "baseline" / "target_png"
SCORE = ROOT.parent.parent / "score_candidate.py"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
for prefix in ("w", "wp", "a", "pic", "r"):
    ET.register_namespace(prefix, NS[prefix])

EMU_PER_INCH = 914400
EMU_PER_PT = 12700


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


def load_document(unpacked: Path) -> tuple[ET.ElementTree, ET.Element]:
    tree = ET.parse(unpacked / "word" / "document.xml")
    root = tree.getroot()
    body = root.find("w:body", NS)
    if body is None:
        raise RuntimeError("word/document.xml has no body")
    return tree, body


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


def all_paragraphs(node: ET.Element):
    if node.tag == qn("w:p"):
        yield node
    else:
        yield from node.findall(".//w:p", NS)


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


def relationship_map(unpacked: Path) -> dict[str, Path]:
    rels = ET.parse(unpacked / "word" / "_rels" / "document.xml.rels").getroot()
    mapping: dict[str, Path] = {}
    for rel in rels.findall("rel:Relationship", NS):
        rid = rel.get("Id")
        target = rel.get("Target", "")
        if rid and target.startswith("media/"):
            mapping[rid] = unpacked / "word" / target
    return mapping


def image_rids_and_extents(unpacked: Path) -> list[tuple[str, int, int]]:
    tree, _ = load_document(unpacked)
    items: list[tuple[str, int, int]] = []
    for inline in tree.findall(".//wp:inline", NS):
        extent = inline.find("wp:extent", NS)
        blip = inline.find(".//a:blip", NS)
        if extent is None or blip is None:
            continue
        rid = blip.get(qn("r:embed"))
        if rid:
            items.append((rid, int(extent.get("cx", "0")), int(extent.get("cy", "0"))))
    return items


def resample_images(unpacked: Path, dpi: int) -> dict[str, int]:
    rels = relationship_map(unpacked)
    counts = {"images": 0, "bytes_before": 0, "bytes_after": 0}
    seen: set[Path] = set()
    for rid, cx, cy in image_rids_and_extents(unpacked):
        path = rels.get(rid)
        if path is None or path in seen or not path.exists():
            continue
        seen.add(path)
        counts["bytes_before"] += path.stat().st_size
        target_w = max(1, round(cx / EMU_PER_INCH * dpi))
        target_h = max(1, round(cy / EMU_PER_INCH * dpi))
        with Image.open(path) as im:
            src_mode = im.mode
            work = im.convert("RGBA") if "A" in src_mode else im.convert("RGB")
            if work.size != (target_w, target_h):
                work = work.resize((target_w, target_h), Image.Resampling.LANCZOS)
            out = BytesIO()
            work.save(out, format="PNG", optimize=True)
        path.write_bytes(out.getvalue())
        counts["bytes_after"] += path.stat().st_size
        counts["images"] += 1
    return counts


def round_inline_extents(unpacked: Path, quantum_pt: float = 0.25) -> int:
    tree, _ = load_document(unpacked)
    quantum = max(1, round(EMU_PER_PT * quantum_pt))
    touched = 0
    for inline in tree.findall(".//wp:inline", NS):
        extent = inline.find("wp:extent", NS)
        pic_ext = inline.find(".//pic:spPr/a:xfrm/a:ext", NS)
        if extent is None:
            continue
        cx = int(extent.get("cx", "0"))
        cy = int(extent.get("cy", "0"))
        new_cx = max(1, round(cx / quantum) * quantum)
        new_cy = max(1, round(cy / quantum) * quantum)
        if (new_cx, new_cy) != (cx, cy):
            extent.set("cx", str(new_cx))
            extent.set("cy", str(new_cy))
            if pic_ext is not None:
                pic_ext.set("cx", str(new_cx))
                pic_ext.set("cy", str(new_cy))
            touched += 1
    tree.write(unpacked / "word" / "document.xml", encoding="utf-8", xml_declaration=True)
    return touched


def patch_rfonts_arial_yahei_hint(unpacked: Path) -> int:
    tree, body = load_document(unpacked)
    touched = 0
    for _, _, _, node in iter_blocks(body):
        for r_pr in node.findall(".//w:rPr", NS):
            fonts = r_pr.find("w:rFonts", NS)
            if fonts is None:
                continue
            ascii_font = fonts.get(qn("w:ascii"), "")
            if ascii_font == "Courier New":
                continue
            fonts.set(qn("w:ascii"), "Arial")
            fonts.set(qn("w:hAnsi"), "Arial")
            fonts.set(qn("w:cs"), "Arial")
            fonts.set(qn("w:eastAsia"), "Microsoft YaHei")
            fonts.set(qn("w:hint"), "eastAsia")
            touched += 1
    tree.write(unpacked / "word" / "document.xml", encoding="utf-8", xml_declaration=True)
    return touched


def add_chapter_bookmarks(unpacked: Path) -> int:
    tree, body = load_document(unpacked)
    bookmark_id = 1000
    touched = 0
    for kind, page, _, p in iter_blocks(body):
        if kind != "p":
            continue
        content = text(p).strip()
        if not content:
            continue
        if not (content.startswith(("01", "02", "03", "04", "05", "06", "07", "08", "09")) or "CH." in content):
            continue
        start = ET.Element(qn("w:bookmarkStart"))
        start.set(qn("w:id"), str(bookmark_id))
        start.set(qn("w:name"), f"p{page}_ch_{bookmark_id}")
        end = ET.Element(qn("w:bookmarkEnd"))
        end.set(qn("w:id"), str(bookmark_id))
        p.insert(0, start)
        p.append(end)
        bookmark_id += 1
        touched += 1
    tree.write(unpacked / "word" / "document.xml", encoding="utf-8", xml_declaration=True)
    return touched


def patch_contextual_spacing(unpacked: Path, hard_pages_only: bool = False) -> int:
    tree, body = load_document(unpacked)
    hard_pages = {3, 9, 11, 14}
    touched = 0
    for _, page, _, node in iter_blocks(body):
        if hard_pages_only and page not in hard_pages:
            continue
        for p in all_paragraphs(node):
            if not text(p).strip():
                continue
            p_pr = ensure(p, "w:pPr", first=True)
            node_cs = ensure(p_pr, "w:contextualSpacing")
            node_cs.set(qn("w:val"), "1")
            touched += 1
    tree.write(unpacked / "word" / "document.xml", encoding="utf-8", xml_declaration=True)
    return touched


VARIANTS = [
    ("iter-1-image-resample-150dpi", lambda d: resample_images(d, 150)),
    ("iter-2-image-resample-300dpi", lambda d: resample_images(d, 300)),
    ("iter-3-inline-extents-quarter-pt", round_inline_extents),
    ("iter-4-rfonts-arial-yahei-hint", patch_rfonts_arial_yahei_hint),
    ("iter-5-bookmarks-before-chapters", add_chapter_bookmarks),
    ("iter-6-contextual-spacing-all", patch_contextual_spacing),
]


def main() -> None:
    if not BASE.exists():
        raise SystemExit(f"missing {BASE}")

    baseline = (
        json.loads((ROOT / "seed-output.score.json").read_text(encoding="utf-8"))
        if (ROOT / "seed-output.score.json").exists()
        else score_docx(BASE)
    )
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
        rows.append(
            {
                "name": name,
                "patch_counts": patch_counts,
                "overall": overall,
                "max": max_page,
                "per_page": result["visual"]["per_page_mean_diff"],
                "pass": result["pass"],
            }
        )
        if result["pass"]["overall"] and (overall < best_score or (overall == best_score and max_page < best_max)):
            best_score = overall
            best_max = max_page
            best_path = docx

    shutil.copy2(best_path, ROOT / "output.docx")
    final = score_docx(ROOT / "output.docx")
    (ROOT / "experiment-summary.json").write_text(
        json.dumps(
            {
                "baseline": baseline,
                "rows": rows,
                "selected": str(best_path),
                "final": final,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
