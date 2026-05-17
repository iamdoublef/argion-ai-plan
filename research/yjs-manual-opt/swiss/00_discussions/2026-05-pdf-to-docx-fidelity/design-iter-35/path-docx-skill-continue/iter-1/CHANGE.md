# iter-1: Fix line=24 typos in 2 table-spacer paragraphs

Two empty spacer paragraphs (between table blocks) had `w:line="24"` instead of `w:line="240"`.
At lineRule=auto, line=24 means 24/240 = 10% of single-spacing — extremely tight. This may
cause line-height collapse and shift downstream content. Fix to 240 (single-line).

Lines affected: 7747, 8790 (both on pages 11 and 13).
