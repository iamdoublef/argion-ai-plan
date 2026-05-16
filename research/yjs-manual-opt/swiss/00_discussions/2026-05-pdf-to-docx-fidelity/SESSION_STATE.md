---
status: in-progress
branch: main
timestamp: 2026-05-16T22:41:29+08:00
session_focus: PDF→Word 像素级美感复刻（4 路并行）
files_modified:
  - .claude/settings.local.json
  - .github/copilot-instructions.md
  - research/yjs-manual-opt/swiss/output/imt050-wevac-eu-cn.docx
  - research/yjs-manual-opt/swiss/output/v23-wevac-eu-cn.docx
  - research/yjs-manual-opt/swiss/template/shared/base/brand-themes.json
  - research/yjs-manual-opt/swiss/tools/export-docx.js
new_dirs:
  - research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/
  - research/yjs-manual-opt/_inbox/参考方案/
  - tmp/
schedule_wakeup:
  - delay_seconds: 3600
  - reason: 大 boss 要求每小时确认一次设计迭代进度
  - prompt_goal: "完全不能接受，一点美感都没有，跟pdf的排版相差太大了，你要生成图片来进行像素级别的对比。"
---

## Working on：PDF→Word 像素级美感复刻

### 总目标

把 `research/yjs-manual-opt/swiss/output/imt050-wevac-eu-cn.pdf`（15 页 A5 中文说明书，威富可 IMT050 制冰机）
复刻为可编辑 Word 文件。客户要可局部修改的 Word，PDF 仅作视觉模板。

### 当前阶段：design-iter-01（美感专项）

**用户判定**：第 1 轮 4 路虽然全部"自动验收 PASS"（视觉差 13.59-16.65），但**视觉美感与 PDF 相差太大，不能接受**。
需要重新进入设计专家模式，做像素级对比 + 持续迭代直到达到 PDF 美感。

刚开始第 2 大轮（design-iter-01）。已完成：
- 200dpi 重渲染目标 PDF（15 页）→ `design-iter-01/hires_target/page-01..15.png`
- 200dpi 重渲染 winner DOCX→PDF → `design-iter-01/hires_winner/page-01..15.png`
- 已设 ScheduleWakeup 60 分钟唤醒（每小时确认）

下一步要做：逐页设计差距清单 + 启动 4 路新一轮（与之前策略一致：2 Claude + 2 Codex）

### 已完成的第 1 大轮（design-iter-00，4 路并行）

4 路全部 PASS（14 个候选 ≤16 页 + 100% 可编辑），但用户拒收（美感不够）：

| 路径 | 工具链 | 最佳 iter | 视觉差 |
|---|---|---|---|
| **B1**（winner 数值） | Codex + docx skill 严格（docx-js fork + 静态 TOC） | iter-03 | 13.59 |
| B2 | Codex + python-docx + HTML 解析 | iter-03 | 14.57 |
| A1 | Claude + docx skill 严格（unpack/edit XML） | FINAL (iter-03) | 14.92 |
| A2 | Claude + python-docx 从 JSON | iter-05 | 16.65 |

**重要**：B1 codex 直接修改了 `research/yjs-manual-opt/swiss/tools/export-docx.js` 主版本（+398 / -197 行）。这是未提交的 working tree 变更，要保留还是回滚由大 boss 决定。

### 关键决策与发现（4 路共识）

1. **客户要可编辑 Word**：禁用 pdf2docx（文本框无法编辑）；全部走 docx-js 或 python-docx 重建。
2. **页数膨胀根因**：原版 docx-js 用 11pt 字号 + 70 DXA cell margins → 24 页。改成 7.5pt + 40-50 margins → 15 页。
3. **PDF 实测字体**：MicrosoftYaHei（不是宋体）+ Arial。色彩 #1A1A1A 主黑 / #E63946 accent 红 / #8E8E93 灰。
4. **TOC 必须静态**：LibreOffice headless 不刷新 Word TOC 字段 → 必须自渲染 TOC 表。
5. **章节标题不强制分页**：移除 pageBreakBefore，让内容紧接标题。
6. **docx skill 在 Windows 修复**：
   - `validate.py` 需 `PYTHONUTF8=1` 才不报 gbk codec 错
   - `scripts/office/schemas/` 子目录本地缺失，从 GitHub 补齐（4 个目录、39 个 .xsd）

### 美感问题清单（待第 2 大轮解决）

