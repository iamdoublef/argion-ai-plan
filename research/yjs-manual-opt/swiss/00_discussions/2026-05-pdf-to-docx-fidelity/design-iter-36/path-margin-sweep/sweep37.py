"""Sweep on iter-37 baseline."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCORE_TOOL = ROOT.parent.parent / "score_candidate.py"
TARGET_PDF = ROOT.parent.parent.parent.parent / "output" / "imt050-wevac-eu-cn.pdf"
BASELINE_PNG = ROOT.parent.parent / "baseline" / "target_png"


def build_and_score(name: str, spec: dict):
    r = subprocess.run(
        ["python", "build_on_iter37.py", name, json.dumps(spec)],
        capture_output=True, text=True, cwd=ROOT,
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    if r.returncode != 0:
        return {"name": name, "spec": spec, "error": "build_failed", "stderr": r.stderr}
    docx = ROOT / f"{name}.docx"
    r = subprocess.run(
        ["python", str(SCORE_TOOL), str(docx), "--target", str(TARGET_PDF),
         "--baseline-pngs", str(BASELINE_PNG)],
        capture_output=True, text=True, cwd=ROOT,
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    if r.returncode != 0:
        return {"name": name, "spec": spec, "error": "score_failed", "stderr": r.stderr}
    sj = ROOT / f"{name}.score.json"
    if not sj.exists():
        return {"name": name, "spec": spec, "error": "no_score_file"}
    data = json.loads(sj.read_text(encoding="utf-8"))
    visual = data.get("visual", {})
    return {
        "name": name,
        "spec": spec,
        "mean": visual.get("overall_mean_diff"),
        "max": visual.get("max_page_diff"),
        "per_page": visual.get("per_page_mean_diff"),
    }


def main():
    if len(sys.argv) < 3:
        print("usage: sweep37.py <round_name> <plan_json_file>")
        sys.exit(1)
    round_name = sys.argv[1]
    plan = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    results = []
    BASE_MEAN = 8.48
    BASE_MAX = 12.20
    for entry in plan:
        name = entry["name"]
        spec = entry["spec"]
        print(f"[run] {name}")
        result = build_and_score(name, spec)
        results.append(result)
        if "error" not in result:
            mean = result["mean"]; mx = result["max"]
            tag = ""
            if mean < BASE_MEAN or mx < BASE_MAX:
                tag = " *** IMPROVE"
            elif mean > BASE_MEAN + 0.05 or mx > BASE_MAX + 0.05:
                tag = " REGRESS"
            print(f"  -> mean={mean} (dM={mean-BASE_MEAN:+.2f}) max={mx} (dM={mx-BASE_MAX:+.2f}){tag}")
        else:
            print(f"  -> ERROR: {result.get('error')}")
    out = ROOT / f"{round_name}.results.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved {out.name}")


if __name__ == "__main__":
    main()
