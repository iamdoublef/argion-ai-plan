"""iter-8: p3 surgical — line=230 -> line=226 on bullet paragraphs 28..51 (24 sites).
Very small tighten (-4 twips, equivalent to ~0.2pt). Surgical, not global.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
doc_path = ROOT / "iter-8" / "unpacked" / "word" / "document.xml"
doc = doc_path.read_text(encoding="utf-8")

p_pat = re.compile(r"(<w:p\b[^>]*>)(.*?)(</w:p>)", re.S)
target_idx = set(range(28, 52))  # 24 bullet paragraphs

new_chunks = []
last = 0
count_modified = 0
for i, m in enumerate(p_pat.finditer(doc)):
    new_chunks.append(doc[last:m.start()])
    body = m.group(0)
    if i in target_idx:
        new_body, n = re.subn(r'(<w:spacing[^/]*?)w:line="230"', r'\1w:line="226"', body)
        if n > 0:
            count_modified += 1
            body = new_body
    new_chunks.append(body)
    last = m.end()
new_chunks.append(doc[last:])

doc2 = "".join(new_chunks)
print(f"Modified {count_modified} paragraphs (target {len(target_idx)})")
doc_path.write_text(doc2, encoding="utf-8")
