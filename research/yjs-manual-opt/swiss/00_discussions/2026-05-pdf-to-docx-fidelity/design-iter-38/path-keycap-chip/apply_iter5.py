"""iter-5: Consolas + bdr sz=6 (thicker border 0.75pt) + space=2"""
from pathlib import Path
import shutil

BASE = Path(__file__).parent
src = BASE / "iter4_unpacked"
out = BASE / "iter5_unpacked"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(src, out)

xml = (out / "word" / "document.xml").read_text(encoding="utf-8")
old = '<w:bdr w:val="single" w:sz="4" w:space="1" w:color="000000"/>'
new = '<w:bdr w:val="single" w:sz="6" w:space="2" w:color="000000"/>'
xml = xml.replace(old, new)
(out / "word" / "document.xml").write_text(xml, encoding="utf-8")
