"""Recon for iter-49: distribution of w:before, w:lineRule, and per-page
(p3, p9, p11, p14) paragraph mapping for single-paragraph surgery.

W36 baseline section-bearing paragraph indices (from iter-48):
[9, 22, 53, 69, 88, 112, 129, 168, 183, 200, 237, 255, 276, 306]
- page 1: 0..9
- page 2: 10..22
- page 3: 23..53
- page 4: 54..69
- page 5: 70..88
- page 6: 89..112
- page 7: 113..129
- page 8: 130..168
- page 9: 169..183
- page 10: 184..200
- page 11: 201..237
- page 12: 238..255
- page 13: 256..276
- page 14: 277..306
- page 15: 307..end
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
doc = (ROOT / "baseline_unpacked" / "word" / "document.xml").read_text(encoding="utf-8")

p_pat = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.S)
spacing_pat = re.compile(r"<w:spacing\b([^/]*)/>", re.S)
pPr_pat = re.compile(r"<w:pPr>(.*?)</w:pPr>", re.S)
sectPr_pat = re.compile(r"<w:sectPr\b", re.S)

# page boundary indices (last paragraph of each page, from iter-48 STATUS.md)
section_bearing = [9, 22, 53, 69, 88, 112, 129, 168, 183, 200, 237, 255, 276, 306]
# page i starts at section_bearing[i-1] + 1 (or 0 for page 1) and ends at section_bearing[i]
def para_to_page(idx):
    if idx <= 9: return 1
    if idx <= 22: return 2
    if idx <= 53: return 3
    if idx <= 69: return 4
    if idx <= 88: return 5
    if idx <= 112: return 6
    if idx <= 129: return 7
    if idx <= 168: return 8
    if idx <= 183: return 9
    if idx <= 200: return 10
    if idx <= 237: return 11
    if idx <= 255: return 12
    if idx <= 276: return 13
    if idx <= 306: return 14
    return 15

before_vals = Counter()
lineRule_vals = Counter()
total_p = 0
p_with_before = 0
p_with_spacing = 0

records = []  # (idx, page, line, before, after, lineRule)

for i, m in enumerate(p_pat.finditer(doc)):
    body = m.group(1)
    total_p += 1
    ppr_m = pPr_pat.search(body)
    if not ppr_m:
        records.append((i, para_to_page(i), None, None, None, None))
        continue
    ppr = ppr_m.group(1)
    sp_m = spacing_pat.search(ppr)
    if not sp_m:
        records.append((i, para_to_page(i), None, None, None, None))
        continue
    p_with_spacing += 1
    attrs = sp_m.group(1)
    line = re.search(r'w:line="(\d+)"', attrs)
    before = re.search(r'w:before="(\d+)"', attrs)
    after = re.search(r'w:after="(\d+)"', attrs)
    lineRule = re.search(r'w:lineRule="(\w+)"', attrs)
    line_v = line.group(1) if line else None
    before_v = before.group(1) if before else None
    after_v = after.group(1) if after else None
    lineRule_v = lineRule.group(1) if lineRule else None
    if before_v is not None:
        p_with_before += 1
        before_vals[before_v] += 1
    if lineRule_v: lineRule_vals[lineRule_v] += 1
    records.append((i, para_to_page(i), line_v, before_v, after_v, lineRule_v))

print(f"=== W36 recon iter-49 ===")
print(f"Total <w:p>: {total_p}  with w:spacing: {p_with_spacing}  with w:before attr: {p_with_before}")
print()
print(f"--- w:before values ({sum(before_vals.values())} sites) ---")
for v, c in before_vals.most_common():
    print(f"  before={v}: {c}")
print()
print(f"--- w:lineRule values ---")
for v, c in lineRule_vals.most_common():
    print(f"  lineRule={v}: {c}")
print()

# per-page breakdown for hot pages p3/p9/p11/p14
hot_pages = [3, 9, 11, 14]
for page in hot_pages:
    page_recs = [r for r in records if r[1] == page]
    print(f"--- page {page} ({len(page_recs)} paragraphs) ---")
    line_c = Counter(r[2] for r in page_recs)
    before_c = Counter(r[3] for r in page_recs)
    after_c = Counter(r[4] for r in page_recs)
    print(f"  line   distribution: {dict(line_c)}")
    print(f"  before distribution: {dict(before_c)}")
    print(f"  after  distribution: {dict(after_c)}")
    print()

# global per-page before distribution
print(f"--- per-page w:before site count ---")
page_before = defaultdict(int)
for r in records:
    if r[3] is not None and r[3] != "0":
        page_before[r[1]] += 1
for page in sorted(page_before):
    print(f"  page {page}: {page_before[page]} sites")
