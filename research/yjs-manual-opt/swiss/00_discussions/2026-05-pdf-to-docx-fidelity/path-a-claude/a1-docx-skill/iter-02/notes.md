# iter-02 notes — 修品牌色块 + 修页眉裁切 + 微调封面

## TL;DR

iter-02 进一步把视觉细节对齐了 iter-01 的小瑕疵：

| 项 | iter-01 | iter-02 |
|---|---|---|
| 页眉 chapter ref | "CH.01 — SAF" (clipped) | "CH.01 — SAFETY" ✓ |
| 章节左侧色块 | 黑色细线 | **红色粗块** ✓ |
| 页脚 page number | "第 ... 页" 显示 | "第 4 页" 完整 ✓ |
| 封面产品图 | 左对齐贴顶 | 左对齐但下沉到页面中部 ✓ |
| 总页数 | 15 | **15** ✓ |

## 改动

1. `renderChapterHeading` — `border.left.size: 18 → 80`，颜色从 `chapterBar`（黑） 改成 `ACTIVE_THEME.accent`（红），indent 140 → 220，space:6
2. `chapterNumberSize: 30 → 26`，`chapterTitleSize: 28 → 30` （让数字与标题字号关系更接近 PDF）
3. `buildHeader` / `buildFooter` — `tabStops.position` 从 `TabStopPosition.MAX` (9072) 改为 `CONTENT_W` (≈7256)，让右对齐文本不再被裁切
4. 封面：
   - 中间空段从 4 个 → 5 个（每段 line=240，把产品图向下推 ~10mm）
   - 产品图 alignment 保持 LEFT（target 也是左对齐）
   - disclaimer 字号 16 → 14（更接近 PDF 视觉小字）

## 验收检查

```
unpack iter-02/output.docx → wp:txbx 数量: 0
<w:t> 节点: 319 (vs baseline 0)
DOCX→PDF: 15 页
```

## 是否还需要 iter-03？

我反复对比 iter-02 vs target 各页：

- 1-3 页（封面/目录/安全须知）：差距已经在视觉细节级（产品图大小、章节红块长度），不影响"可识别为同一份手册"
- 4-15 页：内容、表格、警告框、step number、底部 brand 信息基本对齐
- 所有验收硬指标已满足：≤16 页（15）、TOC 不空、所有文本可编辑、视觉相似度 OK

**iter-02 是建议的最终交付版本**。可能进一步打磨的地方：

- 第 3 页 WARNING box 24 个 bullet 把 box 撑到贴底 — 接近溢出但能装下。如果担心未来增删内容，可以把章节首段（"为了您的安全…" 那行）字号再调小或改成"标题+引言"两行。
- 章节标题左红块比 target 略长，因为 paragraph border-left 会跑满整段（包括行高），target 是高度等于"01"字号的方块。如果一定要精准复刻，需要用 1×3 表格替代 — 但那会丢失现有 keepNext 行为，权衡后我选择保持 paragraph border 方案。
