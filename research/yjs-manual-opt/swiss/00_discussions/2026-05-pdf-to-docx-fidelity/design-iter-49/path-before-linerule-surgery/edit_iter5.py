"""iter-5: w:lineRule="auto" -> "atLeast" globally.
atLeast: line value is minimum twips height; fonts can push higher.
With line=240 (= 12pt) as minimum, content scales up but doesn't shrink below.
Different effect than exact (which is fixed) — possibly less destructive.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
doc_path = ROOT / "iter-5" / "unpacked" / "word" / "document.xml"
doc = doc_path.read_text(encoding="utf-8")

before = len(re.findall(r'w:lineRule="auto"', doc))
doc2 = re.sub(r'w:lineRule="auto"', 'w:lineRule="atLeast"', doc)
after = len(re.findall(r'w:lineRule="atLeast"', doc2))
print(f"auto pre: {before}, atLeast post: {after}")

doc_path.write_text(doc2, encoding="utf-8")
