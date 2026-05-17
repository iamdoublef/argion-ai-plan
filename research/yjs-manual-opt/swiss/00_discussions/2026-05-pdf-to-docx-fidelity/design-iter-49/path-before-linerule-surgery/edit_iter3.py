"""iter-3: w:before loosening cohort.
before=80 -> 100, before=160 -> 200. Opposite direction from iter-2.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
doc_path = ROOT / "iter-3" / "unpacked" / "word" / "document.xml"
doc = doc_path.read_text(encoding="utf-8")

doc2 = re.sub(r'w:before="80"', 'w:before="100"', doc)
doc2 = re.sub(r'w:before="160"', 'w:before="200"', doc2)

print(f"after: before=100 count = {len(re.findall(chr(34) + 'w:before=' + chr(34) + '100' + chr(34), doc2))}")
print(f"after: before=200 count = {len(re.findall(chr(34) + 'w:before=' + chr(34) + '200' + chr(34), doc2))}")

doc_path.write_text(doc2, encoding="utf-8")
print("written")
