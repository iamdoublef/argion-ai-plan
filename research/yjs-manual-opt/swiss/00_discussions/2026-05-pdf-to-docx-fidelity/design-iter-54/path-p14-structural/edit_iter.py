"""Edit driver for iter-54: structural p14 mutations.

Recipes:
  title_color_flip      — title idx=278 "10" red→black + pBdr black→red
  title_color_flip_only — only pBdr black→red (keep "10" red)
  title_num_black       — only "10" red→black, keep pBdr black
  scissors_inject       — inject scissors decorative line paragraph before idx=306
  bold_warranty         — idx=301 split "2 年有限保修" run with bold
  bold_keyrun_wevac     — idx=284 "WEVAC TECHNOLOGY CO., LIMITED" run add bold
  bold_keyrun_argion    — idx=295 widen split "广州亚俊氏..." bold
  bold_keyrun_support305 — idx=305 split "support@wevactech.com" bold
  bullet_red_dot        — idx=302/303/304 change bullet char "•" → larger red dot
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


# =============== TITLE COLOR FLIP (idx=278) ===============
def title_color_flip(doc: str) -> tuple[str, int]:
    """Flip: '10' E63846→000000 AND pBdr 000000→E63846."""
    p = _get_paragraph(doc, 278)
    if not p:
        return doc, 0
    # Change the '10 ' run color from E63846 to 000000
    new_p = p
    # The "10 " is the first run with sz=27 color=E63846
    new_p = re.sub(
        r'(<w:rPr>\s*<w:rFonts[^/]+/>\s*<w:b/>\s*<w:sz w:val="27"/>\s*<w:color w:val=")E63846(")',
        r'\g<1>000000\g<2>',
        new_p,
    )
    # Change the pBdr left color from 000000 to E63846
    new_p = re.sub(
        r'(<w:left w:val="single" w:sz="18" w:space="4" w:color=")000000(")',
        r'\g<1>E63846\g<2>',
        new_p,
    )
    if new_p == p:
        return doc, 0
    return _replace_paragraph(doc, 278, new_p)


def title_num_black(doc: str) -> tuple[str, int]:
    """Only flip '10' E63846→000000, keep pBdr black."""
    p = _get_paragraph(doc, 278)
    if not p:
        return doc, 0
    new_p = re.sub(
        r'(<w:rPr>\s*<w:rFonts[^/]+/>\s*<w:b/>\s*<w:sz w:val="27"/>\s*<w:color w:val=")E63846(")',
        r'\g<1>000000\g<2>',
        p,
    )
    if new_p == p:
        return doc, 0
    return _replace_paragraph(doc, 278, new_p)


def title_bdr_red(doc: str) -> tuple[str, int]:
    """Only flip pBdr 000000→E63846, keep '10' red."""
    p = _get_paragraph(doc, 278)
    if not p:
        return doc, 0
    new_p = re.sub(
        r'(<w:left w:val="single" w:sz="18" w:space="4" w:color=")000000(")',
        r'\g<1>E63846\g<2>',
        p,
    )
    if new_p == p:
        return doc, 0
    return _replace_paragraph(doc, 278, new_p)


# =============== SCISSORS LINE INJECTION ===============
SCISSORS_PARA = """<w:p>
      <w:pPr>
        <w:spacing w:after="0" w:before="120" w:line="240" w:lineRule="auto"/>
        <w:jc w:val="center"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Microsoft YaHei"/>
          <w:sz w:val="14"/>
          <w:color w:val="808080"/>
          <w:spacing w:val="8"/>
        </w:rPr>
        <w:t xml:space="preserve">✂ · · · · · · · · · · · · · · · · · · · · · · · · · · · · ·</w:t>
      </w:r>
    </w:p>
    """


def scissors_inject(doc: str) -> tuple[str, int]:
    """Insert scissors line paragraph between idx=305 and idx=306 (sectPr last)."""
    # Find paragraph at idx=306 and insert before it
    matches = list(p_pat.finditer(doc))
    if len(matches) <= 306:
        return doc, 0
    m306 = matches[306]
    new_doc = doc[:m306.start()] + SCISSORS_PARA + doc[m306.start():]
    return new_doc, 1


# Alternative scissors line: use dashed bottom border on para 305 instead of new para
def scissors_via_border(doc: str) -> tuple[str, int]:
    """Add dashed bottom border below idx=305 'support email' paragraph."""
    p = _get_paragraph(doc, 305)
    if not p:
        return doc, 0
    # add pBdr block inside pPr
    if "<w:pBdr>" in p:
        return doc, 0  # already has border
    new_p = re.sub(
        r"(<w:pPr>\s*<w:spacing[^/]*/>)",
        r"""\g<1>
        <w:pBdr>
          <w:bottom w:val="dashed" w:sz="6" w:space="6" w:color="808080"/>
        </w:pBdr>""",
        p,
        count=1,
    )
    if new_p == p:
        return doc, 0
    return _replace_paragraph(doc, 305, new_p)


# =============== BOLD KEY RUNS ===============
def _set_bold_in_para(doc: str, target_idx: int, text_substr: str, bold: bool = True) -> tuple[str, int]:
    """Change <w:b w:val="0"/> to <w:b/> for run containing text_substr (or split the run)."""
    p = _get_paragraph(doc, target_idx)
    if not p:
        return doc, 0
    if text_substr not in p:
        return doc, 0
    # Simple case: run contains exactly text_substr (and only that)
    # Find run with this text
    run_pat = re.compile(r"<w:r>(.*?)</w:r>", re.S)
    new_p = p
    modified = False
    out = []
    last = 0
    for rm in run_pat.finditer(p):
        if text_substr in rm.group(0):
            run_body = rm.group(0)
            # Set bold = on
            new_body = re.sub(r'<w:b w:val="0"/>', '<w:b/>', run_body)
            if new_body == run_body:
                # No <w:b w:val="0"/> — maybe missing, inject <w:b/> in rPr
                if "<w:b/>" not in new_body:
                    new_body = re.sub(r'(<w:rPr>)', r'\g<1>\n          <w:b/>', new_body, count=1)
            if new_body != run_body:
                out.append(p[last:rm.start()])
                out.append(new_body)
                last = rm.end()
                modified = True
    out.append(p[last:])
    if not modified:
        return doc, 0
    new_p = "".join(out)
    return _replace_paragraph(doc, target_idx, new_p)


def bold_wevac(doc: str) -> tuple[str, int]:
    """idx=284 'WEVAC TECHNOLOGY CO., LIMITED' run: ensure bold."""
    return _set_bold_in_para(doc, 284, "WEVAC TECHNOLOGY CO., LIMITED")


def bold_argion(doc: str) -> tuple[str, int]:
    """idx=295 ensure '广州亚俊氏...' bold (first run)."""
    return _set_bold_in_para(doc, 295, "广州亚俊氏")


def bold_support305(doc: str) -> tuple[str, int]:
    """idx=305 split run and bold 'support@wevactech.com'."""
    p = _get_paragraph(doc, 305)
    if not p:
        return doc, 0
    if "support@wevactech.com" not in p:
        return doc, 0
    # Find the existing single run
    run_pat = re.compile(r"<w:r>(.*?)</w:r>", re.S)
    m = run_pat.search(p)
    if not m:
        return doc, 0
    run = m.group(0)
    # Extract rPr
    rpr_m = re.search(r"<w:rPr>.*?</w:rPr>", run, re.S)
    if not rpr_m:
        return doc, 0
    rpr = rpr_m.group(0)
    rpr_bold = rpr.replace('<w:b w:val="0"/>', '<w:b/>')
    if rpr_bold == rpr:
        rpr_bold = rpr.replace('<w:rPr>', '<w:rPr>\n          <w:b/>', 1)
    # split text into two parts at the email
    # text content: "向我们发送电子邮件申请保修服务： support@wevactech.com"
    text_pat = re.compile(r"<w:t[^>]*>([^<]*)</w:t>", re.S)
    tm = text_pat.search(run)
    if not tm:
        return doc, 0
    text = tm.group(1)
    if "support@wevactech.com" not in text:
        return doc, 0
    prefix, suffix = text.split("support@wevactech.com", 1)
    new_run = (
        f'<w:r>{rpr}<w:t xml:space="preserve">{prefix}</w:t></w:r>'
        f'<w:r>{rpr_bold}<w:t xml:space="preserve">support@wevactech.com</w:t></w:r>'
    )
    if suffix:
        new_run += f'<w:r>{rpr}<w:t xml:space="preserve">{suffix}</w:t></w:r>'
    new_p = p[:m.start()] + new_run + p[m.end():]
    return _replace_paragraph(doc, 305, new_p)


def bold_warranty_period(doc: str) -> tuple[str, int]:
    """idx=301: split '2 年有限保修' as bold."""
    p = _get_paragraph(doc, 301)
    if not p:
        return doc, 0
    target_str = "2 年有限保修"
    if target_str not in p:
        return doc, 0
    run_pat = re.compile(r"<w:r>(.*?)</w:r>", re.S)
    m = run_pat.search(p)
    if not m:
        return doc, 0
    run = m.group(0)
    rpr_m = re.search(r"<w:rPr>.*?</w:rPr>", run, re.S)
    rpr = rpr_m.group(0)
    rpr_bold = rpr.replace('<w:b w:val="0"/>', '<w:b/>')
    if rpr_bold == rpr:
        rpr_bold = rpr.replace('<w:rPr>', '<w:rPr>\n          <w:b/>', 1)
    text_pat = re.compile(r"<w:t[^>]*>([^<]*)</w:t>", re.S)
    tm = text_pat.search(run)
    text = tm.group(1)
    # Split text: replace first occurrence of target with bold marker
    parts = text.split(target_str, 1)
    if len(parts) != 2:
        return doc, 0
    prefix, suffix = parts
    new_run = (
        f'<w:r>{rpr}<w:t xml:space="preserve">{prefix}</w:t></w:r>'
        f'<w:r>{rpr_bold}<w:t xml:space="preserve">{target_str}</w:t></w:r>'
    )
    if suffix:
        new_run += f'<w:r>{rpr}<w:t xml:space="preserve">{suffix}</w:t></w:r>'
    new_p = p[:m.start()] + new_run + p[m.end():]
    return _replace_paragraph(doc, 301, new_p)


# =============== BULLET STYLE CHANGE ===============
def bullet_red_bigger(doc: str) -> tuple[str, int]:
    """idx=302/303/304: change bullet run font to YaHei + size 14 (was sz=11 ArialBlack)."""
    count = 0
    for idx in (302, 303, 304):
        p = _get_paragraph(doc, idx)
        if not p:
            continue
        # change first run sz=11 → sz=14, font Arial Black → Microsoft YaHei
        new_p = re.sub(
            r'(<w:rPr>\s*<w:rFonts )w:ascii="Arial Black" w:hAnsi="Arial Black" w:cs="Arial Black"( w:eastAsia="Microsoft YaHei"/>\s*<w:b/>\s*<w:sz w:val=")11(")',
            r'\g<1>w:ascii="Microsoft YaHei" w:hAnsi="Microsoft YaHei" w:cs="Microsoft YaHei"\g<2>14\g<3>',
            p,
            count=1,
        )
        if new_p != p:
            doc, _ = _replace_paragraph(doc, idx, new_p)
            count += 1
    return doc, count


def bullet_unicode_filled(doc: str) -> tuple[str, int]:
    """idx=302/303/304: replace bullet char '•' (U+2022) with '●' (BLACK CIRCLE) larger."""
    count = 0
    for idx in (302, 303, 304):
        p = _get_paragraph(doc, idx)
        if not p:
            continue
        new_p = p.replace("•    ", "●    ")
        if new_p != p:
            doc, _ = _replace_paragraph(doc, idx, new_p)
            count += 1
    return doc, count


# =============== RECIPE REGISTRY ===============
RECIPES = {
    "title_color_flip":    title_color_flip,
    "title_num_black":     title_num_black,
    "title_bdr_red":       title_bdr_red,
    "scissors_inject":     scissors_inject,
    "scissors_via_border": scissors_via_border,
    "bold_wevac":          bold_wevac,
    "bold_argion":         bold_argion,
    "bold_support305":     bold_support305,
    "bold_warranty_period": bold_warranty_period,
    "bullet_red_bigger":   bullet_red_bigger,
    "bullet_unicode_filled": bullet_unicode_filled,
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
