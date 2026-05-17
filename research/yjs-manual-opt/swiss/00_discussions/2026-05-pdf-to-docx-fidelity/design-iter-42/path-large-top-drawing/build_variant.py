"""Build candidate DOCX from baseline_unpacked, applying patches.

Patches are dicts of:
  pgmar:  {sect_idx (1-based): {'top'|'bottom'|'left'|'right': new_value (int twips)}}
  drawing_extent: list of {'index': i, 'dcx': delta_emu, 'dcy': delta_emu}
  drawing_pos:    list of {'index': i, 'h': posH_off_delta, 'v': posV_off_delta}
  drawing_to_anchor: list of indexes to convert inline -> anchor
  tc_margin: {'top'|'bottom'|'left'|'right': delta_twips}   (applied to ALL tcMar globally)
  tc_margin_per_tbl: {tbl_idx (0-based): {'top'|...: delta}}
  trheight: {tbl_idx: {row_idx (0-based): delta_twips}} or 'all': delta
  bullet_ind: {numId: {'left': delta, 'hanging': delta}}  applied in numbering.xml

Usage:
  from build_variant import build
  build(unpacked_dir, output_docx_path, patches={...})

Use pack.py from docx skill.
"""
import os
import re
import shutil
import subprocess
import sys

DOCX_SKILL_DIR = r'C:\Users\iamdo\.claude\skills\docx\scripts\office'
sys.path.insert(0, DOCX_SKILL_DIR)


def apply_pgmar_patches(xml: str, patches: dict) -> str:
    """patches: {sect_idx (1-based): {'top'|'bottom'|'left'|'right': new_val}}"""
    if not patches:
        return xml
    # Find each sectPr -> pgMar block
    sect_iter = re.finditer(r'<w:pgMar([^/]*)/>', xml)
    blocks = list(sect_iter)
    new_xml = []
    last = 0
    for i, m in enumerate(blocks):
        idx = i + 1
        new_xml.append(xml[last:m.start()])
        attrs_str = m.group(1)
        if idx in patches:
            for key, val in patches[idx].items():
                # Replace exact w:{key}="..." with new value
                attrs_str = re.sub(
                    rf'w:{key}="[^"]*"',
                    f'w:{key}="{val}"',
                    attrs_str,
                )
        new_xml.append(f'<w:pgMar{attrs_str}/>')
        last = m.end()
    new_xml.append(xml[last:])
    return ''.join(new_xml)


def apply_drawing_extent(xml: str, ops: list) -> str:
    """Modify <wp:extent cx=".." cy=".."/> by index across all <w:drawing>.
    ops: [{'index':int, 'dcx':int_emu, 'dcy':int_emu}]"""
    if not ops:
        return xml
    op_by_idx = {o['index']: o for o in ops}
    matches = list(re.finditer(r'<wp:extent\s+cx="(\d+)"\s+cy="(\d+)"\s*/>', xml))
    out = []
    last = 0
    for i, m in enumerate(matches):
        out.append(xml[last:m.start()])
        cx, cy = int(m.group(1)), int(m.group(2))
        if i in op_by_idx:
            dcx = op_by_idx[i].get('dcx', 0)
            dcy = op_by_idx[i].get('dcy', 0)
            cx += dcx
            cy += dcy
        out.append(f'<wp:extent cx="{cx}" cy="{cy}"/>')
        last = m.end()
    out.append(xml[last:])
    return ''.join(out)


def apply_drawing_inline_offset(xml: str, ops: list) -> str:
    """For <wp:inline> drawings (inline anchored), add <wp:positionH>/V offsets by injecting distT/B/L/R or by changing distT.
    Simpler: change wp:inline distT distB distL distR by delta_emu.
    ops: [{'index':int, 'distT':d, 'distB':d, 'distL':d, 'distR':d}]"""
    if not ops:
        return xml
    op_by_idx = {o['index']: o for o in ops}
    # match opening inline tag
    matches = list(re.finditer(r'<wp:inline[^>]*>', xml))
    out = []
    last = 0
    for i, m in enumerate(matches):
        out.append(xml[last:m.start()])
        tag = m.group(0)
        if i in op_by_idx:
            for key in ('distT', 'distB', 'distL', 'distR'):
                delta = op_by_idx[i].get(key, 0)
                if delta == 0:
                    continue
                m2 = re.search(rf'{key}="(\d+)"', tag)
                if m2:
                    new_val = max(0, int(m2.group(1)) + delta)
                    tag = re.sub(rf'{key}="\d+"', f'{key}="{new_val}"', tag)
                else:
                    # insert into tag attributes
                    tag = tag.replace('<wp:inline', f'<wp:inline {key}="{max(0, delta)}"', 1)
        out.append(tag)
        last = m.end()
    out.append(xml[last:])
    return ''.join(out)


