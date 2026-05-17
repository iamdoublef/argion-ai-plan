"""Apply a regex-based edit to baseline_unpacked -> iter-N/unpacked.

Usage:
    python edit_helper.py iter-N <pattern> <replacement>
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"


def apply_edit(iter_name: str, pattern: str, replacement: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    total = 0
    word_dir = unpacked / "word"
    for f in word_dir.glob("*.xml"):
        text = f.read_text(encoding="utf-8")
        new_text, n = re.subn(pattern, replacement, text)
        if n > 0:
            f.write_text(new_text, encoding="utf-8")
            total += n
            print(f"  {f.name}: {n} replacements")
    print(f"TOTAL: {total} replacements")
    return total


if __name__ == "__main__":
    iter_name = sys.argv[1]
    pattern = sys.argv[2]
    replacement = sys.argv[3]
    apply_edit(iter_name, pattern, replacement)
