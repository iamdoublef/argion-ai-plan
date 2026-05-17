"""Edit driver for iter-56: attack next-max pages via pBdr color + run split.

Pages to attack (W42 baseline 7.99/11.93):
  - p14=11.93 (still max, iter-54 found pBdr=E63846 + bold warranty)
  - p3=10.96  (warnings page, 24 bullets, CH.01 banner idx=24)
  - p11=10.92 (troubleshooting table, CH.07 banner idx=202)
  - p9=10.43  (operation page, CH.06 banner idx=170)
  - p13=10.39 (CH.09 banner idx=257)
  - p10=10.01 (CH.06 continued banner idx=185)
  - p5=9.90   (CH.02 banner idx=71)
  - p12=9.79  (CH.08 banner idx=239)

Winning patterns from iter-54:
  - pBdr left color 000000→E63846 (idx=278 p14 won −0.02 max)
  - run split + bold for key text (idx=301 p14 won −0.03 max)
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SRC_UNPACKED = ROOT / "baseline_unpacked"

p_pat = re.compile(r"<w:p\b[^>]*>(.*?)</w:p>", re.S)


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


# =============== pBdr COLOR FLIP (iter-54 winning pattern) ===============
def _bdr_flip(doc: str, target_idx: int) -> tuple[str, int]:
    """Flip pBdr left w:color 000000→E63846 on a given paragraph idx."""
    p = _get_paragraph(doc, target_idx)
    if not p:
        return doc, 0
    new_p = re.sub(
        r'(<w:left w:val="single" w:sz="18" w:space="4" w:color=")000000(")',
        r'\g<1>E63846\g<2>',
        p,
    )
    if new_p == p:
        return doc, 0
    return _replace_paragraph(doc, target_idx, new_p)


def p3_bdr_red(doc: str) -> tuple[str, int]:
    """p3 CH.01 banner idx=24: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 24)


def p11_bdr_red(doc: str) -> tuple[str, int]:
    """p11 CH.07 banner idx=202: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 202)


def p9_bdr_red(doc: str) -> tuple[str, int]:
    """p9 CH.06 banner idx=170: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 170)


def p13_bdr_red(doc: str) -> tuple[str, int]:
    """p13 CH.09 banner idx=257: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 257)


def p10_bdr_red(doc: str) -> tuple[str, int]:
    """p10 CH.06 continued banner idx=185: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 185)


def p5_bdr_red(doc: str) -> tuple[str, int]:
    """p5 CH.02 banner idx=71: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 71)


def p4_bdr_red(doc: str) -> tuple[str, int]:
    """p4 CH.01 continued banner idx=55: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 55)


def p7_bdr_red(doc: str) -> tuple[str, int]:
    """p7 CH.03 banner idx=90: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 90)


def p8_bdr_red(doc: str) -> tuple[str, int]:
    """p8 CH.04 banner idx=114: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 114)


def p9_alt_bdr_red(doc: str) -> tuple[str, int]:
    """p9 CH.05 banner idx=131: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 131)


def p12_bdr_red(doc: str) -> tuple[str, int]:
    """p12 CH.08 banner idx=239: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 239)


def p15_bdr_red(doc: str) -> tuple[str, int]:
    """p15 CH.10 continued banner idx=308: pBdr left 000000→E63846."""
    return _bdr_flip(doc, 308)


def all_bdr_red(doc: str) -> tuple[str, int]:
    """Apply pBdr red to ALL chapter banners that have left color=000000.

    Per recon: idx 24, 55, 71, 90, 114, 131, 170, 185, 202, 239, 257, 308.
    """
    count = 0
    for idx in (24, 55, 71, 90, 114, 131, 170, 185, 202, 239, 257, 308):
        doc, c = _bdr_flip(doc, idx)
        count += c
    return doc, count


# =============== RUN SPLIT + BOLD (iter-54 winning pattern) ===============
def _split_and_bold(doc: str, target_idx: int, target_str: str) -> tuple[str, int]:
    """Split a run in paragraph[target_idx] at target_str and bold the matching segment."""
    p = _get_paragraph(doc, target_idx)
    if not p:
        return doc, 0
    if target_str not in p:
        return doc, 0
    # Iterate runs to find one containing target_str inside <w:t>
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


