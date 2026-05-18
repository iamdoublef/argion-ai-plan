"""iter-5: w:after=120 → 140 (global, 23 sites)."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"


def apply(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")
    n = text.count('w:after="120"')
    text = text.replace('w:after="120"', 'w:after="140"')
    doc.write_text(text, encoding="utf-8")
    print(f"done. after=120->140: {n} sites")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
