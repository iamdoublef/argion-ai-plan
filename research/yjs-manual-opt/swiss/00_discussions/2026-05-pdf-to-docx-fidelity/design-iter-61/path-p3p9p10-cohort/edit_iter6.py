"""iter-6: p3 only spacing val=6 -> 4 (in table cells)."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"


def find_sections(text):
    return [m.start() for m in re.finditer(r'<w:sectPr', text)]


def apply(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")
    secs = find_sections(text)
    # p3 = secs[1]..secs[2]
    s, e = secs[1], secs[2]
    page = text[s:e]
    old = '<w:spacing w:val="6"/>'
    new = '<w:spacing w:val="4"/>'
    n = page.count(old)
    new_page = page.replace(old, new)
    text = text[:s] + new_page + text[e:]
    doc.write_text(text, encoding="utf-8")
    print(f"done. p3 spacing val=6->4: {n} sites")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
