"""Analyze Word doc images and their context to map them to template sections"""
from docx import Document
from pathlib import Path
import re

docx_path = Path(r"d:\work\private\yjsplan\research\yjs-manual-opt\_inbox\IMT050 说明书-通用-中文-A版-20260205.docx")
doc = Document(docx_path)

print("=" * 70)
print("IMT050 Word Doc — Image Context Analysis")
print("=" * 70)

# Walk through document body elements to find images and their surrounding text
from docx.oxml.ns import qn

current_section = "（文档开头）"
current_subsection = ""

for element in doc.element.body:
    tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
    
    if tag == 'p':
        # Paragraph
        text_parts = []
        has_image = False
        image_names = []
        
        for child in element.iter():
            child_tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            
            if child_tag == 't':
                if child.text:
                    text_parts.append(child.text)
            
            if child_tag == 'blip':
                has_image = True
                embed_id = child.get(qn('r:embed'))
                if embed_id:
                    rel = doc.part.rels.get(embed_id)
                    if rel:
                        image_names.append(rel.target_ref.split('/')[-1])
        
        text = ''.join(text_parts).strip()
        
        # Track section headings
        style_el = element.find(qn('w:pPr'))
        if style_el is not None:
            style_id = style_el.find(qn('w:pStyle'))
            if style_id is not None:
                style_name = style_id.get(qn('w:val'), '')
                if '1' in style_name and 'heading' in style_name.lower():
                    current_section = text
                    current_subsection = ""
                elif '2' in style_name and 'heading' in style_name.lower():
                    current_subsection = text
        
        if has_image:
            for img in image_names:
                context = text[:80] if text else "(no surrounding text)"
                print(f"\n[{current_section}] > [{current_subsection}]")
                print(f"  IMAGE: {img}")
                print(f"  Context: {context}")
    
    elif tag == 'tbl':
        # Table - check for images inside
        image_names = []
        for child in element.iter():
            child_tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if child_tag == 'blip':
                embed_id = child.get(qn('r:embed'))
                if embed_id:
                    rel = doc.part.rels.get(embed_id)
                    if rel:
                        image_names.append(rel.target_ref.split('/')[-1])
        
        if image_names:
            for img in image_names:
                print(f"\n[{current_section}] > [{current_subsection}]")
                print(f"  IMAGE (in table): {img}")
