#!/usr/bin/env python3
"""
阶段 1 v2 母版占位符提取器（实施 G1 review 3 项改动）。

输入：`master_unpacked/`（由官方 unpack.py --merge-runs false 解出的 W50 原始 XML）
输出（覆盖输入 + 旁出文件）：
  master_unpacked/word/document.xml + footer*.xml ← 占位符化版（含拆 w:t / 品牌字面化）
  strings/cn.md, strings/cn.json
  docs/_extraction_meta.json

v2 三项改动（G1 review FAIL 后大 boss 决定）：
  改动 1：品牌名"威富可" → 直接字面值 "Wevac"（所有 30 处，包含独立 + 嵌入）
          → cn.json 不再有 brand placeholder；所有语言版本统一 "Wevac"
          → 副作用：CN docx 与 W50 baseline 视觉锚重建，已确认接受
  改动 2：中英混排（ASCII + CJK 在同一 <w:t> 内）→ 拆 <w:t> 节点
          → 不动 <w:r> / <w:rPr>；ASCII 部分作为字面值 <w:t>，CJK 部分作为独立 placeholder
          → 拆完后 OOXML 仍合法（一个 <w:r> 可含多个 <w:t> 节点）
  改动 3：safety 下预切 3 个 subarea：warning / caution / notice
          → p3 → safety_warning_*
          → p4 中 NOTICE box-title 之前 → safety_caution_*
          → p4 中 NOTICE box-title 起 → safety_notice_*

不动的：
  - <w:r> 结构（不合并、不拆 run）
  - <w:rPr>（不改 run 格式）
  - 纯 ASCII <w:t>（型号 / 单位 / 数字单独成节点的 — 不动）
  - 纯 CJK 不含 ASCII 的 <w:t> — 整段替换为单个 placeholder（与 v1 一致）

Key 命名：<area>_[subarea_]<seq>
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

# CJK 字符范围（含 CJK 标点 / 全角符号）
CHINESE_RE = re.compile(r"[一-鿿　-〿＀-￯]")
# 匹配简单 <w:t>...</w:t>（不允许嵌套）
WT_RE = re.compile(r"(<w:t(?:\s[^>]*)?>)([^<]*)(</w:t>)")

# 品牌字面化（改动 1）
BRAND_CN = "威富可"
BRAND_EN = "Wevac"

# NOTICE 框 box-title 文本（改动 3 切换点）
NOTICE_TITLE = "提示 NOTICE"

# 页 → area / subarea 默认映射
PAGE_AREA = {
    1: ("cover", None),
    2: ("toc", None),
    3: ("safety", "warning"),
    4: ("safety", "caution"),    # p4 中遇到 NOTICE box-title 之后切到 "notice"
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


def split_mixed(s: str) -> list[tuple[str, str]]:
    """将含 ASCII + CJK 混排的字符串切成交替的 chunk 列表。

    返回 [(kind, text), ...]，kind ∈ {'cjk', 'ascii'}。
    - CJK 字符（含 CJK 标点 / 全角符号）→ 'cjk'
    - 其他非空白 → 'ascii'
    - 空白 → 附着到当前 chunk；若起始为空白则附给后续第一个非空白 chunk
    - 末尾仅有空白则附给上一个 chunk
    """
    if not s:
        return []
    chunks: list[tuple[str, str]] = []
    cur_kind: str | None = None
    cur_text = ""
    for c in s:
        if c.isspace():
            cur_text += c
        else:
            kind = "cjk" if CHINESE_RE.match(c) else "ascii"
            if cur_kind is None:
                cur_kind = kind
                cur_text += c
            elif kind == cur_kind:
                cur_text += c
            else:
                chunks.append((cur_kind, cur_text))
                cur_kind = kind
                cur_text = c
    if cur_text:
        if cur_kind is None and chunks:
            kp, tp = chunks[-1]
            chunks[-1] = (kp, tp + cur_text)
        elif cur_kind is not None:
            chunks.append((cur_kind, cur_text))
    return chunks


def has_brand(text: str) -> bool:
    return BRAND_CN in text


def needs_whitespace_attr(text: str) -> bool:
    """是否需要 xml:space=\"preserve\"（含前/后空格 或 含 tab/换行）。"""
    return text != text.strip() or "\t" in text or "\n" in text


