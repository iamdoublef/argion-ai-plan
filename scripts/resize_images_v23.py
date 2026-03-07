import os
import re

DIR = r"D:\work\private\yjsplan
esearch\yjs-manual-opt
eleases\2026-03-01_full-fix-v2-v23"
FILES = [
    "v23-cn-main.html",
    "v23-en-main.html",
    "v23-mi-style.html",
    "v23-lifestyle-style.html",
    "v23-swiss-style.html"
]

REPLACEMENTS = [
    # Global fig-wrap styles
    (re.escape("max-width: 80%;"), "max-width: 100%;"),
    (re.escape("max-height: 70mm;"), "max-height: 85mm;"),
    # 6.10 side-by-side images
    (re.escape('style="max-height:40mm;max-width:80%"'), 'style="max-height:55mm;max-width:100%"'),
    # Step images - generic patterns for common sizes
    (re.escape('style="width:45mm;height:auto;max-height:40mm;max-width:45mm"'), 'style="width:55mm;height:auto;max-height:50mm;max-width:55mm"'),
    (re.escape('style="width:45mm;height:auto;max-height:45mm;max-width:45mm"'), 'style="width:55mm;height:auto;max-height:55mm;max-width:55mm"'),
    (re.escape('style="width:40mm;height:auto;max-height:35mm;max-width:40mm"'), 'style="width:55mm;height:auto;max-height:50mm;max-width:55mm"'),
    (re.escape('style="width:40mm;height:auto;max-height:30mm;max-width:40mm"'), 'style="width:55mm;height:auto;max-height:45mm;max-width:55mm"'),
    (re.escape('style="width:40mm;height:auto;max-height:45mm;max-width:40mm"'), 'style="width:55mm;height:auto;max-height:60mm;max-width:55mm"'),
]

for filename in FILES:
    filepath = os.path.join(DIR, filename)
    if not os.path.exists(filepath):
        print(f"Skipping {filename}, file not found.")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old, new in REPLACEMENTS:
        new_content = re.sub(old, new, new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"No changes for {filename}")
