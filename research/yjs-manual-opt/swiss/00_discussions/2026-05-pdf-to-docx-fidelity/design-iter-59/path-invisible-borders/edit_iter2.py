"""Additional lever variants for iter-59."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


def doc_inner_e5_to_f0(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    fp.write_text(c.replace('w:color="E5E5E5"', 'w:color="F0F0F0"'), encoding="utf-8")
    return n


def doc_inner_e5_to_f5(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    fp.write_text(c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"'), encoding="utf-8")
    return n


def doc_inner_e5_to_ee(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    fp.write_text(c.replace('w:color="E5E5E5"', 'w:color="EEEEEE"'), encoding="utf-8")
    return n


def doc_inner_e5_to_fa(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    fp.write_text(c.replace('w:color="E5E5E5"', 'w:color="FAFAFA"'), encoding="utf-8")
    return n


def doc_inner_e5_to_ff(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    fp.write_text(c.replace('w:color="E5E5E5"', 'w:color="FFFFFF"'), encoding="utf-8")
    return n


def doc_line_271_to_240(unpacked_dir: Path) -> int:
    """Banner sz=271 -> 240 (normalize to body)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="271"')
    fp.write_text(c.replace('w:line="271"', 'w:line="240"'), encoding="utf-8")
    return n


def doc_line_271_to_250(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="271"')
    fp.write_text(c.replace('w:line="271"', 'w:line="250"'), encoding="utf-8")
    return n


def doc_line_278_to_240(unpacked_dir: Path) -> int:
    """Big jump: 278 -> 240 (body line standardization)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    fp.write_text(c.replace('w:line="278"', 'w:line="240"'), encoding="utf-8")
    return n


def doc_after_120_to_100(unpacked_dir: Path) -> int:
    """w:after=120 (23 sites)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="120"')
    fp.write_text(c.replace('w:after="120"', 'w:after="100"'), encoding="utf-8")
    return n


def doc_after_120_to_140(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="120"')
    fp.write_text(c.replace('w:after="120"', 'w:after="140"'), encoding="utf-8")
    return n


def doc_after_120_to_80(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="120"')
    fp.write_text(c.replace('w:after="120"', 'w:after="80"'), encoding="utf-8")
    return n


def doc_after_176_to_150(unpacked_dir: Path) -> int:
    """w:after=176 (13 sites)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="176"')
    fp.write_text(c.replace('w:after="176"', 'w:after="150"'), encoding="utf-8")
    return n


def doc_after_176_to_200(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="176"')
    fp.write_text(c.replace('w:after="176"', 'w:after="200"'), encoding="utf-8")
    return n


def doc_after_40_to_50(unpacked_dir: Path) -> int:
    """w:after=40 (22 sites)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="40"')
    fp.write_text(c.replace('w:after="40"', 'w:after="50"'), encoding="utf-8")
    return n


def doc_after_40_to_30(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="40"')
    fp.write_text(c.replace('w:after="40"', 'w:after="30"'), encoding="utf-8")
    return n


# Theme color cohorts: look for w:color="404040" cohorts (text), or others
def doc_color_404040_to_303030(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:val="404040"')
    fp.write_text(c.replace('w:val="404040"', 'w:val="303030"'), encoding="utf-8")
    return n


def doc_color_404040_to_555555(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:val="404040"')
    fp.write_text(c.replace('w:val="404040"', 'w:val="555555"'), encoding="utf-8")
    return n


def doc_color_404040_to_000(unpacked_dir: Path) -> int:
    """Test if 404040 is supposed to be 000000."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:val="404040"')
    fp.write_text(c.replace('w:val="404040"', 'w:val="000000"'), encoding="utf-8")
    return n


# Combine: EC + EB are TIE — let me stack with a SECOND lever
def stack_e5_to_eb_plus_top_sz12_red_sz8(unpacked_dir: Path) -> int:
    """Stack inner E5->EB with top sz=12 red -> sz=8."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n1 = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="EBEBEB"')
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")12(" w:space="\d+" w:color="E63846")',
        r'\g<1>8\g<2>',
        c2
    )
    fp.write_text(new, encoding="utf-8")
    return n1


RECIPES = {
    "doc_inner_e5_to_f0": doc_inner_e5_to_f0,
    "doc_inner_e5_to_f5": doc_inner_e5_to_f5,
    "doc_inner_e5_to_ee": doc_inner_e5_to_ee,
    "doc_inner_e5_to_fa": doc_inner_e5_to_fa,
    "doc_inner_e5_to_ff": doc_inner_e5_to_ff,
    "doc_line_271_to_240": doc_line_271_to_240,
    "doc_line_271_to_250": doc_line_271_to_250,
    "doc_line_278_to_240": doc_line_278_to_240,
    "doc_after_120_to_100": doc_after_120_to_100,
    "doc_after_120_to_140": doc_after_120_to_140,
    "doc_after_120_to_80": doc_after_120_to_80,
    "doc_after_176_to_150": doc_after_176_to_150,
    "doc_after_176_to_200": doc_after_176_to_200,
    "doc_after_40_to_50": doc_after_40_to_50,
    "doc_after_40_to_30": doc_after_40_to_30,
    "doc_color_404040_to_303030": doc_color_404040_to_303030,
    "doc_color_404040_to_555555": doc_color_404040_to_555555,
    "doc_color_404040_to_000": doc_color_404040_to_000,
    "stack_e5_to_eb_plus_top_sz12_red_sz8": stack_e5_to_eb_plus_top_sz12_red_sz8,
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
