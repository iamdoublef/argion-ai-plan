"""Stack lever (from baseline_v2_unpacked).

Usage:
    python stack_lever.py iter-N page_idx "src_str" "dst_str"
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_v2_unpacked"


def find_sections(text):
    return [m.start() for m in re.finditer(r'<w:sectPr', text)]


def page_span(secs, page_idx, total_len):
    if page_idx == 1:
        return 0, secs[0]
    if page_idx <= len(secs):
        return secs[page_idx - 2], secs[page_idx - 1]
    return secs[-1], total_len


def apply(iter_name: str, pages_str: str, src: str, dst: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    pages = [int(x) for x in pages_str.split(",")]

    doc_path = unpacked / "word" / "document.xml"
    text = doc_path.read_text(encoding="utf-8")
    secs = find_sections(text)

    total_n = 0
    for p in sorted(pages, reverse=True):
        s, e = page_span(secs, p, len(text))
        chunk = text[s:e]
        n = chunk.count(src)
        new_chunk = chunk.replace(src, dst)
        text = text[:s] + new_chunk + text[e:]
        print(f"  p{p}: {n} replacements ('{src}' -> '{dst}')")
        total_n += n

    doc_path.write_text(text, encoding="utf-8")
    print(f"TOTAL: {total_n}")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
