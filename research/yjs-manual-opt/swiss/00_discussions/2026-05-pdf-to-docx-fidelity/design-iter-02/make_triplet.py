"""
Build per-page triplet: [TARGET | WINNER | DIFF heatmap with labels]
Annotate differences clearly so a designer can spot exact issues per page.
"""
import sys
import gc
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops

def load_font(size):
    for f in ('C:/Windows/Fonts/arial.ttf', 'arial.ttf'):
        try:
            return ImageFont.truetype(f, size)
        except: pass
    return ImageFont.load_default()

def make_one(target_path, winner_path, out_path, page_num):
    font_title = load_font(28)
    t = Image.open(target_path).convert("RGB")
    w = Image.open(winner_path).convert("RGB")
    if t.size != w.size:
        w = w.resize(t.size, Image.BICUBIC)
    diff = ImageChops.difference(t, w)
    red = Image.new("RGB", t.size, (255, 0, 0))
    mask = diff.convert("L").point(lambda v: min(255, v * 4))
    heat = Image.composite(red, t, mask)
    gap = 20
    title_h = 60
    canvas_w = t.width * 3 + gap * 2
    canvas_h = t.height + title_h
    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    d = ImageDraw.Draw(canvas)
    d.text((10, 10), f"PDF p{page_num}", fill=(180, 0, 0), font=font_title)
    d.text((t.width + gap + 10, 10), f"WINNER p{page_num}", fill=(0, 90, 180), font=font_title)
    d.text((t.width * 2 + gap * 2 + 10, 10), f"DIFF heatmap", fill=(120, 0, 120), font=font_title)
    canvas.paste(t, (0, title_h))
    canvas.paste(w, (t.width + gap, title_h))
    canvas.paste(heat, (t.width * 2 + gap * 2, title_h))
    canvas.save(out_path, optimize=True)
    t.close(); w.close(); diff.close(); red.close(); mask.close(); heat.close(); canvas.close()

def main(target_dir, winner_dir, out_dir):
    td = Path(target_dir)
    wd = Path(winner_dir)
    od = Path(out_dir)
    od.mkdir(parents=True, exist_ok=True)
    targets = sorted(td.glob("page-*.png"))
    winners = sorted(wd.glob("page-*.png"))
    n = min(len(targets), len(winners))
    font_title = load_font(36)
    font_label = load_font(24)
    for i in range(n):
        t = Image.open(targets[i]).convert("RGB")
        w = Image.open(winners[i]).convert("RGB")
        if t.size != w.size:
            w = w.resize(t.size, Image.BICUBIC)
        diff = ImageChops.difference(t, w)
        # tinted heatmap
        red = Image.new("RGB", t.size, (255, 0, 0))
        mask = diff.convert("L").point(lambda v: min(255, v * 4))
        heat = Image.composite(red, t, mask)

        # Combine 3 panels side by side
        gap = 30
        title_h = 80
        canvas_w = t.width * 3 + gap * 2
        canvas_h = t.height + title_h
        canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
        d = ImageDraw.Draw(canvas)
        d.text((10, 10), f"PDF TARGET — page {i+1}", fill=(180, 0, 0), font=font_title)
        d.text((t.width + gap + 10, 10), f"WINNER (B2 iter-04) — page {i+1}", fill=(0, 90, 180), font=font_title)
        d.text((t.width * 2 + gap * 2 + 10, 10), f"DIFF heatmap (red=diff)", fill=(120, 0, 120), font=font_title)
        canvas.paste(t, (0, title_h))
        canvas.paste(w, (t.width + gap, title_h))
        canvas.paste(heat, (t.width * 2 + gap * 2, title_h))
        out = od / f"triplet-{i+1:02d}.png"
        # Save at 50% to keep file size manageable
        small = canvas.resize((canvas.width // 2, canvas.height // 2), Image.BICUBIC)
        small.save(out.as_posix(), optimize=True, quality=85)
        t.close(); w.close(); diff.close(); heat.close(); canvas.close(); small.close()
        del t, w, diff, heat, canvas, small, red, mask, d
        gc.collect()
        print(f"  wrote {out.name}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
