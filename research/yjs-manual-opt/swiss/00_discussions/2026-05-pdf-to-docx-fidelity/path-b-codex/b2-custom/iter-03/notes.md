# Iteration 03 Notes

## Changes

- Added direct text-node handling inside alert boxes.
- Page 11 disclaimer body now renders inside the caution box.

## Verification

- `compare_pdfs.py docx2pdf` produced `iter-03/pdf/output.pdf`.
- `compare_pdfs.py render` produced 15 PNG pages in `iter-03/png`.
- Side-by-side PNGs were generated in `iter-03/side_by_side` with a local fallback because `compare_pdfs.py compare` crashes in Pillow font drawing on this machine.
- OOXML structural check:
  - Paragraphs: 345
  - Tables: 18
  - Inline drawings/images: 17
  - Anchored drawings: 0
  - Text boxes: 0

## Status

Recommended final candidate: `iter-03/output.docx`.

