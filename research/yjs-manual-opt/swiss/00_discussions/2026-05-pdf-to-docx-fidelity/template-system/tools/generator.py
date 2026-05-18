"""
generator.py
============
读取 master/template_unpacked/ 的占位符化 OOXML 树 + strings/<lang>.json，
生成 output/<sku>-<brand>-<region>-<lang>.docx。

用法：
  python tools/generator.py --lang cn --sku imt050 --brand wevac --region eu

参数：
  --lang     必须，与 strings/<lang>.json 对应（cn / en / de / it / hk ...）
  --sku      必须，与 products/<sku>.json 对应（imt050 / imt060 ...）
  --brand    可选，默认 wevac（影响文件名）
  --region   可选，默认 eu（影响文件名）
  --out      可选，指定完整输出路径，覆盖自动命名

行为：
  1. 复制 master/template_unpacked 到 _build/<run_id>/unpacked
  2. 把 strings 文件中所有 {{key}} 在每个 XML part 中替换为对应的 lang 文本
     （未提供的 key 回退到 cn.json，保证不会破文档）
  3. products/<sku>.json 中的字段可覆盖具体 placeholder（用于跨 SKU 复用同一文本骨架）
  4. 调用官方 pack.py（不 validate）打包为 docx

所有路径都用绝对路径，可重复运行。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER_TEMPLATE = ROOT / "master" / "template_unpacked"
STRINGS_DIR = ROOT / "strings"
PRODUCTS_DIR = ROOT / "products"
OUTPUT_DIR = ROOT / "output"
BUILD_DIR = ROOT / "_build"

DOCX_SKILL = Path(r"C:\Users\iamdo\.claude\skills\docx")
PACK = DOCX_SKILL / "scripts" / "office" / "pack.py"
UNPACK = DOCX_SKILL / "scripts" / "office" / "unpack.py"
VALIDATE = DOCX_SKILL / "scripts" / "office" / "validate.py"

PLACEHOLDER_RE = re.compile(r"\{\{([A-Za-z0-9_]+)\}\}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def materialize(xml_text: str, mapping: dict[str, str]) -> str:
    """Replace every {{key}} with the corresponding value (XML-escaped)."""

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key in mapping:
            return xml_escape(mapping[key])
        # leave unknown placeholders intact (visible) so callers notice
        return match.group(0)

    return PLACEHOLDER_RE.sub(repl, xml_text)


def merge_mappings(*sources: dict[str, str]) -> dict[str, str]:
    """Right-most wins. Skips empty/missing values to preserve cn fallback."""
    merged: dict[str, str] = {}
    for src in sources:
        if not src:
            continue
        for key, val in src.items():
            if val is None:
                continue
            if isinstance(val, str) and val == "":
                # treat empty string as "use fallback"
                continue
            merged[key] = val
    return merged


def run(cmd: list[str]) -> None:
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    proc = subprocess.run(cmd, text=True, capture_output=True, env=env,
                          timeout=240)
    if proc.stdout:
        print(proc.stdout.rstrip())
    if proc.stderr:
        print(proc.stderr.rstrip(), file=sys.stderr)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def build(lang: str, sku: str, brand: str, region: str,
          out_path: Path | None = None) -> Path:
    if not MASTER_TEMPLATE.exists():
        raise FileNotFoundError(
            f"{MASTER_TEMPLATE} not found. Run tools/extract_strings.py first."
        )

    cn_path = STRINGS_DIR / "cn.json"
    if not cn_path.exists():
        raise FileNotFoundError(f"{cn_path} not found (run extract_strings).")
    cn = load_json(cn_path)

    lang_path = STRINGS_DIR / f"{lang}.json"
    if not lang_path.exists():
        raise FileNotFoundError(f"{lang_path} not found.")
    lang_strings = load_json(lang_path)

    sku_path = PRODUCTS_DIR / f"{sku}.json"
    sku_data: dict = {}
    if sku_path.exists():
        sku_data = load_json(sku_path)
    sku_strings = sku_data.get("strings", {}).get(lang, {})

    mapping = merge_mappings(cn, lang_strings, sku_strings)

    # Stage build folder
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    run_id = f"{sku}-{brand}-{region}-{lang}-{int(time.time() * 1000)}"
    stage = BUILD_DIR / run_id
    if stage.exists():
        shutil.rmtree(stage)
    shutil.copytree(MASTER_TEMPLATE, stage / "unpacked")

    unpacked = stage / "unpacked"
    word_dir = unpacked / "word"
    parts = [word_dir / "document.xml"]
    parts.extend(sorted(word_dir.glob("footer*.xml")))
    parts.extend(sorted(word_dir.glob("header*.xml")))

    for part in parts:
        if not part.exists():
            continue
        text = part.read_text(encoding="utf-8")
        new_text = materialize(text, mapping)
        part.write_text(new_text, encoding="utf-8")

    # Determine output path
    if out_path is None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = OUTPUT_DIR / f"{sku}-{brand}-{region}-{lang}.docx"
    out_path = out_path.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    run([
        sys.executable,
        str(PACK),
        str(unpacked),
        str(out_path),
        "--validate",
        "false",
    ])
    print(f"\n  -> {out_path}")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate localized DOCX from template.")
    parser.add_argument("--lang", required=True,
                        help="Language code (cn, en, de, it, hk, ...)")
    parser.add_argument("--sku", default="imt050",
                        help="Product SKU (default: imt050)")
    parser.add_argument("--brand", default="wevac",
                        help="Brand name (default: wevac)")
    parser.add_argument("--region", default="eu",
                        help="Region tag (default: eu)")
    parser.add_argument("--out", type=Path, default=None,
                        help="Explicit output path (override naming)")
    args = parser.parse_args()
    build(args.lang, args.sku, args.brand, args.region, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
