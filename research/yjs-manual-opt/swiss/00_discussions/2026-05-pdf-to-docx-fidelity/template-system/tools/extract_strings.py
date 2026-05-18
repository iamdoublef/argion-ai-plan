"""
extract_strings.py
==================
从 W48 master/unpacked/ 解包目录中提取所有 <w:t> 文本节点，构建：

  master/template_unpacked/   占位符化的 OOXML（每个 <w:t>{{key}}</w:t>）
  strings/cn.json             原始中文文本（key → text）

key 命名约定：
  - document.xml          → document_NNN
  - footer<N>.xml         → footerNN_NNN（保留页号）

每个文本节点都会生成一个 placeholder，无论它在哪个 part，
generator.py 会按相同顺序回填。

可重复运行 — 会覆盖输出。
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "master"
UNPACKED = MASTER / "unpacked"
TEMPLATE = MASTER / "template_unpacked"
STRINGS = ROOT / "strings"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NSMAP = {"w": W_NS}


def normalize_key(part_name: str) -> str:
    """word/document.xml -> document; word/footer3.xml -> footer3."""
    stem = Path(part_name).stem
    return re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_") or "part"


def extract_part(xml_path: Path, prefix: str, out_path: Path,
                 strings: dict[str, str]) -> int:
    """Read xml_path, replace each <w:t> text with {{prefix_NNN}}, save out_path,
    populate strings dict. Returns number of placeholders generated."""
    parser = etree.XMLParser(remove_blank_text=False, recover=False)
    tree = etree.parse(str(xml_path), parser)

    nodes = tree.xpath(".//w:t", namespaces=NSMAP)
    count = 0
    for node in nodes:
        value = node.text or ""
        if value == "":
            # preserve empty <w:t/> as-is
            continue
        count += 1
        key = f"{prefix}_{count:03d}"
        strings[key] = value
        node.text = "{{" + key + "}}"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(str(out_path), encoding="utf-8", xml_declaration=True,
               standalone=False)
    return count


def main() -> int:
    if not UNPACKED.exists():
        print(f"ERROR: {UNPACKED} not found. Run unpack first.", file=sys.stderr)
        return 1

    # Mirror entire unpacked tree to template_unpacked
    if TEMPLATE.exists():
        shutil.rmtree(TEMPLATE)
    shutil.copytree(UNPACKED, TEMPLATE)

    STRINGS.mkdir(parents=True, exist_ok=True)
    strings: dict[str, str] = {}

    # Order: document.xml first (deterministic), then footer*.xml sorted by N
    word_dir = TEMPLATE / "word"
    targets: list[Path] = []
    doc_xml = word_dir / "document.xml"
    if doc_xml.exists():
        targets.append(doc_xml)
    footer_paths = sorted(word_dir.glob("footer*.xml"),
                          key=lambda p: int(re.search(r"\d+", p.stem).group(0)))
    targets.extend(footer_paths)

    summary: dict[str, int] = {}
    for path in targets:
        prefix = normalize_key(path.name)
        count = extract_part(path, prefix, path, strings)
        summary[path.name] = count
        print(f"  {path.name:20s}  {count:4d} placeholders")

    cn_path = STRINGS / "cn.json"
    cn_path.write_text(
        json.dumps(strings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\nTotal placeholders: {len(strings)}")
    print(f"Strings written to: {cn_path}")
    print(f"Template written to: {TEMPLATE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
