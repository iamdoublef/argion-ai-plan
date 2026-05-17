#!/usr/bin/env python3
"""
占位符替换器：
  python generator.py --lang cn --output round_trip_cn.docx

读 strings/{lang}.json，把 master_unpacked 中所有 {{key}} 替换为对应译文，
再用官方 docx skill 的 pack.py 打包成 docx。

参数：
  --lang {cn,en,de,it,gb,hk,tw}
  --output <output_docx_path>      默认 output/imt050-wevac-eu-{lang}.docx
  --master-unpacked <dir>          默认 master_unpacked/
  --strings <file>                 默认 strings/{lang}.json
  --validate                       打包后跑 validate.py
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OFFICE_SCRIPTS = Path(r"C:/Users/iamdo/.claude/skills/docx/scripts/office")
PACK_PY = OFFICE_SCRIPTS / "pack.py"
VALIDATE_PY = OFFICE_SCRIPTS / "validate.py"

# Match {{key}} with key as word chars (letters/digits/_)
PLACEHOLDER_RE = re.compile(r"\{\{([A-Za-z0-9_]+)\}\}")


def xml_escape(s: str) -> str:
    """Escape characters that need encoding inside <w:t>."""
    # We must NOT double-escape entities that already exist (the source W50
    # contains literal `&quot;` etc.). The placeholder is the ONLY thing being
    # replaced; the strings/cn.json values come straight from the original
    # w:t innerText (which still contains the original entities like
    # `&#x201C;` / `&quot;` since extract_master.py reads the raw XML).
    # So we leave them alone.
    return s


def replace_placeholders(xml: str, strings: dict[str, str], missing: list[str]) -> tuple[str, int]:
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        key = m.group(1)
        if key not in strings:
            missing.append(key)
            return m.group(0)
        n += 1
        return xml_escape(strings[key])

    new = PLACEHOLDER_RE.sub(repl, xml)
    return new, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", required=True)
    ap.add_argument("--output", default=None,
                    help="Output docx path (default output/imt050-wevac-eu-{lang}.docx)")
    ap.add_argument("--master-unpacked", default=str(ROOT / "master_unpacked"))
    ap.add_argument("--strings", default=None,
                    help="Strings JSON path (default strings/{lang}.json)")
    ap.add_argument("--validate", action="store_true",
                    help="Run validate.py on the packed result")
    args = ap.parse_args()

    lang = args.lang
    master = Path(args.master_unpacked)
    if not master.exists():
        print(f"ERROR: master_unpacked not found: {master}", file=sys.stderr)
        return 1

    strings_path = Path(args.strings) if args.strings else ROOT / "strings" / f"{lang}.json"
    if not strings_path.exists():
        print(f"ERROR: strings file not found: {strings_path}", file=sys.stderr)
        return 1
    strings = json.loads(strings_path.read_text(encoding="utf-8"))

    output = Path(args.output) if args.output else ROOT / "output" / f"imt050-wevac-eu-{lang}.docx"
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f"docxgen_{lang}_") as tmp:
        work = Path(tmp) / "unpacked"
        shutil.copytree(master, work)

        word_dir = work / "word"
        missing: list[str] = []
        total_replaced = 0
        for xml_path in word_dir.glob("*.xml"):
            content = xml_path.read_text(encoding="utf-8")
            if "{{" not in content:
                continue
            new_content, n = replace_placeholders(content, strings, missing)
            if n > 0:
                xml_path.write_text(new_content, encoding="utf-8")
                total_replaced += n

        if missing:
            print(f"WARN: {len(set(missing))} missing keys (first 10): {sorted(set(missing))[:10]}",
                  file=sys.stderr)

        # Verify no residual placeholders
        residual: list[tuple[str, list[str]]] = []
        for xml_path in word_dir.glob("*.xml"):
            content = xml_path.read_text(encoding="utf-8")
            matches = PLACEHOLDER_RE.findall(content)
            if matches:
                residual.append((xml_path.name, sorted(set(matches))))
        if residual:
            print(f"ERROR: residual placeholders in {len(residual)} files:", file=sys.stderr)
            for fn, keys in residual:
                print(f"  {fn}: {keys[:10]}", file=sys.stderr)
            return 2

        print(f"replaced {total_replaced} placeholders → packing...")

        # Pack via official docx skill
        original = ROOT / "00_discussions_W50_ref.docx"
        original_arg = []
        # Try to find original W50 for validation comparison
        w50_path = (ROOT.parent.parent / "00_discussions" / "2026-05-pdf-to-docx-fidelity"
                    / "final" / "imt050-wevac-eu-cn.docx")
        if w50_path.exists():
            original_arg = ["--original", str(w50_path)]

        validate_flag = "true" if args.validate else "false"
        cmd = [sys.executable, str(PACK_PY),
               str(work), str(output),
               "--validate", validate_flag] + original_arg
        # Force UTF-8 mode for validate.py (which uses open() without encoding
        # on Windows and falls back to cp936/GBK on Chinese systems).
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        r = subprocess.run(cmd, capture_output=True, text=True, env=env,
                           encoding="utf-8", errors="replace")
        print(r.stdout)
        if r.stderr:
            print(r.stderr, file=sys.stderr)
        if r.returncode != 0:
            return r.returncode

    print(f"OK: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
