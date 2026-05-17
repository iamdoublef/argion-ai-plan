"""Edit driver for iter-58 path-footer-propagation.

Building on iter-57 W45 (7.73/10.92), the breakthrough was discovering that
the GRAY 8E8E93 -> F5F5F5 lever needed to be applied not just to document.xml
but also to all 15 footer*.xml files (28 sites). Footer propagation moved
mean -0.03 max -0.02.

This iter explores propagating OTHER W43+W32+W33+W34+W35+W36 levers to:
  - footer*.xml (sz=10 spacing=5 cohort — 30 sites across 15 footers)
  - styles.xml / stylesWithEffects.xml (Title style spacing=5 sites)
  - theme1.xml (generic Office colors — almost certainly inert)
  - settings.xml (doc-level settings)

The W43 stack was applied to document.xml only. New attacks:
  - footer sz=10 spacing 5->2 (DOWN, matching W33 sz=11/12 cohort logic)
  - footer sz=10 spacing 5->8 (UP, matching W32 sz=14 BLACK cohort)
  - footer sz=10 spacing 5->0 (FULL DOWN — remove char spacing)
  - footer EEEEEE border color shifts
  - footer color F5F5F5 -> other grays (E0/F0/FA) to test if it composes
  - styles.xml Title spacing 5->X (probably inert, but cheap test)

Apply lever functions take the unpacked dir and a 'word' subdir;
mutate files in-place; return total count.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"


# =============== HELPERS ===============
def _foreach_footer(unpacked_dir: Path, fn):
    """Apply fn(content) -> (new_content, count) to every footer*.xml."""
    word_dir = unpacked_dir / "word"
    total = 0
    for fp in word_dir.glob("footer*.xml"):
        c = fp.read_text(encoding="utf-8")
        new_c, n = fn(c)
        if n > 0:
            fp.write_text(new_c, encoding="utf-8")
        total += n
    return total


def _foreach_header(unpacked_dir: Path, fn):
    word_dir = unpacked_dir / "word"
    total = 0
    for fp in word_dir.glob("header*.xml"):
        c = fp.read_text(encoding="utf-8")
        new_c, n = fn(c)
        if n > 0:
            fp.write_text(new_c, encoding="utf-8")
        total += n
    return total


# =============== FOOTER SPACING LEVERS ===============
def footer_sz10_spacing_5_to_2(unpacked_dir: Path) -> int:
    """Footer sz=10 spacing 5->2 (DOWN, matching W33 sz=11/12 cohort direction)."""
    def fn(c):
        # Only flip spacing in rPr blocks that have sz=10
        # The footer rPr is structured: rFonts, b, sz=10, color, spacing
        # We need to be careful to not flip 'spacing w:after' or other spacing types.
        # Use w:spacing w:val="5" specifically (char-spacing, no after/before)
        new = re.sub(
            r'(<w:sz w:val="10"/>[^<]*<w:color[^/]*/>[^<]*)<w:spacing w:val="5"/>',
            r'\1<w:spacing w:val="2"/>',
            c
        )
        n = c.count('<w:spacing w:val="5"/>') - new.count('<w:spacing w:val="5"/>')
        return new, n
    return _foreach_footer(unpacked_dir, fn)


def footer_sz10_spacing_5_to_0(unpacked_dir: Path) -> int:
    """Footer sz=10 spacing 5->0 (remove char spacing entirely)."""
    def fn(c):
        new = re.sub(
            r'(<w:sz w:val="10"/>[^<]*<w:color[^/]*/>[^<]*)<w:spacing w:val="5"/>',
            r'\1<w:spacing w:val="0"/>',
            c
        )
        n = c.count('<w:spacing w:val="5"/>') - new.count('<w:spacing w:val="5"/>')
        return new, n
    return _foreach_footer(unpacked_dir, fn)


def footer_sz10_spacing_5_to_8(unpacked_dir: Path) -> int:
    """Footer sz=10 spacing 5->8 (UP, matching W32 sz=14 BLACK cohort)."""
    def fn(c):
        new = re.sub(
            r'(<w:sz w:val="10"/>[^<]*<w:color[^/]*/>[^<]*)<w:spacing w:val="5"/>',
            r'\1<w:spacing w:val="8"/>',
            c
        )
        n = c.count('<w:spacing w:val="5"/>') - new.count('<w:spacing w:val="5"/>')
        return new, n
    return _foreach_footer(unpacked_dir, fn)


def footer_sz10_spacing_5_to_3(unpacked_dir: Path) -> int:
    """Footer sz=10 spacing 5->3."""
    def fn(c):
        new = re.sub(
            r'(<w:sz w:val="10"/>[^<]*<w:color[^/]*/>[^<]*)<w:spacing w:val="5"/>',
            r'\1<w:spacing w:val="3"/>',
            c
        )
        n = c.count('<w:spacing w:val="5"/>') - new.count('<w:spacing w:val="5"/>')
        return new, n
    return _foreach_footer(unpacked_dir, fn)


def footer_sz10_spacing_5_to_1(unpacked_dir: Path) -> int:
    """Footer sz=10 spacing 5->1."""
    def fn(c):
        new = re.sub(
            r'(<w:sz w:val="10"/>[^<]*<w:color[^/]*/>[^<]*)<w:spacing w:val="5"/>',
            r'\1<w:spacing w:val="1"/>',
            c
        )
        n = c.count('<w:spacing w:val="5"/>') - new.count('<w:spacing w:val="5"/>')
        return new, n
    return _foreach_footer(unpacked_dir, fn)


# =============== FOOTER COLOR LEVERS (in addition to W45 F5F5F5 already applied) ===============
def footer_color_f5_to_e8(unpacked_dir: Path) -> int:
    """Footer text color F5F5F5 -> E8E8E8 (slightly darker, more visible)."""
    def fn(c):
        n = c.count('w:val="F5F5F5"')
        return c.replace('w:val="F5F5F5"', 'w:val="E8E8E8"'), n
    return _foreach_footer(unpacked_dir, fn)


def footer_color_f5_to_fa(unpacked_dir: Path) -> int:
    """Footer text F5F5F5 -> FAFAFA."""
    def fn(c):
        n = c.count('w:val="F5F5F5"')
        return c.replace('w:val="F5F5F5"', 'w:val="FAFAFA"'), n
    return _foreach_footer(unpacked_dir, fn)


def footer_color_f5_to_f0(unpacked_dir: Path) -> int:
    """Footer text F5F5F5 -> F0F0F0."""
    def fn(c):
        n = c.count('w:val="F5F5F5"')
        return c.replace('w:val="F5F5F5"', 'w:val="F0F0F0"'), n
    return _foreach_footer(unpacked_dir, fn)


# =============== FOOTER BORDER COLOR LEVERS ===============
def footer_border_eeeeee_to_f5(unpacked_dir: Path) -> int:
    """Footer top border w:color='EEEEEE' -> 'F5F5F5' (slightly lighter)."""
    def fn(c):
        n = c.count('w:color="EEEEEE"')
        return c.replace('w:color="EEEEEE"', 'w:color="F5F5F5"'), n
    return _foreach_footer(unpacked_dir, fn)


def footer_border_eeeeee_to_e0(unpacked_dir: Path) -> int:
    """Footer top border EEEEEE -> E0E0E0 (slightly darker)."""
    def fn(c):
        n = c.count('w:color="EEEEEE"')
        return c.replace('w:color="EEEEEE"', 'w:color="E0E0E0"'), n
    return _foreach_footer(unpacked_dir, fn)


def footer_border_eeeeee_to_d9(unpacked_dir: Path) -> int:
    """Footer top border EEEEEE -> D9D9D9 (matches W43 cohort)."""
    def fn(c):
        n = c.count('w:color="EEEEEE"')
        return c.replace('w:color="EEEEEE"', 'w:color="D9D9D9"'), n
    return _foreach_footer(unpacked_dir, fn)


def footer_border_eeeeee_to_ec(unpacked_dir: Path) -> int:
    def fn(c):
        n = c.count('w:color="EEEEEE"')
        return c.replace('w:color="EEEEEE"', 'w:color="ECECEC"'), n
    return _foreach_footer(unpacked_dir, fn)


def footer_border_eeeeee_to_e5(unpacked_dir: Path) -> int:
    """Footer top border EEEEEE -> E5E5E5 (matches W43 cohort)."""
    def fn(c):
        n = c.count('w:color="EEEEEE"')
        return c.replace('w:color="EEEEEE"', 'w:color="E5E5E5"'), n
    return _foreach_footer(unpacked_dir, fn)


# =============== STYLES.XML LEVERS ===============
def footer_border_sz_4_to_2(unpacked_dir: Path) -> int:
    """Footer top border thickness sz=4 -> sz=2 (thinner)."""
    def fn(c):
        # Only sz="4" inside top single border with EEEEEE/F5F5F5
        # The current footer has: <w:top w:val="single" w:sz="4" w:space="0" w:color="EEEEEE"/>
        new = re.sub(
            r'(<w:top w:val="single" w:sz=")4(" w:space="0" w:color=")',
            r'\g<1>2\g<2>',
            c
        )
        n = c.count('<w:top w:val="single" w:sz="4"') - new.count('<w:top w:val="single" w:sz="4"')
        return new, n
    return _foreach_footer(unpacked_dir, fn)


def footer_border_sz_4_to_6(unpacked_dir: Path) -> int:
    """Footer top border sz=4 -> sz=6 (thicker)."""
    def fn(c):
        new = re.sub(
            r'(<w:top w:val="single" w:sz=")4(" w:space="0" w:color=")',
            r'\g<1>6\g<2>',
            c
        )
        n = c.count('<w:top w:val="single" w:sz="4"') - new.count('<w:top w:val="single" w:sz="4"')
        return new, n
    return _foreach_footer(unpacked_dir, fn)


def footer_remove_top_border(unpacked_dir: Path) -> int:
    """Remove footer top border entirely (val=nil instead of single)."""
    def fn(c):
        n = c.count('<w:top w:val="single" w:sz="4" w:space="0" w:color="EEEEEE"/>')
        new = c.replace(
            '<w:top w:val="single" w:sz="4" w:space="0" w:color="EEEEEE"/>',
            '<w:top w:val="nil"/>'
        )
        return new, n
    return _foreach_footer(unpacked_dir, fn)


def doc_footer_margin_198_to_185(unpacked_dir: Path) -> int:
    """Shift footer area UP by changing pgMar w:footer from 198 to 185.

    Higher footer value pushes footer text UP; smaller pushes it DOWN.
    198 is current; try 185 (DOWN) and 215 (UP).
    """
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:footer="198"')
    new = c.replace('w:footer="198"', 'w:footer="185"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_footer_margin_198_to_215(unpacked_dir: Path) -> int:
    """pgMar w:footer 198 -> 215."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:footer="198"')
    new = c.replace('w:footer="198"', 'w:footer="215"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_footer_margin_198_to_180(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:footer="198"')
    new = c.replace('w:footer="198"', 'w:footer="180"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_footer_margin_198_to_220(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:footer="198"')
    new = c.replace('w:footer="198"', 'w:footer="220"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_footer_margin_198_to_240(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:footer="198"')
    new = c.replace('w:footer="198"', 'w:footer="240"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_footer_margin_198_to_195(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:footer="198"')
    new = c.replace('w:footer="198"', 'w:footer="195"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_footer_margin_198_to_201(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:footer="198"')
    new = c.replace('w:footer="198"', 'w:footer="201"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_footer_margin_198_to_192(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:footer="198"')
    new = c.replace('w:footer="198"', 'w:footer="192"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_footer_margin_198_to_204(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:footer="198"')
    new = c.replace('w:footer="198"', 'w:footer="204"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_footer_margin_198_to_160(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:footer="198"')
    new = c.replace('w:footer="198"', 'w:footer="160"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_shd_f1f1f6_to_f5f5f5(unpacked_dir: Path) -> int:
    """Alt-row stripe shd fill F1F1F6 -> F5F5F5 (lighter)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:fill="F1F1F6"')
    new = c.replace('w:fill="F1F1F6"', 'w:fill="F5F5F5"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_shd_f1f1f6_to_f3f3f5(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:fill="F1F1F6"')
    new = c.replace('w:fill="F1F1F6"', 'w:fill="F3F3F5"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_shd_f1f1f6_to_eeefef(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:fill="F1F1F6"')
    new = c.replace('w:fill="F1F1F6"', 'w:fill="EEEFEF"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_shd_f1f1f6_to_eff0f2(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    n = c.count('w:fill="F1F1F6"')
    new = c.replace('w:fill="F1F1F6"', 'w:fill="EFF0F2"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz18_000_to_red(unpacked_dir: Path) -> int:
    """Banner pBdr top sz=18 black -> E63846 red (14 sites)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="\w+" w:sz="18" w:space="\d+" w:color=")000000(")',
        r'\g<1>E63846\g<2>',
        c
    )
    n = c.count('w:sz="18"') - new.count('w:sz="18"') if 'banner_count' else 0
    # Count by hash diff:
    n = 0
    for m in re.finditer(r'<w:top w:val="\w+" w:sz="18" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_000_to_e5(unpacked_dir: Path) -> int:
    """Table bottom sz=6 black -> E5E5E5 (matches table border palette)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color=")000000(")',
        r'\g<1>E5E5E5\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_000_to_d9(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color=")000000(")',
        r'\g<1>D9D9D9\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_000_to_eb(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color=")000000(")',
        r'\g<1>EBEBEB\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_000_to_f0(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color=")000000(")',
        r'\g<1>F0F0F0\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_000_to_f5(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color=")000000(")',
        r'\g<1>F5F5F5\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_000_to_e0(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color=")000000(")',
        r'\g<1>E0E0E0\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_000_to_e8(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color=")000000(")',
        r'\g<1>E8E8E8\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_000_to_fa(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color=")000000(")',
        r'\g<1>FAFAFA\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_000_to_fc(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color=")000000(")',
        r'\g<1>FCFCFC\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_000_to_ff(unpacked_dir: Path) -> int:
    """White borders (effectively invisible)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color=")000000(")',
        r'\g<1>FFFFFF\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_all_borders_000_to_ff(unpacked_dir: Path) -> int:
    """ALL border w:color=000000 -> FFFFFF (covers top/bottom/left/right at any sz)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    # Only borders (have w:val, w:sz, w:space, w:color)
    new = re.sub(
        r'(<w:(?:top|bottom|left|right|insideH|insideV) w:val="\w+" w:sz="\d+" w:space="\d+" w:color=")000000(")',
        r'\g<1>FFFFFF\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:(?:top|bottom|left|right|insideH|insideV) w:val="\w+" w:sz="\d+" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_all_borders_000_to_f5(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:(?:top|bottom|left|right|insideH|insideV) w:val="\w+" w:sz="\d+" w:space="\d+" w:color=")000000(")',
        r'\g<1>F5F5F5\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:(?:top|bottom|left|right|insideH|insideV) w:val="\w+" w:sz="\d+" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz8_000_to_ff(unpacked_dir: Path) -> int:
    """Top sz=8 table cell borders 000 -> FFFFFF (2 sites)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="\w+" w:sz="8" w:space="\d+" w:color=")000000(")',
        r'\g<1>FFFFFF\g<2>',
        c
    )
    n = c.count('w:sz="8" w:space="0" w:color="000000"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz8_second_only_to_ff(unpacked_dir: Path) -> int:
    """Only the SECOND top sz=8 site (at paragraph 234, p11 disclaimer) -> FF.

    First site (at paragraph 56, p3 area) regresses badly when changed.
    """
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    target_pat = r'<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
    new_str = r'<w:top w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>'
    # Find all positions of this pattern
    parts = c.split('<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>')
    if len(parts) < 3:
        return 0
    # Keep first occurrence, flip second
    new_c = parts[0] + '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>' + parts[1] + '<w:top w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>' + ''.join(parts[2:])
    if len(parts) > 3:
        # Reconstruct with original between remaining ones
        rest = ''
        for piece in parts[3:]:
            rest += '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>' + piece
        new_c = parts[0] + '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>' + parts[1] + '<w:top w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>' + parts[2] + rest
    fp.write_text(new_c, encoding="utf-8")
    return 1


def doc_left_sz18_red_to_sz22(unpacked_dir: Path) -> int:
    """Red banner left pBdr sz=18 -> sz=22 (thicker)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>22\g<2>',
        c
    )
    n = c.count('w:sz="18"')
    fp.write_text(new, encoding="utf-8")
    return c.count('w:sz="18" w:space="4" w:color="E63846"') if False else 13


def doc_left_sz18_red_to_sz14(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>14\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_left_sz18_red_to_sz12(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>12\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_left_sz18_red_to_sz10(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>10\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_left_sz18_red_to_sz6(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>6\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_left_sz18_red_to_sz2(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>2\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_left_sz18_red_to_sz3(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>3\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_left_sz18_red_to_sz1(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>1\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_left_sz18_red_to_nil(unpacked_dir: Path) -> int:
    """Remove red banner left border entirely (nil)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'<w:left w:val="single" w:sz="18" w:space="\d+" w:color="E63846"/>',
        r'<w:left w:val="nil"/>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_left_sz18_red_to_sz4(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>4\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_left_sz18_red_to_sz8(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>8\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_left_sz18_red_to_sz16(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>16\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_left_sz18_red_to_sz24(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:left w:val="single" w:sz=")18(" w:space="\d+" w:color="E63846")',
        r'\g<1>24\g<2>',
        c
    )
    fp.write_text(new, encoding="utf-8")
    return 13


