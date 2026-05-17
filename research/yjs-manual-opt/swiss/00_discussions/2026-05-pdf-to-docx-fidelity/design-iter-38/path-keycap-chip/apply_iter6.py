"""iter-6: Consolas + space=0 (tightest possible) + bdr sz=2 (thinnest)"""
from pathlib import Path
import shutil

BASE = Path(__file__).parent
src = BASE / "iter4_unpacked"
out = BASE / "iter6_unpacked"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(src, out)

xml = (out / "word" / "document.xml").read_text(encoding="utf-8")
old = '<w:bdr w:val="single" w:sz="4" w:space="1" w:color="000000"/>'
new = '<w:bdr w:val="single" w:sz="2" w:space="0" w:color="000000"/>'
xml = xml.replace(old, new)
(out / "word" / "document.xml").write_text(xml, encoding="utf-8")
