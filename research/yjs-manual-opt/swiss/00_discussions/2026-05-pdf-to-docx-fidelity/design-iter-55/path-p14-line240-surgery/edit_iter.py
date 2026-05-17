"""Generic edit driver for iter-55 path-p14-line240-surgery.

Recipes are page-isolated line=240 surgery on p14 with various step sizes,
plus stacked/combo variants for the final breakthrough check.

Usage:
  python edit_iter.py iter-2 p14_line_240_to_230
  ...
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"

# Page 14 line=240 cohort — full 21 sites (idx 281..304 minus 291,300,301)
# These are: 18 table rows (after=0) + 3 bullets (after=5) in the WARRANTY page
P14_LINE_240_FULL_IDX = {
    281, 282, 283, 284, 285, 286, 287, 288, 289, 290,   # table 1: 品牌商 (10 rows)
    292, 293, 294, 295, 296, 297, 298, 299,              # table 2: 制造商 (8 rows)
    302, 303, 304,                                       # bullets (3)
}
# Just the 18 table-row sites (after=0 only)
P14_LINE_240_TABLES_ONLY_IDX = {
    281, 282, 283, 284, 285, 286, 287, 288, 289, 290,
    292, 293, 294, 295, 296, 297, 298, 299,
}
# Just the 3 bullet sites (after=5)
P14_LINE_240_BULLETS_ONLY_IDX = {302, 303, 304}

p_pat = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.S)


def _edit_line_targets(doc: str, target_idx: set, old_line: int, new_line: int) -> tuple[str, int]:
    """Change w:line=old_line to w:line=new_line for paragraphs in target_idx."""
    target = set(target_idx)
    count = 0
    parts = []
    last = 0
    for i, m in enumerate(p_pat.finditer(doc)):
        if i in target:
            body = m.group(0)
            new_body = re.sub(
                rf'(<w:spacing\b[^/]*\bw:line="){old_line}(")',
                rf'\g<1>{new_line}\g<2>',
                body,
            )
            if new_body != body:
                count += 1
                parts.append(doc[last:m.start()])
                parts.append(new_body)
                last = m.end()
    parts.append(doc[last:])
    return "".join(parts), count


def edit_p14_line_240_full(doc: str, new_line: int) -> tuple[str, int]:
    return _edit_line_targets(doc, P14_LINE_240_FULL_IDX, 240, new_line)


def edit_p14_line_240_tables(doc: str, new_line: int) -> tuple[str, int]:
    return _edit_line_targets(doc, P14_LINE_240_TABLES_ONLY_IDX, 240, new_line)


def edit_p14_line_240_bullets(doc: str, new_line: int) -> tuple[str, int]:
    return _edit_line_targets(doc, P14_LINE_240_BULLETS_ONLY_IDX, 240, new_line)


RECIPES = {
    # Full 21-site (tables + bullets) — primary
    "p14_line_240_full_to_230":  lambda d: edit_p14_line_240_full(d, 230),
    "p14_line_240_full_to_220":  lambda d: edit_p14_line_240_full(d, 220),
    "p14_line_240_full_to_250":  lambda d: edit_p14_line_240_full(d, 250),
    "p14_line_240_full_to_260":  lambda d: edit_p14_line_240_full(d, 260),
    "p14_line_240_full_to_210":  lambda d: edit_p14_line_240_full(d, 210),
    "p14_line_240_full_to_235":  lambda d: edit_p14_line_240_full(d, 235),
    "p14_line_240_full_to_245":  lambda d: edit_p14_line_240_full(d, 245),
    "p14_line_240_full_to_255":  lambda d: edit_p14_line_240_full(d, 255),
    "p14_line_240_full_to_248":  lambda d: edit_p14_line_240_full(d, 248),
    "p14_line_240_full_to_252":  lambda d: edit_p14_line_240_full(d, 252),
    # Tables only (18 sites)
    "p14_line_240_tables_to_230":  lambda d: edit_p14_line_240_tables(d, 230),
    "p14_line_240_tables_to_220":  lambda d: edit_p14_line_240_tables(d, 220),
    "p14_line_240_tables_to_250":  lambda d: edit_p14_line_240_tables(d, 250),
    "p14_line_240_tables_to_260":  lambda d: edit_p14_line_240_tables(d, 260),
    "p14_line_240_tables_to_235":  lambda d: edit_p14_line_240_tables(d, 235),
    "p14_line_240_tables_to_245":  lambda d: edit_p14_line_240_tables(d, 245),
    # Bullets only (3 sites)
    "p14_line_240_bullets_to_230":  lambda d: edit_p14_line_240_bullets(d, 230),
    "p14_line_240_bullets_to_250":  lambda d: edit_p14_line_240_bullets(d, 250),
}


def stack(doc, names):
    total = 0
    for n in names:
        doc, c = RECIPES[n](doc)
        print(f"  applied {n}: {c} sites")
        total += c
    return doc, total


def apply_recipe(iter_name: str, recipe, src_unpacked=None):
    iter_dir = ROOT / iter_name
    iter_dir.mkdir(exist_ok=True)
    out_unpacked = iter_dir / "unpacked"
    if out_unpacked.exists():
        shutil.rmtree(out_unpacked)
    shutil.copytree(src_unpacked or SRC_UNPACKED, out_unpacked)
    doc_path = out_unpacked / "word" / "document.xml"
    doc = doc_path.read_text(encoding="utf-8")
    names = recipe if isinstance(recipe, list) else [recipe]
    print(f"Applying {iter_name} = {names}")
    new_doc, count = stack(doc, names)
    doc_path.write_text(new_doc, encoding="utf-8")
    print(f"Total {count} sites modified in {iter_name}")
    return count


if __name__ == "__main__":
    iter_name = sys.argv[1]
    recipe = sys.argv[2]
    if "," in recipe:
        recipe = recipe.split(",")
    apply_recipe(iter_name, recipe)
