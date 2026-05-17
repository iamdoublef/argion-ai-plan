"""Edit driver for iter-59 path-invisible-borders.

Building on iter-58 W46 (7.38/10.90 — the showstopper). The W46 baseline
already has the stack applied. New exploration angles:

1. The lone remaining top sz=8 BLACK site at p3 area (iter-58 said it regressed
   p4 by -0.04 ALONE — but composed differently with W46 maybe redeems it?)
2. Line spacing per-page cohorts: line=278 (45 sites — Title?), line=271 (13
   sites — banner), line=264 (9 sites), line=252 (7 sites)
3. p3 / p5 / p15 targeted line shifts
4. spacing-after cohorts: after=27/32/120 — try shrinks/grows
5. Bottom sz=4 E5E5E5 (134 sites) — table inner borders, try lighter colors
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


def doc_top_sz8_first_only_to_ff(unpacked_dir: Path) -> int:
    """Only the FIRST (and only remaining) top sz=8 site at p3 area -> FFFFFF.

    iter-58 said this regressed p4 by ~0.04. But baseline composition has changed,
    retest.
    """
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    parts = c.split('<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>')
    if len(parts) < 2:
        return 0
    new_c = parts[0] + '<w:top w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>' + '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'.join(parts[1:])
    fp.write_text(new_c, encoding="utf-8")
    return 1


def doc_top_sz8_first_only_to_e5(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    parts = c.split('<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>')
    if len(parts) < 2:
        return 0
    new_c = parts[0] + '<w:top w:val="single" w:sz="8" w:space="0" w:color="E5E5E5"/>' + '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'.join(parts[1:])
    fp.write_text(new_c, encoding="utf-8")
    return 1


def doc_top_sz8_first_only_to_d9(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    parts = c.split('<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>')
    if len(parts) < 2:
        return 0
    new_c = parts[0] + '<w:top w:val="single" w:sz="8" w:space="0" w:color="D9D9D9"/>' + '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'.join(parts[1:])
    fp.write_text(new_c, encoding="utf-8")
    return 1


def doc_top_sz8_first_only_to_f0(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    parts = c.split('<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>')
    if len(parts) < 2:
        return 0
    new_c = parts[0] + '<w:top w:val="single" w:sz="8" w:space="0" w:color="F0F0F0"/>' + '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'.join(parts[1:])
    fp.write_text(new_c, encoding="utf-8")
    return 1


# =============== LINE SPACING LEVERS ===============

def doc_line_278_to_276(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    fp.write_text(c.replace('w:line="278"', 'w:line="276"'), encoding="utf-8")
    return n


def doc_line_278_to_280(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    fp.write_text(c.replace('w:line="278"', 'w:line="280"'), encoding="utf-8")
    return n


def doc_line_278_to_272(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    fp.write_text(c.replace('w:line="278"', 'w:line="272"'), encoding="utf-8")
    return n


def doc_line_278_to_274(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="278"')
    fp.write_text(c.replace('w:line="278"', 'w:line="274"'), encoding="utf-8")
    return n


def doc_line_271_to_268(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="271"')
    fp.write_text(c.replace('w:line="271"', 'w:line="268"'), encoding="utf-8")
    return n


def doc_line_271_to_265(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="271"')
    fp.write_text(c.replace('w:line="271"', 'w:line="265"'), encoding="utf-8")
    return n


def doc_line_271_to_273(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="271"')
    fp.write_text(c.replace('w:line="271"', 'w:line="273"'), encoding="utf-8")
    return n


def doc_line_264_to_260(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="264"')
    fp.write_text(c.replace('w:line="264"', 'w:line="260"'), encoding="utf-8")
    return n


def doc_line_264_to_268(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="264"')
    fp.write_text(c.replace('w:line="264"', 'w:line="268"'), encoding="utf-8")
    return n


def doc_line_252_to_248(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="252"')
    fp.write_text(c.replace('w:line="252"', 'w:line="248"'), encoding="utf-8")
    return n


def doc_line_252_to_256(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:line="252"')
    fp.write_text(c.replace('w:line="252"', 'w:line="256"'), encoding="utf-8")
    return n


# =============== SPACING-AFTER LEVERS ===============

def doc_after_27_to_24(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="27"')
    fp.write_text(c.replace('w:after="27"', 'w:after="24"'), encoding="utf-8")
    return n


def doc_after_27_to_30(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="27"')
    fp.write_text(c.replace('w:after="27"', 'w:after="30"'), encoding="utf-8")
    return n


def doc_after_27_to_20(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="27"')
    fp.write_text(c.replace('w:after="27"', 'w:after="20"'), encoding="utf-8")
    return n


def doc_after_32_to_28(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="32"')
    fp.write_text(c.replace('w:after="32"', 'w:after="28"'), encoding="utf-8")
    return n


def doc_after_32_to_36(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:after="32"')
    fp.write_text(c.replace('w:after="32"', 'w:after="36"'), encoding="utf-8")
    return n


# =============== INNER E5 BORDER COHORT ===============

def doc_inner_e5_to_eb(unpacked_dir: Path) -> int:
    """Table sz=4 E5E5E5 -> EBEBEB (lighter, 340 sites)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    fp.write_text(c.replace('w:color="E5E5E5"', 'w:color="EBEBEB"'), encoding="utf-8")
    return n


