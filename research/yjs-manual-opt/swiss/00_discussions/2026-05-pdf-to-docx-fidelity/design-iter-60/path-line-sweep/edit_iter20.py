"""iter-20: Replace char spacing val=10 → 0 ONLY for Arial sz=14 b=0 black runs.

These are disclaimer-body type texts. The pattern is:
<w:rPr>
  <w:rFonts w:ascii="Arial" .../>
  <w:b w:val="0"/>
  <w:sz w:val="14"/>
  <w:color w:val="000000"/>
  <w:spacing w:val="10"/>
</w:rPr>
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE = ROOT / "baseline_unpacked"

OLD = '''<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei"/>
          <w:b w:val="0"/>
          <w:sz w:val="14"/>
          <w:color w:val="000000"/>
          <w:spacing w:val="10"/>'''
NEW = '''<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei"/>
          <w:b w:val="0"/>
          <w:sz w:val="14"/>
          <w:color w:val="000000"/>
          <w:spacing w:val="0"/>'''
# Also handle the indented version inside table (12 spaces vs 10 spaces)
OLD2 = '''<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei"/>
                <w:b w:val="0"/>
                <w:sz w:val="14"/>
                <w:color w:val="000000"/>
                <w:spacing w:val="10"/>'''
NEW2 = '''<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei"/>
                <w:b w:val="0"/>
                <w:sz w:val="14"/>
                <w:color w:val="000000"/>
                <w:spacing w:val="0"/>'''


def apply(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    shutil.copytree(BASELINE, unpacked)

    doc = unpacked / "word" / "document.xml"
    text = doc.read_text(encoding="utf-8")
    n1 = text.count(OLD)
    text2 = text.replace(OLD, NEW)
    n2 = text2.count(OLD2)
    text3 = text2.replace(OLD2, NEW2)
    print(f"replacements: {n1} + {n2}")
    doc.write_text(text3, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(apply(sys.argv[1]))
