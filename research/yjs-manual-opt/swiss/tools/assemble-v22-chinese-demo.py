#!/usr/bin/env python3
"""Assemble a V22 Chinese demo DOCX — full-text translation.

Reads the V22 source DOCX, replaces ALL text (cover, TOC, paragraphs,
tables) with Simplified Chinese from a translation JSON, preserving
all original formatting, images, and layout.

Usage:
    python tools/assemble-v22-chinese-demo.py
    python tools/assemble-v22-chinese-demo.py --source path/to/v22.docx
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import defusedxml.minidom

# ── Paths ─────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
SWISS_DIR = SCRIPT_DIR.parent
DEFAULT_SOURCE = (
    SWISS_DIR.parent / '_inbox' / 'V22 Vacuum Sealer-User Manual-20260206.docx'
)
OUTPUT_DIR = SWISS_DIR / 'output'
TRANSLATIONS_JSON = SCRIPT_DIR / 'v22-cn-translations.json'


# ── Load translations ────────────────────────────────────────────────────

def load_translations(path: Path) -> dict:
    """Load translation JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ── XML helpers ──────────────────────────────────────────────────────────

def get_body_elements(dom):
    """Return (body_node, [element_children])."""
    body = dom.getElementsByTagName('w:body')[0]
    return body, [n for n in body.childNodes if n.nodeType == n.ELEMENT_NODE]


def get_style_id(elem):
    """Get w:pStyle val for a paragraph, or None."""
    if elem.tagName != 'w:p':
        return None
    for child in elem.childNodes:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == 'w:pPr':
            for sub in child.childNodes:
                if (sub.nodeType == sub.ELEMENT_NODE
                        and sub.tagName == 'w:pStyle'):
                    return sub.getAttribute('w:val')
    return None


def get_text(elem):
    """Concatenate all w:t descendant text."""
    parts = []
    for t in elem.getElementsByTagName('w:t'):
        if t.firstChild and t.firstChild.data:
            parts.append(t.firstChild.data)
    return ''.join(parts).strip()


def has_drawing(elem):
    """Check if element contains w:drawing (embedded image)."""
    return len(elem.getElementsByTagName('w:drawing')) > 0


def node_has_ancestor(node, tag_names: set[str]) -> bool:
    """Return True if node has any ancestor whose tagName is in tag_names."""
    parent = node.parentNode
    while parent is not None:
        if getattr(parent, 'tagName', None) in tag_names:
            return True
        parent = parent.parentNode
    return False


def get_text_nodes(paragraph, *, include_textboxes: bool) -> list:
    """Collect text nodes, optionally excluding textbox/shape content."""
    blocked = {'w:txbxContent', 'v:textbox'}
    nodes = []
    for t_node in paragraph.getElementsByTagName('w:t'):
        if not include_textboxes and node_has_ancestor(t_node, blocked):
            continue
        nodes.append(t_node)
    return nodes


def contains_cjk(text: str) -> bool:
    """Return True when text includes CJK characters."""
    return bool(re.search(r'[\u3400-\u9fff\uf900-\ufaff]', text))


def replace_text_inline(paragraph, new_text, dom_doc, *, include_textboxes: bool = True):
    """Replace paragraph text while preserving images and non-text elements.

    Unlike replace_text_preserving_format, this function:
    - Does NOT remove runs that contain w:drawing elements
    - Only modifies w:t text nodes
    - Puts all new text into the first w:t, clears the rest
    """
    t_nodes = get_text_nodes(paragraph, include_textboxes=include_textboxes)
    if not t_nodes:
        return
    for idx, t_node in enumerate(t_nodes):
        if idx == 0:
            if t_node.firstChild:
                t_node.firstChild.data = new_text
            else:
                t_node.appendChild(dom_doc.createTextNode(new_text))
            t_node.setAttribute('xml:space', 'preserve')
        else:
            if t_node.firstChild:
                t_node.firstChild.data = ''


def replace_text_preserving_format(paragraph, new_text, dom_doc):
    """Replace text while preserving the original paragraph skeleton.

    The earlier version removed sibling runs for cleanliness. That damaged
    page-breaks, anchors and other layout controls stored in those runs.
    Fidelity is better when we keep the paragraph structure intact.
    """
    replace_text_inline(paragraph, new_text, dom_doc)


