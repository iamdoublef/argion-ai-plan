# iter-9: Reduce body char spacing 5→2 on sz=14 body color runs

LibreOffice's character-spacing (rPr w:spacing) IS respected. Baseline body
runs (sz=14, color 000000/1A1A1A) have spacing=5 (5 twips = 0.25pt extra per char).
For a 50-char line, that's 250 twips (~12.5mm) of expansion.

Reducing to 2 (=0.1pt) tightens ~3 twips × 30 chars = 90 twips per line, which
may eliminate forced line wraps where candidate currently breaks earlier than
target due to LO's slightly wider CJK rendering.

Targeted: 75 body rPr blocks (matches sz=14 with body text colors).
