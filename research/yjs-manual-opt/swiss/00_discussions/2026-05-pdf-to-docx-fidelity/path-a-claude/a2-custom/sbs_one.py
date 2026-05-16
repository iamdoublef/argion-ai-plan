"""Side-by-side compare one page at a time. Avoids the multi-page segfault."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def make_one(a_path, b_path, out_path, label_a="TARGET", label_b="ITER"):
    a = Image.open(a_path).convert("RGB")
    b = Image.open(b_path).convert("RGB")
    h = max(a.height, b.height)
    label_h = 40
    gap = 14
    canvas = Image.new("RGB", (a.width + gap + b.width, h + label_h), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        font = ImageFont.load_default()
    draw.text((10, 8), label_a, fill=(180, 0, 0), font=font)
    draw.text((a.width + gap + 10, 8), label_b, fill=(0, 90, 180), font=font)
    canvas.paste(a, (0, label_h))
    canvas.paste(b, (a.width + gap, label_h))
    canvas.save(out_path, optimize=True)
    a.close(); b.close(); canvas.close()


if __name__ == "__main__":
    a_dir = Path(sys.argv[1])
    b_dir = Path(sys.argv[2])
    out_dir = Path(sys.argv[3])
    label_a = sys.argv[4] if len(sys.argv) > 4 else "TARGET"
    label_b = sys.argv[5] if len(sys.argv) > 5 else "ITER"
    out_dir.mkdir(parents=True, exist_ok=True)
    a_pages = sorted(a_dir.glob("page-*.png"))
    b_pages = sorted(b_dir.glob("page-*.png"))
    n = max(len(a_pages), len(b_pages))
    for i in range(n):
        a_path = a_pages[i] if i < len(a_pages) else None
        b_path = b_pages[i] if i < len(b_pages) else None
        if a_path is None or b_path is None:
            continue
        out = out_dir / f"side-{i+1:02d}.png"
        try:
            make_one(a_path, b_path, out, label_a, label_b)
            print(f"  ok side-{i+1:02d}")
        except Exception as e:
            print(f"  fail side-{i+1:02d}: {e}")
