# iter-3: Add scissor-cut decoration line to page 14 warranty

Target PDF page 14 has a centered "scissor with dots" decoration after the warranty email,
e.g. `✄ · · · · · · · · · · · · · · · · · · · · · · · · · · · ·`.
Candidate is missing this — likely a top contributor to p14's 12.35 visualdiff.

Added a centered paragraph just before the page-14 sectPr with `✄` (U+2702 scissor) and
27 middle-dots (U+00B7) spaced via w:spacing=20. Targets p14 only.
