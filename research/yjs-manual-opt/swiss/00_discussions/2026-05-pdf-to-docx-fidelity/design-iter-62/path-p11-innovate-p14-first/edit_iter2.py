"""iter-2: p14 line=250 -> 260 (21 sites, page-isolated cohort).

W49 p14=9.67. p14 has 21 sites of line=250. Try +10 (similar magnitude to p14
line=240->250 W43 W43 win) for further compression.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"


def find_sections(text):
    return [m.start() for m in re.finditer(r'<w:sectPr', text)]


def page_span(secs, page_idx, total_len):
    if page_idx == 1:
        return 0, secs[0]
    return secs[page_idx - 2], secs[page_idx - 1] if page_idx <= len(secs) else total_len


def apply(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")
    secs = find_sections(text)

    # p14: line="250" -> "260" (21 sites)
    s, e = page_span(secs, 14, len(text))
    page = text[s:e]
    n = page.count('w:line="250"')
    new_page = page.replace('w:line="250"', 'w:line="260"')
    text = text[:s] + new_page + text[e:]

    doc.write_text(text, encoding="utf-8")
    print(f"done. p14 line=250->260: {n} sites")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
