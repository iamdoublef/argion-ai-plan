"""Stack on iter-38 = F5+252->244+264->260+230->228+271->273 = 7.28/10.16"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


def _apply_base_38(c: str) -> str:
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    c6 = c5.replace('w:line="271"', 'w:line="273"')
    return c6


def hept_38_plus_before_160_170(unpacked_dir: Path) -> int:
    """38 + before=160 -> 170."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:before="160"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:before="160"', 'w:before="170"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hept_38_plus_before_160_165(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:before="160"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:before="160"', 'w:before="165"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hept_38_plus_before_160_175(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:before="160"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:before="160"', 'w:before="175"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hept_38_plus_before_160_180(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:before="160"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:before="160"', 'w:before="180"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hept_38_plus_line_240_239(unpacked_dir: Path) -> int:
    """240->239 minimal step (154 sites)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="240"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:line="240"', 'w:line="239"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hept_38_plus_line_240_241(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="240"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:line="240"', 'w:line="241"')
    fp.write_text(c3, encoding="utf-8")
    return n


# Test: footer cohort (sz=10 spacing 2) — iter-58 said inert, but in new base?
def hept_38_plus_footer_spacing_2_to_1(unpacked_dir: Path) -> int:
    """Apply iter-38 base + footer sz=10 spacing 2 -> 1."""
    # Apply doc base
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    c2 = _apply_base_38(c)
    fp.write_text(c2, encoding="utf-8")
    # Footer
    total = 0
    for fpf in (unpacked_dir / "word").glob("footer*.xml"):
        c = fpf.read_text(encoding="utf-8")
        new_c = re.sub(
            r'(<w:sz w:val="10"/>[^<]*<w:color[^/]*/>[^<]*)<w:spacing w:val="2"/>',
            r'\1<w:spacing w:val="1"/>',
            c
        )
        n = c.count('<w:spacing w:val="2"/>') - new_c.count('<w:spacing w:val="2"/>')
        if n > 0:
            fpf.write_text(new_c, encoding="utf-8")
            total += n
    return total


def hept_38_plus_footer_spacing_2_to_3(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    c2 = _apply_base_38(c)
    fp.write_text(c2, encoding="utf-8")
    total = 0
    for fpf in (unpacked_dir / "word").glob("footer*.xml"):
        c = fpf.read_text(encoding="utf-8")
        new_c = re.sub(
            r'(<w:sz w:val="10"/>[^<]*<w:color[^/]*/>[^<]*)<w:spacing w:val="2"/>',
            r'\1<w:spacing w:val="3"/>',
            c
        )
        n = c.count('<w:spacing w:val="2"/>') - new_c.count('<w:spacing w:val="2"/>')
        if n > 0:
            fpf.write_text(new_c, encoding="utf-8")
            total += n
    return total


# Test p3 — but it's already at 10.03 (down from 10.90). Try p3-targeted: line=240 cohort in p3 area
# We can't easily isolate, but try targeted spacing-after surgery

# Banner Title cohort (line=278) — line is sensitive but try minimal 1-unit step
def hept_38_plus_line_278_279(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:line="278"', 'w:line="279"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hept_38_plus_line_278_277(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:line="278"', 'w:line="277"')
    fp.write_text(c3, encoding="utf-8")
    return n


# Test stripe shd shifts on iter-38 base
def hept_38_plus_shd_f1_to_f5(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:fill="F1F1F6"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:fill="F1F1F6"', 'w:fill="F5F5F5"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hept_38_plus_shd_f1_to_f0(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:fill="F1F1F6"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:fill="F1F1F6"', 'w:fill="F0F0F0"')
    fp.write_text(c3, encoding="utf-8")
    return n


RECIPES = {
    "hept_38_plus_before_160_170": hept_38_plus_before_160_170,
    "hept_38_plus_before_160_165": hept_38_plus_before_160_165,
    "hept_38_plus_before_160_175": hept_38_plus_before_160_175,
    "hept_38_plus_before_160_180": hept_38_plus_before_160_180,
    "hept_38_plus_line_240_239": hept_38_plus_line_240_239,
    "hept_38_plus_line_240_241": hept_38_plus_line_240_241,
    "hept_38_plus_footer_spacing_2_to_1": hept_38_plus_footer_spacing_2_to_1,
    "hept_38_plus_footer_spacing_2_to_3": hept_38_plus_footer_spacing_2_to_3,
    "hept_38_plus_line_278_279": hept_38_plus_line_278_279,
    "hept_38_plus_line_278_277": hept_38_plus_line_278_277,
    "hept_38_plus_shd_f1_to_f5": hept_38_plus_shd_f1_to_f5,
    "hept_38_plus_shd_f1_to_f0": hept_38_plus_shd_f1_to_f0,
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
