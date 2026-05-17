#!/usr/bin/env python3
"""
阶段 1 母版占位符提取器。

读 master_unpacked/word/document.xml + footer*.xml，
把所有包含汉字的 <w:t> 内容替换为 {{key}}，原文写入 strings/cn.md。

规则（master-extraction.md §替换原则）：
- 只换 <w:t> 内容，不动 run 结构
- 跳过不含汉字的 w:t（IMT050 / Wevac 英文 / 数字 / 单位）
- 包含汉字的 w:t 整体替换为 placeholder，cn.md 里保留原文（含混入的 IMT050 等英文）

key 命名：<area>_[subarea_]<seq> （seq 是该 area 内的全局递增）
"""

import io
import json
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MASTER = ROOT / "master_unpacked"
STRINGS_DIR = ROOT / "strings"
DOCS_DIR = ROOT / "docs"

CHINESE_RE = re.compile(r"[一-鿿　-〿＀-￯]")
# match <w:t...>...</w:t> with simple text (no nested tags)
WT_RE = re.compile(r"(<w:t(?:\s[^>]*)?>)([^<]*)(</w:t>)")

# Page (sectPr) → area mapping
PAGE_AREA = {
    1: ("cover", None),
    2: ("toc", None),
    3: ("safety", "warning"),
    4: ("safety", "caution"),
    5: ("install", "prep"),
    6: ("operate", "structure"),
    7: ("operate", "function"),
    8: ("spec", None),
    9: ("operate", "guide"),
    10: ("operate", "guide"),
    11: ("troubleshoot", None),
    12: ("clean", None),
    13: ("install", "transport"),
    14: ("warranty", None),
    15: ("warranty", "card"),
}


def assign_page(pos: int, sect_positions: list[int]) -> int:
    for i, sp in enumerate(sect_positions):
        if pos < sp:
            return i + 1
    return len(sect_positions)


def process_document(xml: str) -> tuple[str, list[dict]]:
    """Replace chinese w:t content with placeholders. Return new_xml + entries."""
    sect_positions = [m.start() for m in re.finditer(r"<w:sectPr", xml)]
    if len(sect_positions) != 15:
        raise RuntimeError(f"expected 15 sectPr, got {len(sect_positions)}")

    entries = []
    seq_counter: dict[str, int] = defaultdict(int)

    def replace(m: re.Match) -> str:
        open_tag, content, close_tag = m.group(1), m.group(2), m.group(3)
        if not CHINESE_RE.search(content):
            return m.group(0)
        pos = m.start()
        page = assign_page(pos, sect_positions)
        area, subarea = PAGE_AREA[page]
        prefix = f"{area}_{subarea}" if subarea else area
        seq_counter[prefix] += 1
        key = f"{prefix}_{seq_counter[prefix]}"
        # Preserve xml:space="preserve" if present in original tag
        new_open = open_tag
        if "xml:space" not in open_tag:
            # add preserve only when content has leading/trailing whitespace
            if content != content.strip():
                new_open = open_tag[:-1] + ' xml:space="preserve">'
        entries.append({
            "key": key,
            "text": content,
            "page": page,
            "area": area,
            "subarea": subarea or "",
            "source": "document.xml",
            "offset": pos,
        })
        return f"{new_open}{{{{{key}}}}}{close_tag}"

    new_xml = WT_RE.sub(replace, xml)
    return new_xml, entries


