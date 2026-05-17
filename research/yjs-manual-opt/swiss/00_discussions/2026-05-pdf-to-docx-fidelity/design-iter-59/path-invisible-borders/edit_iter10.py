"""Stack on iter-56 = iter-38 + before=160->170 = 7.2767/10.16"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


def _apply_base_56(c: str) -> str:
    """iter-56 base."""
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    c6 = c5.replace('w:line="271"', 'w:line="273"')
    c7 = c6.replace('w:before="160"', 'w:before="170"')
    return c7


def oct_56_plus_after_27_to_30(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="27"')
    c2 = _apply_base_56(c)
    c3 = c2.replace('w:after="27"', 'w:after="30"')
    fp.write_text(c3, encoding="utf-8")
    return n


def oct_56_plus_after_27_to_25(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="27"')
    c2 = _apply_base_56(c)
    c3 = c2.replace('w:after="27"', 'w:after="25"')
    fp.write_text(c3, encoding="utf-8")
    return n


def oct_56_plus_before_80_85(unpacked_dir: Path) -> int:
    """+ before=80 -> 85 (small step)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:before="80"')
    c2 = _apply_base_56(c)
    c3 = c2.replace('w:before="80"', 'w:before="85"')
    fp.write_text(c3, encoding="utf-8")
    return n


def oct_56_plus_before_80_75(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:before="80"')
    c2 = _apply_base_56(c)
    c3 = c2.replace('w:before="80"', 'w:before="75"')
    fp.write_text(c3, encoding="utf-8")
    return n


def oct_56_plus_after_32_to_34(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="32"')
    c2 = _apply_base_56(c)
    c3 = c2.replace('w:after="32"', 'w:after="34"')
    fp.write_text(c3, encoding="utf-8")
    return n


def oct_56_plus_after_32_to_30(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="32"')
    c2 = _apply_base_56(c)
    c3 = c2.replace('w:after="32"', 'w:after="30"')
    fp.write_text(c3, encoding="utf-8")
    return n


def oct_56_plus_after_176_180(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="176"')
    c2 = _apply_base_56(c)
    c3 = c2.replace('w:after="176"', 'w:after="180"')
    fp.write_text(c3, encoding="utf-8")
    return n


def oct_56_plus_after_176_172(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="176"')
    c2 = _apply_base_56(c)
    c3 = c2.replace('w:after="176"', 'w:after="172"')
    fp.write_text(c3, encoding="utf-8")
    return n


def oct_56_plus_before_160_168(unpacked_dir: Path) -> int:
    """Replace 170 with 168."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:before="160"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    c6 = c5.replace('w:line="271"', 'w:line="273"')
    c7 = c6.replace('w:before="160"', 'w:before="168"')
    fp.write_text(c7, encoding="utf-8")
    return n


# Try alt-row shd more deeply
def oct_56_plus_shd_f1_to_ebebec(unpacked_dir: Path) -> int:
    """Shd shift; iter-58 said sat but let's confirm in new base."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:fill="F1F1F6"')
    c2 = _apply_base_56(c)
    c3 = c2.replace('w:fill="F1F1F6"', 'w:fill="EBEBEC"')
    fp.write_text(c3, encoding="utf-8")
    return n


# Try a unique angle: w:bottom borders that are still E5 but on tables
# Tables sz=4 already covered. Let me look at insideH / insideV explicitly
def oct_56_plus_inside_e5_to_eb(unpacked_dir: Path) -> int:
    """Only insideH/insideV borders -> EB (subset of 340)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    c2 = _apply_base_56(c)
    # By this time E5E5E5 already replaced to F5F5F5; this is no-op
    return 0


# Cell padding `w:tblCellMar` could be a lever — investigate
def oct_56_plus_tblCellMar_top_50_to_30(unpacked_dir: Path) -> int:
    """tblCellMar w:top w:w="50" -> "30"."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('<w:top w:w="50" w:type="dxa"/>')
    c2 = _apply_base_56(c)
    c3 = c2.replace('<w:top w:w="50" w:type="dxa"/>', '<w:top w:w="30" w:type="dxa"/>')
    fp.write_text(c3, encoding="utf-8")
    return n


def oct_56_plus_tblCellMar_top_50_to_70(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('<w:top w:w="50" w:type="dxa"/>')
    c2 = _apply_base_56(c)
    c3 = c2.replace('<w:top w:w="50" w:type="dxa"/>', '<w:top w:w="70" w:type="dxa"/>')
    fp.write_text(c3, encoding="utf-8")
    return n


# Inspect: list tblCellMar values
def inspect_tblCellMar(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    cands = re.findall(r'<w:(?:top|bottom|left|right) w:w="(\d+)" w:type="dxa"/>', c)
    from collections import Counter
    ctr = Counter(cands)
    for v, n in ctr.most_common():
        print(f"  cellmar value={v}: {n} sites")
    return 0


RECIPES = {
    "oct_56_plus_after_27_to_30": oct_56_plus_after_27_to_30,
    "oct_56_plus_after_27_to_25": oct_56_plus_after_27_to_25,
    "oct_56_plus_before_80_85": oct_56_plus_before_80_85,
    "oct_56_plus_before_80_75": oct_56_plus_before_80_75,
    "oct_56_plus_after_32_to_34": oct_56_plus_after_32_to_34,
    "oct_56_plus_after_32_to_30": oct_56_plus_after_32_to_30,
    "oct_56_plus_after_176_180": oct_56_plus_after_176_180,
    "oct_56_plus_after_176_172": oct_56_plus_after_176_172,
    "oct_56_plus_before_160_168": oct_56_plus_before_160_168,
    "oct_56_plus_shd_f1_to_ebebec": oct_56_plus_shd_f1_to_ebebec,
    "oct_56_plus_tblCellMar_top_50_to_30": oct_56_plus_tblCellMar_top_50_to_30,
    "oct_56_plus_tblCellMar_top_50_to_70": oct_56_plus_tblCellMar_top_50_to_70,
    "inspect_tblCellMar": inspect_tblCellMar,
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
