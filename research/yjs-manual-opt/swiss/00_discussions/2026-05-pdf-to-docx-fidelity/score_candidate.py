"""
评分脚本：对 1 个候选 DOCX 做全面评分。

用法：
  python score_candidate.py <candidate.docx> --target <target.pdf> --baseline-pngs <dir>

输出：
  - JSON 评分结果到 <candidate.docx>.score.json
  - 控制台打印关键指标
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import fitz
from PIL import Image, ImageChops


SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"


def docx_to_pdf(docx_path: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        SOFFICE, "--headless", "--norestore", "--nolockcheck",
        "--convert-to", "pdf",
        "--outdir", str(out_dir),
        str(docx_path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        raise RuntimeError(f"soffice failed: {r.returncode}\n{r.stderr}")
    pdf = out_dir / (docx_path.stem + ".pdf")
    if not pdf.exists():
        pdfs = sorted(out_dir.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not pdfs:
            raise RuntimeError("no pdf produced")
        pdf = pdfs[0]
    return pdf


def render_pdf(pdf_path: Path, out_dir: Path, dpi: int = 150) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    mtx = fitz.Matrix(dpi / 72.0, dpi / 72.0)
    pages = []
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=mtx, alpha=False)
        out = out_dir / f"page-{i:02d}.png"
        pix.save(out.as_posix())
        pages.append(out)
    doc.close()
    return pages


def pdf_text_chars(pdf_path: Path) -> dict:
    doc = fitz.open(pdf_path)
    per_page = []
    total = 0
    for page in doc:
        text = page.get_text("text")
        n = len(re.sub(r"\s+", "", text))
        per_page.append(n)
        total += n
    doc.close()
    return {"per_page": per_page, "total": total}


def docx_editability(docx_path: Path) -> dict:
    """Check whether text lives in editable paragraphs vs text boxes vs page-image hacks."""
    with zipfile.ZipFile(docx_path) as zf:
        document_xml = zf.read("word/document.xml").decode("utf-8", errors="replace")
        # Count embedded images in word/media/
        media_files = [n for n in zf.namelist() if n.startswith("word/media/")]
        total_image_size = sum(zf.getinfo(n).file_size for n in media_files)
    txbx_blocks = len(re.findall(r"<w:txbxContent", document_xml))
    wp_t = len(re.findall(r"<w:t[\s>]", document_xml))
    wp_drawing_text = len(re.findall(r"<wps:txbx", document_xml))
    drawings = document_xml.count("<w:drawing>")
    # Anti-cheat: if drawings ≈ pages and wt_count < 50, this is likely "render each page as an image" hack
    # Real editable Chinese manual should have wt_count ≥ 200 for 15 pages
    is_image_hack = wp_t < 100 and drawings >= 15 and total_image_size > 1_500_000
    return {
        "wt_count": wp_t,
        "txbx_count": txbx_blocks + wp_drawing_text,
        "drawings_count": drawings,
        "image_bytes": total_image_size,
        "image_hack_detected": is_image_hack,
        "editable_pct": round(100 * wp_t / (wp_t + txbx_blocks + wp_drawing_text + 1e-9), 1) if not is_image_hack else 0.0,
    }


def pixel_diff(a_dir: Path, b_dir: Path) -> dict:
    """Per-page mean pixel difference. Resize b to match a."""
    a_pages = sorted(a_dir.glob("page-*.png"))
    b_pages = sorted(b_dir.glob("page-*.png"))
    n = min(len(a_pages), len(b_pages))
    diffs = []
    for i in range(n):
        a = Image.open(a_pages[i]).convert("RGB")
        b = Image.open(b_pages[i]).convert("RGB")
        if a.size != b.size:
            b = b.resize(a.size, Image.BICUBIC)
        d = ImageChops.difference(a, b)
        hist = d.histogram()
        # Calculate mean per channel
        # First 256 = R, next G, next B
        weighted_sum = sum(i * hist[i] for i in range(256)) + \
                       sum(i * hist[256 + i] for i in range(256)) + \
                       sum(i * hist[512 + i] for i in range(256))
        total_pixels = a.size[0] * a.size[1] * 3
        mean_diff = weighted_sum / total_pixels if total_pixels else 0
        diffs.append(round(mean_diff, 2))
        a.close(); b.close(); d.close()
    return {
        "per_page_mean_diff": diffs,
        "overall_mean_diff": round(sum(diffs) / len(diffs), 2) if diffs else None,
        "max_page_diff": max(diffs) if diffs else None,
    }


def score(target_pdf: Path, target_pngs: Path, candidate_docx: Path) -> dict:
    work = candidate_docx.parent / "_score_tmp"
    work.mkdir(parents=True, exist_ok=True)

    # 1. Convert candidate to PDF
    cand_pdf = docx_to_pdf(candidate_docx, work / "pdf")
    cand_pngs_dir = work / "png"
    cand_pngs = render_pdf(cand_pdf, cand_pngs_dir)

    # 2. Text comparison
    target_text = pdf_text_chars(target_pdf)
    cand_text = pdf_text_chars(cand_pdf)

    # 3. Editability check
    edit = docx_editability(candidate_docx)

    # 4. Visual diff
    target_pages = sorted(target_pngs.glob("page-*.png"))
    visual = pixel_diff(target_pngs, cand_pngs_dir) if cand_pngs else {}

    # 5. Score
    target_pages_count = len(target_pages) or 15
    cand_pages_count = len(cand_pngs)
    page_ratio = cand_pages_count / target_pages_count
    text_ratio = cand_text["total"] / max(1, target_text["total"])

    pass_pages = cand_pages_count <= target_pages_count + 1
    pass_text = 0.95 <= text_ratio <= 1.20  # also reject bloat (image-hack with alt-text repetition)
    pass_edit = edit["editable_pct"] >= 95.0 and not edit.get("image_hack_detected", False) and edit["wt_count"] >= 200
    pass_visual = visual.get("overall_mean_diff", 999) < 60  # ≈ 25% pixel diff

    result = {
        "candidate": str(candidate_docx),
        "target": str(target_pdf),
        "pages": {"target": target_pages_count, "candidate": cand_pages_count, "ratio": round(page_ratio, 2)},
        "text": {
            "target_chars": target_text["total"],
            "candidate_chars": cand_text["total"],
            "ratio": round(text_ratio, 2),
        },
        "editability": edit,
        "visual": visual,
        "pass": {
            "pages": pass_pages,
            "text": pass_text,
            "editable": pass_edit,
            "visual": pass_visual,
            "overall": all([pass_pages, pass_text, pass_edit, pass_visual]),
        },
    }

    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("candidate", help="Path to candidate .docx")
    p.add_argument("--target", required=True, help="Path to target .pdf")
    p.add_argument("--baseline-pngs", required=True, help="Directory of pre-rendered target PNGs")
    args = p.parse_args()

    cand = Path(args.candidate)
    if not cand.exists():
        print(f"ERROR: {cand} not found", file=sys.stderr)
        return 1

    target_pdf = Path(args.target)
    target_pngs = Path(args.baseline_pngs)

    result = score(target_pdf, target_pngs, cand)

    out = cand.with_suffix(".score.json")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nScore written: {out}")
    print(f"Pages: target {result['pages']['target']} vs candidate {result['pages']['candidate']}")
    print(f"Text ratio: {result['text']['ratio']}")
    print(f"Editable %: {result['editability']['editable_pct']}")
    if result['visual']:
        print(f"Visual diff (lower=better): overall {result['visual']['overall_mean_diff']}, max page {result['visual']['max_page_diff']}")
    print(f"PASS overall: {result['pass']['overall']}")
    print(f"  pages: {result['pass']['pages']}  text: {result['pass']['text']}  editable: {result['pass']['editable']}  visual: {result['pass']['visual']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
