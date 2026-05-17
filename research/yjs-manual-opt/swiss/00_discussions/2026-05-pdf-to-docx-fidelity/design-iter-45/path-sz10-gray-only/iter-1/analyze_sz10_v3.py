"""Better analysis: walk by paragraph and inspect runs."""
import re
from pathlib import Path
from collections import Counter
from xml.etree import ElementTree as ET

DOC = Path(__file__).parent.parent / "baseline_unpacked" / "word" / "document.xml"
text = DOC.read_text(encoding="utf-8")

# w:r is non-greedy on its own end-tag
runs = re.findall(r"<w:r\b(?:[^>]*)>(.*?)</w:r>", text, re.DOTALL)
print(f"Total <w:r> runs: {len(runs)}")

# tally
combos = Counter()
samples = {}
for run in runs:
    if not re.search(r'<w:sz\s+w:val="10"\s*/>', run):
        continue
    m_color = re.search(r'<w:color\s+w:val="([0-9A-Fa-f]{6})"', run)
    color = m_color.group(1).upper() if m_color else "NONE"
    m_font = re.search(r'<w:rFonts\s+w:ascii="([^"]+)"', run)
    font = m_font.group(1) if m_font else "NONE"
    m_spacing = re.search(r'<w:spacing\s+w:val="(-?\d+)"\s*/>', run)
    spacing = m_spacing.group(1) if m_spacing else "NONE"
    # collect plain text from all <w:t>
    t_pieces = re.findall(r"<w:t(?:[^>]*)>(.*?)</w:t>", run, re.DOTALL)
    run_text = "".join(t_pieces)
    key = (font, color, spacing)
    combos[key] += 1
    if key not in samples:
        samples[key] = []
    if len(samples[key]) < 4:
        samples[key].append(run_text)

print("\n=== Combos with samples ===")
for key in sorted(combos):
    print(f"\n  {key}  count={combos[key]}")
    for s in samples[key]:
        print(f"    | {s!r}")
