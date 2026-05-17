"""iter-1: Apply keycap chip restructure on p7 function table.

Converts cell content from stacked 3-line:
    <w:r><...rPr...><w:t>N</w:t><w:br/><w:t>English</w:t><w:br/><w:t>Chinese</w:t></w:r>
to single-line with chip:
    <w:r><...rPr...><w:t xml:space="preserve">N </w:t></w:r>
    <w:r><...rPr courier+bdr...><w:t>English</w:t></w:r>
    <w:r><...rPr...><w:t xml:space="preserve"> Chinese</w:t></w:r>
"""
from pathlib import Path
import re

BASE = Path(__file__).parent
src = BASE / "baseline_unpacked" / "word" / "document.xml"
xml = src.read_text(encoding="utf-8")

# The 5 p7 keycap cells share the same rPr pattern:
# <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei"/>
# <w:b w:val="0"/><w:sz w:val="13"/><w:color w:val="1A1A1A"/><w:spacing w:val="5"/>

NORMAL_RPR = '''<w:rPr>
                <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei"/>
                <w:b w:val="0"/>
                <w:sz w:val="13"/>
                <w:color w:val="1A1A1A"/>
                <w:spacing w:val="5"/>
              </w:rPr>'''

# Chip rPr: Courier New monospace + single black border with small padding
# w:space="2" = 2pt cell padding inside the border
CHIP_RPR = '''<w:rPr>
                <w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New" w:eastAsia="Courier New"/>
                <w:b w:val="0"/>
                <w:sz w:val="13"/>
                <w:color w:val="1A1A1A"/>
                <w:spacing w:val="0"/>
                <w:bdr w:val="single" w:sz="4" w:space="0" w:color="000000"/>
              </w:rPr>'''

cells = [
    ("1", "Power", "电源"),
    ("2", "Make Ice", "制冰"),
    ("3", "Clean", "清洁"),
    ("4", "ICE FULL", "冰满"),
    ("5", "ADD WATER", "加水"),
]

for num, eng, zh in cells:
    # Match the old stacked pattern. Old pattern:
    # <w:r>\n              <w:rPr>...</w:rPr>\n              <w:t>N</w:t>\n              <w:br/>\n              <w:t>ENG</w:t>\n              <w:br/>\n              <w:t>ZH</w:t>\n            </w:r>
    old_pattern = (
        f'<w:r>\n              {NORMAL_RPR}\n'
        f'              <w:t>{num}</w:t>\n'
        f'              <w:br/>\n'
        f'              <w:t>{eng}</w:t>\n'
        f'              <w:br/>\n'
        f'              <w:t>{zh}</w:t>\n'
        f'            </w:r>'
    )
    new_pattern = (
        f'<w:r>\n              {NORMAL_RPR}\n'
        f'              <w:t xml:space="preserve">{num} </w:t>\n'
        f'            </w:r>\n'
        f'            <w:r>\n              {CHIP_RPR}\n'
        f'              <w:t xml:space="preserve">{eng}</w:t>\n'
        f'            </w:r>\n'
        f'            <w:r>\n              {NORMAL_RPR}\n'
        f'              <w:t xml:space="preserve"> {zh}</w:t>\n'
        f'            </w:r>'
    )
    if old_pattern not in xml:
        print(f"WARN: pattern for cell {num} ({eng}) not found verbatim")
        # Show what's around the keycap to debug
        idx = xml.find(f"<w:t>{eng}</w:t>")
        if idx >= 0:
            print("---context---")
            print(xml[max(0, idx-400):idx+200])
            print("---end---")
        continue
    xml = xml.replace(old_pattern, new_pattern)
    print(f"OK: cell {num} ({eng}) → chip")

out = BASE / "iter1_unpacked"
import shutil
if out.exists():
    shutil.rmtree(out)
shutil.copytree(BASE / "baseline_unpacked", out)
(out / "word" / "document.xml").write_text(xml, encoding="utf-8")
print(f"Written: {out / 'word' / 'document.xml'}")
