# 实验流水日志

格式：每次尝试一节，含 `时间`、`路径`、`方法`、`命令`、`产物`、`保真度评估`、`下一步`。

---

## 2026-05-16 00:00 · Setup · 环境检查与基线规划

**操作**：
- 验证工具链：LibreOffice 在 `C:\Program Files\LibreOffice\program\soffice.exe`；Node 22 + docx-js 9.6.0；Python 3.12 + PyMuPDF 1.26.6 + python-docx 1.2.0；pandoc 3.9.0.2。
- 创建工作目录 `swiss/00_discussions/2026-05-pdf-to-docx-fidelity/{baseline,path-a-claude,path-b-codex,screenshots}`。
- 读取 `export-docx.js` 1646 行，弄清 JSON→DOCX 现有链路。
- 准备双路径并行：A=Claude/docx-js 优化；B=Codex/PDF 直转。

**待办**：
1. 渲染目标 PDF 为 PNG（基线 G0）。
2. 把现有 DOCX 转 PDF，再渲染 PNG（基线 D0），与 G0 并排对比。
3. 启动两条路径 iter-01。

---

## 2026-05-16 00:30 · Baseline · 基线诊断完成

**操作**：
- 渲染目标 PDF → 15 页 PNG（150dpi），存 `baseline/target_png/`
- LibreOffice 把现有 DOCX 转 PDF → **24 页**，存 `baseline/current_docx_pdf/`，再渲染 PNG 存 `baseline/current_docx_png/`
- 并排对比 24 张 PNG 存 `baseline/side_by_side/`

**问题清单（按优先级）**：

| # | 严重度 | 现象 | 根因 | 修复方向 |
|---|---|---|---|---|
| 1 | P0 | DOCX 24 页 vs PDF 15 页（+60%） | 行距、段距、`pageBreakBefore` 过松 | 紧凑化 spacing；移除多余 page break |
| 2 | P0 | 目录页空白（只有"目录"标题，无条目） | docx-js TOC 是 Word field，LibreOffice headless 不更新字段 | 自渲染 TOC 为静态表格 / 调用 Word 自动刷新 |
| 3 | P0 | 章节封面页几乎空白（标题独占一页） | `renderChapterHeading` 后内容被推到下一页 | 移除章节标题独占页的强制分页 |
| 4 | P1 | 封面：品牌名"威富可"字号过大；少 letter-spacing；产品图过大；底部缺失中文免责声明 | `coverBrandSize` 36 偏大；`characterSpacing` 80 不够；`cover.width` 360 偏大；disclaimer 段没渲染 | 调字号到 28，spacing 到 160；图改 280；确保 disclaimer 段输出 |
| 5 | P1 | 表格、警告框、step flow 内边距偏大 | `CELL_MARGINS` top=70 偏大 | 紧凑模式默认开启 |
| 6 | P2 | 页眉右侧 chapter ref 被裁切 | tabStop 计算不准 | 用 `RIGHT_TAB` 到 `MAX` |
| 7 | P2 | 中文渲染：DOCX 用宋体，PDF 用 puppeteer 默认（更接近无衬线/思源） | 字体差异 | DOCX 改用思源黑体/微软雅黑作为 cjk 字体 |

**裁决标准**（用于后续 iter 评估）：
- 量化指标：DOCX→PDF 后 ≤16 页（目标 15）= 通过
- 视觉相似度：每页 side-by-side 对比，关键元素（红色 accent line、章节编号色块、表格、警告框）位置误差 <5%
- 文本完整：所有 PDF 中可见文本在 DOCX 中存在

**下一步**：
- 启动路径 A（Claude） — 直接改 `export-docx.js`，紧凑化 + 修 TOC + 修首页 → iter-01
- 启动路径 B（Codex） — 通过 codex-batch-executor 让 Codex 用完全不同路径（pdf2docx / pandoc）做尝试

---

