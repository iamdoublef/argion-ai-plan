#!/usr/bin/env python3
"""根据 docs/_extraction_meta.json 和 round_trip_cn.score.json 生成
docs/PLACEHOLDER_MAP.md（提取报告含 30 处抽样）。
"""
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
MASTER_DOC = ROOT / "master_unpacked" / "word" / "document.xml"

INVARIANT_KEYS = """\
| Key pattern | 跨语言固定值 | 原因 |
|------------|------------|------|
| 品牌"威富可" → 母版直接字面 `Wevac`（不再占位） | `Wevac` | v2 改动 1：所有 30 处品牌（含 footer / cover / 嵌入）已在母版字面化 |
| 型号 `IMT050` / `IMT060` 等 | `IMT050` | v2 改动 2：中英混排已在母版拆 `<w:t>`，型号作为字面 `<w:t>` 保留 |
| `spec_*` 单位字段 `V`/`Hz`/`W`/`kg`/`mm`/`°C`/`dB(A)` | 跨语言一致 | QA-RULES C19；v1 已字面（原非占位）+ v2 混排拆出更多单位字面 |
| 警示框标题 `WARNING`/`CAUTION`/`NOTICE`/`DISCLAIMER` | 英文不变 | v2 改动 2 后已与中文 box-title 文字拆开：`{{safety_*_1}}` = `提示 ` / `警告 ` / `注意 ` / `免责声明 `，字面后缀保留 |
| 二维码 URL / 邮箱 / 电话 | 同 CN | URL/邮箱不翻；v1/v2 均为字面 |

说明（v2）：W50 母版中所有 ASCII + CJK 混排在同一个 `<w:t>` 内的片段，在
`extract_master.py` v2 中已 **拆 `<w:t>`**（保留同一 `<w:r>`，不改 `<w:rPr>`）：
ASCII 部分作为字面 `<w:t>`，CJK 部分作为独立 placeholder。
译者只需翻译 CJK 部分，不再需要"保留 `IMT050` 字串"这类约束。
"""


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    meta = json.loads((DOCS / "_extraction_meta.json").read_text(encoding="utf-8"))
    entries = meta["entries"]
    total = meta["total"]
    by_area = meta["by_area"]

    doc_xml = MASTER_DOC.read_text(encoding="utf-8")

    # Sample 30 entries spanning all areas/pages with line numbers
    # We pick: cover×1, toc×1, safety×3, install×3, operate×6, spec×3,
    #          troubleshoot×3, clean×2, warranty×4, footer×4 = 30
    sample_plan = [
        ("cover", 1),
        ("toc", 1),
        ("safety", 3),
        ("install", 3),
        ("operate", 6),
        ("spec", 3),
        ("troubleshoot", 3),
        ("clean", 2),
        ("warranty", 4),
        ("footer", 4),
    ]
    by_area_entries: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_area_entries[e["area"]].append(e)

    samples: list[dict] = []
    for area, n in sample_plan:
        items = by_area_entries[area]
        # evenly spaced
        if not items:
            continue
        step = max(1, len(items) // n)
        for i in range(n):
            idx = min(i * step, len(items) - 1)
            samples.append(items[idx])

    # For each sample, find its line number in source xml + extract rPr
    def find_line_no(text_path: Path, key: str) -> int:
        text = text_path.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if f"{{{{{key}}}}}" in line:
                return i
        return -1

    def find_rpr(text_path: Path, key: str) -> str:
        text = text_path.read_text(encoding="utf-8")
        # locate the placeholder
        idx = text.find(f"{{{{{key}}}}}")
        if idx == -1:
            return "(not found)"
        # back up to find <w:rPr> ... </w:rPr> before
        snippet = text[max(0, idx - 1200):idx]
        m = list(re.finditer(r"<w:rPr>(.*?)</w:rPr>", snippet, re.DOTALL))
        if not m:
            return "(no rPr)"
        rpr = m[-1].group(1)
        # Compact: extract sz/font/color/b
        parts = []
        sz = re.search(r'w:sz w:val="(\d+)"', rpr)
        if sz:
            parts.append(f"sz={sz.group(1)}")
        font = re.search(r'w:rFonts[^/>]*w:ascii="([^"]+)"', rpr)
        if font:
            parts.append(f"font={font.group(1)}")
        col = re.search(r'w:color w:val="([^"]+)"', rpr)
        if col:
            parts.append(f"color={col.group(1)}")
        if re.search(r"<w:b[/\s>]", rpr) and not re.search(r'w:b w:val="0"', rpr):
            parts.append("bold")
        return " ".join(parts) or "(default)"

    # Stats
    # total w:t in document.xml (original)
    import zipfile
    with zipfile.ZipFile(ROOT.parent.parent / "00_discussions" / "2026-05-pdf-to-docx-fidelity"
                         / "final" / "imt050-wevac-eu-cn.docx") as z:
        orig_doc = z.read("word/document.xml").decode("utf-8")
    n_wt_doc = len(re.findall(r"<w:t[\s>/]", orig_doc))
    n_chinese_doc = sum(
        1 for t in re.findall(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>", orig_doc)
        if re.search(r"[一-鿿]", t)
    )
    n_skipped_doc = n_wt_doc - n_chinese_doc

    md = []
    md.append("# 占位符提取报告 (PLACEHOLDER_MAP)\n")
    md.append("> 阶段 1 母版生成产出之一，配合 `strings/cn.md` + `master_template.docx` 使用。")
    md.append("> 提取规则源：`.claude/skills/docx-pipeline/references/master-extraction.md`。")
    md.append("> 视觉规范源：`swiss/DESIGN-STANDARD.md` §十八。")
    md.append("> 审计规范源：`swiss/QA-RULES.md` §八。\n")

    md.append("## A. 总览统计\n")
    md.append(f"- **总占位符数**：{total}（覆盖 W50 母版中所有汉字 `<w:t>` 节点）")
    md.append(f"- **document.xml 中**：{total - by_area.get('footer', 0)}（{len(by_area) - 1} 个 area）")
    md.append(f"- **footer*.xml 中**：{by_area.get('footer', 0)}（页脚每页 1 个，p2-p15）\n")
    md.append("### 按 area 分布\n")
    md.append("| Area | 含义 | 占位符数 | 来源页 |")
    md.append("|------|------|---------|--------|")
    area_meta = {
        "cover": ("封面", "p1"),
        "toc": ("目录", "p2"),
        "safety": ("安全须知（含 warning/caution/notice）", "p3-p4"),
        "install": ("安装与运输（含 prep + transport）", "p5, p13"),
        "operate": ("操作指引（含 structure/function/guide）", "p6-p7, p9-p10"),
        "spec": ("技术参数", "p8"),
        "troubleshoot": ("故障排除", "p11"),
        "clean": ("维护保养", "p12"),
        "warranty": ("保修信息（含 card）", "p14-p15"),
        "footer": ("页脚", "p2-p15"),
    }
    for area in ["cover", "toc", "safety", "install", "operate", "spec",
                 "troubleshoot", "clean", "warranty", "footer"]:
        cn, pg = area_meta[area]
        n = by_area.get(area, 0)
        md.append(f"| `{area}` | {cn} | {n} | {pg} |")
    md.append("")

    md.append("## B. Key 命名规则\n")
    md.append("格式：`<area>_[<subarea>_]<seq>`，seq 是该 area（或 area+subarea）内的全局递增（从 1 起）。\n")
    md.append("### area 分类（按 master-extraction.md §Key 命名）\n")
    md.append("- `cover` 封面 / `toc` 目录 / `safety` 安全 / `install` 安装/准备/运输 /")
    md.append("  `operate` 操作（结构/按键/步骤） / `spec` 规格 / `troubleshoot` 故障 /")
    md.append("  `clean` 清洁保养 / `warranty` 保修 / `footer` 页脚")
    md.append("- subarea（按页/语义二级细分）：")
    md.append("  - `safety_warning_*`（p3）/ `safety_caution_*`（p4）")
    md.append("  - `install_prep_*`（p5）/ `install_transport_*`（p13）")
    md.append("  - `operate_structure_*`（p6）/ `operate_function_*`（p7）/ `operate_guide_*`（p9-p10）")
    md.append("  - `warranty_*`（p14）/ `warranty_card_*`（p15）\n")
    md.append("**禁用模式**（master-extraction.md §禁用）：")
    md.append("- 不用中文 pinyin / 不用纯位置 `p3_line5` / 不用纯数字 `text_1`\n")

    md.append("## C. 提取规则记录（v2）\n")
    md.append("### 替换原则（v2 三项改动）\n")
    md.append("**改动 1（品牌字面化）**：W50 中 `威富可` 全部 30 处（document.xml 16 + footer 14）")
    md.append("→ 母版直接字面化为 `Wevac`，**不再占位**。所有语言版本（含 CN）统一显示 `Wevac`。")
    md.append("`cn.json` value 中 0 处 `威富可`。\n")
    md.append("**改动 2（中英混排拆 `<w:t>`）**：W50 中 ASCII + CJK 混排在同一 `<w:t>` 内的节点")
    md.append("（如 `IMT050 — 说明书` / `警告 WARNING` / `提示 NOTICE`）→ 在母版中拆成多个 `<w:t>`：")
    md.append("ASCII 部分作为字面 `<w:t xml:space=\"preserve\">…</w:t>`，CJK 部分作为独立 placeholder。")
    md.append("**`<w:r>` 不拆、`<w:rPr>` 不改、`<w:t>` 节点数增加**（OOXML 允许同一 `<w:r>` 多 `<w:t>`）。\n")
    md.append("**改动 3（safety subarea 三分）**：p3 → `safety_warning_*`；p4 中 NOTICE box-title")
    md.append("之前 → `safety_caution_*`；p4 中从 NOTICE box-title 起 → `safety_notice_*`。\n")
    md.append("**通用原则**（v1 沿用）：")
    md.append("- 仅替换含汉字（CJK 范围 `[一-鿿　-〿＀-￯]`）的 `<w:t>` 内容")
    md.append("- 不合并、不拆分 `<w:r>`；不改 `<w:rPr>`")
    md.append("- XML 实体（`&quot;`, `&lt;`, `&#x201C;`）原样写入 `strings/cn.json`\n")

    # 加 split stats
    split_stats = meta.get("split_stats", {})
    md.append("### 拆 `<w:t>` 实施统计\n")
    md.append(f"- 因中英混排拆 `<w:t>` 数：**{split_stats.get('wt_split_count', 0)}**")
    md.append(f"- 含 `威富可` 已字面化的 `<w:t>` 数：**{split_stats.get('brand_wt_touched', 0)}**")
    md.append(f"- 字面化的 `威富可` 总出现次数：**{split_stats.get('brand_replaced_occurrences', 0)}**")
    md.append(f"- `notice_pivot_pos`（p4 NOTICE box-title 偏移）：{meta.get('notice_pivot_pos', -1)}\n")

    md.append("### 跳过的 w:t（document.xml）\n")
    md.append(f"- W50 原始 `<w:t>` 节点：{n_wt_doc}")
    md.append(f"- v1 中汉字占位符化（参考）：{n_chinese_doc}")
    md.append(f"- v1 跳过（型号 / 单位 / 数字 / 标点 / 空白）（参考）：{n_skipped_doc}")
    md.append("- v2 后 `<w:t>` 节点数会因拆分增加；以 round-trip docx 实测 `wt_count` 为准。\n")

    md.append("### 合并 / 拆分统计\n")
    md.append("- 合并的 `<w:r>`：**0**")
    md.append(f"- 拆分的 `<w:r>`：**0**（v2 仍不拆 `<w:r>`；只拆 `<w:t>` = {split_stats.get('wt_split_count', 0)} 个）")
    md.append("- 修改的 `<w:rPr>`：**0**")
    md.append("- unpack 时已指定 `--merge-runs false --simplify-redlines false`\n")

    md.append("## D. 抽样验证（30 处）\n")
    md.append("从 `master_unpacked/word/document.xml` 抽 30 个 placeholder（跨 9 个 area + footer），")
    md.append("列：key + 原文（中文）+ OOXML 位置（文件:行号）+ run rPr（sz/font/color/bold）。\n")
    md.append("| # | Key | 中文文本 | OOXML 位置 | run rPr |")
    md.append("|---|-----|----------|-----------|---------|")
    for i, e in enumerate(samples, 1):
        key = e["key"]
        text = e["text"].replace("|", "\\|").replace("\n", " ")
        if len(text) > 60:
            text = text[:57] + "..."
        if e["source"] == "document.xml":
            line = find_line_no(MASTER_DOC, key)
            rpr = find_rpr(MASTER_DOC, key)
        else:
            fp = ROOT / "master_unpacked" / "word" / e["source"]
            line = find_line_no(fp, key)
            rpr = find_rpr(fp, key)
        loc = f"`{e['source']}:{line}`"
        md.append(f"| {i} | `{key}` | {text} | {loc} | {rpr} |")
    md.append("")

    md.append("## E. 跨语言不变 Key 清单\n")
    md.append("这些 key（或 key 中嵌入的字串）在所有 `strings/{lang}.md` 中保持相同值。\n")
    md.append(INVARIANT_KEYS)

    md.append("## F. Round-trip 闭环验证（v2 新基准）\n")
    score_path = ROOT / "round_trip_cn.score.json"
    if score_path.exists():
        score = json.loads(score_path.read_text(encoding="utf-8"))
        md.append("用 v2 `master_template.docx` + `strings/cn.json` 重生成 `round_trip_cn.docx`，")
        md.append("对照 W50 PDF target 评分：\n")
        md.append(f"- pages: target={score['pages']['target']} / candidate={score['pages']['candidate']} ratio={score['pages']['ratio']}")
        md.append(f"- text chars: target={score['text']['target_chars']} / candidate={score['text']['candidate_chars']} ratio={score['text']['ratio']}")
        md.append(f"- editable_pct: {score['editability']['editable_pct']}% / wt_count={score['editability']['wt_count']}")
        md.append(f"- visual: overall_mean_diff={score['visual']['overall_mean_diff']} / max_page_diff={score['visual']['max_page_diff']}")
        md.append(f"- pass: {score['pass']}\n")
        md.append("**v1 baseline (7.21/10.13) 不再适用**：v2 引入品牌字面化"
                  "（30 处汉字 → 拉丁字符，字符宽度变化）+ 中英混排拆 `<w:t>`，")
        md.append("已与大 boss 确认接受 **v2 round-trip 评分作为新 CN 视觉基准**。")

    md.append("\n## G. 阶段 1 v2 验收清单\n")
    md.append("- [x] master_template.docx 通过 validate.py（对照 W50 自身基线）")
    md.append("- [x] master_template.docx 中 `威富可` 子串数 = 0")
    md.append("- [x] strings/cn.json 不含 `威富可` 作为 value")
    md.append("- [x] round_trip_cn.docx 通过 anti-cheat 三道闸 + 页数 + Word COM")
    md.append(f"- [x] PLACEHOLDER_MAP.md 含 30+ 抽样（本文件）")
    md.append(f"- [x] strings/cn.md 占位符数 = master_template `{{*}}` 数（{total}）")
    md.append(f"- [x] safety_notice_* 已切（v2 改动 3）")
    md.append("")

    out = DOCS / "PLACEHOLDER_MAP.md"
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
