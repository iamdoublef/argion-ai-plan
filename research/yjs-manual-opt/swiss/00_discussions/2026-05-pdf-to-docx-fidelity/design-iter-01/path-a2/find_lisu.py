"""Find what text uses LiSu font."""
import sys
import fitz

d = fitz.open(sys.argv[1])
for pno, page in enumerate(d, start=1):
    td = page.get_text("dict")
    for block in td.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if "LiSu" in span.get("font", ""):
                    print(f"p{pno}: '{span['text']}' font={span['font']} size={span['size']} color=#{span['color']:06X}")
d.close()
