"""Generic runner: unpack baseline -> apply edit -> pack -> validate -> score.

Usage:
    python run_iter.py iter-N
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
BASELINE_UNPACKED = ROOT / "baseline_unpacked"
SCORE_SCRIPT = ROOT.parent.parent / "score_candidate.py"
TARGET_PDF = ROOT.parent.parent.parent.parent / "output" / "imt050-wevac-eu-cn.pdf"
BASELINE_PNGS = ROOT.parent.parent / "baseline" / "target_png"
OFFICE_BIN = Path(r"C:\Users\iamdo\.claude\skills\docx\scripts\office")
PACK = OFFICE_BIN / "pack.py"

env = os.environ.copy()
env["PYTHONUTF8"] = "1"
env["PYTHONIOENCODING"] = "utf-8"


def pack_validate_score(iter_name: str):
    iter_dir = ROOT / iter_name
    unpacked = iter_dir / "unpacked"
    output_docx = iter_dir / "output.docx"
    if output_docx.exists():
        output_docx.unlink()

    # Pack with validate
    r = subprocess.run(
        ["python", str(PACK), str(unpacked), str(output_docx)],
        env=env, capture_output=True, text=True,
    )
    print("PACK stdout:", r.stdout[-400:] if r.stdout else "")
    if r.returncode != 0:
        print("PACK stderr:", r.stderr)
        return r.returncode

    # Score
    r = subprocess.run(
        [
            "python", str(SCORE_SCRIPT), str(output_docx),
            "--target", str(TARGET_PDF),
            "--baseline-pngs", str(BASELINE_PNGS),
        ],
        env=env, capture_output=True, text=True,
    )
    print("SCORE stdout:", r.stdout[-800:] if r.stdout else "")
    if r.returncode != 0:
        print("SCORE stderr:", r.stderr[-400:])
    return r.returncode


if __name__ == "__main__":
    sys.exit(pack_validate_score(sys.argv[1]))
