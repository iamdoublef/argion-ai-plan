"""iter-10: CONTROL — single line WITHOUT chip styling. Test: does line restructure alone help?
"""
from pathlib import Path
import shutil

BASE = Path(__file__).parent
src = BASE / "baseline_unpacked"
out = BASE / "iter10_unpacked"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(src, out)

xml = (out / "word" / "document.xml").read_text(encoding="utf-8")

NORMAL_RPR = '''<w:rPr>
                <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei"/>
                <w:b w:val="0"/>
                <w:sz w:val="13"/>
                <w:color w:val="1A1A1A"/>
                <w:spacing w:val="5"/>
              </w:rPr>'''

cells = [
    ("1", "Power", "电源"),
    ("2", "Make Ice", "制冰"),
    ("3", "Clean", "清洁"),
    ("4", "ICE FULL", "冰满"),
    ("5", "ADD WATER", "加水"),
]

for num, eng, zh in cells:
    old = (
        f'<w:r>\n              {NORMAL_RPR}\n'
        f'              <w:t>{num}</w:t>\n'
        f'              <w:br/>\n'
        f'              <w:t>{eng}</w:t>\n'
        f'              <w:br/>\n'
        f'              <w:t>{zh}</w:t>\n'
        f'            </w:r>'
    )
    new = (
        f'<w:r>\n              {NORMAL_RPR}\n'
        f'              <w:t xml:space="preserve">{num} {eng} {zh}</w:t>\n'
        f'            </w:r>'
    )
    if old not in xml:
        print(f"WARN: {num} not found")
        continue
    xml = xml.replace(old, new)
    print(f"OK: {num} {eng}")

(out / "word" / "document.xml").write_text(xml, encoding="utf-8")
