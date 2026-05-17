from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from lxml import etree
from PIL import Image


ROOT = Path(r"D:\work\private\yjsplan\research\yjs-manual-opt\swiss")
HTML_PATH = ROOT / "output" / "imt050-wevac-eu-cn.html"
IMAGE_ROOT = ROOT / "output"
BASE_TEMPLATE = ROOT / "template" / "shared" / "docx" / "base-template-cn.docx"
W27_REFERENCE = Path(__file__).resolve().parents[2] / "design-iter-22" / "path-codex" / "output.docx"
DOCX_SKILL = Path(r"C:\Users\iamdo\.claude\skills\docx")
UNPACK = DOCX_SKILL / "scripts" / "office" / "unpack.py"
PACK = DOCX_SKILL / "scripts" / "office" / "pack.py"

PAGE_W = 8391  # 148 mm
PAGE_H = 11906  # 210 mm
MARGIN = 567  # 10 mm
CONTENT_W = PAGE_W - MARGIN * 2

BLACK = "000000"
RED = "E63946"
DARK = "1A1A1A"
GRAY = "8E8E93"
LIGHT_GRAY = "F2F2F7"
BORDER = "CCCCCC"
WHITE = "FFFFFF"

NS = {
    "wpc": "http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "o": "urn:schemas-microsoft-com:office:office",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "v": "urn:schemas-microsoft-com:vml",
    "wp14": "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "w10": "urn:schemas-microsoft-com:office:word",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "wpg": "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
    "wpi": "http://schemas.microsoft.com/office/word/2010/wordprocessingInk",
    "wne": "http://schemas.microsoft.com/office/word/2006/wordml",
    "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
}


def x(s: str) -> str:
    return html.escape(s, quote=True)


def mm_to_twip(mm: float) -> int:
    return int(round(mm * 56.6929))


def pt_to_half(pt: float) -> int:
    return int(round(pt * 2))


def pt_to_twip(pt: float) -> int:
    return int(round(pt * 20))


def emu_from_mm(mm: float) -> int:
    return int(round(mm * 36000))


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def parse_mm(style: str, key: str, default: float | None = None) -> float | None:
    m = re.search(rf"{re.escape(key)}:\s*([0-9.]+)mm", style or "")
    return float(m.group(1)) if m else default


def parse_px(style: str, key: str, default: float | None = None) -> float | None:
    m = re.search(rf"{re.escape(key)}:\s*([0-9.]+)px", style or "")
    return float(m.group(1)) if m else default


def parse_pct(style: str, key: str, default: float | None = None) -> float | None:
    m = re.search(rf"{re.escape(key)}:\s*([0-9.]+)%", style or "")
    return float(m.group(1)) if m else default


class TemplateText:
    def __init__(self, provided: dict[str, str] | None = None) -> None:
        self.params: dict[str, str] = {}
        self.provided = provided or {}
        self.counts: dict[str, int] = {}

    def key(self, prefix: str, text: str) -> str:
        base = re.sub(r"[^A-Za-z0-9]+", "_", prefix).strip("_").lower() or "text"
        idx = self.counts.get(base, 0) + 1
        self.counts[base] = idx
        key = f"{base}_{idx:03d}"
        self.params[key] = text
        return key

    def placeholder(self, prefix: str, text: str) -> str:
        key = self.key(prefix, text)
        return "{{" + key + "}}"

    def resolve(self, placeholder: str) -> str:
        key = placeholder[2:-2]
        return self.provided.get(key, self.params[key])


