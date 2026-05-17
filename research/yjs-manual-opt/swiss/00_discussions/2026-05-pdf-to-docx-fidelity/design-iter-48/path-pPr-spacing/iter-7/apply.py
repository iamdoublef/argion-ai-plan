"""iter-7: contextualSpacing=1 on line=240 cohort.
Insert <w:contextualSpacing/> right after the <w:spacing.../> tag (correct schema order).
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT.parent / "baseline_unpacked"
DST = ROOT / "unpacked"

if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
doc = DST / "word" / "document.xml"
xml = doc.read_text(encoding="utf-8")

# For each pPr that contains w:spacing w:line="240", insert <w:contextualSpacing/>
# immediately after that <w:spacing .../> tag (CT_PPrBase order: spacing, ind, contextualSpacing).
p_pat = re.compile(r"(<w:pPr>)(.*?)(</w:pPr>)", re.S)
c = [0]
def repl(m):
    open_t, body, close_t = m.group(1), m.group(2), m.group(3)
    if 'w:line="240"' not in body:
        return m.group(0)
    if '<w:contextualSpacing' in body:
        return m.group(0)
    # Find spacing tag and any ind tag after it; insert contextualSpacing after ind (or after spacing if no ind).
    # Simple: insert immediately after the spacing tag.
    sp_m = re.search(r'<w:spacing\b[^/]*/>', body)
    if not sp_m:
        return m.group(0)
    end = sp_m.end()
    # If next sibling is <w:ind .../>, place contextualSpacing after it.
    rest = body[end:]
    ind_m = re.match(r'\s*<w:ind\b[^/]*/>', rest)
    if ind_m:
        end = end + ind_m.end()
    new_body = body[:end] + '<w:contextualSpacing/>' + body[end:]
    c[0] += 1
    return open_t + new_body + close_t
xml = p_pat.sub(repl, xml)
print(f"contextualSpacing added to line=240: {c[0]} sites")
doc.write_text(xml, encoding="utf-8")
