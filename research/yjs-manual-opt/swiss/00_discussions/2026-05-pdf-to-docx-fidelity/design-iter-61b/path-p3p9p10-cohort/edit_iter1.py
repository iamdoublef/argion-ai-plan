"""iter-1: stack iter-14 (p9 val=2->0, val=8->6; p10 val=10->8) + p3 val=6->4 (24 sites)."""
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

    # iter-14 stack: p9 val=2->0, val=8->6
    s, e = page_span(secs, 9, len(text))
    page = text[s:e]
    n1 = page.count('<w:spacing w:val="2"/>')
    new_page = page.replace('<w:spacing w:val="2"/>', '<w:spacing w:val="0"/>')
    n2 = new_page.count('<w:spacing w:val="8"/>')
    new_page = new_page.replace('<w:spacing w:val="8"/>', '<w:spacing w:val="6"/>')
    text = text[:s] + new_page + text[e:]

    # iter-14 stack: p10 val=10->8
    s, e = page_span(secs, 10, len(text))
    page = text[s:e]
    n3 = page.count('<w:spacing w:val="10"/>')
    new_page = page.replace('<w:spacing w:val="10"/>', '<w:spacing w:val="8"/>')
    text = text[:s] + new_page + text[e:]

    # NEW: p3 val=6 -> 4 (24 sites)
    s, e = page_span(secs, 3, len(text))
    page = text[s:e]
    n4 = page.count('<w:spacing w:val="6"/>')
    new_page = page.replace('<w:spacing w:val="6"/>', '<w:spacing w:val="4"/>')
    text = text[:s] + new_page + text[e:]

    doc.write_text(text, encoding="utf-8")
    print(f"done. p9 v2->0:{n1}, p9 v8->6:{n2}, p10 v10->8:{n3}, p3 v6->4:{n4}")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
