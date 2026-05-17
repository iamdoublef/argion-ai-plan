"""Recon: dump paragraph index + line/before/after + text snippet for hot pages.
Tells us which paragraphs are good candidates for surgical edits.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
doc = (ROOT / "baseline_unpacked" / "word" / "document.xml").read_text(encoding="utf-8")

p_pat = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.S)
spacing_pat = re.compile(r"<w:spacing\b([^/]*)/>", re.S)
pPr_pat = re.compile(r"<w:pPr>(.*?)</w:pPr>", re.S)
t_pat = re.compile(r"<w:t[^>]*>([^<]*)</w:t>")

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

import sys
hot_pages = set(int(p) for p in sys.argv[1:]) if len(sys.argv) > 1 else {3, 9, 11, 14}

for i, m in enumerate(p_pat.finditer(doc)):
    page = para_to_page(i)
    if page not in hot_pages:
        continue
    body = m.group(1)
    ppr_m = pPr_pat.search(body)
    line = before = after = lineRule = None
    if ppr_m:
        sp_m = spacing_pat.search(ppr_m.group(1))
        if sp_m:
            attrs = sp_m.group(1)
            line_m = re.search(r'w:line="(\d+)"', attrs)
            before_m = re.search(r'w:before="(\d+)"', attrs)
            after_m = re.search(r'w:after="(\d+)"', attrs)
            lr_m = re.search(r'w:lineRule="(\w+)"', attrs)
            line = line_m.group(1) if line_m else None
            before = before_m.group(1) if before_m else None
            after = after_m.group(1) if after_m else None
            lineRule = lr_m.group(1) if lr_m else None
    texts = t_pat.findall(body)
    text = "".join(texts).strip()[:60]
    print(f"p{page} idx={i:3d} line={line} bef={before} aft={after} lr={lineRule}  text={text!r}")