class OoxmlBuilder:
    def __init__(self, unpacked_dir: Path, text: TemplateText) -> None:
        self.unpacked_dir = unpacked_dir
        self.text = text
        self.media_dir = unpacked_dir / "word" / "media"
        self.media_dir.mkdir(parents=True, exist_ok=True)
        self.image_rels: list[tuple[str, str]] = []
        self.image_seq = 1
        self.docpr_seq = 1

    def image_path(self, img: Tag) -> Path:
        src = (img.get("src") or "").replace("./", "")
        return IMAGE_ROOT / src

    def fit_image_mm(self, path: Path, max_w: float, max_h: float) -> tuple[float, float]:
        with Image.open(path) as im:
            w, h = im.size
        scale = min(max_w / w, max_h / h)
        return max(1.0, w * scale), max(1.0, h * scale)

    def add_image_rel(self, src: Path) -> tuple[str, str]:
        ext = src.suffix.lower() or ".png"
        name = f"image{self.image_seq}{ext}"
        self.image_seq += 1
        shutil.copy2(src, self.media_dir / name)
        rid = f"rIdImg{self.image_seq}"
        self.image_rels.append((rid, f"media/{name}"))
        return rid, name

    def run(
        self,
        text: str,
        *,
        size: float = 7.05,
        bold: bool = False,
        color: str = BLACK,
        font: str = "Arial",
        east_asia: str = "Microsoft YaHei",
        preserve: bool = False,
        shade: str | None = None,
        placeholder_prefix: str | None = None,
    ) -> str:
        if placeholder_prefix is not None:
            text = self.text.placeholder(placeholder_prefix, text)
        attrs = ' xml:space="preserve"' if preserve or text[:1].isspace() or text[-1:].isspace() else ""
        bold_xml = "<w:b/>" if bold else ""
        shade_xml = f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>' if shade else ""
        return (
            "<w:r><w:rPr>"
            f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}" w:eastAsia="{east_asia}"/>'
            f"{bold_xml}<w:color w:val=\"{color}\"/><w:sz w:val=\"{pt_to_half(size)}\"/>"
            f"<w:szCs w:val=\"{pt_to_half(size)}\"/><w:spacing w:val=\"5\"/>{shade_xml}</w:rPr>"
            f"<w:t{attrs}>{x(text)}</w:t></w:r>"
        )

    def paragraph(
        self,
        runs: str | list[str] = "",
        *,
        after: float = 2,
        before: float = 0,
        line: float = 1.16,
        jc: str | None = None,
        left: int | None = None,
        first: int | None = None,
        border_left: str | None = None,
        border_bottom: str | None = None,
        border_top: str | None = None,
        tab_right: bool = False,
    ) -> str:
        body = "".join(runs) if isinstance(runs, list) else runs
        ppr = []
        borders = []
        if border_left:
            borders.append(f'<w:left w:val="single" w:sz="18" w:space="4" w:color="{border_left}"/>')
        if border_bottom:
            borders.append(f'<w:bottom w:val="single" w:sz="6" w:space="1" w:color="{border_bottom}"/>')
        if border_top:
            borders.append(f'<w:top w:val="single" w:sz="18" w:space="1" w:color="{border_top}"/>')
        if borders:
            ppr.append("<w:pBdr>" + "".join(borders) + "</w:pBdr>")
        if tab_right:
            ppr.append(f'<w:tabs><w:tab w:val="right" w:pos="{CONTENT_W}"/></w:tabs>')
        ppr.append(
            f'<w:spacing w:before="{pt_to_twip(before)}" w:after="{pt_to_twip(after)}" '
            f'w:line="{int(line * 240)}" w:lineRule="auto"/>'
        )
        if left is not None or first is not None:
            attrs = []
            if left is not None:
                attrs.append(f'w:left="{left}"')
            if first is not None:
                if first < 0:
                    attrs.append(f'w:hanging="{-first}"')
                else:
                    attrs.append(f'w:firstLine="{first}"')
            ppr.append(f"<w:ind {' '.join(attrs)}/>")
        if jc:
            ppr.append(f'<w:jc w:val="{jc}"/>')
        return "<w:p><w:pPr>" + "".join(ppr) + "</w:pPr>" + body + "</w:p>"

    def image_run(self, img: Tag, *, max_w: float, max_h: float) -> str:
        path = self.image_path(img)
        if not path.exists():
            return ""
        w_mm, h_mm = self.fit_image_mm(path, max_w, max_h)
        rid, name = self.add_image_rel(path)
        cx, cy = emu_from_mm(w_mm), emu_from_mm(h_mm)
        docpr = self.docpr_seq
        self.docpr_seq += 1
        return f"""
<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">
  <wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>
  <wp:docPr id="{docpr}" name="{x(name)}"/><wp:cNvGraphicFramePr>
    <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
  </wp:cNvGraphicFramePr>
  <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
      <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
        <pic:nvPicPr><pic:cNvPr id="{docpr}" name="{x(name)}"/><pic:cNvPicPr/></pic:nvPicPr>
        <pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
        <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
      </pic:pic>
    </a:graphicData>
  </a:graphic>
</wp:inline></w:drawing></w:r>"""

    def image_para(self, img: Tag, *, force_w: float | None = None, force_h: float | None = None, after: float = 6, jc: str = "center") -> str:
        style = img.get("style", "")
        max_h = force_h or parse_mm(style, "max-height") or 45
        pct_w = parse_pct(style, "max-width")
        max_w = force_w or (CONTENT_W / 56.6929 * pct_w / 100 if pct_w else CONTENT_W / 56.6929)
        px_h = parse_px(style, "height")
        if px_h:
            max_h = px_h * 0.2645
        return self.paragraph(self.image_run(img, max_w=max_w, max_h=max_h), after=after, line=1, jc=jc)

    def section_pr(self, page_no: int | None = None) -> str:
        footer = '<w:footerReference w:type="default" r:id="rIdFooter1"/>' if page_no is not None else ""
        return (
            "<w:sectPr>"
            f"{footer}<w:pgSz w:w=\"{PAGE_W}\" w:h=\"{PAGE_H}\"/>"
            f"<w:pgMar w:top=\"{MARGIN}\" w:right=\"{MARGIN}\" w:bottom=\"{MARGIN}\" w:left=\"{MARGIN}\" "
            'w:header="227" w:footer="198" w:gutter="0"/>'
            '<w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr>'
        )

    def section_break(self, next_page_no: int) -> str:
        return f"<w:p><w:pPr>{self.section_pr(next_page_no)}</w:pPr></w:p>"

    def header_strip(self, node: Tag) -> str:
        text = clean_text(node.get_text(" ", strip=True))
        if "CH." in text:
            left, right = text.split("CH.", 1)
            right = "CH." + right.strip()
        else:
            parts = text.split(maxsplit=1)
            left = parts[0] if parts else ""
            right = parts[1] if len(parts) > 1 else ""
        return self.paragraph(
            [
                self.run(clean_text(left), size=6.75, bold=True, placeholder_prefix="header_brand"),
                self.run("\t", size=5.4, color=GRAY, font="Courier New", preserve=True),
                self.run(right, size=5.4, color=GRAY, font="Courier New", placeholder_prefix="header_ref"),
            ],
            after=8.8,
            line=1,
            border_top=BLACK,
            tab_right=True,
        )

    def section_title(self, node: Tag) -> str:
        num = node.select_one(".chapter-num")
        num_text = clean_text(num.get_text(" ", strip=True)) if num else ""
        full = clean_text(node.get_text(" ", strip=True))
        title = clean_text(full.replace(num_text, "", 1))
        return self.paragraph(
            [
                self.run(num_text + " ", size=13.5, bold=True, color=RED, placeholder_prefix="chapter_no", preserve=True),
                self.run(title, size=11, bold=True, placeholder_prefix="chapter_title"),
            ],
            after=6,
            line=1,
            left=mm_to_twip(1.5),
            border_left=BLACK,
        )

    def subtitle(self, node: Tag, before: float = 4) -> str:
        return self.paragraph(
            self.run(clean_text(node.get_text(" ", strip=True)), size=7.5, bold=True, placeholder_prefix="subtitle"),
            after=4,
            before=before,
            border_bottom=BLACK,
        )

    def text_from_node(self, node: Tag, prefix: str, *, size: float = 7.05, bold: bool = False, color: str = DARK) -> str:
        return self.run(clean_text(node.get_text(" ", strip=True)), size=size, bold=bold, color=color, placeholder_prefix=prefix)

    def para_node(self, node: Tag) -> str:
        return self.paragraph(self.text_from_node(node, "paragraph"), after=3)

    def bullet_list(self, ul: Tag, *, tight: bool = False) -> str:
        out = []
        for li in ul.find_all("li", recursive=False):
            runs = [
                self.run("•   ", size=5.8 if not tight else 5.25, bold=True, color=RED, preserve=True),
                self.run(clean_text(li.get_text(" ", strip=True)), size=7.05 if not tight else 6.85, color=BLACK, placeholder_prefix="bullet"),
            ]
            out.append(self.paragraph(runs, after=0.7 if tight else 1.6, line=1.0 if tight else 1.13, left=mm_to_twip(3.2), first=-mm_to_twip(3.2)))
        return "".join(out)

    def alert_box(self, node: Tag, *, compact: bool = False) -> str:
        classes = set(node.get("class", []))
        is_note = "note-box" in classes
        color = RED if "warning-box" in classes else (BLACK if "caution-box" in classes else GRAY)
        fill = LIGHT_GRAY if is_note else WHITE
        title = node.select_one(".box-title")
        content = []
        if title:
            content.append(self.paragraph(self.run(clean_text(title.get_text(" ", strip=True)), size=6.4, bold=True, color=color if color != GRAY else BLACK, placeholder_prefix="box_title"), after=1, line=1))
        icon = node.find("img")
        if icon:
            content.append(self.paragraph(self.image_run(icon, max_w=8, max_h=6), after=1, line=1, jc="left"))
        for child in node.children:
            if not isinstance(child, Tag) or child == title or child.name == "img":
                continue
            if child.name == "ul":
                content.append(self.bullet_list(child, tight=True))
            elif child.name == "p":
                content.append(self.paragraph(self.text_from_node(child, "box_para", size=6.9), after=1, line=1.05))
        border = f'<w:tcBorders><w:top w:val="single" w:sz="10" w:color="{color}"/><w:left w:val="single" w:sz="10" w:color="{color}"/><w:bottom w:val="single" w:sz="10" w:color="{color}"/><w:right w:val="single" w:sz="10" w:color="{color}"/></w:tcBorders>' if not is_note else ""
        return (
            f'<w:tbl><w:tblPr><w:tblW w:w="{CONTENT_W}" w:type="dxa"/>'
            '<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>'
            '<w:tblLayout w:type="fixed"/></w:tblPr>'
            f'<w:tblGrid><w:gridCol w:w="{CONTENT_W}"/></w:tblGrid><w:tr><w:tc><w:tcPr><w:tcW w:w="{CONTENT_W}" w:type="dxa"/>'
            f'{border}<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/><w:tcMar><w:top w:w="44" w:type="dxa"/><w:start w:w="170" w:type="dxa"/><w:bottom w:w="44" w:type="dxa"/><w:end w:w="110" w:type="dxa"/></w:tcMar></w:tcPr>'
            f'{"".join(content)}</w:tc></w:tr></w:tbl>{self.paragraph("", after=2, line=0.1)}'
        )

    def image_row(self, node: Tag) -> str:
        imgs = node.find_all("img", recursive=False)
        if not imgs:
            return ""
        cols = max(1, min(len(imgs), 3))
        col_w = CONTENT_W // cols
        cells = []
        for img in imgs[:cols]:
            style = img.get("style", "")
            max_h = parse_mm(style, "max-height") or (24 if "step-figures" in node.get("class", []) else 26)
            pct_w = parse_pct(style, "max-width")
            max_w = min(col_w / 56.6929 - 2, CONTENT_W / 56.6929 * pct_w / 100) if pct_w else col_w / 56.6929 - 2
            cells.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/>'
                '<w:tcBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/></w:tcBorders>'
                '<w:tcMar><w:top w:w="0" w:type="dxa"/><w:start w:w="20" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:end w:w="20" w:type="dxa"/></w:tcMar></w:tcPr>'
                f'{self.paragraph(self.image_run(img, max_w=max_w, max_h=max_h), after=2, line=1, jc="center")}</w:tc>'
            )
        return (
            f'<w:tbl><w:tblPr><w:tblW w:w="{CONTENT_W}" w:type="dxa"/>'
            '<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>'
            '<w:tblLayout w:type="fixed"/></w:tblPr>'
            f'<w:tblGrid>{"".join(f"<w:gridCol w:w=\"{col_w}\"/>" for _ in cells)}</w:tblGrid><w:tr>{"".join(cells)}</w:tr></w:tbl>'
        )

    def html_table(self, node: Tag, *, compact_warranty: bool = False, troubleshooting: bool = False) -> str:
        rows = node.find_all("tr")
        if not rows:
            return ""
        max_cols = max(len(r.find_all(["td", "th"], recursive=False)) for r in rows)
        first_cells = rows[0].find_all(["td", "th"], recursive=False)
        pct_widths: list[float | None] = []
        for idx in range(max_cols):
            style = first_cells[idx].get("style", "") if idx < len(first_cells) else ""
            pct_widths.append(parse_pct(style, "width"))
        used = sum(w for w in pct_widths if w is not None)
        missing = sum(1 for w in pct_widths if w is None)
        fallback = max(0.0, 100.0 - used) / missing if missing else 0.0
        pct_widths = [w if w is not None else fallback for w in pct_widths]
        total = sum(pct_widths) or 100.0
        col_ws = [int(CONTENT_W * w / total) for w in pct_widths]
        if col_ws:
            col_ws[-1] += CONTENT_W - sum(col_ws)
        grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in col_ws)
        out_rows = []
        is_warranty = "warranty-card" in node.get("class", [])
        compact = len(rows) > 8 or is_warranty or compact_warranty
        for r_idx, tr in enumerate(rows):
            cells = tr.find_all(["td", "th"], recursive=False)
            row_cells = []
            for c_idx in range(max_cols):
                raw = clean_text(cells[c_idx].get_text(" ", strip=True)) if c_idx < len(cells) else ""
                col_w = col_ws[c_idx] if c_idx < len(col_ws) else CONTENT_W // max_cols
                fill = DARK if r_idx == 0 and not is_warranty else (LIGHT_GRAY if r_idx % 2 == 0 else WHITE)
                color = WHITE if r_idx == 0 and not is_warranty else DARK
                size = 6.0 if r_idx == 0 else (6.4 if compact else 6.7)
                row_cells.append(
                    f'<w:tc><w:tcPr><w:tcW w:w="{col_w}" w:type="dxa"/>'
                    f'<w:tcBorders><w:top w:val="single" w:sz="4" w:color="{BORDER}"/><w:left w:val="single" w:sz="4" w:color="{BORDER}"/><w:bottom w:val="single" w:sz="4" w:color="{BORDER}"/><w:right w:val="single" w:sz="4" w:color="{BORDER}"/></w:tcBorders>'
                    f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/><w:tcMar><w:top w:w="34" w:type="dxa"/><w:start w:w="55" w:type="dxa"/><w:bottom w:w="34" w:type="dxa"/><w:end w:w="55" w:type="dxa"/></w:tcMar></w:tcPr>'
                    f'{self.paragraph(self.run(raw, size=size, bold=(r_idx == 0 and not is_warranty), color=color, placeholder_prefix="table_cell"), after=0, line=1)}</w:tc>'
                )
            out_rows.append(f'<w:tr><w:trPr><w:trHeight w:val="{225 if compact else 215}" w:hRule="atLeast"/></w:trPr>{"".join(row_cells)}</w:tr>')
        return (
            f'<w:tbl><w:tblPr><w:tblW w:w="{CONTENT_W}" w:type="dxa"/><w:tblLayout w:type="fixed"/></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>{"".join(out_rows)}</w:tbl>'
        )

    def step_flow(self, node: Tag) -> str:
        out = []
        for step in node.select(".step-flow-step"):
            row = step.select_one(".step-flow-row")
            if row:
                num = clean_text(row.select_one(".step-num").get_text(" ", strip=True))
                txt = clean_text(row.select_one(".step-text").get_text(" ", strip=True))
                out.append(
                    self.paragraph(
                        [
                            self.run("  " + num + "  ", size=7.05, bold=True, color=WHITE, shade=BLACK, preserve=True, placeholder_prefix="step_no"),
                            self.run("   ", size=7.05, preserve=True),
                            self.run(txt, size=7.05, color=BLACK, placeholder_prefix="step_text"),
                        ],
                        after=2,
                        line=1.1,
                    )
                )
            for fig in step.select(".figure-row"):
                out.append(self.image_row(fig))
        return "".join(out)

    def cover(self, page: Tag) -> str:
        out = []
        brand = clean_text(page.select_one(".cover-brand").get_text(" ", strip=True))
        out.append(self.paragraph([self.run("━━ ", size=7.5, bold=True, color=RED, preserve=True), self.run(brand, size=7.5, bold=True, placeholder_prefix="cover_brand")], before=20, after=138, line=1))
        img = page.find("img")
        if img:
            out.append(self.image_para(img, force_w=42, force_h=32.5, after=30, jc="left"))
        out.append(self.paragraph(self.text_from_node(page.select_one(".cover-model"), "cover_model", size=6, bold=True, color=RED), after=2, line=1))
        out.append(self.paragraph(self.text_from_node(page.select_one(".cover-title"), "cover_title", size=18, bold=True), after=0, line=1))
        out.append(self.paragraph(self.text_from_node(page.select_one(".cover-subtitle"), "cover_subtitle", size=7.5, color=GRAY), after=1, line=1))
        out.append(self.paragraph(self.run("━━━━", size=7, bold=True, color=RED), after=113, line=1))
        out.append(self.paragraph("", after=3, line=1, border_top=BLACK))
        out.append(self.paragraph(self.text_from_node(page.select_one(".cover-bottom"), "cover_bottom", size=5.4, color=GRAY), after=0, line=1))
        return "".join(out)

    def toc(self, page: Tag) -> str:
        out = [self.header_strip(page.select_one(".header-strip"))]
        out.append(self.paragraph(self.text_from_node(page.select_one(".toc-title"), "toc_title", size=15, bold=True), after=10))
        for item in page.select(".toc-item"):
            out.append(
                self.paragraph(
                    [
                        self.text_from_node(item.select_one(".toc-chapter"), "toc_chapter", size=6.75, bold=True, color=RED),
                        self.run("  ", size=7.5, preserve=True),
                        self.text_from_node(item.select_one(".toc-name"), "toc_name", size=7.5, bold=True),
                        self.run("\t", size=6.4, preserve=True, color=GRAY, font="Courier New"),
                        self.text_from_node(item.select_one(".toc-page"), "toc_page", size=6.4, color=GRAY),
                    ],
                    after=6,
                    line=1,
                    tab_right=True,
                )
            )
        return "".join(out)

    def body_page(self, page: Tag) -> str:
        out = []
        classes_page = set(page.get("class", []))
        previous_was_list = False
        for child in page.find_all(recursive=False):
            if not isinstance(child, Tag):
                continue
            classes = set(child.get("class", []))
            after_list = previous_was_list
            previous_was_list = child.name == "ul"
            if "page-footer" in classes:
                continue
            if "header-strip" in classes:
                out.append(self.header_strip(child))
            elif "section-title" in classes:
                out.append(self.section_title(child))
            elif "sub-title" in classes:
                out.append(self.subtitle(child, before=8 if after_list else 4))
            elif child.name == "p":
                text = clean_text(child.get_text(" ", strip=True))
                if "compact-warranty" in classes_page and "support@wevactech.com |" in text:
                    lead, contact = text.split("support@wevactech.com |", 1)
                    out.append(self.paragraph(self.run(clean_text(lead), size=7.05, color=DARK, placeholder_prefix="paragraph"), after=1, line=1.12))
                    out.append(self.paragraph(self.run("support@wevactech.com |" + contact, size=7.05, color=DARK, placeholder_prefix="paragraph"), after=3, line=1.12))
                else:
                    out.append(self.para_node(child))
            elif child.name == "ul":
                out.append(self.bullet_list(child, tight=("compact-warranty" in classes_page)))
            elif "warning-box" in classes or "caution-box" in classes or "note-box" in classes:
                out.append(self.alert_box(child, compact=("compact-safety" in classes_page)))
            elif "step-flow" in classes:
                out.append(self.step_flow(child))
            elif "fig-wrap" in classes:
                img = child.find("img")
                if img:
                    out.append(self.image_para(img))
            elif "figure-row" in classes:
                out.append(self.image_row(child))
            elif child.name == "table":
                out.append(self.html_table(child, compact_warranty=("compact-warranty" in classes_page), troubleshooting=("troubleshooting-primary" in classes_page)))
        return "".join(out)

    def document_xml(self) -> str:
        soup = BeautifulSoup(HTML_PATH.read_text(encoding="utf-8"), "html.parser")
        pages = soup.select(".page")
        body_parts = []
        for idx, page in enumerate(pages):
            if idx == 0:
                body_parts.append(self.cover(page))
            elif idx == 1:
                body_parts.append(self.toc(page))
            else:
                body_parts.append(self.body_page(page))
            if idx != len(pages) - 1:
                body_parts.append(self.section_break(idx + 2))
        body_parts.append(self.section_pr(len(pages)))
        ns_attrs = " ".join(f'xmlns:{k}="{v}"' for k, v in NS.items())
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:document {ns_attrs} mc:Ignorable="w14 w15 wp14"><w:body>'
            + "".join(body_parts)
            + "</w:body></w:document>"
        )

    def write_rels(self) -> None:
        rels = [
            ('rIdStyles', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles', 'styles.xml'),
            ('rIdSettings', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings', 'settings.xml'),
            ('rIdNumbering', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering', 'numbering.xml'),
            ('rIdFontTable', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable', 'fontTable.xml'),
            ('rIdFooter1', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer', 'footer1.xml'),
        ]
        rels.extend((rid, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image', target) for rid, target in self.image_rels)
        xml = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
               '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
        for rid, typ, target in rels:
            xml.append(f'<Relationship Id="{rid}" Type="{typ}" Target="{target}"/>')
        xml.append("</Relationships>")
        rel_path = self.unpacked_dir / "word" / "_rels" / "document.xml.rels"
        rel_path.parent.mkdir(parents=True, exist_ok=True)
        rel_path.write_text("".join(xml), encoding="utf-8")

    def write_footer(self) -> None:
        xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="{NS["w"]}" xmlns:r="{NS["r"]}">
<w:tbl><w:tblPr><w:tblW w:w="{CONTENT_W}" w:type="dxa"/>
<w:tblBorders><w:top w:val="single" w:sz="4" w:color="EEEEEE"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/><w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders>
<w:tblLayout w:type="fixed"/></w:tblPr>
<w:tblGrid><w:gridCol w:w="{mm_to_twip(92)}"/><w:gridCol w:w="{CONTENT_W - mm_to_twip(92)}"/></w:tblGrid><w:tr>
<w:tc><w:tcPr><w:tcW w:w="{mm_to_twip(92)}" w:type="dxa"/></w:tcPr>{self.paragraph(self.run("威富可 IMT050 说明书", size=5.4, color=GRAY, placeholder_prefix="footer_label"), after=0, line=1)}</w:tc>
<w:tc><w:tcPr><w:tcW w:w="{CONTENT_W - mm_to_twip(92)}" w:type="dxa"/></w:tcPr><w:p><w:pPr><w:jc w:val="right"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:eastAsia="Microsoft YaHei"/><w:color w:val="{GRAY}"/><w:sz w:val="11"/></w:rPr><w:fldChar w:fldCharType="begin"/><w:instrText xml:space="preserve">PAGE</w:instrText><w:fldChar w:fldCharType="separate"/><w:t>1</w:t><w:fldChar w:fldCharType="end"/></w:r></w:p></w:tc>
</w:tr></w:tbl></w:ftr>'''
        merged = dict(self.text.params)
        merged.update(self.text.provided)
        xml = materialize_template(xml, merged)
        (self.unpacked_dir / "word" / "footer1.xml").write_text(xml, encoding="utf-8")

    def patch_content_types(self) -> None:
        path = self.unpacked_dir / "[Content_Types].xml"
        path.write_text(
            '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpg" ContentType="image/jpeg"/>
<Default Extension="jpeg" ContentType="image/jpeg"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
<Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
</Types>''',
            encoding="utf-8",
        )


def prune_unpacked_template(unpacked: Path) -> None:
    word = unpacked / "word"
    for pattern in ("header*.xml", "footer*.xml", "comments.xml", "footnotes.xml", "endnotes.xml", "webSettings.xml"):
        for path in word.glob(pattern):
            path.unlink(missing_ok=True)
    media = word / "media"
    if media.exists():
        shutil.rmtree(media)
    media.mkdir(parents=True, exist_ok=True)
    for rel_dir in (word / "_rels",):
        if rel_dir.exists():
            for rel in rel_dir.glob("header*.rels"):
                rel.unlink(missing_ok=True)
            for rel in rel_dir.glob("footer*.rels"):
                rel.unlink(missing_ok=True)


def materialize_template(template: str, params: dict[str, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        return x(params.get(match.group(1), match.group(0)))

    return re.sub(r"\{\{([A-Za-z0-9_]+)\}\}", repl, template)


OOXML_ORDER = {
    "pPr": [
        "pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl", "numPr",
        "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap",
        "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN", "bidi", "adjustRightInd",
        "snapToGrid", "spacing", "ind", "contextualSpacing", "mirrorIndents", "suppressOverlap",
        "jc", "textDirection", "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle",
        "rPr", "sectPr", "pPrChange",
    ],
    "tblPr": [
        "tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize", "tblStyleColBandSize",
        "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders", "shd", "tblLayout", "tblCellMar",
        "tblLook", "tblCaption", "tblDescription", "tblPrChange",
    ],
    "tcPr": [
        "cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd", "noWrap", "tcMar",
        "textDirection", "tcFitText", "vAlign", "hideMark", "headers", "cellIns", "cellDel",
        "cellMerge", "tcPrChange",
    ],
    "tcBorders": ["top", "left", "bottom", "right", "insideH", "insideV", "tl2br", "tr2bl"],
    "tblBorders": ["top", "left", "bottom", "right", "insideH", "insideV"],
}


def local_name(tag: str) -> str:
    return etree.QName(tag).localname if isinstance(tag, str) else ""


def reorder_known_children(element: etree._Element, names: list[str]) -> None:
    order = {name: idx for idx, name in enumerate(names)}
    children = list(element)
    sorted_children = sorted(
        enumerate(children),
        key=lambda item: (order.get(local_name(item[1].tag), 999), item[0]),
    )
    if [child for _, child in sorted_children] != children:
        element[:] = [child for _, child in sorted_children]


def normalize_ooxml(unpacked: Path) -> None:
    parser = etree.XMLParser(remove_blank_text=False, recover=False)
    for xml_path in (unpacked / "word").rglob("*.xml"):
        try:
            tree = etree.parse(str(xml_path), parser)
        except Exception:
            continue
        root = tree.getroot()
        for element in root.iter():
            name = local_name(element.tag)
            if name in OOXML_ORDER:
                reorder_known_children(element, OOXML_ORDER[name])
            if name == "shd" and f"{{{NS['w']}}}val" not in element.attrib:
                element.set(f"{{{NS['w']}}}val", "clear")
                if f"{{{NS['w']}}}color" not in element.attrib:
                    element.set(f"{{{NS['w']}}}color", "auto")
            if name == "zoom" and f"{{{NS['w']}}}percent" not in element.attrib:
                element.set(f"{{{NS['w']}}}percent", "100")
        tree.write(str(xml_path), encoding="utf-8", xml_declaration=True, standalone=False)


def template_text_part(xml_path: Path, rel_name: str, text: TemplateText, provided: dict[str, str], template_root: Path) -> None:
    parser = etree.XMLParser(remove_blank_text=False, recover=False)
    tree = etree.parse(str(xml_path), parser)
    nodes: list[tuple[etree._Element, str]] = []
    prefix = re.sub(r"[^A-Za-z0-9]+", "_", rel_name).strip("_").lower() or "part"
    for node in tree.xpath(".//w:t", namespaces={"w": NS["w"]}):
        value = node.text or ""
        if value == "":
            continue
        key = text.key(prefix, value)
        nodes.append((node, key))
        node.text = "{{" + key + "}}"
    template_path = template_root / rel_name
    template_path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(str(template_path), encoding="utf-8", xml_declaration=True, standalone=False)
    for node, key in nodes:
        node.text = provided.get(key, text.params[key])
    tree.write(str(xml_path), encoding="utf-8", xml_declaration=True, standalone=False)


def build_from_reference(out_path: Path, params_path: Path | None = None) -> None:
    out_path = out_path.resolve()
    iter_dir = out_path.parent
    iter_dir.mkdir(parents=True, exist_ok=True)
    unpacked = iter_dir / "_unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)

    run([sys.executable, str(UNPACK), str(W27_REFERENCE), str(unpacked), "--merge-runs", "false"], Path.cwd())

    provided = {}
    if params_path and params_path.exists():
        provided = json.loads(params_path.read_text(encoding="utf-8"))
    text = TemplateText(provided)
    template_root = iter_dir / "template_parts"
    if template_root.exists():
        shutil.rmtree(template_root)

    target_parts = [unpacked / "word" / "document.xml"]
    target_parts.extend(sorted((unpacked / "word").glob("header*.xml")))
    target_parts.extend(sorted((unpacked / "word").glob("footer*.xml")))
    for part in target_parts:
        if part.exists():
            rel = part.relative_to(unpacked).as_posix()
            template_text_part(part, rel, text, provided, template_root)

    normalize_ooxml(unpacked)
    merged_params = dict(text.params)
    merged_params.update(provided)
    (iter_dir / "text_params.json").write_text(json.dumps(text.params, ensure_ascii=False, indent=2), encoding="utf-8")
    if params_path:
        params_path.write_text(json.dumps(merged_params, ensure_ascii=False, indent=2), encoding="utf-8")

    run([sys.executable, str(PACK), str(unpacked), str(out_path), "--validate", "false"], Path.cwd())


def run(cmd: list[str], cwd: Path) -> None:
    env = dict(__import__("os").environ)
    env["PYTHONUTF8"] = "1"
    proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, env=env, timeout=180)
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    if proc.returncode:
        raise SystemExit(proc.returncode)


def build(out_path: Path, params_path: Path | None = None) -> None:
    build_from_reference(out_path, params_path)
    return

    out_path = out_path.resolve()
    iter_dir = out_path.parent
    iter_dir.mkdir(parents=True, exist_ok=True)
    unpacked = iter_dir / "_unpacked"
    if unpacked.exists():
        shutil.rmtree(unpacked)
    run([sys.executable, str(UNPACK), str(BASE_TEMPLATE), str(unpacked), "--merge-runs", "false"], Path.cwd())
    prune_unpacked_template(unpacked)

    provided = {}
    if params_path and params_path.exists():
        provided = json.loads(params_path.read_text(encoding="utf-8"))
    text = TemplateText(provided)
    builder = OoxmlBuilder(unpacked, text)
    template_xml = builder.document_xml()
    merged_params = dict(text.params)
    merged_params.update(provided)
    final_xml = materialize_template(template_xml, merged_params)

    (unpacked / "word" / "document.xml").write_text(final_xml, encoding="utf-8")
    builder.write_footer()
    builder.write_rels()
    builder.patch_content_types()
    merged_params = dict(text.params)
    merged_params.update(provided)
    (iter_dir / "document.template.xml").write_text(template_xml, encoding="utf-8")
    (iter_dir / "text_params.json").write_text(json.dumps(text.params, ensure_ascii=False, indent=2), encoding="utf-8")
    if params_path:
        params_path.write_text(json.dumps(merged_params, ensure_ascii=False, indent=2), encoding="utf-8")

    run([sys.executable, str(PACK), str(unpacked), str(out_path), "--original", str(BASE_TEMPLATE)], Path.cwd())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    parser.add_argument("--params", type=Path)
    args = parser.parse_args()
    build(args.out, args.params)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
