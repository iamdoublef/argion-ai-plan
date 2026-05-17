"""iter-2: Chip variant — wider padding (w:space=4) to match target's chunkier chip"""
from pathlib import Path
import shutil

BASE = Path(__file__).parent
src = BASE / "iter1_unpacked"
out = BASE / "iter2_unpacked"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(src, out)

xml = (out / "word" / "document.xml").read_text(encoding="utf-8")

# Change all w:space="0" to w:space="4" in <w:bdr> elements (just the keycap chip ones)
# More targeted: find <w:bdr w:val="single" w:sz="4" w:space="0" w:color="000000"/>
old = '<w:bdr w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
new = '<w:bdr w:val="single" w:sz="4" w:space="4" w:color="000000"/>'
count = xml.count(old)
xml = xml.replace(old, new)
print(f"Replaced {count} chip border w:space=0→4")

(out / "word" / "document.xml").write_text(xml, encoding="utf-8")
print("Written iter2_unpacked/word/document.xml")
