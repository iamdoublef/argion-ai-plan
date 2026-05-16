"""
对比 target/winner 两个 spans.json，逐页输出精确差异报告。
比较维度：drawings (设计元素)、fonts、sizes、colors、位置（关键 spans）。
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def page_stat(page: dict) -> dict:
    fonts = Counter(s["font"] for s in page["spans"])
    sizes = Counter(s["size"] for s in page["spans"])
    colors = Counter(s["color"] for s in page["spans"] if s["color"] != "#000000")
    accent_red_spans = [s for s in page["spans"] if s["color"].upper() == "#E63946"]
    drawings_colored = [
        d for d in page["drawings"]
        if d.get("stroke") and d["stroke"].upper() != "#000000"
        or d.get("fill") and d["fill"].upper() != "#000000"
    ]
    return {
        "page": page["page"],
        "size_pt": page["size_pt"],
        "spans": len(page["spans"]),
        "drawings_total": page["drawings_count"],
        "drawings_colored": len(drawings_colored),
        "images": len(page["images"]),
        "fonts": dict(fonts.most_common()),
        "sizes": dict(sizes.most_common(5)),
        "colors_nonblack": dict(colors.most_common(8)),
        "accent_red_count": len(accent_red_spans),
        "accent_red_text": [s["text"][:30] for s in accent_red_spans][:5],
    }


def main():
    if len(sys.argv) != 4:
        print("Usage: diff_spans.py <target.json> <winner.json> <output.md>", file=sys.stderr)
        sys.exit(1)
    t = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    w = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    out = []
    out.append("# 逐页精确设计差异（target PDF vs winner DOCX→PDF）\n")
    out.append("两侧都用 LibreOffice/Pymupdf 渲染到同一坐标空间。font/size/color 直接来自 OOXML/PDF metadata。\n")

    for tp, wp in zip(t, w):
        ts = page_stat(tp)
        ws = page_stat(wp)
        out.append(f"\n## 第 {ts['page']} 页\n")
        out.append(f"| 维度 | TARGET | WINNER | 差异 |")
        out.append("|---|---|---|---|")
        out.append(f"| text spans | {ts['spans']} | {ws['spans']} | {ws['spans']-ts['spans']:+d} |")
        out.append(f"| drawings | {ts['drawings_total']} | {ws['drawings_total']} | {ws['drawings_total']-ts['drawings_total']:+d} |")
        out.append(f"| 彩色 drawings | {ts['drawings_colored']} | {ws['drawings_colored']} | {ws['drawings_colored']-ts['drawings_colored']:+d} |")
        out.append(f"| images | {ts['images']} | {ws['images']} | {ws['images']-ts['images']:+d} |")
        out.append(f"| accent 红色文字数 | {ts['accent_red_count']} | {ws['accent_red_count']} | {ws['accent_red_count']-ts['accent_red_count']:+d} |")

        out.append(f"\n**字体使用 — TARGET**: `{ts['fonts']}`")
        out.append(f"**字体使用 — WINNER**: `{ws['fonts']}`")

        only_target = set(ts['fonts']) - set(ws['fonts'])
        only_winner = set(ws['fonts']) - set(ts['fonts'])
        if only_target:
            out.append(f"\n❗ 仅 target 用的字体（winner 缺失）: {sorted(only_target)}")
        if only_winner:
            out.append(f"❗ 仅 winner 用的字体（target 没有）: {sorted(only_winner)}")

        out.append(f"\n**主字号** — TARGET top5: `{ts['sizes']}` | WINNER top5: `{ws['sizes']}`")
        out.append(f"**非黑配色** — TARGET: `{ts['colors_nonblack']}` | WINNER: `{ws['colors_nonblack']}`")

        # Accent red text content comparison
        if ts['accent_red_text'] != ws['accent_red_text']:
            out.append(f"\n红色文字差异：")
            out.append(f"  - TARGET: {ts['accent_red_text']}")
            out.append(f"  - WINNER: {ws['accent_red_text']}")

    Path(sys.argv[3]).write_text("\n".join(out), encoding="utf-8")
    print(f"OK → {sys.argv[3]}")


if __name__ == "__main__":
    main()
