"""Find specs table header on page 8."""
import sys
import fitz

d = fitz.open(sys.argv[1])
page = d[7]  # page 8 (0-indexed)
td = page.get_text("dict")
print("=== ALL SPANS ON PAGE 8 ===")
for block in td.get("blocks", []):
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            text = span.get("text", "").strip()
            if not text:
                continue
            print(f"  '{text[:30]}' font={span['font']} size={span['size']} color=#{span['color']:06X} x={span['bbox'][0]:.1f} y={span['bbox'][1]:.1f}")
d.close()
