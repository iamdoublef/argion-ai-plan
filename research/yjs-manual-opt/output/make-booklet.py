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

    # Index list: page number or None for blank.
    page_ix = list(range(n)) + [None] * (padded - n)

    out = fitz.open()
    sheets = padded // 4

    def place(side_page, left_ix, right_ix):
        dst = out.new_page(width=LAND_W, height=LAND_H)
        left_rect = fitz.Rect(0, 0, LAND_W / 2, LAND_H)
        right_rect = fitz.Rect(LAND_W / 2, 0, LAND_W, LAND_H)

        if left_ix is not None:
            dst.show_pdf_page(left_rect, src, left_ix)
        if right_ix is not None:
            dst.show_pdf_page(right_rect, src, right_ix)

    for i in range(sheets):
        # front side
        l_front = padded - 1 - (2 * i)
        r_front = 2 * i
        place(i * 2, page_ix[l_front], page_ix[r_front])

        # back side
        l_back = 2 * i + 1
        r_back = padded - 2 - (2 * i)
        place(i * 2 + 1, page_ix[l_back], page_ix[r_back])

    out.save(out_pdf)
    out.close()
    src.close()


def main():
    base = Path(r'D:/work/private/yjsplan/research/yjs-manual-opt/output')
    exp = Path(r'D:/work/private/yjsplan/research/yjs-manual-opt/experiments/2026-02-26_top-tier-styles')
    jobs = [
        (base / 'V23-Manual-CN-Wevac.pdf', base / 'V23-Manual-CN-Wevac-booklet-A4.pdf'),
        (base / 'V23-Manual-EN-Wevac.pdf', base / 'V23-Manual-EN-Wevac-booklet-A4.pdf'),
        (exp / 'v23-lifestyle-complete-fixed.pdf', exp / 'v23-lifestyle-complete-fixed-booklet-A4.pdf'),
        (exp / 'v23-mi-2.0-full-fixed.pdf', exp / 'v23-mi-2.0-full-fixed-booklet-A4.pdf'),
        (exp / 'v23-swiss-complete-fixed.pdf', exp / 'v23-swiss-complete-fixed-booklet-A4.pdf'),
    ]

    for src, out in jobs:
        if src.exists():
            impose_booklet(src, out)
            print(f'generated: {out.name}')


if __name__ == '__main__':
    main()
