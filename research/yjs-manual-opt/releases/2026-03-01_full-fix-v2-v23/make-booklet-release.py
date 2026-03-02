from pathlib import Path
import fitz

A4_W = 595.276
A4_H = 841.89
LAND_W = A4_H
LAND_H = A4_W


def impose_booklet(src_pdf: Path, out_pdf: Path):
    src = fitz.open(src_pdf)
    n = src.page_count
    padded = ((n + 3) // 4) * 4
    page_ix = list(range(n)) + [None] * (padded - n)

    out = fitz.open()
    sheets = padded // 4

    def place(left_ix, right_ix):
        dst = out.new_page(width=LAND_W, height=LAND_H)
        left_rect = fitz.Rect(0, 0, LAND_W / 2, LAND_H)
        right_rect = fitz.Rect(LAND_W / 2, 0, LAND_W, LAND_H)
        if left_ix is not None:
            dst.show_pdf_page(left_rect, src, left_ix)
        if right_ix is not None:
            dst.show_pdf_page(right_rect, src, right_ix)

    for i in range(sheets):
        place(page_ix[padded - 1 - (2 * i)], page_ix[2 * i])
        place(page_ix[2 * i + 1], page_ix[padded - 2 - (2 * i)])

    out.save(out_pdf)
    out.close()
    src.close()


def main():
    root = Path(r'D:/work/private/yjsplan/research/yjs-manual-opt/releases/2026-03-01_full-fix-v2')
    jobs = [
        ('v23-cn-main-fixed.pdf', 'v23-cn-main-fixed-booklet-A4.pdf'),
        ('v23-en-main-fixed.pdf', 'v23-en-main-fixed-booklet-A4.pdf'),
        ('v23-mi-style-fixed.pdf', 'v23-mi-style-fixed-booklet-A4.pdf'),
        ('v23-lifestyle-style-fixed.pdf', 'v23-lifestyle-style-fixed-booklet-A4.pdf'),
        ('v23-swiss-style-fixed.pdf', 'v23-swiss-style-fixed-booklet-A4.pdf'),
    ]

    for src_name, out_name in jobs:
        src = root / src_name
        out = root / out_name
        if src.exists():
            impose_booklet(src, out)
            print(f'generated: {out.name}')


if __name__ == '__main__':
    main()