def emit_wt(text: str, is_literal: bool = False, key: str | None = None) -> str:
    """组装一个新 <w:t> 节点字符串（无 rPr，由外层 <w:r> 提供）。

    - is_literal=True：text 作为字面值
    - is_literal=False：text 是 placeholder key 字符串（如 cover_3），输出 `{{cover_3}}`
    """
    body = text if is_literal else f"{{{{{key or text}}}}}"
    if is_literal:
        if needs_whitespace_attr(body):
            return f'<w:t xml:space="preserve">{body}</w:t>'
        return f"<w:t>{body}</w:t>"
    # placeholder 通常不含前后空白，但 placeholder body 是 `{{key}}` 不含空白
    return f"<w:t>{body}</w:t>"


def replace_wt_in_text(
    xml: str,
    classify_fn,
    entries: list[dict],
    seq_counter: dict[str, int],
    source_name: str,
    split_stats: dict[str, int],
) -> str:
    """通用 <w:t> 替换。

    对每个 <w:t>:
      1. 先把 "威富可" 替换为 "Wevac"（改动 1）
      2. 若内容不含 CJK → 不动（保持字面）
      3. 若内容仅 CJK（不含 ASCII）→ 整段作为单个 placeholder
      4. 若 CJK + ASCII 混排 → 调 split_mixed 拆成交替 chunk，emit 多个 <w:t>
    """

    def replace(m: re.Match) -> str:
        open_tag, content, close_tag = m.group(1), m.group(2), m.group(3)
        pos = m.start()

        # 改动 1：先做品牌字面化（在文本层；这样后续判定基于改后的文本）
        if has_brand(content):
            content = content.replace(BRAND_CN, BRAND_EN)
            split_stats["brand_replaced_occurrences"] += content.count(BRAND_EN) - 0  # report count
            # 注：单 <w:t> 内可能有多个"威富可"，但 W50 实际只有 1 处含多次的情况
            split_stats["brand_wt_touched"] += 1

        if not CHINESE_RE.search(content):
            # 全 ASCII（含字面 "Wevac"）→ 重写为合法 <w:t>（可能 content 比原来短 — 含 brand 替换）
            # 必要时加 xml:space=preserve
            new_open = open_tag
            if needs_whitespace_attr(content) and "xml:space" not in open_tag:
                new_open = open_tag[:-1] + ' xml:space="preserve">'
            return f"{new_open}{content}{close_tag}"

        # 含 CJK
        # 判断 mixed
        has_ascii = bool(re.search(r"[^　-〿一-鿿＀-￯\s]", content))
        if not has_ascii:
            # 纯 CJK（可能含 CJK 标点 / 空白）→ 单 placeholder
            area, subarea = classify_fn(pos, content)
            prefix = f"{area}_{subarea}" if subarea else area
            seq_counter[prefix] += 1
            key = f"{prefix}_{seq_counter[prefix]}"
            entries.append({
                "key": key,
                "text": content,
                "page": _last_page_for_pos(pos),
                "area": area,
                "subarea": subarea or "",
                "source": source_name,
                "offset": pos,
                "split": False,
            })
            new_open = open_tag
            if "xml:space" not in open_tag and content != content.strip():
                new_open = open_tag[:-1] + ' xml:space="preserve">'
            return f"{new_open}{{{{{key}}}}}{close_tag}"

        # 混排 → 拆 <w:t>（改动 2）
        split_stats["wt_split_count"] += 1
        chunks = split_mixed(content)
        out_parts: list[str] = []
        for kind, text in chunks:
            if kind == "ascii":
                # 字面 <w:t>
                if needs_whitespace_attr(text):
                    out_parts.append(f'<w:t xml:space="preserve">{text}</w:t>')
                else:
                    out_parts.append(f"<w:t>{text}</w:t>")
            else:
                # CJK chunk → placeholder
                area, subarea = classify_fn(pos, text)
                prefix = f"{area}_{subarea}" if subarea else area
                seq_counter[prefix] += 1
                key = f"{prefix}_{seq_counter[prefix]}"
                entries.append({
                    "key": key,
                    "text": text,
                    "page": _last_page_for_pos(pos),
                    "area": area,
                    "subarea": subarea or "",
                    "source": source_name,
                    "offset": pos,
                    "split": True,
                    "chunk_kind": "cjk",
                    "split_origin_text": content,
                })
                if text != text.strip():
                    out_parts.append(f'<w:t xml:space="preserve">{{{{{key}}}}}</w:t>')
                else:
                    out_parts.append(f"<w:t>{{{{{key}}}}}</w:t>")
        return "".join(out_parts)

    return WT_RE.sub(replace, xml)


