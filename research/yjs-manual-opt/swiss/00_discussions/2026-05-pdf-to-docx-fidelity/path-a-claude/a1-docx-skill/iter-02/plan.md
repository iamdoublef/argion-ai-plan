# iter-02 plan — 修品牌色块 + 修页眉裁切 + 微调封面图

## 起点
iter-01 已经 15 页、视觉对齐、可编辑。剩下"锦上添花"的差距：

A. 页眉右上裁切（"CH.01 — SAF" 应为 "CH.01 — SAFETY"）
B. 章节左侧色块：iter-01 黑色细 bar；target 红色粗块
C. 第 3 页警告框略溢出
D. 封面产品图位置不够居中

## 本轮改动
1. **chapterBar 颜色**：theme `chapterBar: '000000'` → `chapterBar: ACTIVE_THEME.accent`（在 renderChapterHeading 里直接用 `ACTIVE_THEME.accent`）
2. **chapterBar 厚度**：border size 12 → 30（更粗的色块）
3. **页眉 tabStop 位置**：从 `TabStopPosition.MAX` 改为显式 `CONTENT_W - 50`，确保 SAFETY 等长字串能完整显示
4. **第 3 页警告框正文（"为了您的安全…"）**：把章节首段 size 调小一档（17 半点）；本轮先不动 box 自身
5. **封面产品图 alignment.CENTER**：替换 AlignmentType.LEFT
6. **轻微提示**：底部 disclaimer 字号 16 → 14（更接近 PDF 看着的小字）