## 2026-05-16 01:00 · Launch · 启动 4 路并行（重新校准目标后）

**用户校准**：客户要的是**可编辑 Word**，PDF 仅是视觉参考。pdf2docx 直转方案被排除（文本框不可编辑）。

**docx skill 升级检查**：
- 本地 `C:\Users\iamdo\.claude\skills\docx\SKILL.md` = 20084 字节
- 官方 GitHub `anthropics/skills` 上的 SKILL.md 内容比对完全一致
- 结论：本地已是最新，无需升级

**4 路启动**：
| 路径 | 执行方 | 约束 | 后台 ID |
|---|---|---|---|
| A1 | Claude swiss-manual-writer agent | 严格 docx skill 工具链（docx-js / unpack-pack） | a2dda796329fd0923 |
| A2 | Claude general-purpose agent | 自选最佳路径（pandoc / python-docx / 混合） | acd0e280a0411b382 |
| B1 | Codex (gpt-5.5) 后台进程 | 严格 docx skill 工具链 | bqfllxrpa |
| B2 | Codex (gpt-5.5) 后台进程 | 自选最佳路径 | bl7f2ksly |

每条路径都有自己的工作目录、独立 iter，互不干扰。

**主控期间辅助**：探查 PDF 内嵌字体、丰富对比指标。

---

## 2026-05-16 01:30 · Midpoint · 4 路 iter-01 中期评分

**第一轮全部完成评估**（自动用 `score_candidate.py`）。

| 路径 | iter | 页数 | 文本比 | 编辑% | 视觉差(overall/max) | 验收 |
|---|---|---|---|---|---|---|
| **B2 (Codex 自选)** | iter-01 | 15/15 ✓ | 0.98 ✓ | 100 ✓ | 17.65/34.6 ✓ | **PASS** |
| **A1 (Claude/docx-skill)** | iter-01 | 16/15 ✓ | 0.99 ✓ | 100 ✓ | 15.61/25.28 ✓ | **PASS** |
| A2 (Claude 自选) baseline-pandoc | n/a | 16/15 ✓ | 1.01 ✓ | 100 ✓ | 15.01/25.14 ✓ | PASS (但视觉简陋) |
| A2 (Claude 自选) output | iter-01 | 21/15 ✗ | 1.07 | 100 | 15.82/25.35 | FAIL |
| B1 (Codex/docx-skill) | 进行中 | — | — | — | — | 运行 |
| baseline (export-docx.js 原版) | — | 24/15 ✗ | 1.07 | 100 | 15.44/27.74 ✓ | FAIL |

**视觉对比关键观察**：
- **A1 iter-01** 封面：顶部"威富可"+短红线 + 居中产品图 + 底部红线 + 中文 disclaimer + 黑色细分割线，与 PDF 高度一致
- **B2 iter-01** 封面：右侧布局，元素齐全（accent 红线、品牌名、MODEL 红字、制冰机、说明书、disclaimer），略偏右但视觉效果好
- **A2 pandoc baseline**：纯文本流，无设计元素 — visual diff 低是因为白边多产生的"误判"，不是真接近
- **A2 output**：与 baseline 类似但 21 页（A2 build_docx.py 仍在演进，未达预期）

**当前 winner（并列）**：A1 iter-01（设计还原最贴）+ B2 iter-01（页数精确 15）

**重要洞察**：visual diff 不是唯一指标 — 必须人工看 side-by-side 图判断"设计感是否传递"。

**下一步**：
- 等 B1 出 iter-01；等 A2、B2 出 iter-02
- 最终在 A1 / B2 / B1 / 升级版 A2 中四选一
- 如果两个候选差不多，让客户决定（或两个都交付）

---

## 2026-05-16 01:50 · Convergence · 4 路全部达标

**最终评分**（按 visual overall 升序，全部 PASS 的取每路最佳 iter）：