def p3_bold_warning(doc: str) -> tuple[str, int]:
    """p3 idx=26 '警告 WARNING' bold split — most prominent string on p3.

    Actually idx=26 is the title of the warnings — it may already be bold/colored.
    """
    return _split_and_bold(doc, 26, "WARNING")


def p11_bold_troubleshooting(doc: str) -> tuple[str, int]:
    """p11 idx=234 '免责声明 DISCLAIMER' — bold split.

    Per recon p11 is troubleshooting table; the disclaimer line comes after.
    """
    return _split_and_bold(doc, 234, "DISCLAIMER")


def p11_bold_check_power(doc: str) -> tuple[str, int]:
    """p11 idx=208 troubleshooting row: bold '检查电源连接及插座是否正常。'."""
    return _split_and_bold(doc, 208, "检查电源连接")


def p3_bold_household(doc: str) -> tuple[str, int]:
    """p3 idx=28 first warning bullet: bold '家庭使用' subphrase."""
    return _split_and_bold(doc, 28, "家庭使用")


# =============== TABLE CELL BORDER COLOR EXPLORATION ===============
def p11_tbl_borders_darker(doc: str) -> tuple[str, int]:
    """p11 troubleshooting table: CCCCCC → A0A0A0 (only inside this table).

    Target rendering shows borders darker than CCCCCC.
    """
    # Find the specific table containing 故障现象
    tbl_pat = re.compile(r"(<w:tbl>)(.*?)(</w:tbl>)", re.S)
    out = []
    last = 0
    count = 0
    for tm in tbl_pat.finditer(doc):
        if "故障现象" not in tm.group(2):
            continue
        body = tm.group(2)
        new_body = body.replace('w:color="CCCCCC"', 'w:color="A0A0A0"')
        if new_body == body:
            continue
        out.append(doc[last:tm.start(2)])
        out.append(new_body)
        last = tm.end(2)
        count += 1
        break
    out.append(doc[last:])
    return "".join(out), count


def p3_tbl_top_border_red(doc: str) -> tuple[str, int]:
    """p3 warning bullet table (idx 26..51): top border 000000→E63846?

    First we check — actually first cell already has E63846 top, so maybe not.
    Try: switch CCCCCC inner borders to E63846 lite.
    """
    tbl_pat = re.compile(r"(<w:tbl>)(.*?)(</w:tbl>)", re.S)
    out = []
    last = 0
    count = 0
    for tm in tbl_pat.finditer(doc):
        body = tm.group(2)
        # p3 warnings table contains the bullet text
        if "本机仅供家庭使用" not in body:
            continue
        # Are there CCCCCC borders inside? p3 uses what color borders?
        new_body = body.replace('w:color="CCCCCC"', 'w:color="A0A0A0"')
        if new_body == body:
            return doc, 0
        out.append(doc[last:tm.start(2)])
        out.append(new_body)
        last = tm.end(2)
        count += 1
        break
    out.append(doc[last:])
    return "".join(out), count


def all_cccccc_darker(doc: str) -> tuple[str, int]:
    """Global: ALL CCCCCC tcBorders → A0A0A0 (196 sites)."""
    new_doc = doc.replace('w:color="CCCCCC"', 'w:color="A0A0A0"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:color="CCCCCC"')
    return new_doc, diff


def all_cccccc_to_d9(doc: str) -> tuple[str, int]:
    """Global: ALL CCCCCC tcBorders → D9D9D9 (lighter shift)."""
    new_doc = doc.replace('w:color="CCCCCC"', 'w:color="D9D9D9"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:color="CCCCCC"')
    return new_doc, diff


def all_cccccc_to_bbbbbb(doc: str) -> tuple[str, int]:
    """Global: ALL CCCCCC → BBBBBB (slightly darker)."""
    new_doc = doc.replace('w:color="CCCCCC"', 'w:color="BBBBBB"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:color="CCCCCC"')
    return new_doc, diff


