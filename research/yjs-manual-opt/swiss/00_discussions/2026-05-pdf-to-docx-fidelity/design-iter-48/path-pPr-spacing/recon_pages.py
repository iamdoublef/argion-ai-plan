"""Recon: map paragraphs to pages using w:lastRenderedPageBreak markers,
or fallback to position-based estimation.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
doc = (ROOT / "baseline_unpacked" / "word" / "document.xml").read_text(encoding="utf-8")

# w:lastRenderedPageBreak marks page boundaries (page break BEFORE the paragraph it appears in)
# Find them by paragraph index.
p_pat = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.S)
page_breaks = []  # paragraph indices where page changes

# Also look for explicit w:br w:type="page"
breaks_by_pidx = {}
for i, m in enumerate(p_pat.finditer(doc)):
    body = m.group(1)
    if 'lastRenderedPageBreak' in body:
        breaks_by_pidx[i] = 'lastRendered'
    elif '<w:br w:type="page"' in body:
        breaks_by_pidx[i] = 'page-br'

# Also look for sectPr (forces new section/page)
sect_indices = []
for i, m in enumerate(p_pat.finditer(doc)):
    body = m.group(1)
    if '<w:sectPr' in body:
        sect_indices.append(i)

# Compute page boundaries
print(f"Total paragraphs: {sum(1 for _ in p_pat.finditer(doc))}")
print(f"page break markers (by para idx): {len(breaks_by_pidx)}")
for k, v in sorted(breaks_by_pidx.items())[:30]:
    print(f"  p_idx={k}: {v}")
print(f"sectPr (paragraph carries section): {sect_indices}")