def process_footer(xml: str, footer_idx: int, seq_counter: dict[str, int]) -> tuple[str, list[dict]]:
    """Process a footer file. Footer page = footer_idx (1..15)."""
    entries = []

    def replace(m: re.Match) -> str:
        open_tag, content, close_tag = m.group(1), m.group(2), m.group(3)
        if not CHINESE_RE.search(content):
            return m.group(0)
        seq_counter["footer"] += 1
        key = f"footer_{seq_counter['footer']}"
        entries.append({
            "key": key,
            "text": content,
            "page": footer_idx,
            "area": "footer",
            "subarea": "",
            "source": f"footer{footer_idx}.xml",
            "offset": m.start(),
        })
        return f"{open_tag}{{{{{key}}}}}{close_tag}"

    new_xml = WT_RE.sub(replace, xml)
    return new_xml, entries


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    STRINGS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    doc_path = MASTER / "word" / "document.xml"
    xml = doc_path.read_text(encoding="utf-8")
    new_xml, doc_entries = process_document(xml)
    doc_path.write_text(new_xml, encoding="utf-8")
    print(f"document.xml: replaced {len(doc_entries)} chinese w:t with placeholders")

    # Footers (1..15). footer1.xml is empty.
    all_entries = list(doc_entries)
    footer_counter = {"footer": 0}
    for i in range(1, 16):
        fp = MASTER / "word" / f"footer{i}.xml"
        if not fp.exists():
            continue
        fxml = fp.read_text(encoding="utf-8")
        new_fxml, f_entries = process_footer(fxml, i, footer_counter)
        if f_entries:
            fp.write_text(new_fxml, encoding="utf-8")
        all_entries.extend(f_entries)
        if f_entries:
            print(f"footer{i}.xml: {len(f_entries)} placeholders")

    print(f"total placeholders: {len(all_entries)}")

    # Write strings/cn.md
    cn_md_path = STRINGS_DIR / "cn.md"
    with cn_md_path.open("w", encoding="utf-8") as f:
        f.write("# IMT050 中文翻译字典\n\n")
        f.write(f"> 总占位符数：{len(all_entries)}（来自 W50）\n")
        f.write("> 来源：final/imt050-wevac-eu-cn.docx (W50, 评分 7.21/10.13)\n")
        f.write("> 评分锚：round-trip 必须复现 W50 (7.21/10.13 ±0.01)\n\n")

        # Group by area
        by_area: dict[str, list[dict]] = defaultdict(list)
        for e in all_entries:
            by_area[e["area"]].append(e)

        area_order = ["cover", "toc", "safety", "install", "operate", "spec",
                      "troubleshoot", "clean", "warranty", "footer"]
        area_title = {
            "cover": "封面 (p1)",
            "toc": "目录 (p2)",
            "safety": "安全须知 (p3-p4)",
            "install": "安装与准备 (p5, p13)",
            "operate": "操作指引（含产品结构、按键、操作步骤）(p6-p7, p9-p10)",
            "spec": "技术参数 (p8)",
            "troubleshoot": "故障排除 (p11)",
            "clean": "维护保养 (p12)",
            "warranty": "保修信息 (p14-p15)",
            "footer": "页脚（每页底部）",
        }
        for area in area_order:
            entries = by_area.get(area, [])
            if not entries:
                continue
            f.write(f"## {area_title.get(area, area)}\n\n")
            f.write("| Key | 中文文本 | 位置 |\n")
            f.write("|-----|----------|------|\n")
            for e in entries:
                # escape pipes/newlines in text for table
                text_esc = e["text"].replace("|", "\\|").replace("\n", " ")
                pos = f"p{e['page']} {e['source']}"
                f.write(f"| {e['key']} | {text_esc} | {pos} |\n")
            f.write("\n")

    print(f"wrote {cn_md_path}")

    # Write JSON sidecar (used by generator.py)
    json_path = STRINGS_DIR / "cn.json"
    cn_dict = OrderedDict((e["key"], e["text"]) for e in all_entries)
    json_path.write_text(json.dumps(cn_dict, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    print(f"wrote {json_path}")

    # Write meta for PLACEHOLDER_MAP
    meta_path = DOCS_DIR / "_extraction_meta.json"
    meta = {
        "total": len(all_entries),
        "by_area": {a: len(v) for a, v in by_area.items()},
        "entries": all_entries,
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    print(f"wrote {meta_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
