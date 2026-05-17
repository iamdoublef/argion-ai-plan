"""iter-10: stack iter-9 + p10 val=4->2 (even deeper)."""
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

    # p9 stack
    s, e = page_span(secs, 9, len(text))
    page = text[s:e]
    new_page = page.replace('<w:spacing w:val="2"/>', '<w:spacing w:val="0"/>')
    new_page = new_page.replace('<w:spacing w:val="8"/>', '<w:spacing w:val="6"/>')
    text = text[:s] + new_page + text[e:]

    # p10 deep stack: 10/8/6 all -> 4, then 4 -> 2
    s, e = page_span(secs, 10, len(text))
    page = text[s:e]
    new_page = page.replace('<w:spacing w:val="10"/>', '<w:spacing w:val="6"/>')
    new_page = new_page.replace('<w:spacing w:val="8"/>', '<w:spacing w:val="6"/>')
    new_page = new_page.replace('<w:spacing w:val="6"/>', '<w:spacing w:val="4"/>')
    # NEW: 4 -> 2
    n4 = new_page.count('<w:spacing w:val="4"/>')
    new_page = new_page.replace('<w:spacing w:val="4"/>', '<w:spacing w:val="2"/>')
    text = text[:s] + new_page + text[e:]

    doc.write_text(text, encoding="utf-8")
    print(f"done. iter-9 stack + p10 val=4->2 (now everything at 2): {n4} sites")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
