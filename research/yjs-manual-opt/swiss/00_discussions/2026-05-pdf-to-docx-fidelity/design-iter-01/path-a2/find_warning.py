"""Find warning spans on page 3."""
import sys
import fitz

d = fitz.open(sys.argv[1])
page = d[2]  # page 3 (0-indexed)
td = page.get_text("dict")
for block in td.get("blocks", []):
    for line in block.get("lines", []):
        for span in line.get("spans", []):
            text = span.get("text", "").strip()
            if "WARNING" in text or "警告" in text or "DANGER" in text or "▲" in text or "△" in text:
                print(f"  '{text}' font={span['font']} size={span['size']} color=#{span['color']:06X} x={span['bbox'][0]:.1f} y={span['bbox'][1]:.1f}")
d.close()
