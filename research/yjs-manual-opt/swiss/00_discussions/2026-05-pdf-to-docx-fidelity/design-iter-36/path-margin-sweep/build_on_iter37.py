"""Build candidate from iter37/iter-9 baseline (8.54/12.24) with per-page pgMar deltas."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UNPACKED = ROOT / "iter37_iter9_unpacked"
PACK_TOOL = Path("C:/Users/iamdo/.claude/skills/docx/scripts/office/pack.py")


def patch_pgmar(content: str, delta_spec: dict) -> str:
    pattern = re.compile(
        r'(<w:pgMar\s+w:top=")(\d+)("\s+w:right=")(\d+)("\s+w:bottom=")(\d+)("\s+w:left=")(\d+)("\s+w:header=")(\d+)("\s+w:footer=")(\d+)("\s+w:gutter=")(\d+)("/>)'
    )
    counter = {"page": 0}

    def repl(m):
        counter["page"] += 1
        page_idx = counter["page"]
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
                vals[k] = max(vals[k] + dv, 0)
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
        print("usage: build_on_iter37.py <out_name> <spec_json>")
        sys.exit(1)
    out_name = sys.argv[1]
    spec_arg = sys.argv[2]
    if Path(spec_arg).exists():
        spec = json.loads(Path(spec_arg).read_text(encoding="utf-8"))
    else:
        spec = json.loads(spec_arg)
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
    cmd = ["python", str(PACK_TOOL), str(staging), str(out_docx)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        sys.exit(1)
    print(f"Built {out_docx.name}")
    shutil.rmtree(staging, ignore_errors=True)


if __name__ == "__main__":
    main()
