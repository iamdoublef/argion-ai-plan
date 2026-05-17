"""Stack more onto iter-24 winner (F5+252->244+264->260 = 7.3507/10.90)."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


# Base winner: F5 + 252->244 + 264->260
def _apply_base_24(c: str) -> str:
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    return c4


def quad_24_plus_line_230_226(unpacked_dir: Path) -> int:
    """+line=230->226 (37 sites)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="230"')
    c2 = _apply_base_24(c)
    c3 = c2.replace('w:line="230"', 'w:line="226"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_24_plus_line_230_234(unpacked_dir: Path) -> int:
    """+line=230->234."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="230"')
    c2 = _apply_base_24(c)
    c3 = c2.replace('w:line="230"', 'w:line="234"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_24_plus_line_230_240(unpacked_dir: Path) -> int:
    """+line=230->240."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="230"')
    c2 = _apply_base_24(c)
    c3 = c2.replace('w:line="230"', 'w:line="240"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_24_plus_line_230_228(unpacked_dir: Path) -> int:
    """+line=230->228 (2-unit step)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="230"')
    c2 = _apply_base_24(c)
    c3 = c2.replace('w:line="230"', 'w:line="228"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_24_plus_line_230_232(unpacked_dir: Path) -> int:
    """+line=230->232."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="230"')
    c2 = _apply_base_24(c)
    c3 = c2.replace('w:line="230"', 'w:line="232"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_24_plus_after_80_70(unpacked_dir: Path) -> int:
    """+w:after=80->70."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="80"')
    c2 = _apply_base_24(c)
    c3 = c2.replace('w:after="80"', 'w:after="70"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_24_plus_after_80_90(unpacked_dir: Path) -> int:
    """+w:after=80->90."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="80"')
    c2 = _apply_base_24(c)
    c3 = c2.replace('w:after="80"', 'w:after="90"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_24_plus_before_80_70(unpacked_dir: Path) -> int:
    """+w:before=80->70 (10 sites)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:before="80"')
    c2 = _apply_base_24(c)
    c3 = c2.replace('w:before="80"', 'w:before="70"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_24_plus_before_80_90(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:before="80"')
    c2 = _apply_base_24(c)
    c3 = c2.replace('w:before="80"', 'w:before="90"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_24_plus_before_160_150(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:before="160"')
    c2 = _apply_base_24(c)
    c3 = c2.replace('w:before="160"', 'w:before="150"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_24_plus_before_160_170(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:before="160"')
    c2 = _apply_base_24(c)
    c3 = c2.replace('w:before="160"', 'w:before="170"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quad_24_plus_line_252_242(unpacked_dir: Path) -> int:
    """+ even more aggressive: 252->244 already, try 252->242."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="242"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    fp.write_text(c4, encoding="utf-8")
    return n


def quad_24_plus_line_264_258(unpacked_dir: Path) -> int:
    """264->258 (between 260 and 256)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="258"')
    fp.write_text(c4, encoding="utf-8")
    return n


# Try shifting the inner E5 even brighter beyond F5
def double_e5_to_fc_line_252_244_264_260(unpacked_dir: Path) -> int:
    """E5 -> FC (even lighter than F5) with line shifts."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="FCFCFC"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    fp.write_text(c4, encoding="utf-8")
    return n


def double_e5_to_f7_line_252_244_264_260(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F7F7F7"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    fp.write_text(c4, encoding="utf-8")
    return n


RECIPES = {
    "quad_24_plus_line_230_226": quad_24_plus_line_230_226,
    "quad_24_plus_line_230_234": quad_24_plus_line_230_234,
    "quad_24_plus_line_230_240": quad_24_plus_line_230_240,
    "quad_24_plus_line_230_228": quad_24_plus_line_230_228,
    "quad_24_plus_line_230_232": quad_24_plus_line_230_232,
    "quad_24_plus_after_80_70": quad_24_plus_after_80_70,
    "quad_24_plus_after_80_90": quad_24_plus_after_80_90,
    "quad_24_plus_before_80_70": quad_24_plus_before_80_70,
    "quad_24_plus_before_80_90": quad_24_plus_before_80_90,
    "quad_24_plus_before_160_150": quad_24_plus_before_160_150,
    "quad_24_plus_before_160_170": quad_24_plus_before_160_170,
    "quad_24_plus_line_252_242": quad_24_plus_line_252_242,
    "quad_24_plus_line_264_258": quad_24_plus_line_264_258,
    "double_e5_to_fc_line_252_244_264_260": double_e5_to_fc_line_252_244_264_260,
    "double_e5_to_f7_line_252_244_264_260": double_e5_to_f7_line_252_244_264_260,
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
