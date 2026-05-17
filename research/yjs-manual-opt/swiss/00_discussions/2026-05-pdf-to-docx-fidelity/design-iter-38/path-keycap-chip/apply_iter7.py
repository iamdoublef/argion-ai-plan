"""iter-7: Try the bare-minimum chip — Consolas only, no extra padding/spacing
Same as iter-4 but use Lucida Console which has narrower glyphs in some Office variants.
"""
from pathlib import Path
import shutil

BASE = Path(__file__).parent
src = BASE / "iter1_unpacked"
out = BASE / "iter7_unpacked"
if out.exists():
    shutil.rmtree(out)
shutil.copytree(src, out)

xml = (out / "word" / "document.xml").read_text(encoding="utf-8")

old_font = '<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New" w:eastAsia="Courier New"/>'
new_font = '<w:rFonts w:ascii="Lucida Console" w:hAnsi="Lucida Console" w:cs="Lucida Console" w:eastAsia="Lucida Console"/>'
xml = xml.replace(old_font, new_font)

old_bdr = '<w:bdr w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
new_bdr = '<w:bdr w:val="single" w:sz="4" w:space="1" w:color="000000"/>'
xml = xml.replace(old_bdr, new_bdr)

(out / "word" / "document.xml").write_text(xml, encoding="utf-8")
