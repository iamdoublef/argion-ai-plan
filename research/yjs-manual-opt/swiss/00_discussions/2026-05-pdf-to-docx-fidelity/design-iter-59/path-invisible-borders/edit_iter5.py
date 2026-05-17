"""More combinations exploring iter-22 (252->244) winner."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


def triple_f5_line_252_244_line_264_260(unpacked_dir: Path) -> int:
    """F5 + line=252->244 + line=264->260."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    fp.write_text(c4, encoding="utf-8")
    return n


def triple_f5_line_252_240_line_264_260(unpacked_dir: Path) -> int:
    """F5 + line=252->240 + line=264->260."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="240"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    fp.write_text(c4, encoding="utf-8")
    return n


def double_f5_line_252_236(unpacked_dir: Path) -> int:
    """F5 + line=252->236 (more aggressive)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="236"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_f5_252_244_264_260_271_268(unpacked_dir: Path) -> int:
    """F5 + 252->244 + 264->260 + 271->268."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="271"', 'w:line="268"')
    fp.write_text(c5, encoding="utf-8")
    return n


def triple_f5_252_244_264_256(unpacked_dir: Path) -> int:
    """F5 + 252->244 + 264->256 (more aggressive 264)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="256"')
    fp.write_text(c4, encoding="utf-8")
    return n


RECIPES = {
    "triple_f5_line_252_244_line_264_260": triple_f5_line_252_244_line_264_260,
    "triple_f5_line_252_240_line_264_260": triple_f5_line_252_240_line_264_260,
    "double_f5_line_252_236": double_f5_line_252_236,
    "quad_f5_252_244_264_260_271_268": quad_f5_252_244_264_260_271_268,
    "triple_f5_252_244_264_256": triple_f5_252_244_264_256,
}


def apply_recipe(iter_name: str, recipe, src_unpacked=None):
    iter_dir = ROOT / iter_name
    iter_dir.mkdir(exist_ok=True)
    out_unpacked = iter_dir / "unpacked"
    if out_unpacked.exists():
        shutil.rmtree(out_unpacked)
    shutil.copytree(src_unpacked or SRC_UNPACKED, out_unpacked)

    names = recipe if isinstance(recipe, list) else [recipe]
    print(f"Applying {iter_name} = {names}")
    total = 0
    for n in names:
        c = RECIPES[n](out_unpacked)
        print(f"  applied {n}: {c} sites")
        total += c
    print(f"Total {total} sites modified in {iter_name}")
    return total


if __name__ == "__main__":
    iter_name = sys.argv[1]
    recipe = sys.argv[2]
    if "," in recipe:
        recipe = recipe.split(",")
    apply_recipe(iter_name, recipe)
