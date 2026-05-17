"""Edit driver for iter-57 path-color-mismatch.

Building on iter-56 W43 (7.76/10.94), this iter attacks document-level
color mismatches that PIL sampling of target PDF revealed:

  - Red in PDF target: #E03840  (NOT E63846 / E63946)
  - Black text: pure 000000 across most areas, but baseline has 1A1A1A text
  - Gray: 8E8E93 is used; PDF shows 8E8E93 ~ #888888-#A0A0A0 range

Levers:
  - all_red_e63846_to_e03840 — text + border color flips for red
  - all_color_1a_to_000 — w:color val=1A1A1A → 000000 (text color, NOT shd)
  - gray_8e_*  — explore 8E8E93 → other values
  - p3 iter-54 pattern overlays
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"

p_pat = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.S)


# =============== HELPERS ===============
def _replace_paragraph(doc: str, target_idx: int, new_para: str) -> tuple[str, int]:
    parts = []
    last = 0
    found = 0
    for i, m in enumerate(p_pat.finditer(doc)):
        if i == target_idx:
            parts.append(doc[last:m.start()])
            parts.append(new_para)
            last = m.end()
            found = 1
            break
    parts.append(doc[last:])
    return "".join(parts), found


def _get_paragraph(doc: str, target_idx: int) -> str | None:
    for i, m in enumerate(p_pat.finditer(doc)):
        if i == target_idx:
            return m.group(0)
    return None


# =============== RED COLOR FLIPS ===============
def all_red_e63846_to_e03840(doc: str) -> tuple[str, int]:
    """Global E63846 → E03840 (text color w:color val + border w:color)."""
    n1 = doc.count('w:val="E63846"')
    n2 = doc.count('w:color="E63846"')
    new_doc = doc.replace('w:val="E63846"', 'w:val="E03840"')
    new_doc = new_doc.replace('w:color="E63846"', 'w:color="E03840"')
    return new_doc, n1 + n2


def all_red_e63846_to_d90000(doc: str) -> tuple[str, int]:
    """E63846 → D90000 (pure-er red)."""
    n1 = doc.count('w:val="E63846"')
    n2 = doc.count('w:color="E63846"')
    new_doc = doc.replace('w:val="E63846"', 'w:val="D90000"')
    new_doc = new_doc.replace('w:color="E63846"', 'w:color="D90000"')
    return new_doc, n1 + n2


def all_red_e63846_to_e60012(doc: str) -> tuple[str, int]:
    """E63846 → E60012 (similar saturation but slight hue shift)."""
    n1 = doc.count('w:val="E63846"')
    n2 = doc.count('w:color="E63846"')
    new_doc = doc.replace('w:val="E63846"', 'w:val="E60012"')
    new_doc = new_doc.replace('w:color="E63846"', 'w:color="E60012"')
    return new_doc, n1 + n2


def all_red_e63846_to_dc3545(doc: str) -> tuple[str, int]:
    """E63846 → DC3545 (Bootstrap red)."""
    n1 = doc.count('w:val="E63846"')
    n2 = doc.count('w:color="E63846"')
    new_doc = doc.replace('w:val="E63846"', 'w:val="DC3545"')
    new_doc = new_doc.replace('w:color="E63846"', 'w:color="DC3545"')
    return new_doc, n1 + n2


# =============== BLACK TEXT COLOR FLIPS ===============
def all_text_1a_to_000(doc: str) -> tuple[str, int]:
    """Global text color val=1A1A1A → 000000 (126 sites)."""
    n = doc.count('w:val="1A1A1A"')
    new_doc = doc.replace('w:val="1A1A1A"', 'w:val="000000"')
    return new_doc, n


def all_text_1a_to_080(doc: str) -> tuple[str, int]:
    """Global text 1A1A1A → 080808."""
    n = doc.count('w:val="1A1A1A"')
    new_doc = doc.replace('w:val="1A1A1A"', 'w:val="080808"')
    return new_doc, n


def all_text_1a_to_111(doc: str) -> tuple[str, int]:
    """Global text 1A1A1A → 111111."""
    n = doc.count('w:val="1A1A1A"')
    new_doc = doc.replace('w:val="1A1A1A"', 'w:val="111111"')
    return new_doc, n


# =============== GRAY TEXT FLIPS ===============
def all_gray_8e_to_888(doc: str) -> tuple[str, int]:
    """Global 8E8E93 → 888888."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="888888"')
    return new_doc, n


