"""iter-4: Try Consolas (a tighter monospace) + small space=1 padding"""
from pathlib import Path
import shutil

BASE = Path(__file__).parent
src = BASE / "iter1_unpacked"
out = BASE / "iter4_unpacked"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(src, out)

xml = (out / "word" / "document.xml").read_text(encoding="utf-8")

# Replace Courier New with Consolas (tighter, more modern mono — closer to chips in target)
old_font = '<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New" w:eastAsia="Courier New"/>'
new_font = '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas" w:eastAsia="Consolas"/>'
count = xml.count(old_font)
xml = xml.replace(old_font, new_font)
print(f"Replaced {count} Courier New → Consolas")

# Bump padding from 0 to 1
old_bdr = '<w:bdr w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
new_bdr = '<w:bdr w:val="single" w:sz="4" w:space="1" w:color="000000"/>'
count2 = xml.count(old_bdr)
xml = xml.replace(old_bdr, new_bdr)
print(f"Replaced {count2} bdr space 0→1")

(out / "word" / "document.xml").write_text(xml, encoding="utf-8")
