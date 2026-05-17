"""Build a candidate docx from W29 baseline by applying per-page pgMar deltas.

Usage:
  python build_candidate.py <out_name> <spec_json>

spec_json format:
  {
    "1": {"top": 0, "right": 0, "bottom": 0, "left": 0, "header": 0, "footer": 0, "gutter": 0},
    "11": {"top": -1, "right": 2},
    ...
  }

Keys are page indices (1-based). Values are deltas (twips) to ADD to the existing W29 baseline value.
Missing pages are kept unchanged; missing keys default to 0.

Output: <out_name>.docx in current working directory.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UNPACKED = ROOT / "W29_unpacked"
PACK_TOOL = Path("C:/Users/iamdo/.claude/skills/docx/scripts/office/pack.py")

ATTR_ORDER = ["top", "right", "bottom", "left", "header", "footer", "gutter"]


def load_doc_xml() -> str:
    p = UNPACKED / "word" / "document.xml"
    return p.read_text(encoding="utf-8")


def write_doc_xml(text: str, target_dir: Path):
    p = target_dir / "word" / "document.xml"
    p.write_text(text, encoding="utf-8")


def patch_pgmar(content: str, delta_spec: dict) -> str:
    """Apply per-page pgMar deltas. Page indexing is 1-based, in document order."""
    pattern = re.compile(
        r'(<w:pgMar\s+w:top=")(\d+)("\s+w:right=")(\d+)("\s+w:bottom=")(\d+)("\s+w:left=")(\d+)("\s+w:header=")(\d+)("\s+w:footer=")(\d+)("\s+w:gutter=")(\d+)("/>)'
    )

    counter = {"page": 0}

    def repl(m):
        counter["page"] += 1
        page_idx = counter["page"]
        # values
        vals = {
            "top": int(m.group(2)),
            "right": int(m.group(4)),
            "bottom": int(m.group(6)),
            "left": int(m.group(8)),
            "header": int(m.group(10)),
            "footer": int(m.group(12)),
            "gutter": int(m.group(14)),
        }
        deltas = delta_spec.get(str(page_idx), {})
        for k, dv in deltas.items():
            if k in vals:
                vals[k] = vals[k] + dv
                if vals[k] < 0:
                    vals[k] = 0  # safety floor
        return (
            f'<w:pgMar w:top="{vals["top"]}" w:right="{vals["right"]}" '
            f'w:bottom="{vals["bottom"]}" w:left="{vals["left"]}" '
            f'w:header="{vals["header"]}" w:footer="{vals["footer"]}" '
            f'w:gutter="{vals["gutter"]}"/>'
        )

    new_content, n = pattern.subn(repl, content)
    if n != 15:
        raise RuntimeError(f"Expected 15 pgMar matches; got {n}")
    return new_content


def main():
    if len(sys.argv) < 3:
        print("usage: build_candidate.py <out_name> <spec_json_or_file>")
        sys.exit(1)
    out_name = sys.argv[1]
    spec_arg = sys.argv[2]
    spec_path = Path(spec_arg)
    if spec_path.exists():
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    else:
        spec = json.loads(spec_arg)

    # Stage a fresh copy of the W29 unpacked tree
    staging = ROOT / f"_stage_{out_name}"
    if staging.exists():
        shutil.rmtree(staging)
    shutil.copytree(UNPACKED, staging)

    content = (staging / "word" / "document.xml").read_text(encoding="utf-8")
    new_content = patch_pgmar(content, spec)
    (staging / "word" / "document.xml").write_text(new_content, encoding="utf-8")

    out_docx = ROOT / f"{out_name}.docx"
    if out_docx.exists():
        out_docx.unlink()
    # pack
    cmd = ["python", str(PACK_TOOL), str(staging), str(out_docx)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        sys.exit(1)
    print(f"Built {out_docx.name}")
    # cleanup staging
    shutil.rmtree(staging, ignore_errors=True)


if __name__ == "__main__":
    main()
