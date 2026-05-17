from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz
import numpy as np
from PIL import Image


def render_pdf_pngs(pdf: Path, outdir: Path) -> list[Path]:
    outdir.mkdir(exist_ok=True, parents=True)
    for old in outdir.glob("page-*.png"):
        old.unlink()
    doc = fitz.open(pdf)
    out: list[Path] = []
    try:
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=fitz.Matrix(150 / 72, 150 / 72), alpha=False)
            path = outdir / f"page-{i:02d}.png"
            pix.save(str(path))
            out.append(path)
    finally:
        doc.close()
    return out


def diff_dirs(target_dir: Path, candidate_dir: Path) -> dict:
    target_pages = sorted(target_dir.glob("page-*.png"))
    candidate_pages = sorted(candidate_dir.glob("page-*.png"))
    diffs: list[float] = []
    for target, candidate in zip(target_pages, candidate_pages):
        target_img = np.array(Image.open(target).convert("RGB"))
        candidate_pil = Image.open(candidate).convert("RGB")
        if target_img.shape != np.array(candidate_pil).shape:
            candidate_pil = candidate_pil.resize((target_img.shape[1], target_img.shape[0]))
        candidate_img = np.array(candidate_pil)
        diffs.append(round(float(np.abs(target_img.astype(int) - candidate_img.astype(int)).mean()), 2))
    return {
        "per_page_mean_diff": diffs,
        "overall_mean_diff": round(sum(diffs) / len(diffs), 2) if diffs else None,
        "max_page_diff": max(diffs) if diffs else None,
        "target_pages": len(target_pages),
        "candidate_pages": len(candidate_pages),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("word_pdf", type=Path)
    parser.add_argument("--baseline-pngs", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    if not args.word_pdf.exists():
        raise SystemExit(f"missing Word-rendered PDF: {args.word_pdf}")
    png_dir = args.word_pdf.parent / "word_png"
    render_pdf_pngs(args.word_pdf, png_dir)
    result = {
        "word_pdf": str(args.word_pdf),
        "word_png_dir": str(png_dir),
        "visual": diff_dirs(args.baseline_pngs, png_dir),
    }
    out = args.out or args.word_pdf.with_suffix(".word-score.json")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    visual = result["visual"]
    print(f"Word visual diff: overall {visual['overall_mean_diff']}, max page {visual['max_page_diff']}")
    print(f"Score written: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