def apply_tc_margin_global(xml: str, deltas: dict) -> str:
    """Apply delta_twips to all <w:tcMar>/<w:top|bottom|left|right|start|end w:w='..' w:type='dxa'/></w:tcMar>
    Accepts side names: top, bottom, left/start, right/end. Maps left->start, right->end automatically."""
    if not deltas:
        return xml
    # build effective deltas mapping all sides
    def get_delta(side):
        if side in deltas:
            return deltas[side]
        if side == 'start' and 'left' in deltas:
            return deltas['left']
        if side == 'end' and 'right' in deltas:
            return deltas['right']
        return 0
    def repl_tcmar(m):
        inner = m.group(1)
        for side in ('top', 'bottom', 'left', 'right', 'start', 'end'):
            delta = get_delta(side)
            if delta == 0:
                continue
            def side_repl(sm):
                w = int(sm.group(1))
                new_w = max(0, w + delta)
                return f'<w:{side} w:w="{new_w}" w:type="dxa"/>'
            inner = re.sub(rf'<w:{side}\s+w:w="(\d+)"\s+w:type="dxa"\s*/>', side_repl, inner)
        return f'<w:tcMar>{inner}</w:tcMar>'
    return re.sub(r'<w:tcMar>(.*?)</w:tcMar>', repl_tcmar, xml, flags=re.DOTALL)


def apply_trheight_global(xml: str, delta: int) -> str:
    """Apply delta_twips to all <w:trHeight w:val="..."/>"""
    if not delta:
        return xml
    def repl(m):
        val = int(m.group(1))
        new_val = max(0, val + delta)
        return m.group(0).replace(f'w:val="{val}"', f'w:val="{new_val}"')
    return re.sub(r'<w:trHeight\s+w:val="(\d+)"[^/]*/>', repl, xml)


def apply_bullet_indent(numbering_xml: str, ops: dict) -> str:
    """ops: {numId or 'all': {'left': delta, 'hanging': delta, 'firstLine': delta}}"""
    if not ops:
        return numbering_xml
    if 'all' in ops:
        # Apply global to all <w:ind ... in numbering
        delta_left = ops['all'].get('left', 0)
        delta_hanging = ops['all'].get('hanging', 0)
        def repl(m):
            tag = m.group(0)
            if delta_left != 0:
                m2 = re.search(r'w:left="(\d+)"', tag)
                if m2:
                    new_v = max(0, int(m2.group(1)) + delta_left)
                    tag = re.sub(r'w:left="\d+"', f'w:left="{new_v}"', tag)
            if delta_hanging != 0:
                m2 = re.search(r'w:hanging="(\d+)"', tag)
                if m2:
                    new_v = max(0, int(m2.group(1)) + delta_hanging)
                    tag = re.sub(r'w:hanging="\d+"', f'w:hanging="{new_v}"', tag)
            return tag
        return re.sub(r'<w:ind[^/]*/>', repl, numbering_xml)
    return numbering_xml


def build(src_unpacked: str, out_unpacked: str, out_docx: str, patches: dict):
    if os.path.exists(out_unpacked):
        shutil.rmtree(out_unpacked)
    shutil.copytree(src_unpacked, out_unpacked)
    # document.xml
    doc_path = os.path.join(out_unpacked, 'word', 'document.xml')
    with open(doc_path, 'r', encoding='utf-8') as f:
        xml = f.read()
    if 'pgmar' in patches:
        xml = apply_pgmar_patches(xml, patches['pgmar'])
    if 'drawing_extent' in patches:
        xml = apply_drawing_extent(xml, patches['drawing_extent'])
    if 'drawing_inline' in patches:
        xml = apply_drawing_inline_offset(xml, patches['drawing_inline'])
    if 'tc_margin_global' in patches:
        xml = apply_tc_margin_global(xml, patches['tc_margin_global'])
    if 'trheight_global' in patches:
        xml = apply_trheight_global(xml, patches['trheight_global'])
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    # numbering.xml
    if 'bullet_ind' in patches:
        num_path = os.path.join(out_unpacked, 'word', 'numbering.xml')
        if os.path.exists(num_path):
            with open(num_path, 'r', encoding='utf-8') as f:
                nxml = f.read()
            nxml = apply_bullet_indent(nxml, patches['bullet_ind'])
            with open(num_path, 'w', encoding='utf-8') as f:
                f.write(nxml)
    # pack
    if os.path.exists(out_docx):
        os.remove(out_docx)
    r = subprocess.run([sys.executable, os.path.join(DOCX_SKILL_DIR, 'pack.py'), out_unpacked, out_docx], capture_output=True, text=True)
    if r.returncode != 0:
        print('PACK STDERR:', r.stderr)
        raise RuntimeError(f'pack failed: {r.returncode}')
    return r.stdout


if __name__ == '__main__':
    pass
