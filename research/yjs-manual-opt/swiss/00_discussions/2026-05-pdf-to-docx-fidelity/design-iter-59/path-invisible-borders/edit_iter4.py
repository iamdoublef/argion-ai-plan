"""Triple/quad-stack iter-17/16 winners with more combinations."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


def triple_e5_f5_line_252_248_line_264_260(unpacked_dir: Path) -> int:
    """F5 + line=252->248 + line=264->260 (combine 16+17)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="248"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    fp.write_text(c4, encoding="utf-8")
    return n


def triple_e5_f5_line_252_256_line_264_260(unpacked_dir: Path) -> int:
    """F5 + line=252->256 + line=264->260."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="256"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    fp.write_text(c4, encoding="utf-8")
    return n


def triple_e5_f5_line_252_248_line_264_268(unpacked_dir: Path) -> int:
    """F5 + line=252->248 + line=264->268 (opposite direction for 264)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="248"')
    c4 = c3.replace('w:line="264"', 'w:line="268"')
    fp.write_text(c4, encoding="utf-8")
    return n


def quad_e5_f5_line_252_248_line_271_268_line_264_260(unpacked_dir: Path) -> int:
    """F5 + line=252->248 + line=271->268 + line=264->260."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="248"')
    c4 = c3.replace('w:line="271"', 'w:line="268"')
    c5 = c4.replace('w:line="264"', 'w:line="260"')
    fp.write_text(c5, encoding="utf-8")
    return n


def double_e5_f5_line_252_244(unpacked_dir: Path) -> int:
    """F5 + line=252->244 (more aggressive)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    fp.write_text(c3, encoding="utf-8")
    return n


def double_e5_f5_line_252_240(unpacked_dir: Path) -> int:
    """F5 + line=252->240 (body line norm)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="240"')
    fp.write_text(c3, encoding="utf-8")
    return n


def double_e5_f5_line_252_250(unpacked_dir: Path) -> int:
    """F5 + line=252->250 (small step)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="250"')
    fp.write_text(c3, encoding="utf-8")
    return n


# Explore tiny size/spacing differences
def stack_e5_to_f5_and_line_252_248_and_left_sz2_to_nil(unpacked_dir: Path) -> int:
    """F5 + line=252->248 + left red sz=2 -> nil (test if zero space recovery helps)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="248"')
    c4 = re.sub(
        r'<w:left w:val="single" w:sz="2" w:space="\d+" w:color="E63846"/>',
        r'<w:left w:val="nil"/>',
        c3
    )
    fp.write_text(c4, encoding="utf-8")
    return n


def stack_e5_to_f5_and_line_252_248_and_left_sz2_to_sz1(unpacked_dir: Path) -> int:
    """F5 + line=252->248 + left red sz=2 -> sz=1."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="248"')
    c4 = re.sub(
        r'(<w:left w:val="single" w:sz=")2(" w:space="\d+" w:color="E63846")',
        r'\g<1>1\g<2>',
        c3
    )
    fp.write_text(c4, encoding="utf-8")
    return n


RECIPES = {
    "triple_e5_f5_line_252_248_line_264_260": triple_e5_f5_line_252_248_line_264_260,
    "triple_e5_f5_line_252_256_line_264_260": triple_e5_f5_line_252_256_line_264_260,
    "triple_e5_f5_line_252_248_line_264_268": triple_e5_f5_line_252_248_line_264_268,
    "quad_e5_f5_line_252_248_line_271_268_line_264_260": quad_e5_f5_line_252_248_line_271_268_line_264_260,
    "double_e5_f5_line_252_244": double_e5_f5_line_252_244,
    "double_e5_f5_line_252_240": double_e5_f5_line_252_240,
    "double_e5_f5_line_252_250": double_e5_f5_line_252_250,
    "stack_e5_to_f5_and_line_252_248_and_left_sz2_to_nil": stack_e5_to_f5_and_line_252_248_and_left_sz2_to_nil,
    "stack_e5_to_f5_and_line_252_248_and_left_sz2_to_sz1": stack_e5_to_f5_and_line_252_248_and_left_sz2_to_sz1,
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
