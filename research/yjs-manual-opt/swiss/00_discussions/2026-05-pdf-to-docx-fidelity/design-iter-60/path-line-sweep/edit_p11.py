"""Apply edits only in p11 region (section 11) of document.xml.

Usage:
    python edit_p11.py iter-N <pattern> <replacement> [--append]

--append: do not re-copy from baseline; modify existing iter-N/unpacked.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"

# Section position boundaries (start byte of section in document.xml)
# Section 11 = page 11 = pos[10]..pos[11] = 226559..272001 (in baseline)
# For edits we re-locate p11 by finding the 11th <w:sectPr position dynamically.

def find_p11_region(text):
    positions = [m.start() for m in re.finditer(r'<w:sectPr', text)]
    if len(positions) < 12:
        # Fall back to baseline byte offsets
        return 226559, 272001
    return positions[10], positions[11]


def apply_edit(iter_name: str, pattern: str, replacement: str, append: bool = False):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if not append:
        if unpacked.exists():
            shutil.rmtree(unpacked)
        shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")

    p11_start, p11_end = find_p11_region(text)
    pre = text[:p11_start]
    page = text[p11_start:p11_end]
    post = text[p11_end:]

    new_page = page.replace(pattern, replacement)
    n = page.count(pattern)
    new_text = pre + new_page + post
    doc.write_text(new_text, encoding="utf-8")
    print(f"document.xml p11 region: {n} replacements (append={append})")
    return n


if __name__ == "__main__":
    iter_name = sys.argv[1]
    pattern = sys.argv[2]
    replacement = sys.argv[3]
    append = ("--append" in sys.argv)
    apply_edit(iter_name, pattern, replacement, append=append)
