"""iter-3: Chip uses sz=12 (6pt) instead of sz=13 (6.5pt) — target uses 6pt mono"""
from pathlib import Path
import shutil

BASE = Path(__file__).parent
src = BASE / "iter1_unpacked"
out = BASE / "iter3_unpacked"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(src, out)

xml = (out / "word" / "document.xml").read_text(encoding="utf-8")

# Target chip rPr block — change sz from 13 to 12 only inside Courier-bordered runs.
# Pattern: rFonts Courier New + sz 13 → sz 12
old = '''<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New" w:eastAsia="Courier New"/>
                <w:b w:val="0"/>
                <w:sz w:val="13"/>'''
new = '''<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New" w:eastAsia="Courier New"/>
                <w:b w:val="0"/>
                <w:sz w:val="12"/>'''
count = xml.count(old)
xml = xml.replace(old, new)
print(f"Replaced {count} chip sz 13→12")

(out / "word" / "document.xml").write_text(xml, encoding="utf-8")
print("Written iter3_unpacked/word/document.xml")
