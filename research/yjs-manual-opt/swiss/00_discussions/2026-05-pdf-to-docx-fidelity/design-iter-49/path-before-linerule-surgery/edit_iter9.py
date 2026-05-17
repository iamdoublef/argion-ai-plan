"""iter-9: p9 surgical — line=264 -> line=256 on p9 cohort (idx 172..181, 7 sites with 264).
Mild tighten (-8 twips). Targets the bullet sub-paragraphs on the operation page.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
doc_path = ROOT / "iter-9" / "unpacked" / "word" / "document.xml"
doc = doc_path.read_text(encoding="utf-8")

p_pat = re.compile(r"(<w:p\b[^>]*>)(.*?)(</w:p>)", re.S)
# only p9 paragraphs (169..183)
target_idx = set(range(169, 184))

new_chunks = []
last = 0
count_modified = 0
for i, m in enumerate(p_pat.finditer(doc)):
    new_chunks.append(doc[last:m.start()])
    body = m.group(0)
    if i in target_idx:
        new_body, n = re.subn(r'(<w:spacing[^/]*?)w:line="264"', r'\1w:line="256"', body)
        if n > 0:
            count_modified += 1
            body = new_body
    new_chunks.append(body)
    last = m.end()
new_chunks.append(doc[last:])

doc2 = "".join(new_chunks)
print(f"Modified {count_modified} paragraphs")
doc_path.write_text(doc2, encoding="utf-8")