def all_gray_8e_to_a0(doc: str) -> tuple[str, int]:
    """Global 8E8E93 → A0A0A0."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="A0A0A0"')
    return new_doc, n


def all_gray_8e_to_999(doc: str) -> tuple[str, int]:
    """Global 8E8E93 → 999999."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="999999"')
    return new_doc, n


def all_gray_8e_to_b0(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> B0B0B0."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="B0B0B0"')
    return new_doc, n


def all_gray_8e_to_bf(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> BFBFBF (much lighter)."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="BFBFBF"')
    return new_doc, n


def all_gray_8e_to_a8(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> A8A8A8."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="A8A8A8"')
    return new_doc, n


def all_gray_8e_to_c0(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> C0C0C0 (lighter)."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="C0C0C0"')
    return new_doc, n


def all_gray_8e_to_c8(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> C8C8C8 (lighter)."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="C8C8C8"')
    return new_doc, n


def all_gray_8e_to_d0(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> D0D0D0 (lighter)."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="D0D0D0"')
    return new_doc, n


def all_gray_8e_to_d8(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> D8D8D8 (very light)."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="D8D8D8"')
    return new_doc, n


def all_gray_8e_to_e0(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> E0E0E0 (very light gray)."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="E0E0E0"')
    return new_doc, n


def all_gray_8e_to_e8(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> E8E8E8 (lighter)."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="E8E8E8"')
    return new_doc, n


def all_gray_8e_to_ec(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> ECECEC."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="ECECEC"')
    return new_doc, n


def all_gray_8e_to_f0(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> F0F0F0."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="F0F0F0"')
    return new_doc, n


def all_gray_8e_to_f5(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> F5F5F5."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="F5F5F5"')
    return new_doc, n


def all_gray_8e_to_fa(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> FAFAFA."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="FAFAFA"')
    return new_doc, n


def all_gray_8e_to_fc(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> FCFCFC."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="FCFCFC"')
    return new_doc, n


def all_gray_8e_to_fe(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> FEFEFE (near white)."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="FEFEFE"')
    return new_doc, n


def all_gray_8e_to_ff(doc: str) -> tuple[str, int]:
    """Global 8E8E93 -> FFFFFF (white, effectively hidden)."""
    n = doc.count('w:val="8E8E93"')
    new_doc = doc.replace('w:val="8E8E93"', 'w:val="FFFFFF"')
    return new_doc, n


# =============== P3-SPECIFIC LEVERS ===============
def p3_bold_warning_header(doc: str) -> tuple[str, int]:
    """p3 idx=26 '警告 WARNING' — bold the text run if present.

    The title of p3 warnings should be visually prominent. Try bolding part.
    """
    return _split_and_bold(doc, 26, "WARNING")


def p3_bold_household(doc: str) -> tuple[str, int]:
    """p3 idx=28 first bullet: bold '家庭使用'."""
    return _split_and_bold(doc, 28, "家庭使用")


def _split_and_bold(doc: str, target_idx: int, target_str: str) -> tuple[str, int]:
    """Split a run in paragraph[target_idx] at target_str and bold the matching segment."""
    p = _get_paragraph(doc, target_idx)
    if not p:
        return doc, 0
    if target_str not in p:
        return doc, 0
    run_pat = re.compile(r"<w:r>(.*?)</w:r>", re.S)
    text_pat = re.compile(r"<w:t[^>]*>([^<]*)</w:t>", re.S)
    for m in run_pat.finditer(p):
        run = m.group(0)
        tm = text_pat.search(run)
        if not tm:
            continue
        text = tm.group(1)
        if target_str not in text:
            continue
        rpr_m = re.search(r"<w:rPr>.*?</w:rPr>", run, re.S)
        if not rpr_m:
            continue
        rpr = rpr_m.group(0)
        rpr_bold = rpr.replace('<w:b w:val="0"/>', '<w:b/>')
        if rpr_bold == rpr:
            if "<w:b/>" not in rpr:
                rpr_bold = rpr.replace('<w:rPr>', '<w:rPr>\n          <w:b/>', 1)
        parts = text.split(target_str, 1)
        if len(parts) != 2:
            return doc, 0
        prefix, suffix = parts
        new_run = ""
        if prefix:
            new_run += f'<w:r>{rpr}<w:t xml:space="preserve">{prefix}</w:t></w:r>'
        new_run += f'<w:r>{rpr_bold}<w:t xml:space="preserve">{target_str}</w:t></w:r>'
        if suffix:
            new_run += f'<w:r>{rpr}<w:t xml:space="preserve">{suffix}</w:t></w:r>'
        new_p = p[:m.start()] + new_run + p[m.end():]
        return _replace_paragraph(doc, target_idx, new_p)
    return doc, 0


# =============== P3 SIZE / SPACING LEVERS ===============
def p3_bullets_sz_13_to_14(doc: str) -> tuple[str, int]:
    """p3 bullets idx 28..51 body text sz=13 -> 14 (bigger text)."""
    targets = set(range(28, 52))
    count = 0
    paras = list(p_pat.finditer(doc))
    out = []
    last = 0
    for i, m in enumerate(paras):
        if i not in targets:
            continue
        p = m.group(0)
        # only flip the sz=13 inside the body run (not the bullet sz=10)
        new_p = re.sub(
            r'(<w:sz w:val=")13(")',
            r'\g<1>14\g<2>',
            p, count=1
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p3_bullets_sz_13_to_15(doc: str) -> tuple[str, int]:
    """p3 bullets sz=13 -> 15."""
    targets = set(range(28, 52))
    count = 0
    paras = list(p_pat.finditer(doc))
    out = []
    last = 0
    for i, m in enumerate(paras):
        if i not in targets:
            continue
        p = m.group(0)
        new_p = re.sub(
            r'(<w:sz w:val=")13(")',
            r'\g<1>15\g<2>',
            p, count=1
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p3_bullets_after_22(doc: str) -> tuple[str, int]:
    """p3 bullets after=27 -> 22."""
    targets = set(range(28, 52))
    count = 0
    paras = list(p_pat.finditer(doc))
    out = []
    last = 0
    for i, m in enumerate(paras):
        if i not in targets:
            continue
        p = m.group(0)
        new_p = re.sub(
            r'(<w:spacing[^/]*?w:after=")27(")',
            r'\g<1>22\g<2>',
            p, count=1
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p3_bullets_left_red_border(doc: str) -> tuple[str, int]:
    """Add red left border (pBdr left E03840 sz=6) to all p3 bullets idx 28..51."""
    targets = set(range(28, 52))
    count = 0
    paras = list(p_pat.finditer(doc))
    out = []
    last = 0
    for i, m in enumerate(paras):
        if i not in targets:
            continue
        p = m.group(0)
        # Add pBdr inside pPr
        if "<w:pBdr>" in p:
            # already has — skip
            continue
        new_p = re.sub(
            r'(<w:pPr>)\s*(<w:spacing[^/]*/>)',
            r'\1\n<w:pBdr><w:left w:val="single" w:sz="6" w:space="4" w:color="E03840"/></w:pBdr>\n\2',
            p, count=1
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p3_bullets_left_red_border_thick(doc: str) -> tuple[str, int]:
    """Add THICK red left border sz=12 to all p3 bullets."""
    targets = set(range(28, 52))
    count = 0
    paras = list(p_pat.finditer(doc))
    out = []
    last = 0
    for i, m in enumerate(paras):
        if i not in targets:
            continue
        p = m.group(0)
        if "<w:pBdr>" in p:
            continue
        new_p = re.sub(
            r'(<w:pPr>)\s*(<w:spacing[^/]*/>)',
            r'\1\n<w:pBdr><w:left w:val="single" w:sz="12" w:space="4" w:color="E03840"/></w:pBdr>\n\2',
            p, count=1
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p3_bullets_red_box(doc: str) -> tuple[str, int]:
    """Add red border on left+right (full box) to all p3 bullets."""
    targets = set(range(28, 52))
    count = 0
    paras = list(p_pat.finditer(doc))
    out = []
    last = 0
    for i, m in enumerate(paras):
        if i not in targets:
            continue
        p = m.group(0)
        if "<w:pBdr>" in p:
            continue
        # Order: left, right (no top/bottom for inner bullets)
        bdr = ('<w:pBdr>'
               '<w:left w:val="single" w:sz="6" w:space="6" w:color="E03840"/>'
               '<w:right w:val="single" w:sz="6" w:space="6" w:color="E03840"/>'
               '</w:pBdr>')
        new_p = re.sub(
            r'(<w:pPr>)\s*(<w:spacing[^/]*/>)',
            rf'\1\n{bdr}\n\2',
            p, count=1
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p3_bullets_box_top_bottom(doc: str) -> tuple[str, int]:
    """Add top border to idx=27 and bottom border to idx=51 (red)."""
    count = 0
    # idx=27 (image paragraph) — add top
    p27 = _get_paragraph(doc, 27)
    if p27 and "<w:pBdr>" not in p27:
        bdr = '<w:pBdr><w:top w:val="single" w:sz="6" w:space="4" w:color="E03840"/></w:pBdr>'
        new_p27 = re.sub(r'(<w:pPr>)', rf'\1\n{bdr}\n', p27, count=1)
        if new_p27 != p27:
            doc, c = _replace_paragraph(doc, 27, new_p27)
            count += c
    # idx=51 (last bullet) — add bottom
    p51 = _get_paragraph(doc, 51)
    if p51 and "<w:pBdr>" not in p51:
        bdr = '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="4" w:color="E03840"/></w:pBdr>'
        new_p51 = re.sub(r'(<w:pPr>)', rf'\1\n{bdr}\n', p51, count=1)
        if new_p51 != p51:
            doc, c = _replace_paragraph(doc, 51, new_p51)
            count += c
    return doc, count


def p11_disclaimer_box(doc: str) -> tuple[str, int]:
    """Wrap p11 DISCLAIMER (idx 234, 235) with a black border box.

    Order required by CT_PBdr schema: top, left, bottom, right, between, bar.
    idx 234 = '免责声明 DISCLAIMER' header → add top + left + right
    idx 235 = body → add left + bottom + right
    """
    count = 0
    p234 = _get_paragraph(doc, 234)
    if p234 and "<w:pBdr>" not in p234:
        bdr = ('<w:pBdr>'
               '<w:top w:val="single" w:sz="6" w:space="6" w:color="000000"/>'
               '<w:left w:val="single" w:sz="6" w:space="6" w:color="000000"/>'
               '<w:right w:val="single" w:sz="6" w:space="6" w:color="000000"/>'
               '</w:pBdr>')
        new_p = re.sub(r'(<w:pPr>)', rf'\1\n{bdr}\n', p234, count=1)
        if new_p != p234:
            doc, c = _replace_paragraph(doc, 234, new_p)
            count += c
    p235 = _get_paragraph(doc, 235)
    if p235 and "<w:pBdr>" not in p235:
        # NOTE order: left, bottom, right
        bdr = ('<w:pBdr>'
               '<w:left w:val="single" w:sz="6" w:space="6" w:color="000000"/>'
               '<w:bottom w:val="single" w:sz="6" w:space="6" w:color="000000"/>'
               '<w:right w:val="single" w:sz="6" w:space="6" w:color="000000"/>'
               '</w:pBdr>')
        new_p = re.sub(r'(<w:pPr>)', rf'\1\n{bdr}\n', p235, count=1)
        if new_p != p235:
            doc, c = _replace_paragraph(doc, 235, new_p)
            count += c
    return doc, count


def p3_warning_box(doc: str) -> tuple[str, int]:
    """Wrap p3 warning section (idx 26..51) with red border box.

    Order: top, left, bottom, right.
    """
    count = 0
    # idx=26: top+left+right
    p26 = _get_paragraph(doc, 26)
    if p26 and "<w:pBdr>" not in p26:
        bdr = ('<w:pBdr>'
               '<w:top w:val="single" w:sz="6" w:space="6" w:color="E63846"/>'
               '<w:left w:val="single" w:sz="6" w:space="6" w:color="E63846"/>'
               '<w:right w:val="single" w:sz="6" w:space="6" w:color="E63846"/>'
               '</w:pBdr>')
        new_p = re.sub(r'(<w:pPr>)', rf'\1\n{bdr}\n', p26, count=1)
        if new_p != p26:
            doc, c = _replace_paragraph(doc, 26, new_p)
            count += c
    # idx 27..50: left+right only
    for idx in range(27, 51):
        p = _get_paragraph(doc, idx)
        if not p or "<w:pBdr>" in p:
            continue
        bdr = ('<w:pBdr>'
               '<w:left w:val="single" w:sz="6" w:space="6" w:color="E63846"/>'
               '<w:right w:val="single" w:sz="6" w:space="6" w:color="E63846"/>'
               '</w:pBdr>')
        if "<w:pPr>" not in p:
            new_p = p.replace("<w:p>", f"<w:p>\n<w:pPr>{bdr}</w:pPr>", 1)
        else:
            new_p = re.sub(r'(<w:pPr>)', rf'\1\n{bdr}\n', p, count=1)
        if new_p != p:
            doc, c = _replace_paragraph(doc, idx, new_p)
            count += c
    # idx=51: left+bottom+right
    p51 = _get_paragraph(doc, 51)
    if p51 and "<w:pBdr>" not in p51:
        bdr = ('<w:pBdr>'
               '<w:left w:val="single" w:sz="6" w:space="6" w:color="E63846"/>'
               '<w:bottom w:val="single" w:sz="6" w:space="6" w:color="E63846"/>'
               '<w:right w:val="single" w:sz="6" w:space="6" w:color="E63846"/>'
               '</w:pBdr>')
        new_p = re.sub(r'(<w:pPr>)', rf'\1\n{bdr}\n', p51, count=1)
        if new_p != p51:
            doc, c = _replace_paragraph(doc, 51, new_p)
            count += c
    return doc, count


def p3_title_sz_27_to_28(doc: str) -> tuple[str, int]:
    """p3 idx=24 title '01 安全须知' sz=27 -> 28."""
    p = _get_paragraph(doc, 24)
    if not p:
        return doc, 0
    new_p = re.sub(
        r'(<w:sz w:val=")27(")',
        r'\g<1>28\g<2>',
        p, count=1
    )
    if new_p == p:
        return doc, 0
    return _replace_paragraph(doc, 24, new_p)


# =============== RECIPE REGISTRY ===============
RECIPES = {
    "all_red_e63846_to_e03840": all_red_e63846_to_e03840,
    "all_red_e63846_to_d90000": all_red_e63846_to_d90000,
    "all_red_e63846_to_e60012": all_red_e63846_to_e60012,
    "all_red_e63846_to_dc3545": all_red_e63846_to_dc3545,
    "all_text_1a_to_000":  all_text_1a_to_000,
    "all_text_1a_to_080":  all_text_1a_to_080,
    "all_text_1a_to_111":  all_text_1a_to_111,
    "all_gray_8e_to_888":  all_gray_8e_to_888,
    "all_gray_8e_to_a0":   all_gray_8e_to_a0,
    "all_gray_8e_to_999":  all_gray_8e_to_999,
    "all_gray_8e_to_b0":   all_gray_8e_to_b0,
    "all_gray_8e_to_bf":   all_gray_8e_to_bf,
    "all_gray_8e_to_a8":   all_gray_8e_to_a8,
    "all_gray_8e_to_c0":   all_gray_8e_to_c0,
    "all_gray_8e_to_c8":   all_gray_8e_to_c8,
    "all_gray_8e_to_d0":   all_gray_8e_to_d0,
    "all_gray_8e_to_d8":   all_gray_8e_to_d8,
    "all_gray_8e_to_e0":   all_gray_8e_to_e0,
    "all_gray_8e_to_e8":   all_gray_8e_to_e8,
    "all_gray_8e_to_ec":   all_gray_8e_to_ec,
    "all_gray_8e_to_f0":   all_gray_8e_to_f0,
    "all_gray_8e_to_f5":   all_gray_8e_to_f5,
    "all_gray_8e_to_fa":   all_gray_8e_to_fa,
    "all_gray_8e_to_fc":   all_gray_8e_to_fc,
    "all_gray_8e_to_fe":   all_gray_8e_to_fe,
    "all_gray_8e_to_ff":   all_gray_8e_to_ff,
    "p3_bold_warning_header": p3_bold_warning_header,
    "p3_bold_household":   p3_bold_household,
    "p3_bullets_sz_13_to_14": p3_bullets_sz_13_to_14,
    "p3_bullets_sz_13_to_15": p3_bullets_sz_13_to_15,
    "p3_bullets_after_22":    p3_bullets_after_22,
    "p3_title_sz_27_to_28":   p3_title_sz_27_to_28,
    "p3_bullets_left_red_border": p3_bullets_left_red_border,
    "p3_bullets_left_red_border_thick": p3_bullets_left_red_border_thick,
    "p3_bullets_red_box":     p3_bullets_red_box,
    "p3_bullets_box_top_bottom": p3_bullets_box_top_bottom,
    "p11_disclaimer_box":      p11_disclaimer_box,
    "p3_warning_box":          p3_warning_box,
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
    # Auto-propagate gray flips to footer files (they have 8E8E93 too).
    gray_map = {
        "888": "888888", "999": "999999", "a0": "A0A0A0", "a8": "A8A8A8",
        "b0": "B0B0B0", "bf": "BFBFBF", "c0": "C0C0C0", "c8": "C8C8C8",
        "d0": "D0D0D0", "d8": "D8D8D8", "e0": "E0E0E0", "e8": "E8E8E8",
        "ec": "ECECEC", "f0": "F0F0F0", "f5": "F5F5F5", "fa": "FAFAFA",
        "fc": "FCFCFC", "fe": "FEFEFE", "ff": "FFFFFF",
    }
    for name in names:
        if name.startswith("all_gray_8e_to_"):
            key = name.split("_")[-1]
            tgt = gray_map.get(key)
            if not tgt:
                continue
            n_total = 0
            for fp in (out_unpacked / "word").glob("footer*.xml"):
                c = fp.read_text(encoding="utf-8")
                n = c.count('w:val="8E8E93"')
                if n > 0:
                    fp.write_text(c.replace('w:val="8E8E93"', f'w:val="{tgt}"'), encoding="utf-8")
                    n_total += n
            print(f"  also flipped {n_total} sites in footer*.xml: 8E8E93 -> {tgt}")
    return count


if __name__ == "__main__":
    iter_name = sys.argv[1]
    recipe = sys.argv[2]
    if "," in recipe:
        recipe = recipe.split(",")
    apply_recipe(iter_name, recipe)
