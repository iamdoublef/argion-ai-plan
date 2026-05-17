"""iter-1 recon: cross-tabulate sz x font x color x spacing in baseline W37.

Specifically interested in:
- sz=14 BLACK (W32 win, 71 sites? expected at val=8) — half-step candidate
- sz=13 BLACK (W37 win, expected at val=9) — Goldilocks anchor
- sz=10 RED (W36 win, expected at val=8) — DOWN candidate
- sz=22, sz=27 BLACK (W36 win, expected at val=11) — saturated controls
- sz=15 BLACK (W37 expected at val=5)
"""
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
doc_path = ROOT / "baseline_unpacked" / "word" / "document.xml"
doc = doc_path.read_text(encoding="utf-8")

# Find all rPr blocks
RPR = re.compile(r'<w:rPr>(.*?)</w:rPr>', re.DOTALL)
SZ = re.compile(r'<w:sz w:val="(\d+)"')
SZCS = re.compile(r'<w:szCs w:val="(\d+)"')
FONT = re.compile(r'<w:rFonts ([^/>]*)/?>')
COLOR = re.compile(r'<w:color w:val="([0-9A-Fa-f]{6})"')
SPACING = re.compile(r'<w:spacing w:val="(-?\d+)"')

blocks = RPR.findall(doc)
print(f"Total rPr blocks: {len(blocks)}")

cohorts = Counter()
sites_by_key = {}

for b in blocks:
    sz_m = SZ.search(b)
    if not sz_m:
        continue
    sz = int(sz_m.group(1))
    color_m = COLOR.search(b)
    color = color_m.group(1).upper() if color_m else "AUTO"
    color_grp = "RED" if color in ("E40714", "C00000", "FF0000", "E63846") else "GRAY" if color in ("808080","595959","8E8E93","1A1A1A") else "BLACK" if color in ("000000","AUTO","262626") else color
    font_m = FONT.search(b)
    font_attrs = font_m.group(1) if font_m else ""
    is_black_font = ("Arial Black" in font_attrs)
    is_arial = ("Arial " in font_attrs or 'w:ascii="Arial"' in font_attrs)
    font_grp = "ArialBlack" if is_black_font else ("Arial" if is_arial else "Other")
    sp_m = SPACING.search(b)
    sp = int(sp_m.group(1)) if sp_m else None
    key = (sz, color_grp, font_grp, sp)
    cohorts[key] += 1

# Print cohorts of interest
print("\n=== Cohorts by (sz, color, font, spacing) ===")
for key, n in sorted(cohorts.items()):
    sz, color, font, sp = key
    if sz in (10, 11, 13, 14, 15, 22, 27, 30, 36):
        sp_s = str(sp) if sp is not None else "None"
        print(f"  sz={sz} {color:6} {font:11} sp={sp_s:>4} -> {n}")

# Aggregate sz=14 BLACK
print("\n=== sz=14 BLACK (any font) spacing distribution ===")
sub = Counter()
for (sz, c, f, sp), n in cohorts.items():
    if sz == 14 and c == "BLACK":
        sub[sp] += n
print(dict(sub))

print("\n=== sz=13 BLACK (any font) spacing distribution ===")
sub = Counter()
for (sz, c, f, sp), n in cohorts.items():
    if sz == 13 and c == "BLACK":
        sub[sp] += n
print(dict(sub))

print("\n=== sz=13 BLACK split by font ===")
for (sz, c, f, sp), n in cohorts.items():
    if sz == 13 and c == "BLACK":
        print(f"  font={f:11} sp={sp} -> {n}")

print("\n=== sz=10 RED spacing distribution ===")
sub = Counter()
for (sz, c, f, sp), n in cohorts.items():
    if sz == 10 and c == "RED":
        sub[sp] += n
print(dict(sub))
