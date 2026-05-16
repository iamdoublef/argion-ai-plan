# 候选 DOCX 评分排行榜

（按 PASS/FAIL 然后 visual overall 升序）


| 候选 | 页数 | 文本比 | 编辑% | 视觉(o/m) | P/T/E/V | 总评 |
|---|---|---|---|---|---|---|
| `path-b-codex/b1-docx-skill/iter-02/output.docx` | 15/15 | 1.01 | 100.0 | 13.59/24.16 | ✓/✓/✓/✓ | **PASS** |
| `path-b-codex/b1-docx-skill/iter-03/output.docx` | 15/15 | 1.03 | 100.0 | 13.59/24.18 | ✓/✓/✓/✓ | **PASS** |
| `path-b-codex/b2-custom/iter-02/output.docx` | 15/15 | 0.98 | 100.0 | 14.4/34.1 | ✓/✓/✓/✓ | **PASS** |
| `path-b-codex/b1-docx-skill/iter-01/output.docx` | 14/15 | 1.0 | 100.0 | 14.52/26.03 | ✓/✓/✓/✓ | **PASS** |
| `path-b-codex/b2-custom/iter-03/output.docx` | 15/15 | 1.0 | 100.0 | 14.57/34.1 | ✓/✓/✓/✓ | **PASS** |
| `path-a-claude/a1-docx-skill/FINAL-output.docx` | 15/15 | 1.0 | 100.0 | 14.92/25.45 | ✓/✓/✓/✓ | **PASS** |
| `path-a-claude/a2-custom/iter-01/baseline.docx` | 16/15 | 1.01 | 100.0 | 15.01/25.14 | ✓/✓/✓/✓ | **PASS** |
| `path-a-claude/a2-custom/iter-02/output.docx` | 16/15 | 1.01 | 100.0 | 16.5/28.09 | ✓/✓/✓/✓ | **PASS** |
| `path-a-claude/a2-custom/iter-04/output.docx` | 15/15 | 1.0 | 100.0 | 16.53/28.14 | ✓/✓/✓/✓ | **PASS** |
| `path-a-claude/a2-custom/iter-03/output.docx` | 15/15 | 1.0 | 100.0 | 16.54/28.14 | ✓/✓/✓/✓ | **PASS** |
| `path-a-claude/a2-custom/iter-05/output.docx` | 15/15 | 1.0 | 100.0 | 16.65/28.14 | ✓/✓/✓/✓ | **PASS** |
| `path-b-codex/b2-custom/iter-01/output.docx` | 15/15 | 0.98 | 100.0 | 17.65/34.6 | ✓/✓/✓/✓ | **PASS** |
| `final/0-pre-iteration-baseline-24pages.docx` | 24/15 | 1.07 | 100.0 | 15.44/27.74 | ✗/✓/✓/✓ | **FAIL** |
| `path-a-claude/a2-custom/iter-01/output.docx` | 21/15 | 1.07 | 100.0 | 15.82/25.35 | ✗/✓/✓/✓ | **FAIL** |

## 验收标准
- 页数（P）：candidate ≤ target+1
- 文本（T）：candidate ≥ target × 0.95
- 可编辑（E）：所有文本在 `<w:t>` 而非 `<wp:txbx>`，editable% ≥ 95
- 视觉（V）：所有页平均像素差异 ≤ 60（0-255）
