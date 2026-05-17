"""Surgical edit helper: change w:spacing val on rPr blocks matching a (sz, color, font?) filter.

Edits rPr blocks that contain:
  - <w:sz w:val="{sz}"/>
  - <w:color w:val="{color_hex}"/> (e.g. 000000 for BLACK; AUTO not included via this path)
  - optional font predicate (Arial Black or any Arial)
  - <w:spacing w:val="{from_val}"/>

Replaces with w:spacing w:val="{to_val}".

Usage: python edit_iter.py <iter_name> <sz> <color_hex> <from> <to> [--font=ArialBlack|Arial|any]
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).parent

RPR_RE = re.compile(r'(<w:rPr>)(.*?)(</w:rPr>)', re.DOTALL)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("iter_name")
    ap.add_argument("--sz", type=int, required=True)
    ap.add_argument("--colors", required=True, help="comma-separated hex colors (or 'AUTO')")
    ap.add_argument("--from-sp", type=int, required=True)
    ap.add_argument("--to-sp", type=int, required=True)
    ap.add_argument("--font", default="any", choices=["any", "ArialBlack", "Arial", "ArialNonBlack"])
    args = ap.parse_args()

    iter_dir = ROOT / args.iter_name
    doc_path = iter_dir / "unpacked" / "word" / "document.xml"
    doc = doc_path.read_text(encoding="utf-8")

    color_list = [c.strip().upper() for c in args.colors.split(",")]

    count = 0

    def repl(m):
        nonlocal count
        body = m.group(2)
        # must have sz=args.sz
        sz_m = re.search(r'<w:sz w:val="(\d+)"', body)
        if not sz_m or int(sz_m.group(1)) != args.sz:
            return m.group(0)
        # must have color in list
        color_m = re.search(r'<w:color w:val="([0-9A-Fa-f]+)"', body)
        if "AUTO" in color_list:
            color_ok = (color_m is None) or (color_m.group(1).upper() in color_list)
        else:
            color_ok = (color_m is not None) and (color_m.group(1).upper() in color_list)
        if not color_ok:
            return m.group(0)
        # font predicate
        font_m = re.search(r'<w:rFonts ([^/>]*)/?>', body)
        font_attrs = font_m.group(1) if font_m else ""
        is_arial_black = "Arial Black" in font_attrs
        is_arial = ("Arial " in font_attrs) or ('"Arial"' in font_attrs) or ("Arial\"" in font_attrs)
        if args.font == "ArialBlack" and not is_arial_black:
            return m.group(0)
        if args.font == "Arial" and not is_arial:
            return m.group(0)
        if args.font == "ArialNonBlack" and (is_arial_black or not is_arial):
            return m.group(0)
        # change spacing
        new_body, n = re.subn(
            rf'<w:spacing w:val="{args.from_sp}"',
            f'<w:spacing w:val="{args.to_sp}"',
            body,
            count=1,
        )
        if n:
            count += n
            return m.group(1) + new_body + m.group(3)
        return m.group(0)

    new_doc = RPR_RE.sub(repl, doc)
    doc_path.write_text(new_doc, encoding="utf-8")
    print(f"Edited {count} sites: sz={args.sz} colors={color_list} font={args.font} sp {args.from_sp}->{args.to_sp}")


if __name__ == "__main__":
    main()
