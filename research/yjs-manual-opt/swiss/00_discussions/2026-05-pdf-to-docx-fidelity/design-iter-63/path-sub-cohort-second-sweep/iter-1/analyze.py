"""iter-1: Analyze page-isolated sub-cohorts for line=228, spacing=0, char-spacing values."""
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent.parent
BASELINE = ROOT / "baseline_unpacked"

doc = (BASELINE / "word" / "document.xml").read_text(encoding="utf-8")

# Find sectPr positions (each marks the END of a page)
secs = [m.start() for m in re.finditer(r'<w:sectPr', doc)]
print(f"sectPr count: {len(secs)} → pages 1..{len(secs)}")

# Page i spans: page 1 = [0, secs[0]); page 2 = [secs[0], secs[1])... page N = [secs[N-2], end)
def page_span(idx, total_len):
    if idx == 1:
        return 0, secs[0]
    if idx <= len(secs):
        return secs[idx - 2], secs[idx - 1]
    return secs[-1], total_len

# Scan each page for various sub-cohort indicators
TOTAL = len(doc)
print(f"\n=== line=228 per-page distribution ===")
for p in range(1, len(secs) + 1):
    s, e = page_span(p, TOTAL)
    chunk = doc[s:e]
    cnt = chunk.count('w:line="228"')
    if cnt > 0:
        print(f"  p{p}: {cnt} sites")

print(f"\n=== spacing=0 per-page distribution ===")
for p in range(1, len(secs) + 1):
    s, e = page_span(p, TOTAL)
    chunk = doc[s:e]
    cnt = chunk.count('w:spacing w:val="0"') + chunk.count('w:spacing="0"')
    # Better: explicit char spacing pattern
    cnt2 = len(re.findall(r'<w:spacing w:val="0"', chunk))
    if cnt2 > 0:
        print(f"  p{p}: {cnt2} spacing val=0 sites")

print(f"\n=== char-spacing values per-page (rPr w:spacing val=NUM) ===")
# Look for rPr level spacing patterns
char_spacings_per_page = {}
for p in range(1, len(secs) + 1):
    s, e = page_span(p, TOTAL)
    chunk = doc[s:e]
    # Find rPr w:spacing w:val="NUM"
    matches = re.findall(r'<w:spacing w:val="(-?\d+)"/>', chunk)
    if matches:
        c = Counter(matches)
        char_spacings_per_page[p] = c

for p, c in char_spacings_per_page.items():
    print(f"  p{p}: {dict(c)}")

print(f"\n=== line values per-page (pPr w:line) ===")
for p in range(1, len(secs) + 1):
    s, e = page_span(p, TOTAL)
    chunk = doc[s:e]
    matches = re.findall(r'w:line="(\d+)"', chunk)
    if matches:
        c = Counter(matches)
        print(f"  p{p}: {dict(c)}")

print(f"\n=== p3 detailed: line / char-spacing / font ===")
s, e = page_span(3, TOTAL)
p3 = doc[s:e]
print(f"  p3 length: {len(p3)}")
print(f"  line= values: {Counter(re.findall(r'w:line=\"(\\d+)\"', p3))}")
print(f"  rPr w:spacing values: {Counter(re.findall(r'<w:spacing w:val=\"(-?\\d+)\"/>', p3))}")
print(f"  w:sz values: {Counter(re.findall(r'<w:sz w:val=\"(\\d+)\"/>', p3))}")

print(f"\n=== p9 detailed ===")
s, e = page_span(9, TOTAL)
p9 = doc[s:e]
print(f"  p9 length: {len(p9)}")
print(f"  line= values: {Counter(re.findall(r'w:line=\"(\\d+)\"', p9))}")
print(f"  rPr w:spacing values: {Counter(re.findall(r'<w:spacing w:val=\"(-?\\d+)\"/>', p9))}")
print(f"  w:sz values: {Counter(re.findall(r'<w:sz w:val=\"(\\d+)\"/>', p9))}")

print(f"\n=== p11 detailed (max page) ===")
s, e = page_span(11, TOTAL)
p11 = doc[s:e]
print(f"  p11 length: {len(p11)}")
print(f"  line= values: {Counter(re.findall(r'w:line=\"(\\d+)\"', p11))}")
print(f"  rPr w:spacing values: {Counter(re.findall(r'<w:spacing w:val=\"(-?\\d+)\"/>', p11))}")
print(f"  w:sz values: {Counter(re.findall(r'<w:sz w:val=\"(\\d+)\"/>', p11))}")
# colors
print(f"  w:color values: {Counter(re.findall(r'<w:color w:val=\"([^\"]+)\"', p11))}")
print(f"  tcBorders sz values: {Counter(re.findall(r'<w:(?:top|bottom|left|right|insideH|insideV) w:val=\"single\" w:sz=\"(\\d+)\" w:space=\"0\" w:color=\"([^\"]+)\"', p11))}")
