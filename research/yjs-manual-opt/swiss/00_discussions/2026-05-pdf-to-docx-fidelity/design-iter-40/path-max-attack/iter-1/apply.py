"""iter-1: p11 fault table tcW redistribution 1596/2395/3265 -> 1500/2800/2956.

Only the failure table at line ~6618 has the (1596,2395,3265) col combo.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
DOC = ROOT / "unpacked" / "word" / "document.xml"

text = DOC.read_text(encoding="utf-8")

# The failure table starts at line ~6618 with gridCol 1596/2395/3265
# We want to convert that table's cells only.
# Strategy: locate the table block by anchor "<w:gridCol w:w=\"1596\"/>\n        <w:gridCol w:w=\"2395\"/>"
# then within that table (until matching </w:tbl>) replace each col-w tag.

start_anchor = '<w:gridCol w:w="1596"/>\n        <w:gridCol w:w="2395"/>\n        <w:gridCol w:w="3265"/>'
assert text.count(start_anchor) == 1, f"Anchor not unique: {text.count(start_anchor)}"
anchor_idx = text.index(start_anchor)

# find enclosing <w:tbl> open and </w:tbl> close
tbl_open = text.rfind("<w:tbl>", 0, anchor_idx)
tbl_close = text.index("</w:tbl>", anchor_idx) + len("</w:tbl>")
assert tbl_open != -1
table_block = text[tbl_open:tbl_close]

# Replace dxa widths inside this block
new_block = table_block
# gridCol replacements first
new_block = new_block.replace('<w:gridCol w:w="1596"/>', '<w:gridCol w:w="1500"/>', 1)
new_block = new_block.replace('<w:gridCol w:w="2395"/>', '<w:gridCol w:w="2800"/>', 1)
new_block = new_block.replace('<w:gridCol w:w="3265"/>', '<w:gridCol w:w="2956"/>', 1)
# tcW dxa replacements: must keep type="dxa" intact
new_block = re.sub(r'(<w:tcW w:type="dxa" w:w=)"1596"', r'\1"1500"', new_block)
new_block = re.sub(r'(<w:tcW w:type="dxa" w:w=)"2395"', r'\1"2800"', new_block)
new_block = re.sub(r'(<w:tcW w:type="dxa" w:w=)"3265"', r'\1"2956"', new_block)

# Sanity: solution col (3265) appears 6 times in another table (page 5/6),
# verify we only touched the failure table block.
# Within this block, count tcW 3265: should be 13 (header + 12 rows)
n_solution_old = table_block.count('<w:tcW w:type="dxa" w:w="3265"/>')
n_solution_new = new_block.count('<w:tcW w:type="dxa" w:w="2956"/>')
print(f"failure table: 3265 occurrences {n_solution_old} -> 2956 {n_solution_new}")
assert n_solution_old == n_solution_new

# Splice back
new_text = text[:tbl_open] + new_block + text[tbl_close:]

# Sanity: outside the block, 3265 should still exist (table at line 3336 has 3265)
outside_old = (text[:tbl_open] + text[tbl_close:]).count('w:w="3265"')
outside_new = (new_text[:tbl_open] + new_text[tbl_open + len(new_block):]).count('w:w="3265"')
print(f"outside: 3265 count {outside_old} -> {outside_new} (should be equal)")
assert outside_old == outside_new

DOC.write_text(new_text, encoding="utf-8")
print(f"Wrote {DOC}")
print(f"length change: {len(text)} -> {len(new_text)}")
