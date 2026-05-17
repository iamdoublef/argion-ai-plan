"""iter-2: p11 failure table tcW reweight 1596/2395/3265 -> 1700/2200/3357.

Shrink cause column, widen solution column slightly - opposite of iter-1.
Symptom slightly wider as a comfort.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "unpacked" / "word" / "document.xml"

text = DOC.read_text(encoding="utf-8")
start_anchor = '<w:gridCol w:w="1596"/>\n        <w:gridCol w:w="2395"/>\n        <w:gridCol w:w="3265"/>'
assert text.count(start_anchor) == 1
anchor_idx = text.index(start_anchor)
tbl_open = text.rfind("<w:tbl>", 0, anchor_idx)
tbl_close = text.index("</w:tbl>", anchor_idx) + len("</w:tbl>")
table_block = text[tbl_open:tbl_close]

new_block = table_block
new_block = new_block.replace('<w:gridCol w:w="1596"/>', '<w:gridCol w:w="1700"/>', 1)
new_block = new_block.replace('<w:gridCol w:w="2395"/>', '<w:gridCol w:w="2200"/>', 1)
new_block = new_block.replace('<w:gridCol w:w="3265"/>', '<w:gridCol w:w="3357"/>', 1)
new_block = re.sub(r'(<w:tcW w:type="dxa" w:w=)"1596"', r'\1"1700"', new_block)
new_block = re.sub(r'(<w:tcW w:type="dxa" w:w=)"2395"', r'\1"2200"', new_block)
new_block = re.sub(r'(<w:tcW w:type="dxa" w:w=)"3265"', r'\1"3357"', new_block)

new_text = text[:tbl_open] + new_block + text[tbl_close:]
# total should still be 7257
DOC.write_text(new_text, encoding="utf-8")
print(f"Wrote {DOC} (1700/2200/3357 -- sum {1700+2200+3357})")