# 模块级辅助 — 用作 classify_fn 的副信息
_SECT_POSITIONS: list[int] = []
_NOTICE_PIVOT_POS: int = -1


def _last_page_for_pos(pos: int) -> int:
    return assign_page(pos, _SECT_POSITIONS)


def make_document_classifier():
    """document.xml 用：基于 pos 判定 page → area/subarea；p4 中处理 notice 切换。"""

    def classify(pos: int, content: str) -> tuple[str, str | None]:
        page = assign_page(pos, _SECT_POSITIONS)
        area, subarea = PAGE_AREA[page]
        if page == 4 and _NOTICE_PIVOT_POS >= 0 and pos >= _NOTICE_PIVOT_POS:
            subarea = "notice"
        return area, subarea

    return classify


def process_document(xml: str, entries: list[dict], seq_counter: dict[str, int],
                    split_stats: dict[str, int]) -> str:
    global _SECT_POSITIONS, _NOTICE_PIVOT_POS
    _SECT_POSITIONS = [m.start() for m in re.finditer(r"<w:sectPr", xml)]
    if len(_SECT_POSITIONS) != 15:
        raise RuntimeError(f"expected 15 sectPr, got {len(_SECT_POSITIONS)}")

    # 改动 3：找 p4 范围内的 NOTICE box-title 起始位置（即 <w:t>提示 NOTICE</w:t> 的 <w:t> 起点）
    # p4 范围 [sect_positions[2], sect_positions[3])
    p4_start, p4_end = _SECT_POSITIONS[2], _SECT_POSITIONS[3]
    _NOTICE_PIVOT_POS = -1
    for m in WT_RE.finditer(xml):
        if not (p4_start <= m.start() < p4_end):
            continue
        if m.group(2).strip() == NOTICE_TITLE:
            _NOTICE_PIVOT_POS = m.start()
            break
    if _NOTICE_PIVOT_POS < 0:
        print("WARN: p4 NOTICE box-title not found; safety_notice subarea will be empty",
              file=sys.stderr)

    classify_fn = make_document_classifier()
    return replace_wt_in_text(
        xml, classify_fn, entries, seq_counter, "document.xml", split_stats
    )


