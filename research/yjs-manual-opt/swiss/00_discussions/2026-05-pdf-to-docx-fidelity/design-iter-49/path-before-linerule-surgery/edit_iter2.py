"""iter-2: w:before tightening cohort.
Change w:before="80" -> w:before="60" on 10 sites (tighten by 20 twips)
AND w:before="160" -> w:before="120" on 7 sites (tighten by 40 twips).
Total: 17 sites.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
doc_path = ROOT / "iter-2" / "unpacked" / "word" / "document.xml"
doc = doc_path.read_text(encoding="utf-8")

# Count before mutation
def count_attr(s, val):
    return len(re.findall(rf'w:before="{val}"', s))

print(f"Pre: before=80 -> {count_attr(doc, 80)} sites, before=160 -> {count_attr(doc, 160)} sites")

doc2 = re.sub(r'w:before="80"', 'w:before="60"', doc)
doc2 = re.sub(r'w:before="160"', 'w:before="120"', doc2)

print(f"Post: before=60 -> {count_attr(doc2, 60)} sites, before=120 -> {count_attr(doc2, 120)} sites")
print(f"Post: before=80 -> {count_attr(doc2, 80)} sites (should be 0)")
print(f"Post: before=160 -> {count_attr(doc2, 160)} sites (should be 0)")

doc_path.write_text(doc2, encoding="utf-8")
print(f"\nWritten: {doc_path}")
