"""Recon for iter-55: locate w:line="240" sites on the W41 baseline (8.00/11.98).

Focus: p14 line=240 cohort (idx 281..305 minus 291/300, body-text paragraphs).
Also probe other pages with line=240 cohorts for potential follow-ups.

Page boundary indices (last paragraph of each page, from iter-49/iter-53 recon):
[9, 22, 53, 69, 88, 112, 129, 168, 183, 200, 237, 255, 276, 306]
- page 14: 277..306

Skip indices for p14 line=240 surgery: 291, 300 (those are after=80 section headings
that saturated in iter-53; we want the body-text paragraphs only).
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
doc = (ROOT / "baseline_unpacked" / "word" / "document.xml").read_text(encoding="utf-8")

p_pat = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.S)
spacing_pat = re.compile(r"<w:spacing\b([^/]*)/>", re.S)
pPr_pat = re.compile(r"<w:pPr>(.*?)</w:pPr>", re.S)
t_pat = re.compile(r"<w:t\b[^>]*>(.*?)</w:t>", re.S)


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


line_sites = defaultdict(list)    # line_value -> [(idx, page, before, after, lineRule, text_preview)]
records = []

for i, m in enumerate(p_pat.finditer(doc)):
    body = m.group(1)
    # gather text preview
    text_parts = t_pat.findall(body)
    text_preview = "".join(text_parts)[:40].replace("\n", " ")

    ppr_m = pPr_pat.search(body)
    if not ppr_m:
        records.append((i, para_to_page(i), None, None, None, None, text_preview))
        continue
    ppr = ppr_m.group(1)
    sp_m = spacing_pat.search(ppr)
    if not sp_m:
        records.append((i, para_to_page(i), None, None, None, None, text_preview))
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
    records.append((i, para_to_page(i), line_v, before_v, after_v, lineRule_v, text_preview))
    if line_v == "240":
        line_sites["240"].append((i, para_to_page(i), before_v, after_v, lineRule_v, text_preview))


print("=== iter-55 recon: line=240 sites on W41 baseline ===")
print()
print(f"--- ALL w:line='240' ({len(line_sites['240'])} sites) ---")
page_count = Counter()
for s in line_sites["240"]:
    page_count[s[1]] += 1
    print(f"  idx={s[0]:>3} page={s[1]:>2} before={s[2]} after={s[3]} lineRule={s[4]} text={s[5]!r}")
print()
print(f"Per-page count: {dict(page_count)}")
print()

# p14 line=240 sub-cohort (excluding 291, 300)
print("--- p14 line=240 sub-cohort (idx 281..305 minus 291, 300) ---")
p14_240 = [s for s in line_sites["240"] if 281 <= s[0] <= 305 and s[0] not in (291, 300)]
print(f"  count = {len(p14_240)}")
for s in p14_240:
    print(f"  idx={s[0]:>3} before={s[2]} after={s[3]} lineRule={s[4]} text={s[5]!r}")
print()

# Full p14 dump for confirmation
print("--- page 14 (277..306) all paras ---")
for r in records:
    if r[1] == 14:
        print(f"  idx={r[0]:>3} line={r[2]} before={r[3]} after={r[4]} lineRule={r[5]} text={r[6]!r}")