def process_footer(xml: str, footer_idx: int, entries: list[dict],
                   seq_counter: dict[str, int], split_stats: dict[str, int]) -> str:
    """Footer 全部归 area='footer'。"""

    def classify(pos: int, content: str) -> tuple[str, str | None]:
        return "footer", None

    # footer 没有 sectPr — 用 footer_idx 当 "page"
    global _SECT_POSITIONS
    _SECT_POSITIONS = []  # not used for footer page; we'll patch _last_page_for_pos

    # override page-for-pos by patching the entries after the fact
    pre_len = len(entries)
    result = replace_wt_in_text(
        xml, classify, entries, seq_counter, f"footer{footer_idx}.xml", split_stats
    )
    for e in entries[pre_len:]:
        e["page"] = footer_idx
    return result


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    STRINGS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    entries: list[dict] = []
    seq_counter: dict[str, int] = defaultdict(int)
    split_stats = {
        "wt_split_count": 0,            # 因混排被拆的 <w:t> 数（每个原始 <w:t> 计 1）
        "brand_wt_touched": 0,           # 含 "威富可" 的 <w:t> 数（被字面化）
        "brand_replaced_occurrences": 0, # 字面化的总 "威富可" 出现次数（≥ touched）
    }

    # document.xml
    doc_path = MASTER / "word" / "document.xml"
    xml = doc_path.read_text(encoding="utf-8")
    new_xml = process_document(xml, entries, seq_counter, split_stats)
    doc_path.write_text(new_xml, encoding="utf-8")
    n_doc_entries = len(entries)
    print(f"document.xml: {n_doc_entries} placeholders")
    print(f"  NOTICE pivot pos = {_NOTICE_PIVOT_POS}")

    # Footers（1..15；footer1 通常为空）
    for i in range(1, 16):
        fp = MASTER / "word" / f"footer{i}.xml"
        if not fp.exists():
            continue
        fxml = fp.read_text(encoding="utf-8")
        before_n = len(entries)
        new_fxml = process_footer(fxml, i, entries, seq_counter, split_stats)
        added = len(entries) - before_n
        if added > 0 or BRAND_CN in fxml:
            fp.write_text(new_fxml, encoding="utf-8")
        if added > 0:
            print(f"footer{i}.xml: {added} placeholders")

    print(f"total placeholders: {len(entries)}")
    print(f"split stats: wt_split={split_stats['wt_split_count']} "
          f"brand_wt={split_stats['brand_wt_touched']} "
          f"brand_occ={split_stats['brand_replaced_occurrences']}")

    # 校验：master_unpacked 中已无 "威富可" 子串
    for fp in (MASTER / "word").glob("*.xml"):
        content = fp.read_text(encoding="utf-8")
        if BRAND_CN in content:
            print(f"ERROR: 威富可 still present in {fp.name}", file=sys.stderr)
            return 2

    # 校验：cn.json values 不含"威富可"
    cn_dict = OrderedDict((e["key"], e["text"]) for e in entries)
    for k, v in cn_dict.items():
        if BRAND_CN in v:
            print(f"ERROR: 威富可 in cn value {k}={v}", file=sys.stderr)
            return 2

    # Group by area for cn.md
    by_area: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_area[e["area"]].append(e)

    cn_md_path = STRINGS_DIR / "cn.md"
    with cn_md_path.open("w", encoding="utf-8") as f:
        f.write("# IMT050 中文翻译字典（v2）\n\n")
        f.write(f"> 总占位符数：{len(entries)}（来自 W50，v2 = v1 - 30 处 brand + 拆 w:t 新增）\n")
        f.write("> 来源：final/imt050-wevac-eu-cn.docx (W50)\n")
        f.write("> v2 改动：品牌字面化 + 中英混排拆 w:t + safety_notice subarea\n\n")
        area_order = ["cover", "toc", "safety", "install", "operate", "spec",
                      "troubleshoot", "clean", "warranty", "footer"]
        area_title = {
            "cover": "封面 (p1)",
            "toc": "目录 (p2)",
            "safety": "安全须知 (p3-p4，三 subarea：warning/caution/notice)",
            "install": "安装与准备 (p5, p13)",
            "operate": "操作指引（含产品结构、按键、操作步骤）(p6-p7, p9-p10)",
            "spec": "技术参数 (p8)",
            "troubleshoot": "故障排除 (p11)",
            "clean": "维护保养 (p12)",
            "warranty": "保修信息 (p14-p15)",
            "footer": "页脚（每页底部）",
        }
        for area in area_order:
            es = by_area.get(area, [])
            if not es:
                continue
            f.write(f"## {area_title.get(area, area)}\n\n")
            f.write("| Key | 中文文本 | 位置 |\n")
            f.write("|-----|----------|------|\n")
            for e in es:
                text_esc = e["text"].replace("|", "\\|").replace("\n", " ")
                pos = f"p{e['page']} {e['source']}"
                f.write(f"| {e['key']} | {text_esc} | {pos} |\n")
            f.write("\n")
    print(f"wrote {cn_md_path}")

    json_path = STRINGS_DIR / "cn.json"
    json_path.write_text(json.dumps(cn_dict, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    print(f"wrote {json_path}")

    # Meta for PLACEHOLDER_MAP
    meta_path = DOCS_DIR / "_extraction_meta.json"
    meta = {
        "version": "v2",
        "total": len(entries),
        "by_area": {a: len(v) for a, v in by_area.items()},
        "split_stats": split_stats,
        "notice_pivot_pos": _NOTICE_PIVOT_POS,
        "entries": entries,
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    print(f"wrote {meta_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
