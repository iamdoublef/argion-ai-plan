"""iter-1: grep w:kern current state.

No mutation. Just inspect the baseline.

Result: word/document.xml has 0 w:kern. styles.xml + stylesWithEffects.xml each have
2 sites for sz=52 heading (val=28). Body is kern-OFF.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
xml = (ROOT / "baseline_unpacked" / "word" / "document.xml").read_text(encoding="utf-8")
print("document.xml w:kern count:", xml.count("<w:kern"))

for p in (ROOT / "baseline_unpacked" / "word").glob("*.xml"):
    n = p.read_text(encoding="utf-8").count("<w:kern")
    if n:
        print(f"  {p.name}: {n}")
