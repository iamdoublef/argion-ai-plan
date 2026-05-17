"""Recon for iter-53: locate w:after="80", w:after="120", w:line="271" sites
on the W40 baseline (8.01/11.98).

Page boundary indices (last paragraph of each page, from iter-49 recon):
[9, 22, 53, 69, 88, 112, 129, 168, 183, 200, 237, 255, 276, 306]
- page 14: 277..306
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
doc = (ROOT / "baseline_unpacked" / "word" / "document.xml").read_text(encoding="utf-8")

p_pat = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.S)
spacing_pat = re.compile(r"<w:spacing\b([^/]*)/>", re.S)
pPr_pat = re.compile(r"<w:pPr>(.*?)</w:pPr>", re.S)

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


after_sites = defaultdict(list)   # after_value -> [(idx, page, line, before)]
line_sites = defaultdict(list)    # line_value -> [(idx, page, before, after)]

records = []

for i, m in enumerate(p_pat.finditer(doc)):
    body = m.group(1)
    ppr_m = pPr_pat.search(body)
    if not ppr_m:
        records.append((i, para_to_page(i), None, None, None, None))
        continue
    ppr = ppr_m.group(1)
    sp_m = spacing_pat.search(ppr)
    if not sp_m:
        records.append((i, para_to_page(i), None, None, None, None))
        continue
    attrs = sp_m.group(1)
    line = re.search(r'w:line="(\d+)"', attrs)
    before = re.search(r'w:before="(\d+)"', attrs)
    after = re.search(r'w:after="(\d+)"', attrs)
    lineRule = re.search(r'w:lineRule="(\w+)"', attrs)
    line_v = line.group(1) if line else None
    before_v = before.group(1) if before else None
    after_v = after.group(1) if after else None
    lineRule_v = lineRule.group(1) if lineRule else None
    records.append((i, para_to_page(i), line_v, before_v, after_v, lineRule_v))
    if after_v == "80":
        after_sites["80"].append((i, para_to_page(i), line_v, before_v))
    if after_v == "120":
        after_sites["120"].append((i, para_to_page(i), line_v, before_v))
    if line_v == "271":
        line_sites["271"].append((i, para_to_page(i), before_v, after_v))


print("=== iter-53 recon on W40 baseline ===")
print()
print(f"--- w:after='80' ({len(after_sites['80'])} sites) ---")
for s in after_sites["80"]:
    print(f"  idx={s[0]:>3} page={s[1]:>2} line={s[2]} before={s[3]}")
print()
print(f"--- w:after='120' ({len(after_sites['120'])} sites) ---")
for s in after_sites["120"]:
    print(f"  idx={s[0]:>3} page={s[1]:>2} line={s[2]} before={s[3]}")
print()
print(f"--- w:line='271' ({len(line_sites['271'])} sites) ---")
for s in line_sites["271"]:
    print(f"  idx={s[0]:>3} page={s[1]:>2} before={s[2]} after={s[3]}")
print()

# Per-page breakdown for p14
print("--- page 14 (277..306) ---")
for r in records:
    if r[1] == 14:
        print(f"  idx={r[0]:>3} line={r[2]} before={r[3]} after={r[4]} lineRule={r[5]}")
