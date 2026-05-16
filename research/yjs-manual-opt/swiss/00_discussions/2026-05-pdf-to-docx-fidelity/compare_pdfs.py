"""
PDF 渲染与对比工具

用法：
  python compare_pdfs.py render path/to/file.pdf out_dir  [--dpi 150]
  python compare_pdfs.py docx2pdf path/to/file.docx out_dir
  python compare_pdfs.py compare A_dir B_dir out_dir [--label-a "PDF" --label-b "DOCX→PDF"]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont, ImageChops

SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"


def render_pdf(pdf_path: Path, out_dir: Path, dpi: int = 150) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    written: list[Path] = []
    zoom = dpi / 72.0
    mtx = fitz.Matrix(zoom, zoom)
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=mtx, alpha=False)
        out = out_dir / f"page-{i:02d}.png"
        pix.save(out.as_posix())
        written.append(out)
    doc.close()
    print(f"  rendered {len(written)} pages @ {dpi}dpi → {out_dir}")
    return written


def docx_to_pdf(docx_path: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        SOFFICE,
        "--headless",
        "--norestore",
        "--nolockcheck",
        "--convert-to", "pdf",
        "--outdir", str(out_dir),
        str(docx_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print("STDOUT:", result.stdout, file=sys.stderr)
        print("STDERR:", result.stderr, file=sys.stderr)
        raise RuntimeError(f"soffice failed: {result.returncode}")
    pdf_path = out_dir / (docx_path.stem + ".pdf")
    if not pdf_path.exists():
        # Sometimes soffice picks a different name; pick the freshest pdf
        pdfs = sorted(out_dir.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not pdfs:
            raise RuntimeError("no pdf produced")
        pdf_path = pdfs[0]
    print(f"  docx→pdf: {pdf_path}")
    return pdf_path


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for cand in ("arial.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"):
        try:
            return ImageFont.truetype(cand, size)
        except Exception:
            continue
    return ImageFont.load_default()


def make_side_by_side(a_dir: Path, b_dir: Path, out_dir: Path,
                       label_a: str = "A", label_b: str = "B") -> None:
    import gc
    out_dir.mkdir(parents=True, exist_ok=True)
    a_pages = sorted(a_dir.glob("page-*.png"))
    b_pages = sorted(b_dir.glob("page-*.png"))
    n = max(len(a_pages), len(b_pages))
    print(f"  comparing: A has {len(a_pages)} pages, B has {len(b_pages)} pages")

    placeholder_size = None
    for i in range(n):
        font = _load_font(28)
        a = Image.open(a_pages[i]).convert("RGB") if i < len(a_pages) else None
        b = Image.open(b_pages[i]).convert("RGB") if i < len(b_pages) else None
        if a is not None and placeholder_size is None:
            placeholder_size = a.size
        if b is not None and placeholder_size is None:
            placeholder_size = b.size
        if a is None:
            a = Image.new("RGB", b.size if b is not None else placeholder_size, (240, 240, 240))
        if b is None:
            b = Image.new("RGB", a.size, (240, 240, 240))

        h = max(a.height, b.height)
        label_h = 50
        gap = 20
        canvas = Image.new("RGB", (a.width + gap + b.width, h + label_h + 10), (255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 10), f"{label_a}  p{i+1}", fill=(180, 0, 0), font=font)
        draw.text((a.width + gap + 10, 10), f"{label_b}  p{i+1}", fill=(0, 90, 180), font=font)
        canvas.paste(a, (0, label_h))
        canvas.paste(b, (a.width + gap, label_h))

        out = out_dir / f"side-{i+1:02d}.png"
        canvas.save(out.as_posix(), optimize=True)
        a.close(); b.close(); canvas.close()
        del a, b, canvas, draw, font
        gc.collect()
    print(f"  wrote {n} comparison images → {out_dir}")


def make_overlay_diff(a_dir: Path, b_dir: Path, out_dir: Path) -> None:
    """Pixel-wise diff: same size pages only. Writes diff-XX.png with red-tinted differences."""
    import gc
    out_dir.mkdir(parents=True, exist_ok=True)
    a_pages = sorted(a_dir.glob("page-*.png"))
    b_pages = sorted(b_dir.glob("page-*.png"))
    n = min(len(a_pages), len(b_pages))
    for i in range(n):
        a = Image.open(a_pages[i]).convert("RGB")
        b = Image.open(b_pages[i]).convert("RGB")
        if a.size != b.size:
            b = b.resize(a.size, Image.BICUBIC)
        diff = ImageChops.difference(a, b)
        bbox = diff.getbbox()
        out = out_dir / f"diff-{i+1:02d}.png"
        # Tint diff red and overlay onto a (50% opacity)
        red = Image.new("RGB", a.size, (255, 0, 0))
        mask = diff.convert("L").point(lambda v: min(255, v * 4))
        composite = Image.composite(red, a, mask)
        composite.save(out.as_posix(), optimize=True)
        a.close(); b.close(); diff.close(); composite.close()
        del a, b, diff, red, mask, composite
        gc.collect()
    print(f"  wrote {n} diff images → {out_dir}")


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    s_render = sub.add_parser("render")
    s_render.add_argument("pdf")
    s_render.add_argument("out")
    s_render.add_argument("--dpi", type=int, default=150)

    s_docx = sub.add_parser("docx2pdf")
    s_docx.add_argument("docx")
    s_docx.add_argument("out")

    s_cmp = sub.add_parser("compare")
    s_cmp.add_argument("a_dir")
    s_cmp.add_argument("b_dir")
    s_cmp.add_argument("out")
    s_cmp.add_argument("--label-a", default="A")
    s_cmp.add_argument("--label-b", default="B")

    s_dif = sub.add_parser("diff")
    s_dif.add_argument("a_dir")
    s_dif.add_argument("b_dir")
    s_dif.add_argument("out")

    args = p.parse_args()

    if args.cmd == "render":
        render_pdf(Path(args.pdf), Path(args.out), dpi=args.dpi)
    elif args.cmd == "docx2pdf":
        docx_to_pdf(Path(args.docx), Path(args.out))
    elif args.cmd == "compare":
        make_side_by_side(Path(args.a_dir), Path(args.b_dir), Path(args.out),
                          label_a=args.label_a, label_b=args.label_b)
    elif args.cmd == "diff":
        make_overlay_diff(Path(args.a_dir), Path(args.b_dir), Path(args.out))

    return 0


if __name__ == "__main__":
    sys.exit(main())
