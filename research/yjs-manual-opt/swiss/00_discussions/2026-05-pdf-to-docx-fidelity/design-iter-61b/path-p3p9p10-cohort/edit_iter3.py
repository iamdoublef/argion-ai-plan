"""iter-3: stack iter-2 + p3 val=9->7 (24 sites) — opposite direction from iter-1."""
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

    # iter-14 stack (p9): val=2->0, val=8->6
    s, e = page_span(secs, 9, len(text))
    page = text[s:e]
    new_page = page.replace('<w:spacing w:val="2"/>', '<w:spacing w:val="0"/>')
    new_page = new_page.replace('<w:spacing w:val="8"/>', '<w:spacing w:val="6"/>')
    text = text[:s] + new_page + text[e:]

    # iter-2 stack (p10): val=10->6
    s, e = page_span(secs, 10, len(text))
    page = text[s:e]
    new_page = page.replace('<w:spacing w:val="10"/>', '<w:spacing w:val="6"/>')
    text = text[:s] + new_page + text[e:]

    # NEW: p3 val=9->7 (24 sites char-spacing, opposite from iter-1 which went 6->4 wrong)
    s, e = page_span(secs, 3, len(text))
    page = text[s:e]
    n4 = page.count('<w:spacing w:val="9"/>')
    new_page = page.replace('<w:spacing w:val="9"/>', '<w:spacing w:val="7"/>')
    text = text[:s] + new_page + text[e:]

    doc.write_text(text, encoding="utf-8")
    print(f"done. iter-2 stack + p3 val=9->7: {n4} sites")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
