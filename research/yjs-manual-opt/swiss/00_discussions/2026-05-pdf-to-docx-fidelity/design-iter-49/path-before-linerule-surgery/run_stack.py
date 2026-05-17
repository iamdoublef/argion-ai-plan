"""Pack + score for iter-stack-w38 — uses W38 final as the original/baseline."""
import json
import os
import subprocess
import sys
from pathlib import Path

ENV = os.environ.copy()
ENV["PYTHONUTF8"] = "1"
ENV["PYTHONIOENCODING"] = "utf-8"

ROOT = Path(__file__).parent
DOCX_SKILL = Path(r"C:/Users/iamdo/.claude/skills/docx/scripts/office")
SCORE = ROOT.parent.parent / "score_candidate.py"
TARGET_PDF = ROOT.parent.parent.parent.parent / "output" / "imt050-wevac-eu-cn.pdf"
BASELINE_PNGS = ROOT.parent.parent / "baseline" / "target_png"
W38_DOCX = ROOT.parent.parent / "final" / "imt050-wevac-eu-cn.docx"


def run(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    out = iter_dir / "output.docx"

    if not unpacked.exists():
        print(f"ERROR: {unpacked} missing")
        return 1

    cmd = ["python", str(DOCX_SKILL / "pack.py"), str(unpacked), str(out),
           "--original", str(W38_DOCX)]
    r = subprocess.run(cmd, capture_output=True, text=True, env=ENV,
                       encoding="utf-8", errors="replace")
    print("PACK stdout:", (r.stdout or "")[-400:])
    print("PACK stderr:", (r.stderr or "")[-400:])
    if r.returncode != 0:
        return 1

    iter_env = ENV.copy()
    iter_env["LO_USER_PROFILE"] = str(iter_dir / "_lo_profile")
    cmd = ["python", str(SCORE), str(out),
           "--target", str(TARGET_PDF),
           "--baseline-pngs", str(BASELINE_PNGS)]
    r = subprocess.run(cmd, capture_output=True, text=True, env=iter_env,
                       encoding="utf-8", errors="replace")
    print("SCORE stdout:", r.stdout)
    if r.stderr:
        print("SCORE stderr:", r.stderr[-400:])

    score_json = out.with_suffix(".score.json")
    if score_json.exists():
        d = json.loads(score_json.read_text(encoding="utf-8"))
        v = d.get("visual", {})
        print(f"\n=== {iter_name} ===")
        print(f"mean: {v.get('overall_mean_diff')} max: {v.get('max_page_diff')}")
        print(f"per-page: {v.get('per_page_mean_diff')}")
        print(f"wt_count: {d['editability']['wt_count']}  text_ratio: {d['text']['ratio']}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(run(sys.argv[1]))
