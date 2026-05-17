# anti-cheat.py 实现骨架

> 规范定义在 `swiss/QA-RULES.md §8.2`（SOT）。本文是 docx 流水线的 Python 实现。

## 用法
```bash
python anti_cheat.py output/imt050-wevac-eu-de.docx \
    --baseline final/imt050-wevac-eu-cn.docx
# 退出码：0 = 全通过，1 = 任一 ERROR
```

## 实现

```python
#!/usr/bin/env python3
"""anti-cheat 三道闸 + 辅助检查 (QA-RULES §8.2)"""
import sys
import re
import zipfile
import argparse
from pathlib import Path


def count_wt(docx_path: Path) -> int:
    """w:t 节点数。阈值 ≥ 300。"""
    with zipfile.ZipFile(docx_path) as z:
        xml = z.read('word/document.xml').decode('utf-8')
    return len(re.findall(r'<w:t[ >/]', xml))


def count_media(docx_path: Path) -> int:
    """word/media/ 文件数。比 baseline 多 ≥ 2 视为 image_hack。"""
    with zipfile.ZipFile(docx_path) as z:
        return len([n for n in z.namelist() if n.startswith('word/media/')])


def count_chars(docx_path: Path) -> int:
    """所有文本字符数（用于 text_ratio）。"""
    from docx import Document
    doc = Document(str(docx_path))
    total = sum(len(p.text) for p in doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                total += len(cell.text)
    return total


def count_pages(docx_path: Path) -> int:
    """LO headless 转 PDF → 数页数。"""
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ['soffice', '--headless', '--convert-to', 'pdf',
             '--outdir', tmp, str(docx_path)],
            check=True, capture_output=True
        )
        pdf_path = Path(tmp) / docx_path.with_suffix('.pdf').name
        import pypdf
        return len(pypdf.PdfReader(str(pdf_path)).pages)


def check_word_com(docx_path: Path) -> bool:
    """docx2pdf 试转 → 不报错即 Word COM 可打开。W28 教训硬约束。"""
    try:
        from docx2pdf import convert
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'word_check.pdf'
            convert(str(docx_path), str(out))
            return out.exists() and out.stat().st_size > 0
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('docx', type=Path)
    ap.add_argument('--baseline', type=Path, required=True,
                    help='W50 cn docx for ratio baselines')
    ap.add_argument('--skip-word-com', action='store_true',
                    help='本机无 MS Word 时跳过（仅 dev）')
    args = ap.parse_args()

    results = []

    # 1. wt_count ≥ 300
    wt = count_wt(args.docx)
    results.append(('wt_count', wt >= 300, f'wt_count={wt}'))

    # 2. image_hack（media count 异常）
    media_actual = count_media(args.docx)
    media_baseline = count_media(args.baseline)
    image_hack = media_actual > media_baseline + 1
    results.append(('image_hack', not image_hack,
                    f'media={media_actual} baseline={media_baseline}'))

    # 3. text_ratio ∈ [0.95, 1.20]
    actual = count_chars(args.docx)
    baseline = count_chars(args.baseline)
    ratio = actual / baseline if baseline else 0
    results.append(('text_ratio', 0.95 <= ratio <= 1.20,
                    f'ratio={ratio:.3f}'))

    # 4. 页数 = 15 (±1)
    pages = count_pages(args.docx)
    results.append(('page_count', 14 <= pages <= 16, f'pages={pages}'))

    # 5. Word COM
    if not args.skip_word_com:
        results.append(('word_com', check_word_com(args.docx), 'docx2pdf'))

    # 输出
    ok = all(passed for _, passed, _ in results)
    for name, passed, detail in results:
        mark = 'PASS' if passed else 'FAIL'
        print(f'[{mark}] {name}: {detail}')

    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
```

## 部署位置
`swiss/tools/docx-pipeline/anti_cheat.py`

## 跑的时机
- 每次 `generator.py` 跑完
- 每次 `ai-qa.py` 应用 patch 后
- QA Phase 5 全变体验证

## 失败时的处理
按 `fix-checklist.md` §二 "Fix 决策表" 处理。**不许改阈值绕过**。

## 与 SOT 的关系

阈值定义在 `QA-RULES.md §8.2`，本脚本是实现。任何阈值变动 → 改 SOT → 本脚本同步。
