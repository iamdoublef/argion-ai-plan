"""Inject <w:autoSpaceDE w:val="0"/><w:autoSpaceDN w:val="0"/> into every pPr
that has <w:spacing>. Place immediately BEFORE <w:spacing.

This targets the LO/Word CJK-ASCII auto-spacing behavior that causes
'87-105 号' wide drift vs target '87-105号'.
"""
import re
from pathlib import Path

p = Path(__file__).parent / "unpacked" / "word" / "document.xml"
s = p.read_text(encoding="utf-8")

# Only target pPr-level <w:spacing>. pPr spacings have attrs starting with w:after/w:before/w:line.
# rPr spacing has just w:val. Differentiate by the attribute pattern.
# pPr spacing: <w:spacing w:after=... or w:before=... or w:line=...
# rPr spacing: <w:spacing w:val="N"/>
pattern = re.compile(r"(\n( +)<w:spacing w:(after|before|line)=)", re.MULTILINE)


def repl(m):
    indent = m.group(2)
    inject = f"\n{indent}<w:autoSpaceDE w:val=\"0\"/>\n{indent}<w:autoSpaceDN w:val=\"0\"/>"
    return inject + m.group(1)


new_s, n = pattern.subn(repl, s)
print(f"Replaced {n} sites")
p.write_text(new_s, encoding="utf-8")
