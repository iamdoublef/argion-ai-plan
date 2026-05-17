"""Recon: pPr w:spacing attributes (line/before/after/lineRule/contextualSpacing)
in W36 baseline. Find cohorts and per-page distribution.
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
doc = (ROOT / "baseline_unpacked" / "word" / "document.xml").read_text(encoding="utf-8")

# Find all <w:p ...>...</w:p> blocks; within each, find pPr/spacing
p_pat = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.S)
spacing_pat = re.compile(r"<w:spacing\b([^/]*)/>", re.S)
pPr_pat = re.compile(r"<w:pPr>(.*?)</w:pPr>", re.S)
contextual_pat = re.compile(r"<w:contextualSpacing\b[^/]*/>", re.S)

# Cohorts by attribute set
attr_counter = Counter()
line_vals = Counter()
before_vals = Counter()
after_vals = Counter()
lineRule_vals = Counter()
contextual_count = 0
total_p = 0
p_with_pPr = 0
p_with_spacing = 0
per_para_records = []

for i, m in enumerate(p_pat.finditer(doc)):
    body = m.group(1)
    total_p += 1
    ppr_m = pPr_pat.search(body)
    if not ppr_m:
        continue
    p_with_pPr += 1
    ppr = ppr_m.group(1)
    sp_m = spacing_pat.search(ppr)
    has_ctx = bool(contextual_pat.search(ppr))
    if has_ctx:
        contextual_count += 1
    if not sp_m:
        continue
    p_with_spacing += 1
    attrs = sp_m.group(1)
    # parse attrs
    line = re.search(r'w:line="(\d+)"', attrs)
    before = re.search(r'w:before="(\d+)"', attrs)
    after = re.search(r'w:after="(\d+)"', attrs)
    lineRule = re.search(r'w:lineRule="(\w+)"', attrs)
    line_v = line.group(1) if line else None
    before_v = before.group(1) if before else None
    after_v = after.group(1) if after else None
    lineRule_v = lineRule.group(1) if lineRule else None
    if line_v: line_vals[line_v] += 1
    if before_v: before_vals[before_v] += 1
    if after_v: after_vals[after_v] += 1
    if lineRule_v: lineRule_vals[lineRule_v] += 1
    key = (line_v, before_v, after_v, lineRule_v)
    attr_counter[key] += 1
    per_para_records.append((i, line_v, before_v, after_v, lineRule_v))

print(f"=== W36 baseline pPr w:spacing recon ===")
print(f"Total <w:p>: {total_p}")
print(f"With pPr: {p_with_pPr}")
print(f"With pPr/w:spacing: {p_with_spacing}")
print(f"With pPr/w:contextualSpacing: {contextual_count}")
print()
print(f"--- w:line values ({sum(line_vals.values())} sites) ---")
for v, c in line_vals.most_common():
    print(f"  line={v}: {c}")
print()
print(f"--- w:before values ({sum(before_vals.values())} sites) ---")
for v, c in before_vals.most_common():
    print(f"  before={v}: {c}")
print()
print(f"--- w:after values ({sum(after_vals.values())} sites) ---")
for v, c in after_vals.most_common():
    print(f"  after={v}: {c}")
print()
print(f"--- w:lineRule values ---")
for v, c in lineRule_vals.most_common():
    print(f"  lineRule={v}: {c}")
print()
print(f"--- Top 20 attr-tuples (line, before, after, lineRule) ---")
for k, c in attr_counter.most_common(20):
    print(f"  {k}: {c}")
print()
# Check sectPr (page-level) lineRule/line is irrelevant — sectPr has different schema.

# Look for line values that suggest tightening could help (e.g., near common heading sizes)
# heading-ish: line in [200..320], before in [0..200], after in [0..200]
print(f"--- Line value distribution by para index (first/last 5 of each line cohort) ---")
by_line = defaultdict(list)
for rec in per_para_records:
    by_line[rec[1]].append(rec[0])
for line_v, indices in sorted(by_line.items(), key=lambda x: -len(x[1]))[:10]:
    print(f"  line={line_v}: count={len(indices)}  first_idx={indices[0]}  last_idx={indices[-1]}")
