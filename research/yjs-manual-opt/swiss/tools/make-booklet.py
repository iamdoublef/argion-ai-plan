#!/usr/bin/env python3
"""
make-booklet.py — Generic PDF booklet imposer

Usage:
  python make-booklet.py input.pdf                    # outputs input-booklet-A4.pdf
  python make-booklet.py output/v23-wevac-eu-cn.pdf  # full path
  python make-booklet.py --all output/               # process all PDFs in a directory
  python make-booklet.py --pattern output/*-cn.pdf   # glob pattern (PowerShell: use quotes)

Dependencies: pip install pymupdf
"""
import sys
import fitz
from pathlib import Path


A4_W = 595.276
A4_H = 841.89


def impose_booklet(src_path: Path, out_path: Path) -> bool:
    """Convert a regular PDF into a booklet-imposed PDF.
    
    Detects source page size and creates output sheets that are 
    2× source width × source height (e.g., A5 input → landscape A4 output).
    """
    try:
        src = fitz.open(src_path)
        n = src.page_count
        
        # Detect source page size from first page
        src_page = src[0]
        src_w = src_page.rect.width
        src_h = src_page.rect.height
        
        # Output sheet: two source pages side by side
        out_w = src_w * 2
        out_h = src_h
        
        # Pad to multiple of 4
        sheets = (n + 3) // 4
        padded = sheets * 4
        pages = list(range(n)) + [None] * (padded - n)

        # Build booklet order: [last, first, second, second-to-last, ...]
        order = []
        for i in range(sheets):
            order.append(pages[padded - 1 - i * 2])
            order.append(pages[i * 2])
            order.append(pages[i * 2 + 1])
            order.append(pages[padded - 2 - i * 2])

        dst = fitz.open()
        left_rect  = fitz.Rect(0,     0, src_w, out_h)
        right_rect = fitz.Rect(src_w, 0, out_w, out_h)

        for i in range(0, padded, 2):
            out_page = dst.new_page(width=out_w, height=out_h)
            left_ix  = order[i]
            right_ix = order[i + 1]
            if left_ix is not None:
                out_page.show_pdf_page(left_rect, src, left_ix)
            if right_ix is not None:
                out_page.show_pdf_page(right_rect, src, right_ix)

        dst.save(out_path)
        page_count = src.page_count
        src.close()
        dst.close()
        print(f"  OK: {out_path.name} ({page_count} pages → {sheets} sheets)")
        return True
    except Exception as e:
        print(f"  ERROR: {src_path.name} — {e}", file=sys.stderr)
        return False


def booklet_path(src_path: Path) -> Path:
    """Return the booklet output path for a given input PDF."""
    return src_path.with_name(src_path.stem + "-booklet-A4.pdf")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    jobs = []

    if args[0] == "--all":
        # Process all PDFs in the given directory (skip existing booklets)
        directory = Path(args[1]) if len(args) > 1 else Path(".")
        pdfs = sorted(directory.glob("*.pdf"))
        for p in pdfs:
            if "-booklet-" not in p.stem:
                jobs.append((p, booklet_path(p)))

    elif args[0] == "--pattern":
        # Caller should expand glob before passing (on Windows, use PowerShell)
        for pat_arg in args[1:]:
            import glob
            for match in glob.glob(pat_arg):
                p = Path(match)
                if "-booklet-" not in p.stem:
                    jobs.append((p, booklet_path(p)))

    else:
        # Positional args = specific files
        for arg in args:
            p = Path(arg)
            if not p.exists():
                print(f"WARN: file not found: {p}", file=sys.stderr)
                continue
            jobs.append((p, booklet_path(p)))

    if not jobs:
        print("No PDF files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(jobs)} PDF(s)...")
    ok = sum(1 for src, out in jobs if impose_booklet(src, out))
    print(f"Done: {ok}/{len(jobs)} booklets generated.")
    if ok < len(jobs):
        sys.exit(1)


if __name__ == "__main__":
    main()
