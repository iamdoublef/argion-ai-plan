# iter-1: w:kern现状grep

## Findings
- `word/document.xml` 中 **0** 处 `<w:kern>` → body 文本完全没用 kerning
- `word/styles.xml`: 2 处, both for sz=52 large headings, val=28
- `word/stylesWithEffects.xml`: 2 处, 同 styles.xml (mirror copy)

## Implication
w:kern 是真正未开垦的维度。整个文档 body 跑在 kerning OFF 状态。
后续 iter 可以在 document.xml 的 rPr 里直接加 `<w:kern w:val="X"/>`，
threshold X 半点单位:
- val=2  → 启用 1pt+ 字体 kerning（≈所有正文）
- val=14 → 启用 7pt+ 字体 kerning（≈大部分正文，过滤掉脚注）
- val=22 → 启用 11pt+ 字体（≈sz=11+, 仅sz≥14 启用）
- val=28 → 现有 heading 用的值，启用 14pt+ 字体

## 候选战场
按 iter-39 的 sz cohort 普查：
- sz=14 black: 71 sites（已在 W32 winning spacing=8 上，加 kern 不动 spacing）
- sz=12 (6pt): 后续 grep 计数
- sz=11 (5.5pt, footer): 后续 grep 计数
