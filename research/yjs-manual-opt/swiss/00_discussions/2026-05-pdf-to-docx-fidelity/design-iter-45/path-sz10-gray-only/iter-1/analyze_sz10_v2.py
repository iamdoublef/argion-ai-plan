"""Analyze sz=10 cohort with text samples to understand what these runs are."""
import re
from pathlib import Path
from collections import Counter

DOC = Path(__file__).parent.parent / "baseline_unpacked" / "word" / "document.xml"
text = DOC.read_text(encoding="utf-8")

# Find every <w:r>...</w:r> that contains sz=10
runs = re.findall(r"<w:r>(.*?)</w:r>", text, re.DOTALL)
print(f"Total w:r blocks: {len(runs)}")

# Also pick up runs with attributes
runs_attr = re.findall(r"<w:r[^>]*>(.*?)</w:r>", text, re.DOTALL)
print(f"Total w:r blocks (incl attrs): {len(runs_attr)}")

sz10_runs = []
for r in runs_attr:
    if re.search(r'<w:sz\s+w:val="10"\s*/>', r):
        # extract color, font, spacing, text
        m_color = re.search(r'<w:color\s+w:val="([0-9A-Fa-f]{6})"', r)
        color = m_color.group(1).upper() if m_color else "NONE"
        m_font = re.search(r'<w:rFonts\s+w:ascii="([^"]+)"', r)
        font = m_font.group(1) if m_font else "NONE"
        m_spacing = re.search(r'<w:spacing\s+w:val="(-?\d+)"\s*/>', r)
        spacing = m_spacing.group(1) if m_spacing else "NONE"
        m_text = re.search(r"<w:t[^>]*>(.*?)</w:t>", r, re.DOTALL)
        run_text = m_text.group(1) if m_text else ""
        sz10_runs.append((font, color, spacing, run_text[:60]))

print(f"sz=10 runs (with text): {len(sz10_runs)}")
print("\n=== Sample texts per combo ===")
seen = {}
for f, c, s, t in sz10_runs:
    key = (f, c, s)
    if key not in seen:
        seen[key] = []
    if len(seen[key]) < 3:
        seen[key].append(t)
for key, samples in seen.items():
    print(f"\n  {key}:")
    for s in samples:
        print(f"    | {s!r}")
