"""iter-6: p11 surgical — change line=240 to line=220 (-20 twips) on
paragraphs 203..232 (the troubleshooting table rows).
Hypothesis: PDF table is denser than W36's auto 240 lineheight; tighten to 220
to match PDF row density. 30 sites total.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
doc_path = ROOT / "iter-6" / "unpacked" / "word" / "document.xml"
doc = doc_path.read_text(encoding="utf-8")

p_pat = re.compile(r"(<w:p\b[^>]*>)(.*?)(</w:p>)", re.S)

target_idx = set(range(203, 233))  # 30 paragraphs in p11 table

new_chunks = []
last = 0
count_modified = 0
for i, m in enumerate(p_pat.finditer(doc)):
    new_chunks.append(doc[last:m.start()])
    body = m.group(0)
    if i in target_idx:
        # Replace w:line="240" with w:line="220" within this paragraph only
        new_body, n = re.subn(r'(<w:spacing[^/]*?)w:line="240"', r'\1w:line="220"', body)
        if n > 0:
            count_modified += 1
            body = new_body
    new_chunks.append(body)
    last = m.end()
new_chunks.append(doc[last:])

doc2 = "".join(new_chunks)
print(f"Modified {count_modified} paragraphs (target {len(target_idx)})")
doc_path.write_text(doc2, encoding="utf-8")
