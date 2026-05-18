"""iter-13: stack iter-8 (p9 val=2->0) + p9 val=8 -> 6."""
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

    # iter-8 stack: p9 val=2->0
    s, e = page_span(secs, 9, len(text))
    page = text[s:e]
    n1 = page.count('<w:spacing w:val="2"/>')
    new_page = page.replace('<w:spacing w:val="2"/>', '<w:spacing w:val="0"/>')
    text = text[:s] + new_page + text[e:]

    # new: p9 val=8 -> 6
    s, e = page_span(secs, 9, len(text))
    page = text[s:e]
    n2 = page.count('<w:spacing w:val="8"/>')
    new_page = page.replace('<w:spacing w:val="8"/>', '<w:spacing w:val="6"/>')
    text = text[:s] + new_page + text[e:]

    doc.write_text(text, encoding="utf-8")
    print(f"done. p9 val=2->0: {n1}, p9 val=8->6: {n2}")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