def normalize_cjk_run_fonts(dom_doc, east_asia_font: str | None = None) -> int:
    """Set eastAsia font on runs containing Chinese text.

    This keeps the source style system intact while preventing Word from
    falling back to mixed body fonts for injected Chinese content.
    """
    east_asia_font = east_asia_font or CN_FONT
    updated = 0
    for run in dom_doc.getElementsByTagName('w:r'):
        texts = []
        for t_node in run.getElementsByTagName('w:t'):
            if t_node.firstChild and t_node.firstChild.data:
                texts.append(t_node.firstChild.data)
        joined = ''.join(texts)
        if not joined or not contains_cjk(joined):
            continue

        rpr = None
        for child in run.childNodes:
            if child.nodeType == child.ELEMENT_NODE and child.tagName == 'w:rPr':
                rpr = child
                break
        if rpr is None:
            rpr = dom_doc.createElement('w:rPr')
            if run.firstChild is not None:
                run.insertBefore(rpr, run.firstChild)
            else:
                run.appendChild(rpr)

        rfonts = None
        for child in rpr.childNodes:
            if child.nodeType == child.ELEMENT_NODE and child.tagName == 'w:rFonts':
                rfonts = child
                break
        if rfonts is None:
            rfonts = dom_doc.createElement('w:rFonts')
            rpr.appendChild(rfonts)

        if rfonts.getAttribute('w:eastAsia') != east_asia_font:
            rfonts.setAttribute('w:eastAsia', east_asia_font)
            updated += 1
    return updated


def split_mixed_figure_paragraphs(dom_doc) -> int:
    """Split paragraphs that mix floating figure captions and list-step text.

    In the V22 source, some operation steps store the floating figure caption
    and the actual list sentence in the same paragraph. When Chinese text is
    injected, Word can reflow that sentence into the figure area. We split the
    sentence into its own numbered paragraph and leave the original paragraph
    as a pure figure/caption carrier.
    """
    body = dom_doc.getElementsByTagName('w:body')[0]
    paragraphs = [
        node for node in body.childNodes
        if getattr(node, 'tagName', None) == 'w:p'
    ]
    changed = 0

    for paragraph in paragraphs:
        full_text = get_text(paragraph)
        if not has_drawing(paragraph):
            continue
        if not re.match(r'^Figure\s*\d+(?:Figure\s*\d+)+', full_text):
            continue

        body_text_nodes = get_text_nodes(paragraph, include_textboxes=False)
        body_text = ''.join(
            (node.firstChild.data if node.firstChild else '')
            for node in body_text_nodes
        ).strip()
        if not body_text:
            continue

        ppr = None
        for child in paragraph.childNodes:
            if getattr(child, 'tagName', None) == 'w:pPr':
                ppr = child
                break
        if ppr is None:
            continue

        # Build a new numbered paragraph for the actual step text.
        new_para = dom_doc.createElement('w:p')
        new_para.appendChild(ppr.cloneNode(deep=True))

        template_run = None
        for child in paragraph.childNodes:
            if getattr(child, 'tagName', None) != 'w:r':
                continue
            text_nodes = [
                n for n in child.getElementsByTagName('w:t')
                if not node_has_ancestor(n, {'w:txbxContent', 'v:textbox'})
            ]
            if text_nodes:
                template_run = child
                break
        if template_run is None:
            continue

        new_run = dom_doc.createElement('w:r')
        for child in template_run.childNodes:
            if getattr(child, 'tagName', None) == 'w:rPr':
                new_run.appendChild(child.cloneNode(deep=True))
                break
        new_text = dom_doc.createElement('w:t')
        new_text.setAttribute('xml:space', 'preserve')
        new_text.appendChild(dom_doc.createTextNode(body_text))
        new_run.appendChild(new_text)
        new_para.appendChild(new_run)

        body.insertBefore(new_para, paragraph)

        # Remove numbering from the figure-only paragraph so only the new
        # paragraph carries the list item number.
        for child in list(ppr.childNodes):
            if getattr(child, 'tagName', None) == 'w:numPr':
                ppr.removeChild(child)

        for node in body_text_nodes:
            if node.firstChild:
                node.firstChild.data = ''

        changed += 1

    return changed


