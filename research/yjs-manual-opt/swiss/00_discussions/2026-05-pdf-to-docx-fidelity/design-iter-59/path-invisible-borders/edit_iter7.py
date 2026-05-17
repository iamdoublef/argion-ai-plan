"""Stack onto iter-29 winner (F5+252->244+264->260+230->228 = 7.302/10.16)."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


# Base winner (iter-29): F5 + 252->244 + 264->260 + 230->228
def _apply_base_29(c: str) -> str:
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    return c5


def quin_29_plus_line_278_276(unpacked_dir: Path) -> int:
    """+ line=278 -> 276 (TITLE line, 45 sites)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    c2 = _apply_base_29(c)
    c3 = c2.replace('w:line="278"', 'w:line="276"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quin_29_plus_line_278_280(unpacked_dir: Path) -> int:
    """+ line=278 -> 280."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    c2 = _apply_base_29(c)
    c3 = c2.replace('w:line="278"', 'w:line="280"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quin_29_plus_after_27_to_24(unpacked_dir: Path) -> int:
    """+ w:after=27 -> 24 (37 sites)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="27"')
    c2 = _apply_base_29(c)
    c3 = c2.replace('w:after="27"', 'w:after="24"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quin_29_plus_line_240_238(unpacked_dir: Path) -> int:
    """+ line=240 -> 238 (the big 154-site cohort, mostly body)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="240"')
    c2 = _apply_base_29(c)
    c3 = c2.replace('w:line="240"', 'w:line="238"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quin_29_plus_line_240_242(unpacked_dir: Path) -> int:
    """+ line=240 -> 242."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="240"')
    c2 = _apply_base_29(c)
    c3 = c2.replace('w:line="240"', 'w:line="242"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quin_29_plus_line_278_274(unpacked_dir: Path) -> int:
    """+ line=278 -> 274 (more aggressive)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    c2 = _apply_base_29(c)
    c3 = c2.replace('w:line="278"', 'w:line="274"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quin_29_plus_line_271_269(unpacked_dir: Path) -> int:
    """+ line=271 -> 269 (banner)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="271"')
    c2 = _apply_base_29(c)
    c3 = c2.replace('w:line="271"', 'w:line="269"')
    fp.write_text(c3, encoding="utf-8")
    return n


def quin_29_plus_line_271_273(unpacked_dir: Path) -> int:
    """+ line=271 -> 273."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="271"')
    c2 = _apply_base_29(c)
    c3 = c2.replace('w:line="271"', 'w:line="273"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hex_29_with_278_276_and_278_274(unpacked_dir: Path) -> int:
    """Test both directions at once doesn't make sense — pick winner."""
    return 0


# Try line=230 even finer: stop at 228 might not be optimal — try 229
# (oh wait, line is integer; can't go finer than 1)
# Already 230->228; try 230->227
def quin_29_minus_line_230_to_227(unpacked_dir: Path) -> int:
    """Replace base 228 with 227 (one step more aggressive)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="230"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="227"')
    fp.write_text(c5, encoding="utf-8")
    return n


def quin_29_plus_line_230_229(unpacked_dir: Path) -> int:
    """Replace 228 with 229 (one step less aggressive)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="230"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="229"')
    fp.write_text(c5, encoding="utf-8")
    return n


# Try also tweaking the inner E5 to F7 instead of F5 with iter-29 base
def quin_29_with_e5_to_f7(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F7F7F7"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    fp.write_text(c5, encoding="utf-8")
    return n


def quin_29_with_e5_to_fa(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="FAFAFA"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    fp.write_text(c5, encoding="utf-8")
    return n


def quin_29_with_e5_to_ec(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="ECECEC"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    fp.write_text(c5, encoding="utf-8")
    return n


RECIPES = {
    "quin_29_plus_line_278_276": quin_29_plus_line_278_276,
    "quin_29_plus_line_278_280": quin_29_plus_line_278_280,
    "quin_29_plus_after_27_to_24": quin_29_plus_after_27_to_24,
    "quin_29_plus_line_240_238": quin_29_plus_line_240_238,
    "quin_29_plus_line_240_242": quin_29_plus_line_240_242,
    "quin_29_plus_line_278_274": quin_29_plus_line_278_274,
    "quin_29_plus_line_271_269": quin_29_plus_line_271_269,
    "quin_29_plus_line_271_273": quin_29_plus_line_271_273,
    "quin_29_minus_line_230_to_227": quin_29_minus_line_230_to_227,
    "quin_29_plus_line_230_229": quin_29_plus_line_230_229,
    "quin_29_with_e5_to_f7": quin_29_with_e5_to_f7,
    "quin_29_with_e5_to_fa": quin_29_with_e5_to_fa,
    "quin_29_with_e5_to_ec": quin_29_with_e5_to_ec,
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
