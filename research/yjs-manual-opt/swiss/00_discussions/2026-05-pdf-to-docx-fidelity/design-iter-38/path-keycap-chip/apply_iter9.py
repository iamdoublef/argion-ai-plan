"""iter-9: chip spacing val=5 (match normal run's spacing)"""
from pathlib import Path
import shutil

BASE = Path(__file__).parent
src = BASE / "iter4_unpacked"
out = BASE / "iter9_unpacked"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(src, out)

xml = (out / "word" / "document.xml").read_text(encoding="utf-8")

old = '<w:spacing w:val="0"/>\n                <w:bdr w:val="single" w:sz="4" w:space="1" w:color="000000"/>'
new = '<w:spacing w:val="5"/>\n                <w:bdr w:val="single" w:sz="4" w:space="1" w:color="000000"/>'
count = xml.count(old)
xml = xml.replace(old, new)
print(f"Replaced {count}")
(out / "word" / "document.xml").write_text(xml, encoding="utf-8")
