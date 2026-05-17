"""iter-4: p14 char-spacing cascade tighten (val=10->8, val=8->6, val=11->9).

p14 has 4 sites val=10, 5 sites val=8, 2 sites val=11.
Try tighten (matches METHODOLOGY p9/p10 cascade pattern). Avoid touching val=5 (Goldilocks?).
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

    # p14 char-spacing cascade tighten
    s, e = page_span(secs, 14, len(text))
    page = text[s:e]
    n11 = page.count('<w:spacing w:val="11"/>')
    n10 = page.count('<w:spacing w:val="10"/>')
    n8  = page.count('<w:spacing w:val="8"/>')
    # do not touch val=5 or val=0
    new_page = page.replace('<w:spacing w:val="11"/>', '<w:spacing w:val="9"/>')
    new_page = new_page.replace('<w:spacing w:val="10"/>', '<w:spacing w:val="8"/>')
    new_page = new_page.replace('<w:spacing w:val="8"/>', '<w:spacing w:val="6"/>')
    text = text[:s] + new_page + text[e:]

    doc.write_text(text, encoding="utf-8")
    print(f"done. p14 cspc 11->9: {n11}, 10->8: {n10}, 8->6: {n8} sites")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
