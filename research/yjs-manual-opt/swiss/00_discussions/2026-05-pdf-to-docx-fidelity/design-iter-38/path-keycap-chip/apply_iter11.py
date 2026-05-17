"""iter-11: Try chip with bold weight"""
from pathlib import Path
import shutil

BASE = Path(__file__).parent
src = BASE / "iter8_unpacked"
out = BASE / "iter11_unpacked"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(src, out)

xml = (out / "word" / "document.xml").read_text(encoding="utf-8")

# In chip rPr, change <w:b w:val="0"/> to <w:b/>
# Pattern only inside Consolas + bdr block
old = '''<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas" w:eastAsia="Consolas"/>
                <w:b w:val="0"/>
                <w:sz w:val="13"/>'''
new = '''<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas" w:eastAsia="Consolas"/>
                <w:b/>
                <w:sz w:val="13"/>'''
count = xml.count(old)
xml = xml.replace(old, new)
print(f"Replaced {count} chips b 0→bold")

(out / "word" / "document.xml").write_text(xml, encoding="utf-8")
