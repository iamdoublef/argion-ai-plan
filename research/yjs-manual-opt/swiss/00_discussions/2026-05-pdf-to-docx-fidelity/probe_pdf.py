"""
探查 PDF 的字体、文字块、配色，供子代理参考样式细节。
用法：python probe_pdf.py <target.pdf> > pdf_probe.md
"""
import sys
import json
from collections import Counter, defaultdict
from pathlib import Path

import fitz  # PyMuPDF


def main(pdf_path: str) -> int:
    doc = fitz.open(pdf_path)
    print(f"# PDF 探查报告：{Path(pdf_path).name}\n")
    print(f"- 总页数：{len(doc)}")
    print(f"- 页面尺寸：{doc[0].rect.width:.1f} × {doc[0].rect.height:.1f} pt")
    w_mm = doc[0].rect.width / 72 * 25.4
    h_mm = doc[0].rect.height / 72 * 25.4
    print(f"- 折合：{w_mm:.1f} × {h_mm:.1f} mm")
    print()

    # 全文档字体清单
    font_use: Counter = Counter()
    font_sizes: defaultdict = defaultdict(list)
    color_use: Counter = Counter()
    page_text_lens = []

    for pno, page in enumerate(doc, start=1):
        text_dict = page.get_text("dict")
        page_chars = 0
        for block in text_dict.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    f = span.get("font", "?")
                    sz = round(span.get("size", 0), 2)
                    col = span.get("color", 0)
                    text = span.get("text", "")
                    font_use[f] += 1
                    font_sizes[f].append(sz)
                    if col != 0:
                        # color is 0xRRGGBB int
                        hexcol = f"#{col:06X}"
                        color_use[hexcol] += 1
                    page_chars += len(text)
        page_text_lens.append((pno, page_chars))

    print("## 字体使用统计（按 span 数）\n")
    print("| 字体 | spans | 主要字号 (pt) |")
    print("|---|---|---|")
    for f, n in font_use.most_common():
        sizes = font_sizes[f]
        common_sz = Counter(round(s, 1) for s in sizes).most_common(3)
        sz_str = " / ".join(f"{s}({c}×)" for s, c in common_sz)
        print(f"| `{f}` | {n} | {sz_str} |")
    print()

    print("## 非黑色配色（≥3 次）\n")
    print("| 颜色 | 次数 |")
    print("|---|---|")
    for c, n in color_use.most_common():
        if n >= 3:
            print(f"| {c} | {n} |")
    print()

    print("## 每页文本量\n")
    print("| 页 | 字符数 |")
    print("|---|---|")
    for pno, n in page_text_lens:
        print(f"| {pno} | {n} |")
    print()

    print("## 第 1 页文字块（仅前 20 个 span）\n")
    page = doc[0]
    text_dict = page.get_text("dict")
    span_count = 0
    print("| span# | bbox | font | sz | color | text |")
    print("|---|---|---|---|---|---|")
    for block in text_dict.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                if span_count >= 20:
                    break
                bbox = span["bbox"]
                col = span.get("color", 0)
                hexcol = f"#{col:06X}" if col else "#000000"
                txt = span.get("text", "").replace("|", "\\|")[:50]
                print(f"| {span_count} | ({bbox[0]:.0f},{bbox[1]:.0f},{bbox[2]:.0f},{bbox[3]:.0f}) | {span['font']} | {span['size']:.1f} | {hexcol} | {txt} |")
                span_count += 1
    print()

    # Image inventory
    print("## 图片清单\n")
    print("| 页 | xref | 大小 |")
    print("|---|---|---|")
    total_imgs = 0
    for pno, page in enumerate(doc, start=1):
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            w = img_info[2]
            h = img_info[3]
            print(f"| {pno} | {xref} | {w}×{h} |")
            total_imgs += 1
    print(f"\n共 {total_imgs} 张图片引用。\n")

    doc.close()
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: probe_pdf.py <pdf>", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