def all_d9d9d9_to_cccccc(doc: str) -> tuple[str, int]:
    """Global: ALL D9D9D9 → CCCCCC (slightly darker for p14 tables)."""
    new_doc = doc.replace('w:color="D9D9D9"', 'w:color="CCCCCC"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:color="D9D9D9"')
    return new_doc, diff


def all_d9d9d9_lighter_e5(doc: str) -> tuple[str, int]:
    """Global: D9D9D9 → E5E5E5 (lighter)."""
    new_doc = doc.replace('w:color="D9D9D9"', 'w:color="E5E5E5"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:color="D9D9D9"')
    return new_doc, diff


def all_d9d9d9_lighter_dd(doc: str) -> tuple[str, int]:
    """Global: D9D9D9 → DDDDDD (slightly lighter)."""
    new_doc = doc.replace('w:color="D9D9D9"', 'w:color="DDDDDD"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:color="D9D9D9"')
    return new_doc, diff


def all_d9d9d9_darker(doc: str) -> tuple[str, int]:
    """Global: D9D9D9 → BFBFBF (darker)."""
    new_doc = doc.replace('w:color="D9D9D9"', 'w:color="BFBFBF"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:color="D9D9D9"')
    return new_doc, diff


def all_d9d9d9_to_e0(doc: str) -> tuple[str, int]:
    """Global: D9D9D9 → E0E0E0."""
    new_doc = doc.replace('w:color="D9D9D9"', 'w:color="E0E0E0"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:color="D9D9D9"')
    return new_doc, diff


def p11_header_shade_2a(doc: str) -> tuple[str, int]:
    """p11 header shade 1A1A1A → 2A2A2A (slightly lighter dark)."""
    tbl_pat = re.compile(r"(<w:tbl>)(.*?)(</w:tbl>)", re.S)
    out = []
    last = 0
    count = 0
    for tm in tbl_pat.finditer(doc):
        body = tm.group(2)
        if "故障现象" not in body:
            continue
        new_body = body.replace('w:fill="1A1A1A"', 'w:fill="2A2A2A"')
        if new_body == body:
            return doc, 0
        out.append(doc[last:tm.start(2)])
        out.append(new_body)
        last = tm.end(2)
        count += 1
        break
    out.append(doc[last:])
    return "".join(out), count


def all_shd_1a_to_000(doc: str) -> tuple[str, int]:
    """Global: shd fill 1A1A1A → 000000 (15 sites — all dark header rows)."""
    new_doc = doc.replace('w:fill="1A1A1A"', 'w:fill="000000"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:fill="1A1A1A"')
    return new_doc, diff


def all_shd_1a_to_111(doc: str) -> tuple[str, int]:
    """Global: shd fill 1A1A1A → 111111 (between dark)."""
    new_doc = doc.replace('w:fill="1A1A1A"', 'w:fill="111111"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:fill="1A1A1A"')
    return new_doc, diff


def all_shd_1a_to_080(doc: str) -> tuple[str, int]:
    """Global: shd fill 1A1A1A → 080808 (very near black)."""
    new_doc = doc.replace('w:fill="1A1A1A"', 'w:fill="080808"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:fill="1A1A1A"')
    return new_doc, diff


def all_shd_1a_to_222(doc: str) -> tuple[str, int]:
    """Global: shd fill 1A1A1A → 222222 (lighter than 1A)."""
    new_doc = doc.replace('w:fill="1A1A1A"', 'w:fill="222222"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:fill="1A1A1A"')
    return new_doc, diff


def all_shd_1a_to_2a(doc: str) -> tuple[str, int]:
    """Global: shd fill 1A1A1A → 2A2A2A (slightly lighter)."""
    new_doc = doc.replace('w:fill="1A1A1A"', 'w:fill="2A2A2A"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:fill="1A1A1A"')
    return new_doc, diff


def all_shd_f1f1f6_to_white(doc: str) -> tuple[str, int]:
    """Global: shd fill F1F1F6 → FFFFFF (eliminate alt-row stripe)."""
    new_doc = doc.replace('w:fill="F1F1F6"', 'w:fill="FFFFFF"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:fill="F1F1F6"')
    return new_doc, diff


