import zipfile, xml.etree.ElementTree as ET, sys
sys.stdout.reconfigure(encoding='utf-8')

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
path = r'D:\work\private\yjsplan\research\yjs-manual-opt\V23-修正版-20260225.docx'

def get_text(para):
    return ''.join(t.text for t in para.findall('.//' + W + 't') if t.text)

with zipfile.ZipFile(path) as z:
    with z.open('word/document.xml') as f:
        root = ET.parse(f).getroot()

paras = root.findall('.//' + W + 'p')

def check_item(name, found):
    status = 'FAIL 仍存在' if found else 'OK   已修复'
    print(f'  [{status}]  {name}')

check_item('双句号', any('。。' in get_text(p) for p in paras))
check_item('错别字事务', any('其他事务' in get_text(p) for p in paras))
check_item('Pulse手动密封', any('手动密封' in get_text(p) and 'Pulse' in get_text(p) for p in paras))
check_item('Vesta品牌', any('Precision Appliance' in get_text(p) or 'vestaprecision' in get_text(p) for p in paras))
check_item('ADVANCED品牌', any('ADVANCED CUISINE' in get_text(p) for p in paras))

note_count = sum(1 for p in paras if '发热器温度很高' in get_text(p))
status = 'OK  ' if note_count <= 1 else 'FAIL'
print(f'  [{status}]  Note出现次数: {note_count} (期望1)')

wevac = any('WEVAC' in get_text(p) for p in paras)
status = 'OK  ' if wevac else 'FAIL'
print(f'  [{status}]  Wevac品牌信息保留')

red = any(
    run.find('.//' + W + 'color') is not None and
    run.find('.//' + W + 'color').get(W + 'val','') == 'EE0000'
    for run in root.findall('.//' + W + 'r')
)
green = any(shd.get(W + 'fill','').upper() == '00B050' for shd in root.findall('.//' + W + 'shd'))
check_item('红色注释文字', red)
check_item('绿色表头', green)

pgMar = root.find('.//' + W + 'pgMar')
top = pgMar.get(W + 'top','?') if pgMar is not None else '?'
status = 'OK  ' if top == '720' else 'FAIL'
print(f'  [{status}]  页边距 top={top} (期望720)')

thanks = any('感谢您选择 WEVAC' in get_text(p) for p in paras)
status = 'OK  ' if thanks else 'FAIL'
print(f'  [{status}]  感谢语已统一')

email_marked = any('请填写：客服邮箱地址' in get_text(p) for p in paras)
status = 'OK  ' if email_marked else 'FAIL'
print(f'  [{status}]  客服邮箱占位符已标记')
