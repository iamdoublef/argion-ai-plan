"""iter-8: Consolas + spacing val=2 (instead of 0) — small spread for chip readability"""
from pathlib import Path
import shutil

BASE = Path(__file__).parent
src = BASE / "iter4_unpacked"  # iter-4 best so far
out = BASE / "iter8_unpacked"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(src, out)

xml = (out / "word" / "document.xml").read_text(encoding="utf-8")

# Inside the chip rPr, change spacing val="0" to val="2" (very subtle letter spread)
old = '''<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas" w:eastAsia="Consolas"/>
                <w:b w:val="0"/>
                <w:sz w:val="13"/>
                <w:color w:val="1A1A1A"/>
                <w:spacing w:val="0"/>'''
new = '''<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas" w:eastAsia="Consolas"/>
                <w:b w:val="0"/>
                <w:sz w:val="13"/>
                <w:color w:val="1A1A1A"/>
                <w:spacing w:val="2"/>'''
count = xml.count(old)
xml = xml.replace(old, new)
print(f"Replaced {count} chip spacing 0→2")
(out / "word" / "document.xml").write_text(xml, encoding="utf-8")
