"""iter-stack-w39: Stack p9 line=264->252 on top of parallel agent's W39
(iter-51/iter-5/output.docx, 8.06/11.98). Test if my path composes with theirs.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
doc_path = ROOT / "iter-stack-w39" / "unpacked" / "word" / "document.xml"
doc = doc_path.read_text(encoding="utf-8")

p_pat = re.compile(r"(<w:p\b[^>]*>)(.*?)(</w:p>)", re.S)
target_idx = set(range(169, 184))

new_chunks = []
last = 0
count_modified = 0
for i, m in enumerate(p_pat.finditer(doc)):
    new_chunks.append(doc[last:m.start()])
    body = m.group(0)
    if i in target_idx:
        new_body, n = re.subn(r'(<w:spacing[^/]*?)w:line="264"', r'\1w:line="252"', body)
        if n > 0:
            count_modified += 1
            body = new_body
    new_chunks.append(body)
    last = m.end()
new_chunks.append(doc[last:])

doc2 = "".join(new_chunks)
print(f"Modified {count_modified} paragraphs (target {len(target_idx)})")
doc_path.write_text(doc2, encoding="utf-8")
