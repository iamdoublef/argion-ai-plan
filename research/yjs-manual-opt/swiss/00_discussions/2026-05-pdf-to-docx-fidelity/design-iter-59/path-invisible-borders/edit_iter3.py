"""Stack levers based on iter-9 F5 winner."""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


# Best single: E5 -> F5 (-0.010)
def stack_e5_to_f5(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    fp.write_text(c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"'), encoding="utf-8")
    return n


def stack_e5_to_f5_and_line_264_to_260(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n1 = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="264"', 'w:line="260"')
    fp.write_text(c3, encoding="utf-8")
    return n1


def stack_e5_to_f5_and_line_252_to_248(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n1 = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="248"')
    fp.write_text(c3, encoding="utf-8")
    return n1


def stack_e5_to_f5_and_line_252_to_256(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n1 = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="252"', 'w:line="256"')
    fp.write_text(c3, encoding="utf-8")
    return n1


def stack_e5_to_f5_and_after_27_changes_only_visual(unpacked_dir: Path) -> int:
    """Test: F5 + leave after alone (control)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    fp.write_text(c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"'), encoding="utf-8")
    return n


def stack_e5_to_f5_and_top_sz18_sz20(unpacked_dir: Path) -> int:
    """F5 + banner sz=18 -> sz=20 (thicker, more black). iter-58 inert."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")18(" w:space="\d+" w:color="000000")',
        r'\g<1>20\g<2>',
        c2
    )
    fp.write_text(new, encoding="utf-8")
    return n


def stack_e5_to_f5_and_top_sz18_sz16(unpacked_dir: Path) -> int:
    """F5 + banner sz=18 -> sz=16."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    new = re.sub(
        r'(<w:top w:val="single" w:sz=")18(" w:space="\d+" w:color="000000")',
        r'\g<1>16\g<2>',
        c2
    )
    fp.write_text(new, encoding="utf-8")
    return n


# Try a wider lighter palette + targeted line spacing on small cohorts that might be the worst pages
def stack_e5_to_f5_and_line_278_to_280(unpacked_dir: Path) -> int:
    """F5 + line=278 -> 280 (loosen Title spacing)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:color="E5E5E5"')
    c2 = c.replace('w:color="E5E5E5"', 'w:color="F5F5F5"')
    c3 = c2.replace('w:line="278"', 'w:line="280"')
    fp.write_text(c3, encoding="utf-8")
    return n


# Test some banner-specific deltas (try to make banner top BLACKER, contrast — opposite direction)
def doc_top_sz18_000_to_111111(unpacked_dir: Path) -> int:
    """Banner top BLACK to slightly lighter — already iter-58 said this was inert."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="single" w:sz="18" w:space="\d+" w:color=")000000(")',
        r'\g<1>111111\g<2>',
        c
    )
    n = 14
    fp.write_text(new, encoding="utf-8")
    return n


# Try shifting shd (alt-row stripe) — saturated per iter-58 but try sib values
def doc_shd_f1f1f6_to_f4f5f8(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:fill="F1F1F6"')
    fp.write_text(c.replace('w:fill="F1F1F6"', 'w:fill="F4F5F8"'), encoding="utf-8")
    return n


# pgMar tiny shifts (right/left/top/bottom margin)
def doc_pgmar_top_tiny(unpacked_dir: Path) -> int:
    """Inspect & dump pgMar for analysis."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    m = re.search(r'<w:pgMar[^/]+/>', c)
    if m:
        print("pgMar:", m.group(0))
    return 0


RECIPES = {
    "stack_e5_to_f5": stack_e5_to_f5,
    "stack_e5_to_f5_and_line_264_to_260": stack_e5_to_f5_and_line_264_to_260,
    "stack_e5_to_f5_and_line_252_to_248": stack_e5_to_f5_and_line_252_to_248,
    "stack_e5_to_f5_and_line_252_to_256": stack_e5_to_f5_and_line_252_to_256,
    "stack_e5_to_f5_and_top_sz18_sz20": stack_e5_to_f5_and_top_sz18_sz20,
    "stack_e5_to_f5_and_top_sz18_sz16": stack_e5_to_f5_and_top_sz18_sz16,
    "stack_e5_to_f5_and_line_278_to_280": stack_e5_to_f5_and_line_278_to_280,
    "doc_top_sz18_000_to_111111": doc_top_sz18_000_to_111111,
    "doc_shd_f1f1f6_to_f4f5f8": doc_shd_f1f1f6_to_f4f5f8,
    "doc_pgmar_top_tiny": doc_pgmar_top_tiny,
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
