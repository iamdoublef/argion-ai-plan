"""iter-15: stack iter-9 + p11 line loosen on the failure table.

In failure table at line 6603, the inner paragraphs have w:line="240".
Try changing failure table inner p's line spacing.
Also examine p11 region outside the table.
"""
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "unpacked" / "word" / "document.xml"
text = DOC.read_text(encoding="utf-8")
lines = text.split("\n")

P13_START, P13_END = 8382, 8867
P9_START, P9_END = 5301, 5787
for i in range(P13_START, P13_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="278"')
for i in range(P9_START, P9_END):
    if 'w:line="271"' in lines[i]:
        lines[i] = lines[i].replace('w:line="271"', 'w:line="264"')

# p11 region 6534-7835; failure table is 6603-7759. Modify the table's spacing line=240 within
# Try changing inner cell <w:line="240"> -> <w:line="245"> ONLY in the failure table (anchored)
text2 = "\n".join(lines)
# locate failure table
start_anchor = '<w:gridCol w:w="1596"/>\n        <w:gridCol w:w="2395"/>\n        <w:gridCol w:w="3265"/>'
anchor_idx = text2.index(start_anchor)
tbl_open = text2.rfind("<w:tbl>", 0, anchor_idx)
tbl_close = text2.index("</w:tbl>", anchor_idx) + len("</w:tbl>")
block = text2[tbl_open:tbl_close]
n_orig = block.count('w:line="240"')
new_block = block.replace('w:line="240"', 'w:line="245"')
print(f"failure table: w:line='240' -> '245' (orig {n_orig})")
new_text = text2[:tbl_open] + new_block + text2[tbl_close:]
DOC.write_text(new_text, encoding="utf-8")
