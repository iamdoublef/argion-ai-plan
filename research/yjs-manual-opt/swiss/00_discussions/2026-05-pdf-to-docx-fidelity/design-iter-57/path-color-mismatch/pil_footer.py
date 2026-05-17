"""Sample footer page number colors more precisely."""
from PIL import Image
from collections import Counter
from pathlib import Path

TARGET_PNG_DIR = Path("D:/work/private/yjsplan/research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/baseline/target_png")

def sample(img, box):
    crop = img.crop(box).convert("RGB")
    pixels = list(crop.getdata())
    # Filter out near-white pixels
    non_white = [p for p in pixels if not (p[0] > 245 and p[1] > 245 and p[2] > 245)]
    # Also filter near-black for text only
    text = [p for p in non_white if not (p[0] < 30 and p[1] < 30 and p[2] < 30)]
    if not text:
        return Counter()
    bucketed = [(p[0]//8*8, p[1]//8*8, p[2]//8*8) for p in text]
    return Counter(bucketed)


for page in ["03", "04", "05", "06", "07", "11"]:
    img = Image.open(TARGET_PNG_DIR / f"page-{page}.png")
    W, H = img.size
    # Footer: bottom ~5%, around left margin where IMT050/page num sits
    foot_left = sample(img, (int(W*0.04), int(H*0.93), int(W*0.40), int(H*0.99)))
    foot_right = sample(img, (int(W*0.55), int(H*0.93), int(W*0.95), int(H*0.99)))
    print(f"p{page} footer-left top non-white-non-black 4:")
    for c, n in foot_left.most_common(4):
        print(f"  #{c[0]:02X}{c[1]:02X}{c[2]:02X} = {n}")
    print(f"p{page} footer-right:")
    for c, n in foot_right.most_common(4):
        print(f"  #{c[0]:02X}{c[1]:02X}{c[2]:02X} = {n}")
