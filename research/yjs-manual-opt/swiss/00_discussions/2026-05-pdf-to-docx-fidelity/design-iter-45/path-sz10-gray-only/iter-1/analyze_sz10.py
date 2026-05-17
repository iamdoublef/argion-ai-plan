"""Analyze sz=10 cohort distribution in word/document.xml."""
import re
from pathlib import Path
from collections import Counter

DOC = Path(__file__).parent.parent / "baseline_unpacked" / "word" / "document.xml"
text = DOC.read_text(encoding="utf-8")

# Find all rPr blocks - properly handle nested structures
# An rPr block is <w:rPr>...</w:rPr>
rpr_blocks = re.findall(r"<w:rPr>(.*?)</w:rPr>", text, re.DOTALL)
print(f"Total rPr blocks: {len(rpr_blocks)}")

# Filter to those containing sz=10
sz10_blocks = [b for b in rpr_blocks if re.search(r'<w:sz\s+w:val="10"\s*/>', b)]
print(f"sz=10 rPr blocks: {len(sz10_blocks)}")

# Tally distribution
color_counter = Counter()
font_counter = Counter()
spacing_counter = Counter()
combo_counter = Counter()
spacing_5_blocks = []

for b in sz10_blocks:
    # color
    m_color = re.search(r'<w:color\s+w:val="([0-9A-Fa-f]{6})"', b)
    color = m_color.group(1).upper() if m_color else "NONE"

    # font
    m_font = re.search(r'<w:rFonts\s+w:ascii="([^"]+)"', b)
    if m_font:
        font = m_font.group(1)
    else:
        font = "NONE"

    # spacing
    m_spacing = re.search(r'<w:spacing\s+w:val="(-?\d+)"\s*/>', b)
    spacing = m_spacing.group(1) if m_spacing else "NONE"

    color_counter[color] += 1
    font_counter[font] += 1
    spacing_counter[spacing] += 1
    combo_counter[(font, color, spacing)] += 1

    if spacing == "5":
        spacing_5_blocks.append((font, color))

print("\n=== Color distribution ===")
for k, v in color_counter.most_common():
    print(f"  {k}: {v}")
print("\n=== Font distribution ===")
for k, v in font_counter.most_common():
    print(f"  {k}: {v}")
print("\n=== Spacing distribution ===")
for k, v in spacing_counter.most_common():
    print(f"  val={k}: {v}")

print("\n=== Combo (font / color / spacing) ===")
for combo, v in combo_counter.most_common():
    print(f"  {combo[0]} / {combo[1]} / spacing={combo[2]}: {v}")

# spacing=5 subset
print(f"\n=== Spacing=5 subset detail: {len(spacing_5_blocks)} total ===")
sub_counter = Counter()
for f, c in spacing_5_blocks:
    sub_counter[(f, c)] += 1
for combo, v in sub_counter.most_common():
    print(f"  {combo[0]} / {combo[1]}: {v}")

# GRAY (1A1A1A) + sz=10 + spacing=5 — the target cohort
gray_sz10_sp5 = sum(1 for f, c in spacing_5_blocks if c == "1A1A1A")
black_sz10_sp5 = sum(1 for f, c in spacing_5_blocks if c == "000000")
red_sz10_sp5 = sum(1 for f, c in spacing_5_blocks if c == "E63846")
none_sz10_sp5 = sum(1 for f, c in spacing_5_blocks if c == "NONE")
print(f"\n=== Targets for GRAY-only experiment ===")
print(f"  GRAY 1A1A1A sz=10 spacing=5: {gray_sz10_sp5}")
print(f"  BLACK 000000 sz=10 spacing=5: {black_sz10_sp5}")
print(f"  RED E63846 sz=10 spacing=5: {red_sz10_sp5}")
print(f"  NONE color sz=10 spacing=5: {none_sz10_sp5}")
