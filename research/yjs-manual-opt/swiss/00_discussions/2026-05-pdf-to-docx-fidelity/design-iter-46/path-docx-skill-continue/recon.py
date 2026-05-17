"""W35 baseline cohort recon: enumerate rPr blocks by sz/color/spacing/font/position.

Outputs counts to help target untested levers. Iter-1 surveys; iter-2..10 apply.
"""
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "baseline_unpacked" / "word" / "document.xml"
xml = DOC.read_text(encoding="utf-8")

rpr_pat = re.compile(r'<w:rPr>((?:(?!</w:rPr>).)*?)</w:rPr>', re.S)
rprs = rpr_pat.findall(xml)
print(f"Total rPr blocks: {len(rprs)}")

def get(b, tag, attr="w:val"):
    m = re.search(rf'<w:{tag}[^/>]*\b{attr}="([^"]+)"', b)
    return m.group(1) if m else None

def has(b, frag):
    return frag in b

# sz cohort overview
sz_counts = Counter()
sz_color = Counter()
sz_color_space = Counter()
sz_color_font = Counter()
sz_pos = Counter()
sz_vert = Counter()

for b in rprs:
    sz = get(b, "sz") or "0"
    color = get(b, "color") or "NONE"
    sp = get(b, "spacing") or "NONE"
    font_main = get(b, "rFonts", "w:ascii") or get(b, "rFonts", "w:eastAsia") or "NONE"
    pos = get(b, "position") or "NONE"
    vert = get(b, "vertAlign") or "NONE"

    sz_counts[sz] += 1
    sz_color[(sz, color)] += 1
    sz_color_space[(sz, color, sp)] += 1
    sz_color_font[(sz, color, font_main)] += 1
    if pos != "NONE":
        sz_pos[(sz, pos)] += 1
    if vert != "NONE":
        sz_vert[(sz, vert)] += 1

print("\n=== sz counts ===")
for sz, n in sorted(sz_counts.items(), key=lambda x: (-int(x[0]))):
    print(f"  sz={sz}: {n}")

print("\n=== sz=15+ cohorts (heading-ish) ===")
big = [s for s in sz_counts if int(s) >= 15]
for s in sorted(big, key=lambda x: -int(x)):
    print(f"  sz={s} total {sz_counts[s]}")
    for (sz, c), n in sorted(sz_color.items()):
        if sz == s:
            print(f"    color={c}: {n}")
    for (sz, c, sp), n in sorted(sz_color_space.items()):
        if sz == s:
            print(f"    color={c} spacing={sp}: {n}")
    for (sz, c, f), n in sorted(sz_color_font.items()):
        if sz == s:
            print(f"    color={c} font={f}: {n}")

print("\n=== sz=11 by color (already touched as GRAY+BLACK 5->2) ===")
for (sz, c, sp), n in sorted(sz_color_space.items()):
    if sz == "11":
        print(f"  color={c} spacing={sp}: {n}")

print("\n=== sz=12 by color (already touched as 5->2) ===")
for (sz, c, sp), n in sorted(sz_color_space.items()):
    if sz == "12":
        print(f"  color={c} spacing={sp}: {n}")
print("\n  sz=12 by font:")
for (sz, c, f), n in sorted(sz_color_font.items()):
    if sz == "12":
        print(f"    color={c} font={f}: {n}")

print("\n=== sz=13 by color (W35 GRAY-only 5->2 applied) ===")
for (sz, c, sp), n in sorted(sz_color_space.items()):
    if sz == "13":
        print(f"  color={c} spacing={sp}: {n}")

print("\n=== sz=14 by color (W32 BLACK 5->8) ===")
for (sz, c, sp), n in sorted(sz_color_space.items()):
    if sz == "14":
        print(f"  color={c} spacing={sp}: {n}")

print("\n=== w:position usage (untested lever) ===")
print(f"  total w:position rPr: {sum(sz_pos.values())}")
for (sz, p), n in sorted(sz_pos.items()):
    print(f"    sz={sz} position={p}: {n}")

print("\n=== w:vertAlign usage (untested lever) ===")
print(f"  total w:vertAlign rPr: {sum(sz_vert.values())}")
for (sz, v), n in sorted(sz_vert.items()):
    print(f"    sz={sz} vertAlign={v}: {n}")

# All unique spacing values seen
sp_counts = Counter()
for b in rprs:
    sp = get(b, "spacing")
    sp_counts[sp] += 1
print("\n=== spacing val distribution ===")
for v, n in sorted(sp_counts.items(), key=lambda x: (x[0] or "")):
    print(f"  spacing={v}: {n}")
