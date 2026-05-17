"""Generic modifier: apply spacing change to rPr blocks matching color/size/font filters.

Usage:
  python modify.py <iter_dir> --color 8E8E93 --new-spacing 2

Operates on iter_dir/unpacked/word/document.xml.
"""
import argparse
import re
import sys
from pathlib import Path


def modify(unpacked_dir: Path, color_filter: str | None, font_filter: str | None,
           current_spacing: str | None, new_spacing: str | None, size: str = "10") -> int:
    """Return number of rPr blocks modified.

    - color_filter: None matches any color (or 'NONE' to require missing color)
    - current_spacing: None matches any spacing (use 'NONE' for missing only;
      'ANY' for both present/missing); '5' to match val=5 only
    - new_spacing: 'REMOVE' to delete spacing tag; otherwise val to set/add
    """
    doc_xml = unpacked_dir / "word" / "document.xml"
    text = doc_xml.read_text(encoding="utf-8")

    # Iteratively find and replace rPr blocks
    pattern = re.compile(r"<w:rPr>(.*?)</w:rPr>", re.DOTALL)
    count = 0
    out_parts = []
    last_end = 0
    for m in pattern.finditer(text):
        inner = m.group(1)
        # Check size
        if not re.search(rf'<w:sz\s+w:val="{size}"\s*/>', inner):
            continue
        # Check color
        m_color = re.search(r'<w:color\s+w:val="([0-9A-Fa-f]{6})"', inner)
        actual_color = m_color.group(1).upper() if m_color else "NONE"
        if color_filter is not None:
            if color_filter == "NONE":
                if actual_color != "NONE":
                    continue
            else:
                if actual_color != color_filter.upper():
                    continue
        # Check font
        if font_filter is not None:
            m_font = re.search(r'<w:rFonts\s+w:ascii="([^"]+)"', inner)
            actual_font = m_font.group(1) if m_font else "NONE"
            if actual_font != font_filter:
                continue
        # Check current spacing
        m_spacing = re.search(r'<w:spacing\s+w:val="(-?\d+)"\s*/>', inner)
        actual_spacing = m_spacing.group(1) if m_spacing else "NONE"
        if current_spacing is not None and current_spacing != "ANY":
            if current_spacing != actual_spacing:
                continue

        # Build modified inner
        if new_spacing == "REMOVE":
            new_inner = re.sub(r'<w:spacing\s+w:val="-?\d+"\s*/>', "", inner)
        else:
            new_tag = f'<w:spacing w:val="{new_spacing}"/>'
            if m_spacing:
                new_inner = re.sub(r'<w:spacing\s+w:val="-?\d+"\s*/>', new_tag, inner)
            else:
                # Insert spacing tag after <w:sz w:val=...> for consistency
                # Actually safer to append at end inside rPr
                new_inner = inner + new_tag
        count += 1
        out_parts.append(text[last_end:m.start()])
        out_parts.append(f"<w:rPr>{new_inner}</w:rPr>")
        last_end = m.end()
    out_parts.append(text[last_end:])
    new_text = "".join(out_parts)

    if count > 0:
        doc_xml.write_text(new_text, encoding="utf-8")
    return count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("iter_dir")
    ap.add_argument("--color", default=None,
                    help="hex color filter (or 'NONE' for missing). Omit to match any.")
    ap.add_argument("--font", default=None)
    ap.add_argument("--size", default="10")
    ap.add_argument("--current-spacing", default=None,
                    help="match current spacing value ('5', 'NONE', 'ANY'). Omit = any.")
    ap.add_argument("--new-spacing", required=True, help="new value, or REMOVE")
    args = ap.parse_args()

    unpacked = Path(args.iter_dir) / "unpacked"
    n = modify(unpacked, args.color, args.font, args.current_spacing,
               args.new_spacing, args.size)
    print(f"Modified {n} rPr blocks (sz={args.size}, color={args.color}, "
          f"font={args.font}, curr_spacing={args.current_spacing}, "
          f"new_spacing={args.new_spacing})")


if __name__ == "__main__":
    main()
