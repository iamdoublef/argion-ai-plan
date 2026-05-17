"""Reduce character spacing on body text (sz=14, color=000000 or 1A1A1A).

Approach: find rPr blocks that have w:sz=14 AND body color, AND
w:spacing=5; then text-replace that ONE spacing inside.
"""
import re
from pathlib import Path

p = Path(__file__).parent / "unpacked" / "word" / "document.xml"
s = p.read_text(encoding="utf-8")

# Match each individual <w:rPr>...</w:rPr> block
rpr_re = re.compile(r"<w:rPr>(.*?)</w:rPr>", re.DOTALL)

new_pieces = []
last_end = 0
count = 0
for m in rpr_re.finditer(s):
    block = m.group(1)
    new_pieces.append(s[last_end:m.start()])
    if (
        '<w:sz w:val="14"/>' in block
        and ('<w:color w:val="000000"/>' in block or '<w:color w:val="1A1A1A"/>' in block)
        and '<w:spacing w:val="5"/>' in block
    ):
        new_block = block.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="8"/>', 1)
        count += 1
    else:
        new_block = block
    new_pieces.append("<w:rPr>" + new_block + "</w:rPr>")
    last_end = m.end()

new_pieces.append(s[last_end:])
new_s = "".join(new_pieces)
print(f"Replaced {count} body rPr blocks")
p.write_text(new_s, encoding="utf-8")
