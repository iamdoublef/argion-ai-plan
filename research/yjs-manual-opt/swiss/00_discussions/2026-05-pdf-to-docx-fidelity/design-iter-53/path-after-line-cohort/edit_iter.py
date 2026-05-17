"""Generic edit driver for iter-53.

Usage:
  python edit_iter.py iter-2 p14_after_80_to_60
  python edit_iter.py iter-3 p14_after_80_to_70
  python edit_iter.py iter-4 p14_after_80_to_90
  python edit_iter.py iter-5 line_271_to_265
  python edit_iter.py iter-6 line_271_to_278
  python edit_iter.py iter-7 after_120_to_100
  python edit_iter.py iter-8 after_120_to_140
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"

# Cohort target indices (p14 after=80 only — idx 280/291/300)
P14_AFTER_80_IDX = {280, 291, 300}
# w:line="271" sites — all 17
LINE_271_IDX = {73, 74, 75, 76, 77, 79, 80, 81, 82, 84, 85, 86, 87, 251, 252, 253, 254}
# w:after="120" sites — all 23
AFTER_120_IDX = {12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 24, 55, 71, 90, 114, 131, 170, 185, 202, 239, 257, 278, 308}


p_pat = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.S)


def edit_p14_after_80(doc: str, new_after: int) -> tuple[str, int]:
    """Change w:after="80" to new value for p14 paragraphs (idx 280/291/300)."""
    target = set(P14_AFTER_80_IDX)
    count = 0
    parts = []
    last = 0
    for i, m in enumerate(p_pat.finditer(doc)):
        if i in target:
            body = m.group(0)
            # only touch the spacing element with after=80
            new_body = re.sub(
                r'(<w:spacing\b[^/]*\bw:after=")80(")',
                rf'\g<1>{new_after}\g<2>',
                body,
            )
            if new_body != body:
                count += 1
                parts.append(doc[last:m.start()])
                parts.append(new_body)
                last = m.end()
    parts.append(doc[last:])
    return "".join(parts), count


def edit_line_271(doc: str, new_line: int) -> tuple[str, int]:
    """Change w:line='271' to new_line on the 17 known sites."""
    target = set(LINE_271_IDX)
    count = 0
    parts = []
    last = 0
    for i, m in enumerate(p_pat.finditer(doc)):
        if i in target:
            body = m.group(0)
            new_body = re.sub(
                r'(<w:spacing\b[^/]*\bw:line=")271(")',
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


def edit_after_120(doc: str, new_after: int) -> tuple[str, int]:
    """Change w:after='120' to new_after on the 23 known sites."""
    target = set(AFTER_120_IDX)
    count = 0
    parts = []
    last = 0
    for i, m in enumerate(p_pat.finditer(doc)):
        if i in target:
            body = m.group(0)
            new_body = re.sub(
                r'(<w:spacing\b[^/]*\bw:after=")120(")',
                rf'\g<1>{new_after}\g<2>',
                body,
            )
            if new_body != body:
                count += 1
                parts.append(doc[last:m.start()])
                parts.append(new_body)
                last = m.end()
    parts.append(doc[last:])
    return "".join(parts), count


# Page-specific line=271 sub-cohorts
LINE_271_P5_IDX = {73, 74, 75, 76, 77, 79, 80, 81, 82, 84, 85, 86, 87}  # 13 sites on p5
LINE_271_P12_IDX = {251, 252, 253, 254}  # 4 sites on p12


def edit_line_271_p12_only(doc: str, new_line: int) -> tuple[str, int]:
    target = set(LINE_271_P12_IDX)
    count = 0
    parts = []
    last = 0
    for i, m in enumerate(p_pat.finditer(doc)):
        if i in target:
            body = m.group(0)
            new_body = re.sub(
                r'(<w:spacing\b[^/]*\bw:line=")271(")',
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


def edit_line_271_p5_only(doc: str, new_line: int) -> tuple[str, int]:
    target = set(LINE_271_P5_IDX)
    count = 0
    parts = []
    last = 0
    for i, m in enumerate(p_pat.finditer(doc)):
        if i in target:
            body = m.group(0)
            new_body = re.sub(
                r'(<w:spacing\b[^/]*\bw:line=")271(")',
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


# Recipe registry: name -> callable(doc) -> (doc, count)
RECIPES = {
    "p14_after_80_to_60":   lambda d: edit_p14_after_80(d, 60),
    "p14_after_80_to_70":   lambda d: edit_p14_after_80(d, 70),
    "p14_after_80_to_90":   lambda d: edit_p14_after_80(d, 90),
    "p14_after_80_to_40":   lambda d: edit_p14_after_80(d, 40),
    "p14_after_80_to_100":  lambda d: edit_p14_after_80(d, 100),
    "line_271_to_265":      lambda d: edit_line_271(d, 265),
    "line_271_to_278":      lambda d: edit_line_271(d, 278),
    "line_271_to_252":      lambda d: edit_line_271(d, 252),
    "line_271_to_260":      lambda d: edit_line_271(d, 260),
    "line_271_p12_to_265":  lambda d: edit_line_271_p12_only(d, 265),
    "line_271_p12_to_260":  lambda d: edit_line_271_p12_only(d, 260),
    "line_271_p12_to_252":  lambda d: edit_line_271_p12_only(d, 252),
    "line_271_p12_to_256":  lambda d: edit_line_271_p12_only(d, 256),
    "line_271_p12_to_240":  lambda d: edit_line_271_p12_only(d, 240),
    "line_271_p12_to_278":  lambda d: edit_line_271_p12_only(d, 278),
    "line_271_p5_to_265":   lambda d: edit_line_271_p5_only(d, 265),
    "line_271_p5_to_260":   lambda d: edit_line_271_p5_only(d, 260),
    "after_120_to_100":     lambda d: edit_after_120(d, 100),
    "after_120_to_140":     lambda d: edit_after_120(d, 140),
    "after_120_to_80":      lambda d: edit_after_120(d, 80),
    "after_120_to_60":      lambda d: edit_after_120(d, 60),
}


def stack(doc, names):
    """Apply multiple recipes in sequence."""
    total = 0
    for n in names:
        doc, c = RECIPES[n](doc)
        print(f"  applied {n}: {c} sites")
        total += c
    return doc, total


def apply_recipe(iter_name: str, recipe: str | list[str], src_unpacked: Path | None = None):
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