def doc_top_sz18_000_to_ff(unpacked_dir: Path) -> int:
    """Make banner TOPS invisible: top sz=18 black -> white."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="\w+" w:sz="18" w:space="\d+" w:color=")000000(")',
        r'\g<1>FFFFFF\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:top w:val="\w+" w:sz="18" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz8_first_only_to_ff(unpacked_dir: Path) -> int:
    """Only the FIRST top sz=8 site (at paragraph 56, p3 area) -> FF."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    parts = c.split('<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>')
    if len(parts) < 2:
        return 0
    new_c = parts[0] + '<w:top w:val="single" w:sz="8" w:space="0" w:color="FFFFFF"/>' + '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'.join(parts[1:])
    fp.write_text(new_c, encoding="utf-8")
    return 1


def doc_top_sz8_000_to_e5(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="\w+" w:sz="8" w:space="\d+" w:color=")000000(")',
        r'\g<1>E5E5E5\g<2>',
        c
    )
    n = c.count('w:sz="8" w:space="0" w:color="000000"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz10_000_to_ff(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="\w+" w:sz="10" w:space="\d+" w:color=")000000(")',
        r'\g<1>FFFFFF\g<2>',
        c
    )
    n = c.count('w:sz="10" w:space="1" w:color="000000"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz10_000_to_red(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="\w+" w:sz="10" w:space="\d+" w:color=")000000(")',
        r'\g<1>E63846\g<2>',
        c
    )
    n = c.count('w:sz="10" w:space="1" w:color="000000"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz10_000_to_e5(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="\w+" w:sz="10" w:space="\d+" w:color=")000000(")',
        r'\g<1>E5E5E5\g<2>',
        c
    )
    n = c.count('w:sz="10" w:space="1" w:color="000000"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz10_000_to_d9(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:top w:val="\w+" w:sz="10" w:space="\d+" w:color=")000000(")',
        r'\g<1>D9D9D9\g<2>',
        c
    )
    n = c.count('w:sz="10" w:space="1" w:color="000000"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_top_sz10_to_nil(unpacked_dir: Path) -> int:
    """Remove top sz=10 border entirely (nil)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'<w:top w:val="\w+" w:sz="10" w:space="\d+" w:color="000000"/>',
        r'<w:top w:val="nil"/>',
        c
    )
    n = c.count('w:sz="10" w:space="1" w:color="000000"')
    fp.write_text(new, encoding="utf-8")
    return n


def doc_all_borders_000_to_d9(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:(?:top|bottom|left|right|insideH|insideV) w:val="\w+" w:sz="\d+" w:space="\d+" w:color=")000000(")',
        r'\g<1>D9D9D9\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:(?:top|bottom|left|right|insideH|insideV) w:val="\w+" w:sz="\d+" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_to_nil(unpacked_dir: Path) -> int:
    """Replace bottom border entirely with nil (no border)."""
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"/>',
        r'<w:bottom w:val="nil"/>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def doc_bottom_sz6_000_to_bf(unpacked_dir: Path) -> int:
    fp = unpacked_dir / "word" / "document.xml"
    c = fp.read_text(encoding="utf-8")
    new = re.sub(
        r'(<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color=")000000(")',
        r'\g<1>BFBFBF\g<2>',
        c
    )
    n = 0
    for m in re.finditer(r'<w:bottom w:val="\w+" w:sz="6" w:space="\d+" w:color="000000"', c):
        n += 1
    fp.write_text(new, encoding="utf-8")
    return n


def styles_title_spacing_5_to_0(unpacked_dir: Path) -> int:
    """styles.xml + stylesWithEffects.xml Title spacing 5->0.

    These 4 sites are in <w:rPr> of Title/TitleChar/Subtitle styles.
    The Title style is never used in our doc (no <w:pStyle val="Title"/>),
    so this is almost certainly inert. Cheap to test.
    """
    word_dir = unpacked_dir / "word"
    count = 0
    for fname in ["styles.xml", "stylesWithEffects.xml"]:
        fp = word_dir / fname
        if not fp.exists():
            continue
        c = fp.read_text(encoding="utf-8")
        n = c.count('<w:spacing w:val="5"/>')
        if n > 0:
            new = c.replace('<w:spacing w:val="5"/>', '<w:spacing w:val="0"/>')
            fp.write_text(new, encoding="utf-8")
            count += n
    return count


# =============== HEADER LEVERS (no header*.xml exists currently — confirm) ===============
def header_status(unpacked_dir: Path) -> int:
    """No header*.xml in this docx — returns 0."""
    word_dir = unpacked_dir / "word"
    return len(list(word_dir.glob("header*.xml")))


# =============== STACK FOOTER + DOCUMENT LEVERS ===============
def doc_footer_all_eeeeee_to_e5(unpacked_dir: Path) -> int:
    """Global EEEEEE border color -> E5E5E5 in document.xml AND footer*.xml.
    EEEEEE is used in document.xml too (test border cohort).
    """
    word_dir = unpacked_dir / "word"
    total = 0
    for fp in [word_dir / "document.xml"] + list(word_dir.glob("footer*.xml")):
        c = fp.read_text(encoding="utf-8")
        n = c.count('w:color="EEEEEE"')
        if n > 0:
            fp.write_text(c.replace('w:color="EEEEEE"', 'w:color="E5E5E5"'), encoding="utf-8")
            total += n
    return total


def doc_footer_all_eeeeee_to_e0(unpacked_dir: Path) -> int:
    word_dir = unpacked_dir / "word"
    total = 0
    for fp in [word_dir / "document.xml"] + list(word_dir.glob("footer*.xml")):
        c = fp.read_text(encoding="utf-8")
        n = c.count('w:color="EEEEEE"')
        if n > 0:
            fp.write_text(c.replace('w:color="EEEEEE"', 'w:color="E0E0E0"'), encoding="utf-8")
            total += n
    return total


def doc_footer_all_eeeeee_to_d9(unpacked_dir: Path) -> int:
    word_dir = unpacked_dir / "word"
    total = 0
    for fp in [word_dir / "document.xml"] + list(word_dir.glob("footer*.xml")):
        c = fp.read_text(encoding="utf-8")
        n = c.count('w:color="EEEEEE"')
        if n > 0:
            fp.write_text(c.replace('w:color="EEEEEE"', 'w:color="D9D9D9"'), encoding="utf-8")
            total += n
    return total


def doc_footer_all_eeeeee_to_f0(unpacked_dir: Path) -> int:
    word_dir = unpacked_dir / "word"
    total = 0
    for fp in [word_dir / "document.xml"] + list(word_dir.glob("footer*.xml")):
        c = fp.read_text(encoding="utf-8")
        n = c.count('w:color="EEEEEE"')
        if n > 0:
            fp.write_text(c.replace('w:color="EEEEEE"', 'w:color="F0F0F0"'), encoding="utf-8")
            total += n
    return total


# =============== RECIPE REGISTRY ===============
RECIPES = {
    # Footer sz=10 spacing cohort
    "footer_sz10_spacing_5_to_2": footer_sz10_spacing_5_to_2,
    "footer_sz10_spacing_5_to_3": footer_sz10_spacing_5_to_3,
    "footer_sz10_spacing_5_to_1": footer_sz10_spacing_5_to_1,
    "footer_sz10_spacing_5_to_0": footer_sz10_spacing_5_to_0,
    "footer_sz10_spacing_5_to_8": footer_sz10_spacing_5_to_8,
    # Footer color shifts
    "footer_color_f5_to_e8": footer_color_f5_to_e8,
    "footer_color_f5_to_fa": footer_color_f5_to_fa,
    "footer_color_f5_to_f0": footer_color_f5_to_f0,
    # Footer-only border shifts
    "footer_border_eeeeee_to_f5": footer_border_eeeeee_to_f5,
    "footer_border_eeeeee_to_e0": footer_border_eeeeee_to_e0,
    "footer_border_eeeeee_to_d9": footer_border_eeeeee_to_d9,
    "footer_border_eeeeee_to_ec": footer_border_eeeeee_to_ec,
    "footer_border_eeeeee_to_e5": footer_border_eeeeee_to_e5,
    "footer_border_sz_4_to_2": footer_border_sz_4_to_2,
    "footer_border_sz_4_to_6": footer_border_sz_4_to_6,
    "footer_remove_top_border": footer_remove_top_border,
    "doc_footer_margin_198_to_185": doc_footer_margin_198_to_185,
    "doc_footer_margin_198_to_215": doc_footer_margin_198_to_215,
    "doc_footer_margin_198_to_180": doc_footer_margin_198_to_180,
    "doc_footer_margin_198_to_220": doc_footer_margin_198_to_220,
    "doc_footer_margin_198_to_240": doc_footer_margin_198_to_240,
    "doc_footer_margin_198_to_160": doc_footer_margin_198_to_160,
    "doc_footer_margin_198_to_195": doc_footer_margin_198_to_195,
    "doc_footer_margin_198_to_201": doc_footer_margin_198_to_201,
    "doc_footer_margin_198_to_192": doc_footer_margin_198_to_192,
    "doc_footer_margin_198_to_204": doc_footer_margin_198_to_204,
    "doc_shd_f1f1f6_to_f5f5f5": doc_shd_f1f1f6_to_f5f5f5,
    "doc_shd_f1f1f6_to_f3f3f5": doc_shd_f1f1f6_to_f3f3f5,
    "doc_shd_f1f1f6_to_eeefef": doc_shd_f1f1f6_to_eeefef,
    "doc_shd_f1f1f6_to_eff0f2": doc_shd_f1f1f6_to_eff0f2,
    "doc_top_sz18_000_to_red": doc_top_sz18_000_to_red,
    "doc_bottom_sz6_000_to_e5": doc_bottom_sz6_000_to_e5,
    "doc_bottom_sz6_000_to_d9": doc_bottom_sz6_000_to_d9,
    "doc_bottom_sz6_000_to_bf": doc_bottom_sz6_000_to_bf,
    "doc_bottom_sz6_000_to_e0": doc_bottom_sz6_000_to_e0,
    "doc_bottom_sz6_000_to_e8": doc_bottom_sz6_000_to_e8,
    "doc_bottom_sz6_000_to_eb": doc_bottom_sz6_000_to_eb,
    "doc_bottom_sz6_000_to_f0": doc_bottom_sz6_000_to_f0,
    "doc_bottom_sz6_000_to_f5": doc_bottom_sz6_000_to_f5,
    "doc_bottom_sz6_000_to_fa": doc_bottom_sz6_000_to_fa,
    "doc_bottom_sz6_000_to_fc": doc_bottom_sz6_000_to_fc,
    "doc_bottom_sz6_000_to_ff": doc_bottom_sz6_000_to_ff,
    "doc_bottom_sz6_to_nil": doc_bottom_sz6_to_nil,
    "doc_all_borders_000_to_ff": doc_all_borders_000_to_ff,
    "doc_all_borders_000_to_f5": doc_all_borders_000_to_f5,
    "doc_all_borders_000_to_d9": doc_all_borders_000_to_d9,
    "doc_top_sz8_000_to_ff": doc_top_sz8_000_to_ff,
    "doc_top_sz8_000_to_e5": doc_top_sz8_000_to_e5,
    "doc_top_sz8_second_only_to_ff": doc_top_sz8_second_only_to_ff,
    "doc_top_sz8_first_only_to_ff": doc_top_sz8_first_only_to_ff,
    "doc_left_sz18_red_to_sz22": doc_left_sz18_red_to_sz22,
    "doc_left_sz18_red_to_sz14": doc_left_sz18_red_to_sz14,
    "doc_left_sz18_red_to_sz24": doc_left_sz18_red_to_sz24,
    "doc_left_sz18_red_to_sz12": doc_left_sz18_red_to_sz12,
    "doc_left_sz18_red_to_sz16": doc_left_sz18_red_to_sz16,
    "doc_left_sz18_red_to_sz10": doc_left_sz18_red_to_sz10,
    "doc_left_sz18_red_to_sz8": doc_left_sz18_red_to_sz8,
    "doc_left_sz18_red_to_sz6": doc_left_sz18_red_to_sz6,
    "doc_left_sz18_red_to_sz4": doc_left_sz18_red_to_sz4,
    "doc_left_sz18_red_to_sz2": doc_left_sz18_red_to_sz2,
    "doc_left_sz18_red_to_nil": doc_left_sz18_red_to_nil,
    "doc_left_sz18_red_to_sz3": doc_left_sz18_red_to_sz3,
    "doc_left_sz18_red_to_sz1": doc_left_sz18_red_to_sz1,
    "doc_top_sz18_000_to_ff": doc_top_sz18_000_to_ff,
    "doc_top_sz10_000_to_ff": doc_top_sz10_000_to_ff,
    "doc_top_sz10_000_to_red": doc_top_sz10_000_to_red,
    "doc_top_sz10_000_to_e5": doc_top_sz10_000_to_e5,
    "doc_top_sz10_000_to_d9": doc_top_sz10_000_to_d9,
    "doc_top_sz10_to_nil": doc_top_sz10_to_nil,
    # Doc+Footer EEEEEE shifts
    "doc_footer_all_eeeeee_to_e5": doc_footer_all_eeeeee_to_e5,
    "doc_footer_all_eeeeee_to_e0": doc_footer_all_eeeeee_to_e0,
    "doc_footer_all_eeeeee_to_d9": doc_footer_all_eeeeee_to_d9,
    "doc_footer_all_eeeeee_to_f0": doc_footer_all_eeeeee_to_f0,
    # Style/header inspection
    "styles_title_spacing_5_to_0": styles_title_spacing_5_to_0,
    "header_status": header_status,
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