def pack_docx(input_dir: Path, output_path: Path) -> None:
    """ZIP a directory into a .docx file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in input_dir.rglob('*'):
            if f.is_file():
                zf.write(f, f.relative_to(input_dir).as_posix())


# ── Typography optimization ──────────────────────────────────────────────

# Target Chinese font (already used in H1/H3 styles of the source DOCX)
CN_FONT = 'HarmonyOS Sans SC'

# Old fonts to unify → CN_FONT
_REPLACE_FONTS = ('宋体', '微软雅黑')


def optimize_chinese_typography(tmp_dir: Path) -> dict:
    """Post-process DOCX XML files to improve Chinese typography.

    Fixes applied:
    1. Replace 宋体/微软雅黑 → HarmonyOS Sans SC across all XML files
    2. Update theme fallback font for Hans (CJK Simplified) script
    3. Add w:eastAsia attribute to rFonts elements missing it
    4. Ensure CN_FONT is registered in fontTable.xml

    Returns stats dict.
    """
    stats = {'fonts_replaced': 0, 'theme_fixed': False, 'eastasia_added': 0}

    xml_files = [
        tmp_dir / 'word' / 'styles.xml',
        tmp_dir / 'word' / 'document.xml',
    ]

    # ── 1. Unify fonts in styles.xml and document.xml ──
    for xml_path in xml_files:
        if not xml_path.exists():
            continue
        text = xml_path.read_text(encoding='utf-8')
        for old_font in _REPLACE_FONTS:
            count = text.count(f'"{old_font}"')
            text = text.replace(f'"{old_font}"', f'"{CN_FONT}"')
            stats['fonts_replaced'] += count
        xml_path.write_text(text, encoding='utf-8')

    # ── 2. Add w:eastAsia to rFonts missing it (document.xml) ──
    doc_path = tmp_dir / 'word' / 'document.xml'
    if doc_path.exists():
        text = doc_path.read_text(encoding='utf-8')
        added = [0]  # mutable counter for closure

        def _add_eastasia(m: re.Match) -> str:
            tag = m.group(0)
            # Skip if any eastAsia attribute already present
            if 'eastAsia' in tag:
                return tag
            added[0] += 1
            return tag.replace('/>', f' w:eastAsia="{CN_FONT}"/>')

        text = re.sub(r'<w:rFonts [^>]*?/>', _add_eastasia, text)
        stats['eastasia_added'] = added[0]
        doc_path.write_text(text, encoding='utf-8')

    # ── 3. Patch theme1.xml Hans script font ──
    theme_path = tmp_dir / 'word' / 'theme' / 'theme1.xml'
    if theme_path.exists():
        text = theme_path.read_text(encoding='utf-8')
        patched = re.sub(
            r'<a:font script="Hans" typeface="[^"]*"',
            f'<a:font script="Hans" typeface="{CN_FONT}"',
            text,
        )
        if patched != text:
            stats['theme_fixed'] = True
            theme_path.write_text(patched, encoding='utf-8')

    # ── 4. Register CN_FONT in fontTable.xml if absent ──
    ft_path = tmp_dir / 'word' / 'fontTable.xml'
    if ft_path.exists():
        text = ft_path.read_text(encoding='utf-8')
        if CN_FONT not in text:
            entry = (
                f'<w:font w:name="{CN_FONT}">'
                '<w:charset w:val="86"/>'
                '<w:family w:val="swiss"/>'
                '<w:pitch w:val="variable"/>'
                '</w:font>'
            )
            text = text.replace('</w:fonts>', entry + '</w:fonts>')
            ft_path.write_text(text, encoding='utf-8')

    return stats


def preserve_reference_typography(_: Path) -> dict:
    """No-op typography strategy used for fidelity-first output."""
    return {'fonts_replaced': 0, 'theme_fixed': False, 'eastasia_added': 0}


# ── Matching helpers ─────────────────────────────────────────────────────

def strip_toc_page_number(text: str) -> str:
    """Remove trailing page number from TOC entry text."""
    return re.sub(r'\d+$', '', text).strip()


def normalize_quotes(text: str) -> str:
    """Normalize smart quotes and degree symbols for matching."""
    return (text
            .replace('\u201c', '"').replace('\u201d', '"')  # smart double quotes
            .replace('\u2018', "'").replace('\u2019', "'")  # smart single quotes
            .replace('\u00ba', '\u00b0')                    # º -> °
            )


def find_paragraph_match(text: str, paragraphs: dict) -> str | None:
    """Find translation by exact match first, then normalized/substring match."""
    # Exact match
    if text in paragraphs:
        return paragraphs[text]
    # Normalized match
    norm = normalize_quotes(text)
    for eng, chn in paragraphs.items():
        if normalize_quotes(eng) == norm:
            return chn
    # Substring match (for paragraphs with Figure prefixes)
    for eng, chn in paragraphs.items():
        if eng in text or normalize_quotes(eng) in norm:
            return chn
    return None


# ── Table translation ────────────────────────────────────────────────────

def translate_tables(dom, tables_map: dict, dom_doc) -> dict:
    """Translate all table cells. Returns stats."""
    stats = {'cells': 0}
    all_tables = dom.getElementsByTagName('w:tbl')
    # Merge all table sub-maps into one lookup
    cell_map = {}
    for sub in tables_map.values():
        cell_map.update(sub)

    for tbl in all_tables:
        cells = tbl.getElementsByTagName('w:tc')
        for cell in cells:
            cell_text = get_text(cell)
            if not cell_text:
                continue
            cn = cell_map.get(cell_text)
            if cn is not None:
                # Replace text in cell paragraphs
                for cp in cell.getElementsByTagName('w:p'):
                    cp_text = get_text(cp)
                    if cp_text and cp_text in cell_map:
                        replace_text_inline(cp, cell_map[cp_text], dom_doc)
                        stats['cells'] += 1
    return stats


# ── Core logic ───────────────────────────────────────────────────────────

def assemble_chinese_demo(source_docx: Path, output_path: Path,
                          translations: dict,
                          *,
                          fidelity_first: bool = True) -> dict:
    """Build the Chinese demo DOCX. Returns stats dict."""
    cover_map = translations['cover']
    toc_map = translations['toc']
    para_map = translations['paragraphs']
    tables_map = translations['tables']

    stats = {
        'cover': 0,
        'toc': 0,
        'chapter_titles': 0,
        'section_titles': 0,
        'body_paragraphs': 0,
        'table_cells': 0,
        'total_elements': 0,
        'unmatched': [],
    }

    with tempfile.TemporaryDirectory(prefix='v22-cn-demo-') as tmp:
        tmp_dir = Path(tmp) / 'docx'
        with zipfile.ZipFile(source_docx, 'r') as zf:
            zf.extractall(tmp_dir)

        doc_xml_path = tmp_dir / 'word' / 'document.xml'
        dom = defusedxml.minidom.parse(str(doc_xml_path))
        dom_doc = dom
        _, elements = get_body_elements(dom)
        stats['total_elements'] = len(elements)

        for elem in elements:
            if elem.tagName != 'w:p':
                continue

            style = get_style_id(elem)
            text = get_text(elem)
            if not text:
                continue

            img = has_drawing(elem)
            body_text_nodes = get_text_nodes(elem, include_textboxes=False)
            pure_figure_caption = bool(
                re.fullmatch(r'Figure\s*\d+(?:Figure\s*\d+)?', text)
            )
            if img and not body_text_nodes and pure_figure_caption:
                stats['unmatched'].append(f'figure-caption:{text!r}')
                continue

            if img and body_text_nodes:
                replacer = lambda para, value, doc: replace_text_inline(
                    para,
                    value,
                    doc,
                    include_textboxes=False,
                )
            else:
                replacer = replace_text_inline if img else replace_text_preserving_format

            # ── Cover text (style=None, early paragraphs) ──
            if style is None and text in cover_map:
                replacer(elem, cover_map[text], dom_doc)
                stats['cover'] += 1
                print(f'  cover: {text!r} -> {cover_map[text]!r}')
                continue

            # ── TOC heading ──
            if style is None and text == 'Table of Contents' and 'Table of Contents' in toc_map:
                replacer(elem, toc_map['Table of Contents'], dom_doc)
                stats['toc'] += 1
                print(f'  toc-title: {text!r} -> {toc_map["Table of Contents"]!r}')
                continue

            # ── TOC entries (style=10 or 11) ──
            if style in ('10', '11'):
                stripped = strip_toc_page_number(text)
                cn = toc_map.get(stripped)
                if cn is not None:
                    # Replace only the text part, keep page number
                    page_num = text[len(text) - len(text.lstrip(stripped)):] if stripped != text else ''
                    # Actually: find the page number suffix
                    m = re.search(r'(\d+)$', text)
                    page_suffix = m.group(1) if m else ''
                    replace_text_inline(elem, cn + page_suffix, dom_doc)
                    stats['toc'] += 1
                    print(f'  toc: {stripped!r} -> {cn!r}')
                else:
                    stats['unmatched'].append(f'toc:{text!r}')
                continue

            # ── Chapter titles (style=2) ──
            if style == '2':
                cn = find_paragraph_match(text, para_map)
                if cn is not None:
                    replacer(elem, cn, dom_doc)
                    stats['chapter_titles'] += 1
                    print(f'  h1: {text[:50]!r} -> {cn!r}')
                else:
                    stats['unmatched'].append(f'h1:{text[:60]!r}')
                continue

            # ── Section titles (style=3) ──
            if style == '3':
                cn = find_paragraph_match(text, para_map)
                if cn is not None:
                    replacer(elem, cn, dom_doc)
                    stats['section_titles'] += 1
                    print(f'  h2: {text[:50]!r} -> {cn!r}')
                else:
                    stats['unmatched'].append(f'h2:{text[:60]!r}')
                continue

            # ── Body paragraphs (style=41, 50, None) ──
            if style in ('41', '50', None):
                cn = find_paragraph_match(text, para_map)
                if cn is not None:
                    replacer(elem, cn, dom_doc)
                    stats['body_paragraphs'] += 1
                else:
                    stats['unmatched'].append(f's{style or "N"}:{text[:60]!r}')
                continue

        # ── Translate tables ──
        tbl_stats = translate_tables(dom, tables_map, dom_doc)
        stats['table_cells'] = tbl_stats['cells']
        stats['mixed_figure_paragraphs_split'] = split_mixed_figure_paragraphs(dom_doc)
        stats['cjk_runs_normalized'] = normalize_cjk_run_fonts(dom_doc)

        # Write modified XML
        doc_xml_path.write_bytes(dom.toxml(encoding='utf-8'))

        # Preserving the original Word typography is usually closer to the
        # approved reference file than globally normalizing fonts.
        typography_fn = (
            preserve_reference_typography if fidelity_first
            else optimize_chinese_typography
        )
        typo_stats = typography_fn(tmp_dir)
        stats['typography'] = typo_stats
        print(f'\n  Typography: {typo_stats["fonts_replaced"]} fonts unified, '
              f'{typo_stats["eastasia_added"]} eastAsia added, '
              f'theme={"fixed" if typo_stats["theme_fixed"] else "ok"}')

        # Pack output
        pack_docx(tmp_dir, output_path)

    return stats


# ── Main ─────────────────────────────────────────────────────────────────

def main() -> None:
    sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(
        description='Assemble V22 Chinese demo DOCX — full text translation.',
    )
    parser.add_argument(
        '--source', type=Path, default=DEFAULT_SOURCE,
        help='Path to source V22 DOCX',
    )
    parser.add_argument(
        '--output', type=Path, default=OUTPUT_DIR / 'v22-wevac-cn-demo.docx',
        help='Output path',
    )
    parser.add_argument(
        '--translations', type=Path, default=TRANSLATIONS_JSON,
        help='Translation JSON path',
    )
    parser.add_argument(
        '--normalize-typography', action='store_true',
        help='Apply the old font-normalization pass instead of preserving '
             'the reference file typography.',
    )
    args = parser.parse_args()

    source: Path = args.source.resolve()
    output: Path = args.output.resolve()
    trans_path: Path = args.translations.resolve()

    if not source.exists():
        print(f'ERROR: source not found: {source}')
        raise SystemExit(1)
    if not trans_path.exists():
        print(f'ERROR: translations not found: {trans_path}')
        raise SystemExit(1)

    print(f'Source: {source}')
    print(f'Translations: {trans_path}')
    print(f'Output: {output}')
    print()

    translations = load_translations(trans_path)
    stats = assemble_chinese_demo(
        source,
        output,
        translations,
        fidelity_first=not args.normalize_typography,
    )

    print()
    print(f'Done! Output: {output}')
    print(f'  File size: {output.stat().st_size:,} bytes')
    print(f'  Total elements: {stats["total_elements"]}')
    print(f'  Cover: {stats["cover"]}/{len(translations["cover"])}')
    print(f'  TOC: {stats["toc"]}/{len(translations["toc"])}')
    print(f'  Chapter titles (H1): {stats["chapter_titles"]}/9')
    print(f'  Section titles (H2): {stats["section_titles"]}/17')
    print(f'  Body paragraphs: {stats["body_paragraphs"]}')
    print(f'  Table cells: {stats["table_cells"]}')

    total_replaced = (stats['cover'] + stats['toc'] + stats['chapter_titles']
                      + stats['section_titles'] + stats['body_paragraphs']
                      + stats['table_cells'])
    print(f'  TOTAL replaced: {total_replaced}')

    if stats['unmatched']:
        print(f'\n  WARN: {len(stats["unmatched"])} unmatched paragraphs:')
        for u in stats['unmatched'][:20]:
            print(f'    {u}')
        if len(stats['unmatched']) > 20:
            print(f'    ... and {len(stats["unmatched"]) - 20} more')


if __name__ == '__main__':
    main()