从 side-by-side 对比图（200dpi）目测：
1. **封面布局错位**：
   - PDF：顶部"威富可"小字 + 短红线（左上角），居中产品图（小），底部 MODEL + 制冰机 + 说明书 + 红线 + 中文 disclaimer 两行 + 黑色细分隔线
   - B1 winner：顶部红线（贯穿整宽，粗）+"威富可"大红字 + 居中产品图（大），底部 disclaimer 一行（没分隔线）
2. **章节标题左侧色块**：PDF 黑色细 bar，候选用了粗 bar 或红色 bar
3. **WARNING 框**：PDF 有顶部 ▲ 警告图标，候选缺这个图标
4. **整体留白节奏**：PDF 紧凑但有节奏感，候选偏松散

### 关键资产路径

| 资产 | 路径 |
|---|---|
| 目标 PDF | `research/yjs-manual-opt/swiss/output/imt050-wevac-eu-cn.pdf` |
| 源 HTML | `research/yjs-manual-opt/swiss/output/imt050-wevac-eu-cn.html` |
| 源 JSON | `research/yjs-manual-opt/swiss/products/imt050/{product.json,images.json}` |
| 共享 brief | `research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/BRIEF_SHARED.md` |
| 评分工具 | `.../2026-05-pdf-to-docx-fidelity/score_candidate.py` |
| 对比工具 | `.../2026-05-pdf-to-docx-fidelity/compare_pdfs.py` |
| 探查工具 | `.../2026-05-pdf-to-docx-fidelity/probe_pdf.py` |
| 排行榜 | `.../2026-05-pdf-to-docx-fidelity/RANKING.md` |
| Codex 第三方裁决 | `.../2026-05-pdf-to-docx-fidelity/CROSS_REVIEW.md` |
| Final 候选 | `.../2026-05-pdf-to-docx-fidelity/final/candidates/` |
| 工作目录 | `.../2026-05-pdf-to-docx-fidelity/design-iter-01/` |

### 工具链（已验证 Windows + git bash）

- LibreOffice：`C:\Program Files\LibreOffice\program\soffice.exe`
- Node 22 + docx-js 9.6.0（项目根已 npm install）
- Python 3.12 + PyMuPDF 1.26.6 + python-docx 1.2.0 + Pillow 9.5.0 + bs4
- pandoc 3.9.0.2
- Codex CLI 0.130.0（gpt-5.5，--dangerously-bypass-approvals-and-sandbox 模式）
- docx skill：`C:\Users\iamdo\.claude\skills\docx\scripts\office\`（schemas 已补齐）

### Pillow segfault 兜底

Pillow 9.5.0 + 多次 `Image.open` + LANCZOS 在循环超过 17 张时 segfault。`compare_pdfs.py compare` 已加 `gc.collect()` 缓解，但有时仍需重跑或用 codex 写的 fallback。

### 远未完成 / Notes

1. **下一步立刻做**（同会话继续）：逐页设计差距清单 + 启动 4 路第 2 大轮
2. **每小时确认**：ScheduleWakeup 已设 3600s，自动唤醒检查迭代进度
3. **额度耗尽对策**：用户授权暂停，下一循环继续
4. **A2/A1/B1/B2 sub-agent task IDs**（如需 SendMessage 续接）：
   - A1: a2dda796329fd0923（已完成）
   - A2: acd0e280a0411b382（已完成）
   - B1: bqfllxrpa（已完成 exit 0）
   - B2: bl7f2ksly（已完成 exit 0）
   - 新一轮要重启 4 个 agent（SendMessage 续接受限于 token 预算，新 Agent 调用更稳）
5. **未提交主版改动**：B1 codex 已改 export-docx.js 主版（紧凑化），大 boss 决定是否 commit
6. **CLAUDE.md 风格规则**：人称"管理之神 / 大 boss"，企业负责人统一称"管理者"

### 下次会话恢复入口

读：
1. 本文件 `SESSION_STATE.md`
2. `RANKING.md` — 看 14 个候选评分
3. `CROSS_REVIEW.md` — 看 Codex 的独立裁决
4. `log.md` — 看完整实验流水
5. `BRIEF_SHARED.md` — 共享技术 brief
6. `design-iter-01/` 工作目录（如果有新一轮产出）

恢复后第一件事：检查 `design-iter-01/` 是否已有 sub-agent 产出（B1/B2 codex 后台进程的 codex_log.txt 是关键看板）。
