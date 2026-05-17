"""iter-7: p11 surgical — line=240 -> line=260 on paragraphs 203..232.
Loosen direction. 30 sites.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
doc_path = ROOT / "iter-7" / "unpacked" / "word" / "document.xml"
doc = doc_path.read_text(encoding="utf-8")

p_pat = re.compile(r"(<w:p\b[^>]*>)(.*?)(</w:p>)", re.S)
target_idx = set(range(203, 233))

new_chunks = []
last = 0
count_modified = 0
for i, m in enumerate(p_pat.finditer(doc)):
    new_chunks.append(doc[last:m.start()])
    body = m.group(0)
    if i in target_idx:
        new_body, n = re.subn(r'(<w:spacing[^/]*?)w:line="240"', r'\1w:line="260"', body)
        if n > 0:
            count_modified += 1
            body = new_body
    new_chunks.append(body)
    last = m.end()
new_chunks.append(doc[last:])

doc2 = "".join(new_chunks)
print(f"Modified {count_modified} paragraphs")
doc_path.write_text(doc2, encoding="utf-8")
