# iter-01 notes

Starting point: `design-iter-02/path-codex/build_b2_docx.py`.

## Changes

- Shifted body-page content down after header strips to align the section-title and first content baseline with the PDF.
- Changed sub-title typography from 9 pt to 7.5 pt to match target headings.
- Removed generated inline alert icons when the HTML already contains a real warning icon.
- Compressed alert-box list spacing and table cell internals.
- Increased figure paragraph spacing so structure/function images and following tables align closer to the PDF.
- Split p14 warranty contact intro line before `support@wevactech.com`.

## Score

- Overall: `12.88 -> 11.36`
- Max page: `19.59 -> 25.07`
- Pages: `15`, editable: `100%`

## Per-page changes

| Page | Previous | iter-01 | Note |
| --- | ---: | ---: | --- |
| p3 | 17.99 | 15.80 | Warning box duplicate title icon removed; box over-compressed. |
| p5 | 14.49 | 13.45 | Subtitle size/position closer; bullets slightly over-compressed. |
| p6 | 14.70 | 7.39 | Product image/table alignment improved strongly. |
| p7 | 17.01 | 8.17 | Image/table vertical alignment improved strongly. |
| p9 | 12.71 | 13.96 | Normal bullet rhythm became too compressed upstream of step images. |
| p11 | 16.89 | 14.67 | Troubleshooting table improved but disclaimer moved too high. |
| p13 | 15.02 | 14.35 | WEEE box improved slightly but page rhythm too compressed. |
| p14 | 19.59 | 25.07 | Regressed because warranty separator rendered full-width. |

Decision: continue to iter-02, focused on p14 separator plus over-compression.