def all_shd_f1f1f6_to_f5(doc: str) -> tuple[str, int]:
    """Global: shd fill F1F1F6 → F5F5F5 (slightly different gray)."""
    new_doc = doc.replace('w:fill="F1F1F6"', 'w:fill="F5F5F5"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:fill="F1F1F6"')
    return new_doc, diff


def p3_line230_to_240(doc: str) -> tuple[str, int]:
    """p3 paragraphs 28..51 (24 warnings bullets): line=230 → 240 (UP +10 twips)."""
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
            r'(<w:spacing[^/]*?w:line=")230(")',
            r'\g<1>240\g<2>',
            p,
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p3_line230_to_220(doc: str) -> tuple[str, int]:
    """p3 paragraphs 28..51: line=230 → 220 (DOWN −10 twips)."""
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
            r'(<w:spacing[^/]*?w:line=")230(")',
            r'\g<1>220\g<2>',
            p,
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p3_bullet_after_24(doc: str) -> tuple[str, int]:
    """p3 bullets after=27 → 24 (slightly tighter spacing between bullets)."""
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
            r'\g<1>24\g<2>',
            p,
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p3_bullet_after_30(doc: str) -> tuple[str, int]:
    """p3 bullets after=27 → 30 (slightly looser)."""
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
            r'\g<1>30\g<2>',
            p,
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p3_bullet_after_20(doc: str) -> tuple[str, int]:
    """p3 bullets after=27 → 20 (tighter)."""
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
            r'\g<1>20\g<2>',
            p,
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p11_line240_to_250(doc: str) -> tuple[str, int]:
    """p11 paragraphs 203..232 (troubleshoot table): line=240 → 250 (UP)."""
    targets = set(range(203, 233))
    count = 0
    paras = list(p_pat.finditer(doc))
    out = []
    last = 0
    for i, m in enumerate(paras):
        if i not in targets:
            continue
        p = m.group(0)
        new_p = re.sub(
            r'(<w:spacing[^/]*?w:line=")240(")',
            r'\g<1>250\g<2>',
            p,
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def p14_line240_to_250(doc: str) -> tuple[str, int]:
    """iter-55 lever: p14 paragraphs 281..304 minus {291, 300, 301}:
    w:line='240' → w:line='250' (UP +10 twips on the line-240 cohort).
    21 sites: 18 table rows + 3 bullets.
    """
    targets = set(range(281, 305)) - {291, 300, 301}
    count = 0
    paras = list(p_pat.finditer(doc))
    out = []
    last = 0
    for i, m in enumerate(paras):
        if i not in targets:
            continue
        p = m.group(0)
        new_p = re.sub(
            r'(<w:spacing[^/]*?w:line=")240(")',
            r'\g<1>250\g<2>',
            p,
        )
        if new_p == p:
            continue
        out.append(doc[last:m.start()])
        out.append(new_p)
        last = m.end()
        count += 1
    out.append(doc[last:])
    return "".join(out), count


def all_shd_f1f1f6_to_e6(doc: str) -> tuple[str, int]:
    """Global: shd fill F1F1F6 → E6E6E6 (slightly darker)."""
    new_doc = doc.replace('w:fill="F1F1F6"', 'w:fill="E6E6E6"')
    if new_doc == doc:
        return doc, 0
    diff = doc.count('w:fill="F1F1F6"')
    return new_doc, diff


def p11_header_shade_000(doc: str) -> tuple[str, int]:
    """p11 header shade 1A1A1A → 000000 (full black)."""
    tbl_pat = re.compile(r"(<w:tbl>)(.*?)(</w:tbl>)", re.S)
    out = []
    last = 0
    count = 0
    for tm in tbl_pat.finditer(doc):
        body = tm.group(2)
        if "故障现象" not in body:
            continue
        new_body = body.replace('w:fill="1A1A1A"', 'w:fill="000000"')
        if new_body == body:
            return doc, 0
        out.append(doc[last:tm.start(2)])
        out.append(new_body)
        last = tm.end(2)
        count += 1
        break
    out.append(doc[last:])
    return "".join(out), count


def p11_tbl_borders_red_subtle(doc: str) -> tuple[str, int]:
    """p11 troubleshoot table: CCCCCC → E63846 lite (subtle red wash)?
    Use F5BCC2 (light red) to slightly tint the row lines.
    """
    tbl_pat = re.compile(r"(<w:tbl>)(.*?)(</w:tbl>)", re.S)
    out = []
    last = 0
    count = 0
    for tm in tbl_pat.finditer(doc):
        body = tm.group(2)
        if "故障现象" not in body:
            continue
        new_body = body.replace('w:color="CCCCCC"', 'w:color="F5BCC2"')
        if new_body == body:
            return doc, 0
        out.append(doc[last:tm.start(2)])
        out.append(new_body)
        last = tm.end(2)
        count += 1
        break
    out.append(doc[last:])
    return "".join(out), count


# =============== RECIPE REGISTRY ===============
RECIPES = {
    # iter-54 pattern A: pBdr color flip on per-page chapter banners
    "p3_bdr_red":      p3_bdr_red,
    "p4_bdr_red":      p4_bdr_red,
    "p5_bdr_red":      p5_bdr_red,
    "p7_bdr_red":      p7_bdr_red,
    "p8_bdr_red":      p8_bdr_red,
    "p9_bdr_red":      p9_bdr_red,
    "p9_alt_bdr_red":  p9_alt_bdr_red,
    "p10_bdr_red":     p10_bdr_red,
    "p11_bdr_red":     p11_bdr_red,
    "p12_bdr_red":     p12_bdr_red,
    "p13_bdr_red":     p13_bdr_red,
    "p15_bdr_red":     p15_bdr_red,
    "all_bdr_red":     all_bdr_red,
    # iter-54 pattern B: run split + bold
    "p3_bold_warning":         p3_bold_warning,
    "p11_bold_troubleshooting": p11_bold_troubleshooting,
    "p11_bold_check_power":    p11_bold_check_power,
    "p3_bold_household":       p3_bold_household,
    # iter-56 new structural levers: table border colors
    "p11_tbl_borders_darker":    p11_tbl_borders_darker,
    "p3_tbl_top_border_red":     p3_tbl_top_border_red,
    "all_cccccc_darker":         all_cccccc_darker,
    "all_cccccc_to_d9":          all_cccccc_to_d9,
    "all_cccccc_to_bbbbbb":      all_cccccc_to_bbbbbb,
    "all_d9d9d9_to_cccccc":      all_d9d9d9_to_cccccc,
    "p11_tbl_borders_red_subtle": p11_tbl_borders_red_subtle,
    "all_d9d9d9_lighter_e5":     all_d9d9d9_lighter_e5,
    "all_d9d9d9_lighter_dd":     all_d9d9d9_lighter_dd,
    "all_d9d9d9_darker":         all_d9d9d9_darker,
    "all_d9d9d9_to_e0":          all_d9d9d9_to_e0,
    "p11_header_shade_2a":       p11_header_shade_2a,
    "p11_header_shade_000":      p11_header_shade_000,
    "all_shd_1a_to_000":         all_shd_1a_to_000,
    "all_shd_1a_to_111":         all_shd_1a_to_111,
    "all_shd_1a_to_080":         all_shd_1a_to_080,
    "all_shd_1a_to_222":         all_shd_1a_to_222,
    "all_shd_1a_to_2a":          all_shd_1a_to_2a,
    "all_shd_f1f1f6_to_white":   all_shd_f1f1f6_to_white,
    "all_shd_f1f1f6_to_f5":      all_shd_f1f1f6_to_f5,
    "all_shd_f1f1f6_to_e6":      all_shd_f1f1f6_to_e6,
    "p14_line240_to_250":        p14_line240_to_250,
    "p3_line230_to_240":         p3_line230_to_240,
    "p3_line230_to_220":         p3_line230_to_220,
    "p11_line240_to_250":        p11_line240_to_250,
    "p3_bullet_after_24":        p3_bullet_after_24,
    "p3_bullet_after_30":        p3_bullet_after_30,
    "p3_bullet_after_20":        p3_bullet_after_20,
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
