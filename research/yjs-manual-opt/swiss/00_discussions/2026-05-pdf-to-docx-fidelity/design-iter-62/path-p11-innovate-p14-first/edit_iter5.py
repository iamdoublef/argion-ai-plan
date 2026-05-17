"""iter-5: p11 tcMar internal cell margins reduce (innovative).

p11 has many tcMar entries with top=32/bot=32, start=55/end=55. Try reduce
both top/bot to 16 (half) -- this is page-isolated and never tried.
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

    # p11 tcMar top/bot 32 -> 16 (half)
    s, e = page_span(secs, 11, len(text))
    page = text[s:e]
    n_top = page.count('<w:top w:w="32" w:type="dxa"/>')
    n_bot = page.count('<w:bottom w:w="32" w:type="dxa"/>')
    new_page = page.replace('<w:top w:w="32" w:type="dxa"/>', '<w:top w:w="16" w:type="dxa"/>')
    new_page = new_page.replace('<w:bottom w:w="32" w:type="dxa"/>', '<w:bottom w:w="16" w:type="dxa"/>')
    text = text[:s] + new_page + text[e:]

    doc.write_text(text, encoding="utf-8")
    print(f"done. p11 tcMar top 32->16: {n_top}, bot 32->16: {n_bot}")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
