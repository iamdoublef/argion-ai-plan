import xml.etree.ElementTree as ET
import os

path = os.path.join("research", "yjs-manual-opt", "_inbox", "问题反馈", "_unpacked", "word", "document.xml")
tree = ET.parse(path)
root = tree.getroot()
ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# Also track images
drawing_ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
rel_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
wp_ns = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
r_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

lines = []
img_counter = 0
for p in root.iter(f"{{{ns}}}p"):
    texts = [t.text for t in p.iter(f"{{{ns}}}t") if t.text]
    # Check for drawings/images in this paragraph
    drawings = list(p.iter(f"{{{wp_ns}}}inline")) + list(p.iter(f"{{{wp_ns}}}anchor"))
    if drawings:
        img_counter += 1
        lines.append(f"[图片 image{img_counter}]")
    if texts:
        lines.append("".join(texts))
    elif not drawings:
        lines.append("")

with open("_temp_issues.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"Wrote {len(lines)} lines")
