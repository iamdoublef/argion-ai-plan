"""Stack onto iter-38 (= F5 + 252->244 + 264->260 + 230->228 + 271->273 = 7.28/10.16)."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


def _apply_base_38(c: str) -> str:
    """Base = iter-38 winner."""
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    c6 = c5.replace('w:line="271"', 'w:line="273"')
    return c6


def hex_38_plus_line_278_280(unpacked_dir: Path) -> int:
    """+ line=278 -> 280."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:line="278"', 'w:line="280"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hex_38_plus_line_271_275(unpacked_dir: Path) -> int:
    """Replace base 273 with 275."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="271"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    c6 = c5.replace('w:line="271"', 'w:line="275"')
    fp.write_text(c6, encoding="utf-8")
    return n


def hex_38_plus_line_271_277(unpacked_dir: Path) -> int:
    """271 -> 277 (more aggressive)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="271"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    c6 = c5.replace('w:line="271"', 'w:line="277"')
    fp.write_text(c6, encoding="utf-8")
    return n


def hex_38_plus_line_271_272(unpacked_dir: Path) -> int:
    """271 -> 272 (tiny step)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="271"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    c6 = c5.replace('w:line="271"', 'w:line="272"')
    fp.write_text(c6, encoding="utf-8")
    return n


def hex_38_plus_line_271_274(unpacked_dir: Path) -> int:
    """271 -> 274."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="271"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="244"')
    c4 = c3.replace('w:line="264"', 'w:line="260"')
    c5 = c4.replace('w:line="230"', 'w:line="228"')
    c6 = c5.replace('w:line="271"', 'w:line="274"')
    fp.write_text(c6, encoding="utf-8")
    return n


def hex_38_plus_line_278_276(unpacked_dir: Path) -> int:
    """38 base + 278->276."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:line="278"', 'w:line="276"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hex_38_plus_line_240_238(unpacked_dir: Path) -> int:
    """38 + line=240->238 (154-site big cohort)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="240"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:line="240"', 'w:line="238"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hex_38_plus_line_240_242(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="240"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:line="240"', 'w:line="242"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hex_38_plus_after_120_100(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="120"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:after="120"', 'w:after="100"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hex_38_plus_after_120_140(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="120"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:after="120"', 'w:after="140"')
    fp.write_text(c3, encoding="utf-8")
    return n


def hex_38_plus_after_120_110(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="120"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:after="120"', 'w:after="110"')
    fp.write_text(c3, encoding="utf-8")
    return n


# Tease both 278->280 and 271->273
def hex_38_plus_line_278_280_aggressive(unpacked_dir: Path) -> int:
    """38 base + 278 -> 280 (UP)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    c2 = _apply_base_38(c)
    c3 = c2.replace('w:line="278"', 'w:line="280"')
    fp.write_text(c3, encoding="utf-8")
    return n


RECIPES = {
    "hex_38_plus_line_278_280": hex_38_plus_line_278_280,
    "hex_38_plus_line_271_275": hex_38_plus_line_271_275,
    "hex_38_plus_line_271_277": hex_38_plus_line_271_277,
    "hex_38_plus_line_271_272": hex_38_plus_line_271_272,
    "hex_38_plus_line_271_274": hex_38_plus_line_271_274,
    "hex_38_plus_line_278_276": hex_38_plus_line_278_276,
    "hex_38_plus_line_240_238": hex_38_plus_line_240_238,
    "hex_38_plus_line_240_242": hex_38_plus_line_240_242,
    "hex_38_plus_after_120_100": hex_38_plus_after_120_100,
    "hex_38_plus_after_120_140": hex_38_plus_after_120_140,
    "hex_38_plus_after_120_110": hex_38_plus_after_120_110,
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
