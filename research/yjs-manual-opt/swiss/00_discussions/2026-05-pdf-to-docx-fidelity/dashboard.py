"""
扫描所有 score.json，输出一张 markdown 排行榜。
"""
import json
import sys
from pathlib import Path


def main(root: str) -> int:
    rows = []
    for sf in Path(root).rglob("*.score.json"):
        try:
            data = json.loads(sf.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"# skip {sf}: {e}", file=sys.stderr)
            continue
        cand_abs = Path(data["candidate"])
        try:
            cand = cand_abs.relative_to(Path(root).resolve())
        except ValueError:
            cand = cand_abs.name
        rows.append({
            "candidate": str(cand).replace("\\", "/"),
            "pages": f"{data['pages']['candidate']}/{data['pages']['target']}",
            "text_ratio": data["text"]["ratio"],
            "editable_pct": data["editability"]["editable_pct"],
            "visual_overall": data["visual"]["overall_mean_diff"] if data["visual"] else None,
            "visual_max": data["visual"]["max_page_diff"] if data["visual"] else None,
            "pass_pages": "✓" if data["pass"]["pages"] else "✗",
            "pass_text": "✓" if data["pass"]["text"] else "✗",
            "pass_edit": "✓" if data["pass"]["editable"] else "✗",
            "pass_visual": "✓" if data["pass"]["visual"] else "✗",
            "overall": "PASS" if data["pass"]["overall"] else "FAIL",
        })

    rows.sort(key=lambda r: (
        0 if r["overall"] == "PASS" else 1,
        r["visual_overall"] if r["visual_overall"] is not None else 9999,
    ))

    out = []
    out.append("# 候选 DOCX 评分排行榜\n")
    out.append("（按 PASS/FAIL 然后 visual overall 升序）\n")
    out.append("\n| 候选 | 页数 | 文本比 | 编辑% | 视觉(o/m) | P/T/E/V | 总评 |")
    out.append("|---|---|---|---|---|---|---|")
    for r in rows:
        vov = r["visual_overall"]
        vmx = r["visual_max"]
        vc = f"{vov}/{vmx}" if vov is not None else "—"
        ptev = f"{r['pass_pages']}/{r['pass_text']}/{r['pass_edit']}/{r['pass_visual']}"
        out.append(f"| `{r['candidate']}` | {r['pages']} | {r['text_ratio']} | {r['editable_pct']} | {vc} | {ptev} | **{r['overall']}** |")

    out.append("\n## 验收标准")
    out.append("- 页数（P）：candidate ≤ target+1")
    out.append("- 文本（T）：candidate ≥ target × 0.95")
    out.append("- 可编辑（E）：所有文本在 `<w:t>` 而非 `<wp:txbx>`，editable% ≥ 95")
    out.append("- 视觉（V）：所有页平均像素差异 ≤ 60（0-255）")

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(main(root))
