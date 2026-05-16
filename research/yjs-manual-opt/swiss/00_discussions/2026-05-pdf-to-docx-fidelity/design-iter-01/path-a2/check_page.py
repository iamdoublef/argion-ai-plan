"""Compare a single page's drawings/spans between PDF1 and PDF2 to understand visual diff."""
import sys
import fitz

p1 = fitz.open(sys.argv[1])  # target
p2 = fitz.open(sys.argv[2])  # candidate
page_idx = int(sys.argv[3]) - 1

t = p1[page_idx]
c = p2[page_idx]

def page_info(pg, label):
    print(f"\n=== {label} ===")
    td = pg.get_text("dict")
    spans = []
    for b in td.get("blocks", []):
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                spans.append(s)
    print(f"  spans: {len(spans)}")
    drawings = list(pg.get_drawings())
    print(f"  drawings: {len(drawings)}")
    images = pg.get_images(full=True)
    print(f"  images: {len(images)}")
    print(f"  size_pt: {pg.rect.width:.1f} x {pg.rect.height:.1f}")
    # First few spans
    print("  First 10 spans (text/font/size/y):")
    for s in spans[:10]:
        print(f"    '{s['text'][:20]:20}' {s['font'][:25]:25} {s['size']:.2f}pt y={s['bbox'][1]:.1f}")

page_info(t, f"TARGET p{page_idx+1}")
page_info(c, f"CAND p{page_idx+1}")
p1.close()
p2.close()
