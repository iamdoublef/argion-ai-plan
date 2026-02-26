"""
补回被误删的 Note 段落（产品结构图下方）
Note：工作结束后，发热器温度很高，请不要触摸，以免烫伤！
"""
import zipfile, xml.etree.ElementTree as ET, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

# 在 unpacked 目录操作
path = r'D:\work\private\yjsplan\research\yjs-manual-opt\v23-unpacked\word\document.xml'

def get_text(para):
    return ''.join(t.text for t in para.findall('.//' + W + 't') if t.text)

tree = ET.parse(path)
root = tree.getroot()
body = root.find('.//' + W + 'body')
paras = list(body)  # 直接子元素（包含段落和表格）

# 找"切袋刀"段落的位置（产品结构表格最后一个零件），在其后插入 Note
# 先找到包含"切袋刀"的段落索引
insert_after_idx = None
for i, elem in enumerate(paras):
    if elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
        t = get_text(elem)
        if t.strip() == '切袋刀':
            insert_after_idx = i
            print(f'找到插入位置: 行{i} "{t}"')

if insert_after_idx is None:
    # 备选：找"卷袋仓"后面
    for i, elem in enumerate(paras):
        if elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
            t = get_text(elem)
            if '卷袋仓' in t and len(t) < 10:
                insert_after_idx = i
                print(f'备选插入位置: 行{i} "{t}"')

if insert_after_idx is not None:
    # 构造 Note 段落 XML
    note_xml = '''<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:pPr>
    <w:pStyle w:val="af0"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:b/>
    </w:rPr>
    <w:t xml:space="preserve">Note：</w:t>
  </w:r>
  <w:r>
    <w:t>工作结束后，发热器温度很高，请不要触摸，以免烫伤！</w:t>
  </w:r>
</w:p>'''
    note_elem = ET.fromstring(note_xml)
    body.insert(insert_after_idx + 1, note_elem)
    print('Note 段落已插入')
    tree.write(path, xml_declaration=True, encoding='UTF-8')
else:
    print('未找到插入位置，请手动处理')