| 排名 | 候选 | iter | 页数 | 视觉差(o/m) | 备注 |
|---|---|---|---|---|---|
| 1 | **B1 iter-03** | docx-js 改造 + 静态 TOC | 15/15 | 13.59/24.18 | Codex 通过 export-docx.js fork |
| 2 | B2 iter-03 | python-docx + HTML 解析 | 15/15 | 14.57/34.10 | Codex 自给自足脚本 |
| 3 | A1 iter-02 | docx-js 改造 + 章节色块 | 15/15 | 14.71/25.19 | Claude 严守 docx skill 流程，封面最忠实 PDF |
| 4 | A2 iter-04 | python-docx + 模板 | 15/15 | 16.53/28.14 | Claude 自选路径 |

**Codex 双路 1-2 位**（13.59/14.57），**Claude 双路 3-4 位**（14.71/16.53）。
四路都做到 **15 页 + 100% 可编辑文本**。

**关键技术发现**（共享 BRIEF）：
- PDF 实际用 MicrosoftYaHei，不是宋体（现有 export-docx.js 字体配错）
- 字号 7.5pt → DOCX size 15 half-pt（现有 22 偏大，导致页数膨胀）
- accent 红 `#E63946` / 主黑 `#1A1A1A` / 灰 `#8E8E93`
- LibreOffice headless 不刷新 Word TOC field → 必须用静态 TOC
- `docx skill validate.py` 在 Windows 需 `PYTHONUTF8=1` 才不报 gbk codec 错
- docx skill 缺失 `schemas/` 子目录，需从 GitHub 补齐
- pdf2docx 输出文本框、客户无法编辑，必须放弃

**Final 候选已暂存** `final/candidates/`：
- `B1-iter03_visualdiff_13.59.docx`（数值最优）
- `A1-iter02_visualdiff_14.71.docx`（设计最忠实）
- `B2-iter03_visualdiff_14.57.docx`（独立自洽脚本）
- `A2-iter04_visualdiff_16.53.docx`
- `0-original_baseline_24pages_FAIL.docx`（原版，FAIL）
- `_target.pdf`（参考目标）

**Cross-review codex** 仍在跑（独立第三方评判），完成后写 CROSS_REVIEW.md。

---

## 2026-05-16 02:00 · Final · 收官

**Codex 独立 cross-review 出结果**（`CROSS_REVIEW.md`）：
- Winner: B1 iter-03（同我自评）
- Runner-up: B2 iter-03

**意外发现**：B1 codex 不仅在 path-b-codex/b1-docx-skill/ 里做迭代，还**直接修改了主版** `swiss/tools/export-docx.js`（398 insertions, 197 deletions）。验证：
```
node export-docx.js --region cn --product products/imt050
→ 15 pages, visual diff 13.59, PASS
```
**主版已自动沉淀紧凑方案**，下次新产品只需照常跑 export-docx.js 即可。

**多 region 验证**：cn / gb / hk 全部产出 15 页 docx（与目标 PDF 一致）。

**Final 交付**：
- `final/imt050-wevac-eu-cn.docx` — 推荐交付（视觉差 13.59）
- `final/imt050-wevac-eu-cn.preview.pdf` — DOCX→PDF 预览
- `final/0-pre-iteration-baseline-24pages.docx` — 实验前备份
- `final/candidates/*.docx` — 4 路最佳 iter 备选
- `FINAL_REPORT.md` — 给大 boss 看的综合报告
- `CROSS_REVIEW.md` — Codex 独立裁决
- `RANKING.md` — 13 个候选完整评分

**待大 boss 拍板**：
1. 接受 winner 直接覆盖 `swiss/output/imt050-wevac-eu-cn.docx`
2. 或先用 final/imt050-wevac-eu-cn.docx 在 Word 实测编辑性，确认后再交付
3. （主版 export-docx.js 已被 B1 改成紧凑版，影响所有 region/brand 后续产出 — 这是个 commit 级决策，需大 boss 确认是否 commit）






