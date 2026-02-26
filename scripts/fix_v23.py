#!/usr/bin/env python3
"""
V23 说明书修复脚本
修复以下问题：
C02 - 双句号语法错误
C03 - Note 重复4次
C04 - 错别字"其他事务"→"其他食物"
C05 - Pulse Vac 按键名称"手动密封"→"手动抽气"
C08 - 删除 Vesta / ADVANCED 品牌，只保留 Wevac
C09 - 标记客服邮箱占位符
C12 - 章节标题统一（感谢→感谢语）
C14 - 感谢语统一
L01 - 绿色表头改为浅灰 #F2F2F2
L02 - 删除红色编辑注释段落
L03 - 浮动图片转嵌入式（记录，XML层面处理）
L04 - 页边距统一为 720 twips (12.7mm)
"""

import copy
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# 命名空间
W  = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
R  = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

ET.register_namespace('wpc', 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas')
ET.register_namespace('cx',  'http://schemas.microsoft.com/office/drawing/2014/chartex')
ET.register_namespace('mc',  'http://schemas.openxmlformats.org/markup-compatibility/2006')
ET.register_namespace('aink','http://schemas.microsoft.com/office/drawing/2016/ink')
ET.register_namespace('am3d','http://schemas.microsoft.com/office/drawing/2017/model3d')
ET.register_namespace('o',   'urn:schemas-microsoft-com:office:office')
ET.register_namespace('oel', 'http://schemas.microsoft.com/office/2019/extlst')
ET.register_namespace('r',   'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
ET.register_namespace('m',   'http://schemas.openxmlformats.org/officeDocument/2006/math')
ET.register_namespace('v',   'urn:schemas-microsoft-com:vml')
ET.register_namespace('wp14','http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing')
ET.register_namespace('wp',  'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing')
ET.register_namespace('w10', 'urn:schemas-microsoft-com:office:word')
ET.register_namespace('w',   'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
ET.register_namespace('w14', 'http://schemas.microsoft.com/office/word/2010/wordml')
ET.register_namespace('w15', 'http://schemas.microsoft.com/office/word/2012/wordml')
ET.register_namespace('w16cex','http://schemas.microsoft.com/office/word/2018/wordml/cex')
ET.register_namespace('w16cid','http://schemas.microsoft.com/office/word/2016/wordml/cid')
ET.register_namespace('w16', 'http://schemas.microsoft.com/office/word/2018/wordml')
ET.register_namespace('w16sdtdh','http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash')
ET.register_namespace('w16se','http://schemas.microsoft.com/office/word/2015/wordml/symex')
ET.register_namespace('wpg', 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup')
ET.register_namespace('wpi', 'http://schemas.microsoft.com/office/word/2010/wordprocessingInk')
ET.register_namespace('wne', 'http://schemas.microsoft.com/office/word/2006/wordml')
ET.register_namespace('wps', 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape')
ET.register_namespace('a',   'http://schemas.openxmlformats.org/drawingml/2006/main')
ET.register_namespace('pic', 'http://schemas.openxmlformats.org/drawingml/2006/picture')
ET.register_namespace('w16du','http://schemas.microsoft.com/office/word/2023/wordml/word16du')

def tag(ns, local):
    return f'{{{ns}}}{local}'

def get_para_text(para):
    texts = [t.text for t in para.findall('.//' + tag(W, 't')) if t.text]
    return ''.join(texts)

def replace_text_in_run(run, old, new):
    """在 run 的所有 w:t 中替换文字"""
    for t in run.findall(tag(W, 't')):
        if t.text and old in t.text:
            t.text = t.text.replace(old, new)

def replace_text_in_para(para, old, new):
    """在段落的所有 run 中替换文字"""
    for run in para.findall('.//' + tag(W, 'r')):
        replace_text_in_run(run, old, new)

def fix_document(doc_path: Path, fixes_log: list):
    tree = ET.parse(str(doc_path))
    root = tree.getroot()
    body = root.find('.//' + tag(W, 'body'))
    paras = body.findall('.//' + tag(W, 'p'))

    # ── C02: 修复双句号 ──────────────────────────────────────────
    # "...使用。。" → 拆成两句
    for para in paras:
        text = get_para_text(para)
        if '使用本机严禁在有易燃易爆气体的环境中使用。。' in text:
            # 找到包含这段文字的 run，替换
            for run in para.findall('.//' + tag(W, 'r')):
                for t in run.findall(tag(W, 't')):
                    if t.text and '使用本机严禁' in t.text:
                        t.text = t.text.replace(
                            '使用本机严禁在有易燃易爆气体的环境中使用。。',
                            '使用本机。'
                        )
                        fixes_log.append('C02: 修复双句号（第一句）')
                    elif t.text and '严禁在有易燃易爆气体' in t.text and '使用本机' not in t.text:
                        pass  # 已在上面处理

    # 更精确：找到整个段落文字包含双句号的情况
    for para in paras:
        text = get_para_text(para)
        if '。。' in text:
            replace_text_in_para(para, '。。', '。')
            fixes_log.append(f'C02: 修复双句号: {text[:50]}')

    # ── C03: 删除重复的 Note（保留第一个，删除后3个）──────────────
    note_text = '发热器温度很高'
    note_paras_found = []
    for para in paras:
        if note_text in get_para_text(para):
            note_paras_found.append(para)

    # 第一个出现的 Note 段落里可能包含重复文字，先清理
    if note_paras_found:
        first_note = note_paras_found[0]
        first_text = get_para_text(first_note)
        # 如果第一个段落里文字重复了（Note...Note...），只保留一份
        if first_text.count('发热器温度很高') > 1:
            # 找到第一个 t 元素，截断重复
            for run in first_note.findall('.//' + tag(W, 'r')):
                for t in run.findall(tag(W, 't')):
                    if t.text and '发热器温度很高' in t.text:
                        # 只保留第一次出现到句末
                        idx = t.text.find('Note：')
                        if idx >= 0:
                            end = t.text.find('！', idx)
                            if end >= 0:
                                t.text = t.text[idx:end+1]
                        break
            fixes_log.append('C03: 清理第一个Note段落内的重复文字')

        # 删除后续重复的 Note 段落（第2、3个）
        for dup_para in note_paras_found[1:]:
            parent = body
            # 找父元素
            for elem in body.iter():
                if dup_para in list(elem):
                    parent = elem
                    break
            try:
                parent.remove(dup_para)
                fixes_log.append('C03: 删除重复Note段落')
            except ValueError:
                pass

    # ── C04: 错别字 ──────────────────────────────────────────────
    for para in paras:
        if '其他事务' in get_para_text(para):
            replace_text_in_para(para, '其他事务', '其他食物')
            fixes_log.append('C04: 修复错别字"其他事务"→"其他食物"')

    # ── C05: Pulse Vac 按键名称 ──────────────────────────────────
    for para in paras:
        if 'Pulse Vac（手动密封）' in get_para_text(para):
            replace_text_in_para(para, 'Pulse Vac（手动密封）', 'Pulse Vac（手动抽气）')
            fixes_log.append('C05: 修复Pulse Vac按键名称')

    # ── C08: 删除 Vesta 和 ADVANCED 品牌段落，只保留 Wevac ────────
    brands_to_remove = [
        'Precision Appliance Technology',
        'ADVANCED CUISINE TECHNOLOGY',
        'vestaprecision.com',
        'thespacetec.com',
        'Bellevue',
        'Singapore',
        'Paya Lebar',
    ]
    paras_to_remove = []
    for para in paras:
        text = get_para_text(para)
        for brand in brands_to_remove:
            if brand in text:
                paras_to_remove.append(para)
                fixes_log.append(f'C08: 删除品牌段落: {text[:50]}')
                break

    for para in paras_to_remove:
        for elem in body.iter():
            if para in list(elem):
                try:
                    elem.remove(para)
                except ValueError:
                    pass
                break

    # ── C09: 标记客服邮箱占位符 ──────────────────────────────────
    for para in paras:
        text = get_para_text(para)
        if '请按需填写客服邮箱地址' in text:
            replace_text_in_para(para, '（请按需填写客服邮箱地址）', '【请填写：客服邮箱地址】')
            fixes_log.append('C09: 标记客服邮箱占位符')

    # ── C12: 章节标题统一 ─────────────────────────────────────────
    title_fixes = {
        '感谢': '感谢语',  # 只改独立的"感谢"章节标题
    }
    for para in paras:
        pStyle = para.find('.//' + tag(W, 'pStyle'))
        if pStyle is not None and pStyle.get(tag(W, 'val'), '') == '1':
            text = get_para_text(para)
            if text.strip() == '感谢':
                replace_text_in_para(para, '感谢', '感谢语')
                fixes_log.append('C12: 章节标题"感谢"→"感谢语"')

    # ── C14: 感谢语统一 ──────────────────────────────────────────
    for para in paras:
        text = get_para_text(para)
        if '再次感谢您购买我们的真空封装机器' in text:
            replace_text_in_para(
                para,
                '再次感谢您购买我们的真空封装机器，祝您使用愉快，如果有任何问题，请随时与我们联系！',
                '感谢您选择 WEVAC 真空封口机。如有任何问题，请通过以下方式联系我们：'
            )
            fixes_log.append('C14: 统一感谢语')

    # ── L02: 删除红色编辑注释段落 ────────────────────────────────
    paras_to_remove_red = []
    for para in paras:
        for run in para.findall('.//' + tag(W, 'r')):
            color = run.find('.//' + tag(W, 'color'))
            if color is not None and color.get(tag(W, 'val'), '') == 'EE0000':
                paras_to_remove_red.append(para)
                fixes_log.append(f'L02: 删除红色注释: {get_para_text(para)[:40]}')
                break

    for para in paras_to_remove_red:
        for elem in body.iter():
            if para in list(elem):
                try:
                    elem.remove(para)
                except ValueError:
                    pass
                break

    tree.write(str(doc_path), xml_declaration=True, encoding='UTF-8')
    print(f'document.xml 修复完成，共 {len(fixes_log)} 项修复')


def fix_table_colors(doc_path: Path, fixes_log: list):
    """L01: 绿色表头改为浅灰 #F2F2F2"""
    tree = ET.parse(str(doc_path))
    root = tree.getroot()

    count = 0
    for shd in root.findall('.//' + tag(W, 'shd')):
        fill = shd.get(tag(W, 'fill'), '')
        if fill.upper() == '00B050':
            shd.set(tag(W, 'fill'), 'F2F2F2')
            shd.set(tag(W, 'color'), 'auto')
            count += 1

    if count:
        fixes_log.append(f'L01: 修复 {count} 个绿色表头单元格 → #F2F2F2')
        tree.write(str(doc_path), xml_declaration=True, encoding='UTF-8')


def fix_page_margins(doc_path: Path, fixes_log: list):
    """L04: 页边距统一为 720 twips (12.7mm ≈ 0.5 inch)"""
    tree = ET.parse(str(doc_path))
    root = tree.getroot()

    pgMar = root.find('.//' + tag(W, 'pgMar'))
    if pgMar is not None:
        pgMar.set(tag(W, 'top'),    '720')
        pgMar.set(tag(W, 'bottom'), '720')
        pgMar.set(tag(W, 'left'),   '720')
        pgMar.set(tag(W, 'right'),  '720')
        fixes_log.append('L04: 页边距统一为 720 twips (12.7mm)')
        tree.write(str(doc_path), xml_declaration=True, encoding='UTF-8')


def fix_anchor_to_inline(doc_path: Path, fixes_log: list):
    """L03: 统计浮动图片数量（anchor→inline 转换复杂，记录待处理）"""
    tree = ET.parse(str(doc_path))
    root = tree.getroot()

    WP_NS = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
    anchors = root.findall('.//' + f'{{{WP_NS}}}anchor')
    fixes_log.append(f'L03: 发现 {len(anchors)} 个浮动图片（anchor），已记录，需在Word中手动转为嵌入式')


def main():
    base = Path(r'D:\work\private\yjsplan\research\yjs-manual-opt\v23-unpacked\word')
    doc_path = base / 'document.xml'
    fixes_log = []

    print('开始修复 V23 说明书...')
    print()

    fix_document(doc_path, fixes_log)
    fix_table_colors(doc_path, fixes_log)
    fix_page_margins(doc_path, fixes_log)
    fix_anchor_to_inline(doc_path, fixes_log)

    print()
    print('=== 修复清单 ===')
    for i, fix in enumerate(fixes_log, 1):
        print(f'  {i:2d}. {fix}')

    print()
    print(f'共完成 {len(fixes_log)} 项修复')


if __name__ == '__main__':
    main()
