import re

with open('output/v23-wevac-eu-cn.html', 'r', encoding='utf-8') as f:
    html = f.read()

pages = re.split(r'<div class="page"', html)
for i, page in enumerate(pages[1:], 1):
    title_m = re.search(r'class="section-title"[^>]*>.*?<span[^>]*>(.*?)</span>', page, re.DOTALL)
    header_m = re.search(r'class="header-chapter"[^>]*>(.*?)</div>', page, re.DOTALL)
    subs = re.findall(r'class="sub-title"[^>]*>(.*?)</[dh]', page)
    st = title_m.group(1).strip() if title_m else '-'
    hd = header_m.group(1).strip() if header_m else '-'
    # Count images
    imgs = len(re.findall(r'<img ', page))
    # Count tables
    tbls = len(re.findall(r'<table', page))
    print(f'P{i:02d} | sec={st[:20]:20s} | hdr={hd[:30]:30s} | imgs={imgs} tbls={tbls} | subs={[s[:20] for s in subs[:4]]}')
