"""Build side-by-side comparisons and diff heatmaps for W27 vs target PDF.

Outputs:
  comparisons/page-XX-sidebyside-LO.png          (W27 LO render | target)
  comparisons/page-XX-sidebyside-WORD.png        (Word-rendered W27 | target)
  diffmaps/page-XX-heatmap.png                   (target | W27 LO | abs diff cmap | binary mask)

Per-page numeric stats are dumped to _work/stats.json so the audit prose stays grounded.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFont
import matplotlib
matplotlib.use("Agg")
import matplotlib.cm as cm

ROOT = Path(r"D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity")
AUDIT_DIR = ROOT / "design-iter-34" / "path-design-audit"
COMP_DIR = AUDIT_DIR / "comparisons"
DIFF_DIR = AUDIT_DIR / "diffmaps"
WORK_DIR = AUDIT_DIR / "_work"

TARGET_PNG = ROOT / "baseline" / "target_png"
W27_LO_PNG = ROOT / "final" / "_score_tmp" / "png"
W27_WORD_PNG = ROOT / "design-iter-28" / "path-codex" / "iter-1" / "_score_tmp" / "png"

PAGES = list(range(1, 16))
HARD_PAGES = [3, 9, 11, 14]


def load_pair(p_target: Path, p_cand: Path) -> tuple[Image.Image, Image.Image]:
    a = Image.open(p_target).convert("RGB")
    b = Image.open(p_cand).convert("RGB")
    # Normalize to identical pixel grid (target wins)
    if a.size != b.size:
        b = b.resize(a.size, Image.LANCZOS)
    return a, b


def _label_strip(width: int, text_left: str, text_right: str, gap: int) -> Image.Image:
    """Build a small label strip so we never invoke TrueType on a huge canvas (Pillow 9.5 + win32 segfault)."""
    strip = Image.new("RGB", (width, 36), "white")
    d = ImageDraw.Draw(strip)
    f = ImageFont.load_default()
    d.text((10, 10), text_left, fill="black", font=f)
    # right label position: width//2 + gap//2
    d.text((width // 2 + gap // 2 + 10, 10), text_right, fill="black", font=f)
    return strip


def side_by_side(left: Image.Image, right: Image.Image, left_label: str, right_label: str, out: Path):
    gap = 24
    pad_top = 40
    W = left.width + right.width + gap
    H = max(left.height, right.height) + pad_top
    canvas = Image.new("RGB", (W, H), "white")
    strip = _label_strip(W, left_label, right_label, gap)
    canvas.paste(strip, (0, 0))
    canvas.paste(left, (0, pad_top))
    canvas.paste(right, (left.width + gap, pad_top))
    # divider drawn with rectangle so we don't need ImageDraw on the giant canvas
    div = Image.new("RGB", (1, H), "#999999")
    canvas.paste(div, (left.width + gap // 2, 0))
    canvas.save(out, optimize=True)


def heatmap_quad(target: Image.Image, cand: Image.Image, page_no: int, out: Path) -> dict:
    arr_t = np.asarray(target, dtype=np.int16)
    arr_c = np.asarray(cand, dtype=np.int16)
    diff = np.abs(arr_t - arr_c).mean(axis=2).astype(np.float32)  # HxW
    diff_norm = np.clip(diff / 50.0, 0.0, 1.0)  # 50 grey-levels = saturation
    heat = (cm.inferno(diff_norm)[:, :, :3] * 255).astype(np.uint8)
    heat_im = Image.fromarray(heat)

    mask = (diff > 18).astype(np.uint8) * 255  # hard threshold mask of "visible" diffs
    mask_rgb = np.stack([mask] * 3, axis=2)
    # Overlay mask on grayscale target for spatial context
    gray = np.asarray(target.convert("L"), dtype=np.float32)
    gray3 = np.stack([gray, gray, gray], axis=2)
    blended = gray3.copy()
    red = np.array([220, 30, 30], dtype=np.float32)
    m = mask.astype(bool)
    blended[m] = 0.55 * gray3[m] + 0.45 * red
    blended_im = Image.fromarray(np.clip(blended, 0, 255).astype(np.uint8))

    # Build 2x2 grid: target | cand / heat | mask-overlay
    W, H = target.size
    gap = 20
    pad_top = 48
    grid_w = W * 2 + gap
    grid_h = H * 2 + gap + pad_top
    # Top label strip (small canvas — safe to use ImageDraw)
    strip = Image.new("RGB", (grid_w, pad_top), "white")
    d = ImageDraw.Draw(strip)
    f = ImageFont.load_default()
    d.text((10, 6), f"Page {page_no:02d}  TL:target  TR:W27 LO  BL:|diff| heatmap (inferno, sat=50)  BR:target+mask(diff>18)", fill="black", font=f)
    canvas = Image.new("RGB", (grid_w, grid_h), "white")
    canvas.paste(strip, (0, 0))
    canvas.paste(target, (0, pad_top))
    canvas.paste(cand, (W + gap, pad_top))
    canvas.paste(heat_im, (0, pad_top + H + gap))
    canvas.paste(blended_im, (W + gap, pad_top + H + gap))
    canvas.save(out, optimize=True)

    stats = {
        "page": page_no,
        "mean_diff": float(diff.mean()),
        "p95_diff": float(np.percentile(diff, 95)),
        "p99_diff": float(np.percentile(diff, 99)),
        "max_diff": float(diff.max()),
        "frac_visible_diff": float(m.mean()),  # fraction of pixels with diff>18
        "frac_strong_diff": float((diff > 40).mean()),
    }
    return stats


def column_profile(target: Image.Image, cand: Image.Image, page_no: int) -> dict:
    """Row-wise (vertical) and column-wise (horizontal) ink density profiles.

    Looks for shifts / scale mismatches: if W27's text band sits 4px lower than target,
    horizontal-correlation profile will reveal it via cross-corr peak offset.
    """
    t = 255 - np.asarray(target.convert("L"), dtype=np.float32)
    c = 255 - np.asarray(cand.convert("L"), dtype=np.float32)
    row_t = t.mean(axis=1)
    row_c = c.mean(axis=1)
    col_t = t.mean(axis=0)
    col_c = c.mean(axis=0)
    # cross-corr offset for rows (vertical alignment)
    def best_shift(a, b, max_shift=30):
        best, best_v = 0, -1e18
        for s in range(-max_shift, max_shift + 1):
            if s < 0:
                v = np.dot(a[-s:], b[: len(b) + s])
            elif s > 0:
                v = np.dot(a[: len(a) - s], b[s:])
            else:
                v = np.dot(a, b)
            if v > best_v:
                best_v, best = v, s
        return best
    vshift = best_shift(row_t, row_c)
    hshift = best_shift(col_t, col_c)
    return {"page": page_no, "vertical_shift_px": int(vshift), "horizontal_shift_px": int(hshift),
            "ink_t": float(row_t.sum()), "ink_c": float(row_c.sum()),
            "ink_ratio_c_over_t": float(row_c.sum() / max(row_t.sum(), 1.0))}


def main():
    COMP_DIR.mkdir(parents=True, exist_ok=True)
    DIFF_DIR.mkdir(parents=True, exist_ok=True)
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    stats_all = {"sidebyside_done": [], "heatmap_stats": {}, "profile_stats": {}, "word_sidebyside_done": []}

    for p in PAGES:
        print(f"[page {p:02d}] start", flush=True)
        name = f"page-{p:02d}.png"
        t_path = TARGET_PNG / name
        lo_path = W27_LO_PNG / name
        word_path = W27_WORD_PNG / name
        if not (t_path.exists() and lo_path.exists()):
            print("skip", p, "missing PNG")
            continue

        t_lo, c_lo = load_pair(t_path, lo_path)
        # LO side-by-side: W27 (left) | target (right)
        out_lo = COMP_DIR / f"page-{p:02d}-sidebyside-LO.png"
        side_by_side(c_lo, t_lo, f"W27 LO render p{p}", f"target PDF p{p}", out_lo)
        stats_all["sidebyside_done"].append(p)

        print(f"[page {p:02d}] LO sbs done", flush=True)
        if word_path.exists():
            t_w, c_w = load_pair(t_path, word_path)
            out_w = COMP_DIR / f"page-{p:02d}-sidebyside-WORD.png"
            side_by_side(c_w, t_w, f"W27 Word render p{p}", f"target PDF p{p}", out_w)
            stats_all["word_sidebyside_done"].append(p)
            print(f"[page {p:02d}] WORD sbs done", flush=True)

        # Per-page profile stats (cheap, even for non-hard pages — helps narrative)
        stats_all["profile_stats"][p] = column_profile(t_lo, c_lo, p)
        print(f"[page {p:02d}] profile done", flush=True)

        if p in HARD_PAGES:
            out_h = DIFF_DIR / f"page-{p:02d}-heatmap.png"
            s = heatmap_quad(t_lo, c_lo, p, out_h)
            stats_all["heatmap_stats"][p] = s
            print(f"[page {p:02d}] heatmap done", flush=True)

    with open(WORK_DIR / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats_all, f, indent=2, ensure_ascii=False)
    print("done:", json.dumps({k: (len(v) if isinstance(v, list) else len(v)) for k, v in stats_all.items()}))


if __name__ == "__main__":
    main()
