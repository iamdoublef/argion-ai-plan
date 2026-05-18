"""iter-8: p9 only val=2 -> 0."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"


def find_sections(text):
    return [m.start() for m in re.finditer(r'<w:sectPr', text)]


def apply(iter_name: str, page_idx: int):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")
    secs = find_sections(text)
    # page n: text[secs[n-2]:secs[n-1]] for n>=2, or text[0:secs[0]] for n=1
    if page_idx == 1:
        s, e = 0, secs[0]
    else:
        s = secs[page_idx - 2]
        e = secs[page_idx - 1]
    page = text[s:e]
    n = page.count('<w:spacing w:val="2"/>')
    new_page = page.replace('<w:spacing w:val="2"/>', '<w:spacing w:val="0"/>')
    text = text[:s] + new_page + text[e:]
    doc.write_text(text, encoding="utf-8")
    print(f"done. p{page_idx} val=2->0: {n} sites")
    return 0


if __name__ == "__main__":
    pidx = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    sys.exit(apply(sys.argv[1], pidx))
