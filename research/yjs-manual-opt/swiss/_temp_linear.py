"""Extract Word doc as a linear sequence of text and images"""
from docx import Document
from docx.oxml.ns import qn
from pathlib import Path

docx_path = Path(r"d:\work\private\yjsplan\research\yjs-manual-opt\_inbox\IMT050 说明书-通用-中文-A版-20260205.docx")
doc = Document(docx_path)

elements = []
for para in doc.paragraphs:
    text = para.text.strip()
    style = para.style.name if para.style else "Normal"
    
    # Check for images in this paragraph
    imgs = []
    for run in para.runs:
        for child in run._element.iter():
            tag = child.tag.split('}')[-1]
            if tag == 'blip':
                embed = child.get(qn('r:embed'))
                if embed and embed in doc.part.rels:
                    rel = doc.part.rels[embed]
                    imgs.append(rel.target_ref.split('/')[-1])
    
    if text or imgs:
        elements.append({'text': text, 'style': style, 'imgs': imgs})

# Print linearly
print("=" * 60)
print("IMT050 Word Doc — Linear Content Flow")
print("=" * 60)

for i, el in enumerate(elements):
    prefix = ""
    if "Heading 1" in el['style']:
        prefix = "\n>>> H1: "
    elif "Heading 2" in el['style']:
        prefix = "\n  >> H2: "
    elif "Heading 3" in el['style']:
        prefix = "    > H3: "
    else:
        prefix = "    "
    
    if el['text']:
        line = el['text'][:100]
        print(f"{prefix}{line}")
    
    if el['imgs']:
        for img in el['imgs']:
            print(f"    📷 {img}")
