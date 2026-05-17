"""Generate heatmaps for additional pages and a focused crop comparison for p7 (keycap table)."""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.cm as cm

ROOT = Path(r"D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity")
AUDIT = ROOT / "design-iter-34" / "path-design-audit"
TARG = ROOT / "baseline" / "target_png"
W27 = ROOT / "final" / "_score_tmp" / "png"


def heatmap(page_no, out_dir, label="LO"):
    name = f"page-{page_no:02d}.png"
    t = Image.open(TARG / name).convert("RGB")
    c = Image.open(W27 / name).convert("RGB")
    if c.size != t.size:
        c = c.resize(t.size, Image.LANCZOS)
    arr_t = np.asarray(t, dtype=np.int16)
    arr_c = np.asarray(c, dtype=np.int16)
    diff = np.abs(arr_t - arr_c).mean(axis=2).astype(np.float32)
    diff_norm = np.clip(diff / 50.0, 0.0, 1.0)
    heat = (cm.inferno(diff_norm)[:, :, :3] * 255).astype(np.uint8)
    heat_im = Image.fromarray(heat)
    mask = (diff > 18).astype(np.uint8) * 255
    gray = np.asarray(t.convert("L"), dtype=np.float32)
    gray3 = np.stack([gray, gray, gray], axis=2)
    blended = gray3.copy()
    red = np.array([220, 30, 30], dtype=np.float32)
    m = mask.astype(bool)
    blended[m] = 0.55 * gray3[m] + 0.45 * red
    blended_im = Image.fromarray(np.clip(blended, 0, 255).astype(np.uint8))
    W, H = t.size
    gap, pad_top = 20, 48
    canvas = Image.new("RGB", (W * 2 + gap, H * 2 + gap + pad_top), "white")
    # label strip
    strip = Image.new("RGB", (canvas.width, pad_top), "white")
    d = ImageDraw.Draw(strip)
    f = ImageFont.load_default()
    d.text((10, 6), f"Page {page_no:02d}  TL:target  TR:W27 {label}  BL:|diff| heatmap (inferno, sat=50)  BR:target+mask(diff>18)", fill="black", font=f)
    canvas.paste(strip, (0, 0))
    canvas.paste(t, (0, pad_top))
    canvas.paste(c, (W + gap, pad_top))
    canvas.paste(heat_im, (0, pad_top + H + gap))
    canvas.paste(blended_im, (W + gap, pad_top + H + gap))
    canvas.save(out_dir / f"page-{page_no:02d}-heatmap.png", optimize=True)


def crop_compare(page_no, box, tag):
    """Crop a region on both images and stack side-by-side at 2x scale."""
    name = f"page-{page_no:02d}.png"
    t = Image.open(TARG / name).convert("RGB")
    c = Image.open(W27 / name).convert("RGB")
    if c.size != t.size:
        c = c.resize(t.size, Image.LANCZOS)
    t_crop = t.crop(box)
    c_crop = c.crop(box)
    # 2x upscale
    t_crop = t_crop.resize((t_crop.width * 2, t_crop.height * 2), Image.LANCZOS)
    c_crop = c_crop.resize((c_crop.width * 2, c_crop.height * 2), Image.LANCZOS)
    gap = 20
    pad = 40
    canvas = Image.new("RGB", (t_crop.width + c_crop.width + gap, max(t_crop.height, c_crop.height) + pad), "white")
    strip = Image.new("RGB", (canvas.width, pad), "white")
    d = ImageDraw.Draw(strip)
    f = ImageFont.load_default()
    d.text((10, 6), f"p{page_no:02d} {tag}: W27 (left) | target (right), 2x crop", fill="black", font=f)
    canvas.paste(strip, (0, 0))
    canvas.paste(c_crop, (0, pad))
    canvas.paste(t_crop, (c_crop.width + gap, pad))
    out = AUDIT / "diffmaps" / f"page-{page_no:02d}-crop-{tag}.png"
    canvas.save(out, optimize=True)


if __name__ == "__main__":
    # Additional heatmaps for pages that scored 10+
    for p in (5, 7, 8, 12, 13):
        heatmap(p, AUDIT / "diffmaps")
        print("heatmap", p)
    # Focused crops on pages with structural defects
    # p7 keycap table region (lower part of page)
    crop_compare(7, (40, 600, 870, 980), "keycap-table")
    # p4 CAUTION+NOTICE boxes
    crop_compare(4, (40, 180, 870, 600), "caution-notice-boxes")
    # p6 product structure table
    crop_compare(6, (40, 660, 870, 970), "structure-table")
    # p2 TOC entries spacing
    crop_compare(2, (40, 470, 870, 1200), "toc-spacing")
    # p11 troubleshooting table header band
    crop_compare(11, (40, 220, 870, 380), "trouble-header-band")
    # p1 footer paragraph break
    crop_compare(1, (0, 1080, 875, 1240), "footer")
    print("done")
