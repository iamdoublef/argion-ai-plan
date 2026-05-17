"""Test cellMar levers on iter-56 base = 7.2767/10.16"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


def _apply_base_56(c: str) -> str:
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    c6 = c5.replace('w:line="271"', 'w:line="273"')
    c7 = c6.replace('w:before="160"', 'w:before="170"')
    return c7


# cellMar value=32 (168 sites) — try slight tweaks (probably top/bottom)
def oct_56_plus_cellmar_32_to_30(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    pat = '<w:top w:w="32" w:type="dxa"/>'
    pat_b = '<w:bottom w:w="32" w:type="dxa"/>'
    n = c.count(pat) + c.count(pat_b)
    c2 = _apply_base_56(c)
    c3 = c2.replace(pat, '<w:top w:w="30" w:type="dxa"/>')
    c4 = c3.replace(pat_b, '<w:bottom w:w="30" w:type="dxa"/>')
    fp.write_text(c4, encoding="utf-8")
    return n


def oct_56_plus_cellmar_32_to_34(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    pat = '<w:top w:w="32" w:type="dxa"/>'
    pat_b = '<w:bottom w:w="32" w:type="dxa"/>'
    n = c.count(pat) + c.count(pat_b)
    c2 = _apply_base_56(c)
    c3 = c2.replace(pat, '<w:top w:w="34" w:type="dxa"/>')
    c4 = c3.replace(pat_b, '<w:bottom w:w="34" w:type="dxa"/>')
    fp.write_text(c4, encoding="utf-8")
    return n


def oct_56_plus_cellmar_32_to_28(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    pat = '<w:top w:w="32" w:type="dxa"/>'
    pat_b = '<w:bottom w:w="32" w:type="dxa"/>'
    n = c.count(pat) + c.count(pat_b)
    c2 = _apply_base_56(c)
    c3 = c2.replace(pat, '<w:top w:w="28" w:type="dxa"/>')
    c4 = c3.replace(pat_b, '<w:bottom w:w="28" w:type="dxa"/>')
    fp.write_text(c4, encoding="utf-8")
    return n


def oct_56_plus_cellmar_36_to_34(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    pat = '<w:top w:w="36" w:type="dxa"/>'
    pat_b = '<w:bottom w:w="36" w:type="dxa"/>'
    n = c.count(pat) + c.count(pat_b)
    c2 = _apply_base_56(c)
    c3 = c2.replace(pat, '<w:top w:w="34" w:type="dxa"/>')
    c4 = c3.replace(pat_b, '<w:bottom w:w="34" w:type="dxa"/>')
    fp.write_text(c4, encoding="utf-8")
    return n


def oct_56_plus_cellmar_36_to_38(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    pat = '<w:top w:w="36" w:type="dxa"/>'
    pat_b = '<w:bottom w:w="36" w:type="dxa"/>'
    n = c.count(pat) + c.count(pat_b)
    c2 = _apply_base_56(c)
    c3 = c2.replace(pat, '<w:top w:w="38" w:type="dxa"/>')
    c4 = c3.replace(pat_b, '<w:bottom w:w="38" w:type="dxa"/>')
    fp.write_text(c4, encoding="utf-8")
    return n


# Try targeting only insideV cellMar at sz=2 left red borders — banners
def oct_56_plus_left_sz2_red_space_4_to_6(unpacked_dir: Path) -> int:
    """Banner left sz=2 red, w:space="4" -> "6"."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    pat = '<w:left w:val="single" w:sz="2" w:space="4" w:color="E63846"/>'
    rep = '<w:left w:val="single" w:sz="2" w:space="6" w:color="E63846"/>'
    n = c.count(pat)
    c2 = _apply_base_56(c)
    c3 = c2.replace(pat, rep)
    fp.write_text(c3, encoding="utf-8")
    return n


def oct_56_plus_left_sz2_red_space_4_to_2(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    pat = '<w:left w:val="single" w:sz="2" w:space="4" w:color="E63846"/>'
    rep = '<w:left w:val="single" w:sz="2" w:space="2" w:color="E63846"/>'
    n = c.count(pat)
    c2 = _apply_base_56(c)
    c3 = c2.replace(pat, rep)
    fp.write_text(c3, encoding="utf-8")
    return n


def oct_56_plus_left_sz2_red_space_4_to_0(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    pat = '<w:left w:val="single" w:sz="2" w:space="4" w:color="E63846"/>'
    rep = '<w:left w:val="single" w:sz="2" w:space="0" w:color="E63846"/>'
    n = c.count(pat)
    c2 = _apply_base_56(c)
    c3 = c2.replace(pat, rep)
    fp.write_text(c3, encoding="utf-8")
    return n


RECIPES = {
    "oct_56_plus_cellmar_32_to_30": oct_56_plus_cellmar_32_to_30,
    "oct_56_plus_cellmar_32_to_34": oct_56_plus_cellmar_32_to_34,
    "oct_56_plus_cellmar_32_to_28": oct_56_plus_cellmar_32_to_28,
    "oct_56_plus_cellmar_36_to_34": oct_56_plus_cellmar_36_to_34,
    "oct_56_plus_cellmar_36_to_38": oct_56_plus_cellmar_36_to_38,
    "oct_56_plus_left_sz2_red_space_4_to_6": oct_56_plus_left_sz2_red_space_4_to_6,
    "oct_56_plus_left_sz2_red_space_4_to_2": oct_56_plus_left_sz2_red_space_4_to_2,
    "oct_56_plus_left_sz2_red_space_4_to_0": oct_56_plus_left_sz2_red_space_4_to_0,
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
