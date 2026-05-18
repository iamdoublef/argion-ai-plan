"""iter-10: stack p9 val=2->0 (iter-8 win) + try p8 val=2->0 (36 sites adjacent)."""
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


def apply(iter_name: str, pages=(8, 9)):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")
    secs = find_sections(text)
    # Edit pages from highest to lowest to preserve indices
    total_replaced = 0
    for pidx in sorted(pages, reverse=True):
        s, e = page_span(secs, pidx, len(text))
        page = text[s:e]
        n = page.count('<w:spacing w:val="2"/>')
        new_page = page.replace('<w:spacing w:val="2"/>', '<w:spacing w:val="0"/>')
        text = text[:s] + new_page + text[e:]
        total_replaced += n
        print(f"  page {pidx}: {n} sites cleared")
    doc.write_text(text, encoding="utf-8")
    print(f"done. total val=2->0: {total_replaced} sites across {pages}")
    return 0


if __name__ == "__main__":
    pages_arg = sys.argv[2] if len(sys.argv) > 2 else "8,9"
    pages = tuple(int(x) for x in pages_arg.split(','))
    sys.exit(apply(sys.argv[1], pages))
