# IMT050 Word DOCX 视觉保真评分记录

## 当前最优：W29（design-iter-33 OOXML 微调）

- **文件**: `final/imt050-wevac-eu-cn.docx`
- **LibreOffice 渲染评分**: `8.63 / 12.30`（mean / max）— 突破 W27 plateau
- **Anti-cheat**: PASS（wt_count=445, image_hack=false, text_ratio=1.0, drawings=16）
- **MS Word 可打开**: PASS（docx2pdf Word COM 渲染 15 页）
- **页数**: 15（与目标 PDF 一致）
- **可编辑性**: 100%（无 text_box / 图片 hack）
- **突破手法**: per-section pgMar w:top 子像素微调（p3/p5/p9/p12/p13 各 +3 twips，p14 +1 twip）
- **详见**: `design-iter-33/path-ooxml-microtune/STATUS.md`

## 历史 W27（前 plateau）

- **LibreOffice 渲染评分**: `8.67 / 12.35`（mean / max）
- **MS Word 渲染评分**: `9.16 / 15.27`（mean / max）
- 已被 W29 替换

## 评分基准说明

`score_candidate.py` 用 LibreOffice headless 渲染 docx→PDF→PNG，与目标 PDF 的 PNG 比对 mean RGB 差。
- **优点**: 与目标 PDF 的 Adobe 渲染较接近（freetype 基础一致）
- **缺点**: 客户实际打开用 MS Word，Word 渲染中文字距/行距与 LibreOffice 不同

## 28 路径迭代历史（按 visualdiff 升序）

| Winner | Path | Visualdiff | 备注 |
|--------|------|-----------|------|
| W29 | design-iter-33 path-ooxml-microtune | **8.63 / 12.30** | **当前 final** — pgMar w:top 子像素微调 |
| W27 | codex-design-iter22-iter08 | 8.67 / 12.35 | 前 final，已被 W29 替换 |
| W28 | codex-design-iter24-pathA | 8.67 / OOXML autospace | ⚠ Word 报"文件损坏" — 已回退 |
| W26 | 双路并发 char-spacing + image | 8.69 / 12.40 | |
| W25 | per-page surgical | 8.71 / 12.40 | |
| W9 | design-iter02-iter05 | 12.88 | THRESHOLD_PASS |
| W2 | design-iter01-main-iter02 | 14.14 | FONTS_FIXED baseline |

详见 `final/candidates/`

## 硬瓶颈页（W27 LibreOffice 评分）

| 页 | diff | 内容类型 | 难点 |
|----|------|---------|------|
| p3 | 12.04 | 中文长段落 + 产品图 | CJK 段落字距 |
| p9 | 11.99 | 中文长段落 + 操作步骤 | 行高 + 字距 |
| p11 | 12.14 | 中文长段落 + 警告框 | 红色警告框 |
| p14 | 12.35 | 保修条款表格 | 表格密集中文 |

## 28 路径已尝试且失败的优化

字距 4-8 twips（5 最优）、页眉页脚 hairline、封面图位、step badge 大小、警告框 padding、line-spacing exact 模式、浮动表、字间距、autoSpace 关、East Asia font hint、gridCol 显式、JPEG 嵌图、anchored drawings、numPr 真实 bullet、run vertical position offset、szCs 匹配、noWrap、显式 page margin、frame_pr、bookmark、contextualSpacing、char spacing 子像素调整、image DPI 99%/101%、tab_stops、tcMar tweaks、subtitle space_after 子点变化、body 7.05→7.00pt — 全部回归或中性。

**注**: 之前曾把"per-page section margin"列入失败清单，但 design-iter-33 实证 pgMar w:top 子 twip 量级（+3/+1）逐页选择性应用可突破 plateau（W27 → W29）。

## 当前后台任务

- **iter-29 path-codex**（PID 后台 `badya9dit`）：用 Word baseline 评分新角度（w:kern, hint=eastAsia, autoSpaceDE 仅 body 段、tcMar 紧缩硬页）。⚠ 需通过 Word-open 闸门。
- **cron**：每 5 小时第 13 分自动检查迭代进度（job 待重建）。

## 待办

- [ ] design-iter-30：调用官方 `/docx` skill 走另一路径
- [ ] 验证 W27 在 MS Word 里替换文字的可编辑性（"通过替换文字实现新版本快速交付"）

## 2026-05-17 进展

### iter-29 path-codex（Word baseline 角度）
- 全部 6 轮回归（LO +1.79~+1.95，max +7.20~+9.96）
- Word COM gate 在 codex sandbox 无法跑（pywintypes COM session 错误）
- 结论：w:hint=eastAsia + w:szCs + w:kern 反而让 LO 评分变差，需绕路。W27 default 保留为 fallback。

### iter-30 path-docx-skill（官方 docx skill 重做）
- 新约束：用 `C:/Users/iamdo/.claude/skills/docx/` 的 unpack/pack/validate 工作流
- 新需求：docx 必须可参数化（文字替换 → 快速交付 IMT060/IMT070 等变体）
- 进行中（后台 bqacq4kha）

### iter-33 path-ooxml-microtune（W29 突破）
- 操作: per-section pgMar w:top 微调（p3/p5/p9/p12/p13 +3 twips, p14 +1 twip）
- 结果: **8.67 / 12.35 → 8.63 / 12.30**（mean -0.04, max -0.05）
- Word-safe 验证: validate.py + Word COM 15 页渲染 PASS
- 关键洞察: pgMar 调整对 LO 评分**逐页敏感度不同**——p11 反向劣化、p14 仅+1 受益；偏移量级 1-3 twips 是甜区，>5 过冲

### iter-30 path-docx-skill 完成 ✅ 里程碑

**官方 docx skill 路径达成等同 W27 视觉 + 完整文字参数化**

- 评分：`8.67 / 12.35`（与 W27 等同）
- 官方 validate.py：**All validations PASSED**
- Anti-cheat：wt_count=457, image_hack=false, text_ratio=1.0
- 流程：unpack W27 → 提取文本到 params.json + template_parts/ → pack → validate
- 产物：
  - docx: `design-iter-30/path-docx-skill/iter-4/output.docx`
  - 参数化: `iter-4/params.json` + `iter-4/text_params.json`
  - 模板片段: `iter-4/template_parts/`
  - 说明: `design-iter-30/path-docx-skill/TEMPLATE.md`

**意义**：boss 要的两个核心需求（视觉一致 + 文字替换批量交付）**通过官方 docx skill 路径达成**。但仍未突破 8.67 plateau，所以 iter-35 持续优化 agent 已启动。

### iter-35 path-docx-skill-continue 启动（不能断的 docx skill 路径）

- 基线：iter-30/iter-4 (8.67/12.35)
- 工作流：官方 unpack/edit XML/pack
- 角度：硬瓶颈页 OOXML 段落微调、tcMar、行高 exact、cx/cy EMU 重定位、framePr
- 预算：10 轮
