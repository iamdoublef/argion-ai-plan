"""iter-1: Grep baseline document.xml for sz=13 rPr blocks and tally spacing distribution.

Goals:
- Count sz=13 sites in total
- Tally spacing values (incl. NONE)
- Tally font/color distribution (BLACK / GRAY / WHITE / RED / etc.)
"""
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent
DOC = ROOT.parent / "baseline_unpacked" / "word" / "document.xml"

xml = DOC.read_text(encoding="utf-8")

# All rPr blocks
RPR = re.compile(r'<w:rPr>(?:(?!</w:rPr>).)*?</w:rPr>', re.S)
SZ13 = []
for m in RPR.finditer(xml):
    blk = m.group(0)
    if '<w:sz w:val="13"/>' in blk:
        SZ13.append(blk)

print(f"Total sz=13 rPr blocks: {len(SZ13)}")

# Spacing distribution
sp_counter = Counter()
for blk in SZ13:
    m = re.search(r'<w:spacing w:val="(-?\d+)"/>', blk)
    sp_counter[m.group(1) if m else "NONE"] += 1
print("\nspacing distribution:")
for k, v in sorted(sp_counter.items(), key=lambda x: (-x[1], x[0])):
    print(f"  spacing={k}: {v}")

# Font color distribution
col_counter = Counter()
for blk in SZ13:
    m = re.search(r'<w:color w:val="([0-9A-Fa-f]{6})"', blk)
    col_counter[m.group(1).upper() if m else "NONE"] += 1
print("\ncolor distribution:")
for k, v in sorted(col_counter.items(), key=lambda x: (-x[1], x[0])):
    print(f"  color={k}: {v}")

# Font name distribution
fn_counter = Counter()
for blk in SZ13:
    m = re.search(r'<w:rFonts[^/>]*w:ascii="([^"]+)"', blk)
    fn_counter[m.group(1) if m else "NONE"] += 1
print("\nfont distribution:")
for k, v in sorted(fn_counter.items(), key=lambda x: (-x[1], x[0])):
    print(f"  font={k}: {v}")

# Combinations of (font, color, spacing) for sz=13
combo = Counter()
for blk in SZ13:
    m_font = re.search(r'<w:rFonts[^/>]*w:ascii="([^"]+)"', blk)
    m_col = re.search(r'<w:color w:val="([0-9A-Fa-f]{6})"', blk)
    m_sp = re.search(r'<w:spacing w:val="(-?\d+)"/>', blk)
    combo[(
        m_font.group(1) if m_font else "?",
        m_col.group(1).upper() if m_col else "?",
        m_sp.group(1) if m_sp else "NONE",
    )] += 1
print("\n(font, color, spacing) combo:")
for (f, c, s), v in sorted(combo.items(), key=lambda x: (-x[1], x[0])):
    print(f"  font={f} color={c} spacing={s}: {v}")