def doc_inner_e5_to_e0(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    fp.write_text(c.replace('w:color="E5E5E5"', 'w:color="E0E0E0"'), encoding="utf-8")
    return n


def doc_inner_e5_to_dc(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    fp.write_text(c.replace('w:color="E5E5E5"', 'w:color="DCDCDC"'), encoding="utf-8")
    return n


def doc_inner_e5_to_ec(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    fp.write_text(c.replace('w:color="E5E5E5"', 'w:color="ECECEC"'), encoding="utf-8")
    return n


# =============== TOP SZ=12 RED COHORT (1 site) ===============

def doc_top_sz12_red_to_sz8(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")12(" w:space="\d+" w:color="E63846")',
        r'\g<1>8\g<2>',
        c
    )
    n = c.count('w:sz="12"') - new.count('w:sz="12"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz12_red_to_sz6(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")12(" w:space="\d+" w:color="E63846")',
        r'\g<1>6\g<2>',
        c
    )
    n = c.count('w:sz="12"') - new.count('w:sz="12"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz12_red_to_sz4(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")12(" w:space="\d+" w:color="E63846")',
        r'\g<1>4\g<2>',
        c
    )
    n = c.count('w:sz="12"') - new.count('w:sz="12"')
    fp.write_text(new, encoding="utf-8")
    return n


# =============== TOP SZ=18 BLACK BANNER (14 sites — iter-58 said MUST stay) ===============

def doc_top_sz18_000_to_sz14(unpacked_dir: Path) -> int:
    """Banner top sz=18 -> sz=14 (thinner but still black, vs FFFFFF inert)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")18(" w:space="\d+" w:color="000000")',
        r'\g<1>14\g<2>',
        c
    )
    n = c.count('w:sz="18"') - new.count('w:sz="18"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz18_000_to_sz12(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")18(" w:space="\d+" w:color="000000")',
        r'\g<1>12\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 14


def doc_top_sz18_000_to_sz10(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")18(" w:space="\d+" w:color="000000")',
        r'\g<1>10\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 14


def doc_top_sz18_000_to_sz16(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")18(" w:space="\d+" w:color="000000")',
        r'\g<1>16\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 14


def doc_top_sz18_000_to_sz20(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")18(" w:space="\d+" w:color="000000")',
        r'\g<1>20\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 14


def doc_top_sz18_000_to_sz22(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")18(" w:space="\d+" w:color="000000")',
        r'\g<1>22\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 14


# =============== RECIPE REGISTRY ===============
RECIPES = {
    "doc_top_sz8_first_only_to_ff": doc_top_sz8_first_only_to_ff,
    "doc_top_sz8_first_only_to_e5": doc_top_sz8_first_only_to_e5,
    "doc_top_sz8_first_only_to_d9": doc_top_sz8_first_only_to_d9,
    "doc_top_sz8_first_only_to_f0": doc_top_sz8_first_only_to_f0,
    "doc_line_278_to_276": doc_line_278_to_276,
    "doc_line_278_to_280": doc_line_278_to_280,
    "doc_line_278_to_272": doc_line_278_to_272,
    "doc_line_278_to_274": doc_line_278_to_274,
    "doc_line_271_to_268": doc_line_271_to_268,
    "doc_line_271_to_265": doc_line_271_to_265,
    "doc_line_271_to_273": doc_line_271_to_273,
    "doc_line_264_to_260": doc_line_264_to_260,
    "doc_line_264_to_268": doc_line_264_to_268,
    "doc_line_252_to_248": doc_line_252_to_248,
    "doc_line_252_to_256": doc_line_252_to_256,
    "doc_after_27_to_24": doc_after_27_to_24,
    "doc_after_27_to_30": doc_after_27_to_30,
    "doc_after_27_to_20": doc_after_27_to_20,
    "doc_after_32_to_28": doc_after_32_to_28,
    "doc_after_32_to_36": doc_after_32_to_36,
    "doc_inner_e5_to_eb": doc_inner_e5_to_eb,
    "doc_inner_e5_to_e0": doc_inner_e5_to_e0,
    "doc_inner_e5_to_dc": doc_inner_e5_to_dc,
    "doc_inner_e5_to_ec": doc_inner_e5_to_ec,
    "doc_top_sz12_red_to_sz8": doc_top_sz12_red_to_sz8,
    "doc_top_sz12_red_to_sz6": doc_top_sz12_red_to_sz6,
    "doc_top_sz12_red_to_sz4": doc_top_sz12_red_to_sz4,
    "doc_top_sz18_000_to_sz14": doc_top_sz18_000_to_sz14,
    "doc_top_sz18_000_to_sz12": doc_top_sz18_000_to_sz12,
    "doc_top_sz18_000_to_sz10": doc_top_sz18_000_to_sz10,
    "doc_top_sz18_000_to_sz16": doc_top_sz18_000_to_sz16,
    "doc_top_sz18_000_to_sz20": doc_top_sz18_000_to_sz20,
    "doc_top_sz18_000_to_sz22": doc_top_sz18_000_to_sz22,
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
