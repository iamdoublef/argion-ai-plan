# IMT050 Word DOCX 视觉保真评分记录

## 当前最优：W33（design-iter-41 path-kern-smallsz iter-11 — 小字号 spacing DOWN）

- **文件**: `final/imt050-wevac-eu-cn.docx`
- **LibreOffice 渲染评分**: `8.28 / 12.06`（mean / max）— 突破 W32 plateau，max -0.08
- **手法**: W32 基础上对 sz=11 (35 sites, RED accent) + sz=12 (22 sites, Arial Black/Arial) 的 rPr w:spacing 从 5 收紧到 2 — 与 sz=14 的 spacing UP 完全反向
- **要点**: 大字号 (sz=14, 7pt) 缺空, 小字号 (sz=11/12, 5.5-6pt) 过空, 方向相反
- 详见: `design-iter-41/path-kern-smallsz/STATUS.md`

## 历史 W32（design-iter-36 多维 pgMar 扫描 + iter-37 设计修复 + iter-39 rPr 字距）

- **LibreOffice 渲染评分**: `8.28 / 12.14`（mean / max，重测 W32 base）
- **手法**: W31 + sz=14 BLACK rPr w:spacing 5→8 (71 sites)
- 已被 W33 替换

## 历史 W31（design-iter-36 多维 pgMar 扫描 + iter-37 设计修复叠加）

- **LibreOffice 渲染评分**: `8.30 / 12.20`（mean / max）— 突破 W30 plateau
- **Anti-cheat**: PASS（wt_count=446, image_hack=false, text_ratio=1.0, drawings=16）
- **MS Word 可打开**: PASS（docx2pdf Word COM 渲染 15 页）
- **页数**: 15（与目标 PDF 一致）
- **可编辑性**: 100%（无 text_box / 图片 hack）
- **突破手法**: 在 iter-37 W30（设计修复）baseline 上叠加 iter-36 多维 pgMar 调整——key wins：p6 top +20（−1.84）、p4 top +10（−0.75）、p11 top −17（−1.05）、p14 right +5 / top −3（−0.10）
- **详见**: `design-iter-36/path-margin-sweep/STATUS.md`

## 历史 W30a（design-iter-36 仅 pgMar）

- **LibreOffice 渲染评分**: `8.57 / 12.26`（mean / max）
- **突破手法**: per-section pgMar 多维度子像素扫描——w:right（p14 +5/p3 +3/p5 +3/p9 +2/p11 +1）、w:top 大幅度反向（p11 -17/p10 -5/p14 -3/p13 +3）
- 已被 W31 替换

## 历史 W30b（design-iter-37 仅设计修复）

- **LibreOffice 渲染评分**: `8.54 / 12.24`（mean / max）
- **突破手法**: zebra F1F1F6, WARNING/CAUTION 边框, 红 E63846, p1 footer split
- 已被 W31 替换

## 历史 W29（前 plateau）

- **LibreOffice 渲染评分**: `8.63 / 12.30`（mean / max）
- **突破手法**: per-section pgMar w:top 子像素微调（p3/p5/p9/p12/p13 各 +3 twips，p14 +1 twip）
- 已被 W30/W31 替换

## 历史 W27（前 plateau）

- **LibreOffice 渲染评分**: `8.67 / 12.35`（mean / max）
- **MS Word 渲染评分**: `9.16 / 15.27`（mean / max）
- 已被 W29/W30 替换

## 评分基准说明

`score_candidate.py` 用 LibreOffice headless 渲染 docx→PDF→PNG，与目标 PDF 的 PNG 比对 mean RGB 差。
- **优点**: 与目标 PDF 的 Adobe 渲染较接近（freetype 基础一致）
- **缺点**: 客户实际打开用 MS Word，Word 渲染中文字距/行距与 LibreOffice 不同

## 28 路径迭代历史（按 visualdiff 升序）

| Winner | Path | Visualdiff | 备注 |
|--------|------|-----------|------|
| W32 | iter-39 path-docx-skill-stack (iter-9) | **8.27 / 12.22** | **当前 final** — W31 + sz=14 black rPr spacing 5→8 (71 sites) |
| W31 | iter-36 + iter-37 双层叠加 | 8.30 / 12.20 | pgMar + 设计修复正交叠加 (前 final) |
| W30a | design-iter-36 path-margin-sweep | 8.57 / 12.26 | 仅 pgMar 多维 |
| W30b | design-iter-37 path-design-fixes | 8.54 / 12.24 | 仅设计修复 |
| W29 | design-iter-33 path-ooxml-microtune | 8.63 / 12.30 | 前 final |
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

### iter-35 path-docx-skill-continue ✅ 突破（2026-05-17）

- 基线：iter-30/iter-4 (8.67/12.35)
- 工作流：官方 unpack/edit XML/pack
- **iter-10 BREAKTHROUGH**: body rPr `<w:spacing w:val="5"/>` → `8` on 75 sz=14 body runs
- 评分：**8.64 / 12.29**（mean -0.03, max -0.06）— 突破 plateau，max 比 W29 的 12.30 还低
- 改善：p5 -0.23, p9 -0.10, p13 -0.11, p14 -0.06
- 小回归（均 <0.05）：p3 +0.03, p10 +0.03, p11 +0.01
- Word-safe: validate.py PASS + Word COM 15 页 PASS（3.4s, 无 corruption）
- 关键发现：LO 忽略 settings/compat 层的 CJK 控制（autoSpaceDE/DN, useFELayout, themeFontLang, noPunctuationKerning），唯一对 LO 生效的是 rPr 字符间距。LO 比 target PDF 渲染**更窄**，反向加宽 +3 twips 强制更早换行匹配 target wrap points
- 路径：`design-iter-35/path-docx-skill-continue/final/imt050-wevac-eu-cn.docx`
- iter 摘要：iter-1..9 都是 neutral 或 regression；iter-9 (5→2) 反向劣化证实方向错误，iter-10 (5→8) 反向加宽即破局

### W29 突破 ✅✅ (2026-05-17, iter-33 path-ooxml-microtune)

**首次突破 8.67 plateau**：8.63 mean (-0.04) / 12.30 max (-0.05)

- 方法：per-page sectPr/pgMar w:top 子像素 +3 twips（p3/5/9/12/13）+ p14 +1
- 6 页改善 0 页劣化
- Word-safe: validate.py PASS + Word COM 渲染 PASS
- Anti-cheat: 通过
- commit: `00c6720`

**关键教训（更正历史认知）**：
- 之前 SCORES.md "已尝试且失败" 把 per-page section margin 列为失败 ⚠️**这是错的**
- 真实情况：1-3 twips 是甜区，每页方向不同（p3/5/9/12/13 吃 top+3，p14 吃 top+1）
- 30+ 路径漏掉这个甜区，因为粒度调错（之前都是大刀阔斧 ±10-50 twips）
- **新方法论**：所有"失败"的角度可能只是粒度不对，值得用子像素 (1-3) 重新验证

### iter-36 path-margin-sweep 启动

基于 W29 继续探索 right/bottom/left/gutter/mirror 维度的子像素 margin 调整，p11 (现 max=12.30) 重点攻。

### W30 突破 ✅✅✅ (2026-05-17, iter-36 path-margin-sweep)

**首次突破 W29 plateau**：8.57 mean (-0.06) / 12.26 max (-0.04)

- 方法：多维 per-section pgMar 子像素扫描（10 轮 r1-r10）
  - **w:right**（W29 未触及的维度）：p3 +3、p5 +3、p9 +2、p11 +1、p14 +5
  - **w:top 反向**（W29 只加未减）：p10 -5、p11 -17、p14 -3、p13 +3
- 6 页改善 0 页劣化
  - p3: 11.89→11.86 / p9: 11.88→11.87 / p10: 10.14→10.01 / **p11: 12.14→11.56 (-0.58)** / p13: 11.68→11.57 / p14: 12.30→12.26
- Word-safe: validate.py PASS（vs W29，paragraphs 327→327）+ Word COM 15 页 PASS
- Anti-cheat: wt_count=445, image_hack=false, text_ratio=1.0
- 路径: `design-iter-36/path-margin-sweep/W30-winner.docx`
- 详见: `design-iter-36/path-margin-sweep/STATUS.md`

**关键教训（再次更正历史认知）**：
- W29 STATUS 提到 "p11 受 +3 反向" → 实证发现：**p11 对 top 负方向（向上推）极敏感**，-15..-17 twips 让 p11 减 0.56
- "w:right" 在 28 路径里未被独立测试，p14 right+5 单维就让 max 从 12.30→12.27
- **w:right 和 w:top 是有效维度**；w:bottom/w:left/w:gutter/w:header/w:footer 几乎全噪声层（LO 不敏感）
- plateau 8.57/12.26 多变体同分，是 LO rasterization rounding 下限
- **下一突破方向**：行间距/字间距子像素（spacing/jc 维度）、drawing anchor 微调、image extent 子像素


### W30 突破 ✅ (iter-37, 2026-05-17)

**实施 5 条设计修复**：8.54 / 12.24（mean -0.09, max -0.06）

**接受的 FIX**：
- iter-2b: FIX #7 zebra `F2F2F7` → `F1F1F6`（PIL 实测纠正审计 F0F0F0）
- iter-4: WARNING 边框 4 边 → 仅 top
- iter-5: CAUTION 边框 4 边 → 仅 top（单次最大 -0.05）
- iter-6: 红色 `E63946` → `E63846`（品质修正）
- iter-9: p1 footer 拆 2 段

**拒绝**：
- FIX #1 字号 styles.xml 无效（W29 已用 inline `w:sz` 覆盖 — **重要发现：styles.xml 是被绕过的**）
- FIX #6 trHeight 破坏对齐
- FIX #5 TOC line spacing 反退
- FIX #B1 top margin 大退化

commit: `5bd3db5`

### iter-38 path-keycap-chip 启动

唯一未尝试的高影响审计修复 FIX #2：p7/p11 按键说明双行堆叠 → 单行内联 chip（带 Courier 边框 + 黑色 chip），预测 mean -1.0。

### iter-31 path-swiss-pipeline 部分完成 (2026-05-17)

**目标**：把 W27 视觉 backport 到 swiss pipeline (docx-js)。
**结果**：swiss/output/imt050-wevac-eu-cn.docx 从 **13.87/26.65** → **11.74/18.83**（部分改善）
**未达 W30 水平**，但产出详细视觉参数对比表（见 STATUS.md）：
- 字号差距：W27 body 7pt vs Swiss 7pt (match)，但 table/header/title 较大
- 字距：W27 char spacing 5/8 twips，Swiss 无 per-run spacing
- Padding：alert box 90→176/205 dxa，table cell pad 60→32/56 dxa
- Bullet indent：太宽 (420/210)，应 3.2mm/3.2mm

集成建议：把 sizes 放进 brand-themes.json 的 docx 块，保持多 SKU 支持。

### iter-32 path-docxjs-fromscratch 完成（保留作参考）

docx-js 独立路径：**11.32/17.77**（比 W30 差 2.65 mean）。p3/p6/p7 较差。但是 anti-cheat + validate.py + Word 全通过。结论：docx-js 路径短期内难突破 W30 水平。

### iter-35 path-docx-skill-continue 突破 ✅ (官方 docx skill 路径)

**iter-10 突破**：8.64/12.29 (-0.03 / -0.06 vs W27)
**关键杠杆**：body rPr `w:spacing 5→8`（75 sites, sz=14）— widen char spacing 改 line-wrap
**洞察**：LO 默默忽略 autoSpaceDE/DN at pPr, useFELayout, themeFontLang, autoSpaceLikeWord95, noPunctuationKerning
**commit**: `d0fcca3`

### iter-36 path-margin-sweep 突破 ✅ (W30 = 当前 final)

**iter-9 突破**：**8.57/12.26**（mean -0.06, max -0.04 vs W29）
**关键杠杆**：多维 per-page sectPr/pgMar 微调
- p11 top -17 twips → p11 12.14 → 11.56 (-0.58!) 反向突破
- p14 right +5 → -0.04（top+right 加性）
- p10 top -5 → -0.13
- p13 top +3 → -0.11
**新教训**：top **反向**（-17）在某些页是甜区，不只 +3。

## 累计 plateau 突破进展

| Winner | 评分 | 关键突破 |
|--------|------|---------|
| W27 baseline | 8.67/12.35 | 30 路径 plateau |
| W29 (iter-33) | 8.63/12.30 | pgMar top +3 子像素 |
| W30a (iter-36 单独) | 8.57/12.26 | 多维 pgMar 微调 |
| W30b (iter-37 单独) | 8.54/12.24 | 设计修复 zebra/border/red/footer |
| W31 (iter-36 + iter-37 叠加) | 8.30/12.20 | 两路径正交叠加 + p4/p6 大幅度 top +10/+20 |
| **W32 (iter-39 stack)** | **8.27/12.22** | **rPr w:spacing 5→8 on sz=14 black (71 sites) — 与几何修复正交** |

**正在跑**：
- iter-38 keycap chip 结构（FIX #2，预测 -1.0）
- iter-39 docx skill 续跑 + iter-35/36 叠加（实际 -0.03 ✓）

### W31 突破 ✅✅✅ (2026-05-17, iter-36 阶段 3 — pgMar 叠加 iter-37 设计修复)

**双层突破**：8.30 mean (-0.33 vs W29) / 12.20 max (-0.10 vs W29)

- 方法：发现 iter-37 (W30 设计修复) 与 iter-36 (pgMar 多维) **正交**，叠加后 7 页继续改善
- W30plus baseline: iter-37 W30 + iter-36 pgMar (W30a) → 8.48/12.20
- 继续 sweep r11-r20：
  - **p6 top +20**：p6 6.18 → 4.35 (-1.84！) — 单页最大改进，因 p6 内容轻、上半空白
  - **p4 top +10**：p4 7.09 → 6.34 (-0.75)
  - p7 right +3 / top +3、p5 top +3、p15 top +3 各微贡献
- 累计 11 页改善，0 页超阈值（>+0.05）回退
- Word-safe: validate.py PASS (paragraphs 328→328) + Word COM 15 页 PASS
- Anti-cheat: wt_count=446, image_hack=false, text_ratio=1.0
- 路径: `design-iter-36/path-margin-sweep/W31-winner.docx`
- 详见: `design-iter-36/path-margin-sweep/STATUS.md`

**重大方法论教训**：
- **w:top 大幅度调整（10-20 twips）在内容轻的页是巨大甜区**（p4/p6/p15）
- p11 顶部空白少 → 反向 top -17 也是甜区
- **结构修复（zebra/border/color）与几何修复（pgMar）正交**，可独立叠加
- iter-36 与 iter-37 在不同 baseline 下竞争，叠加后达成超 1+1
- **下一瓶颈**：p9 (11.88) / p12 (9.85) — pgMar 调整不再有效，需要内部段落/drawing 微调

### W32 突破 ✅ (2026-05-17, iter-39 path-docx-skill-stack — rPr 字距叠加 W31)

**第三层突破**：8.27 mean (-0.03 vs W31) / 12.22 max (+0.02, 容差内)

- 方法：W31 已经叠加了 iter-36 几何 + iter-37 设计；本轮验证 iter-35 的 **rPr w:spacing**
  字距 lever 是否还能继续叠加 — 答案是**可以**
- 关键修正：任务规范说 baseline=W30 (8.57/12.26)，实测 HEAD 已经是 W31 (8.30/12.20)
- W31 中 sz=14 body 88 个 site 仍全部为 w:spacing val=5（iter-35 的胜利动作在 W27→W30
  迁移时丢失），是干净的 stack 目标
- iter-39 sweep 10 轮，发现 sweet spot：**sz=14 BLACK 71 sites, val=5 → val=8**
  - val=9 (iter-35 用的) 在新 baseline 下让 p10/p12 超阈值
  - val=7 增益不够，val=10 over-shoot 全面回退
  - sz=13 / sz=14 white 都不能动
- 累计 3 页改善 (p5 -0.27, p9 -0.10, p13 -0.13)，0 页超阈值
- Word-safe: validate.py PASS + Word COM PASS (3s)
- 路径: `design-iter-39/path-docx-skill-stack/iter-9/output.docx`
- candidate: `final/candidates/W32-iter39-sz14-black-spacing8-stacked.docx`

**方法论教训**：
- **rPr 字距 lever 与 sectPr 几何 lever 在 LibreOffice 渲染上完全正交**，可堆叠
- 同样的「+3 twips magic number」在 W27 → W31 跨基线后**仍然成立**
- 但**作用集合需要重新搜索**（W27 用 75 sites all colors→9；W31 用 71 sites black-only→8）
- 下一瓶颈：p3 (11.66) / p9 (11.78) / p11 (11.09) / p13 (11.40) / p14 (12.22) 五页 plateau

### W31 → W32 五连突破

| Winner | 评分 | 突破方法 |
|--------|------|---------|
| W31 (iter-38) | 8.49/12.26 | keycap chip 结构 (Consolas+bdr，p7 -1.13) |
| W32 (iter-39) | **8.27/12.22** | sz=14 BLACK rPr w:spacing 5→8 (71 sites，p5/p9/p13 改善) |

**iter-39 关键发现**：
- W31 的 W30→W31 迁移链丢失了 iter-35 的 char spacing 胜利动作（sz=14 body 88 sites 仍全 spacing=5）
- 重新应用 spacing 5→8 在 W32 基础上立刻 -0.20 mean
- val=9 在新基线下让 p10/p12 超阈值；val=8 是新甜区

**累计 plateau 突破**：8.67 → 8.27 = **-0.40**（5 个 winner，30+ 路径都不知道的甜区集合）

### iter-31 swiss-pipeline backport 完成 ✅ 里程碑

**boss 第二核心目标达成**：swiss pipeline 视觉改善 + 模板化批量交付

**评分**：
- Swiss baseline: 13.87 / 26.65
- **Swiss 最终: 11.74 / 18.83**（mean -15.4%, max -29.3%）

**关键改动 5 项**：
1. **Line spacing 公式 bug 修复**：原公式 `Math.max(180, size * 13.5)` 算出 0.79 行高（错），改为 280 ≈ 1.16 行高 — **单项最大贡献**
2. W27 字号集（body 7pt, table 6.7pt, header 6pt, small 5.4pt）通过新的 `DEFAULT_DOCX_SIZES` 路由（theme-overridable）
3. 手动 `•   ` 红色 Arial Black bullet 替代 docx-js numbering（LO 渲染问题）
4. 内联 shaded step-flow badge（替代 2-col 表）
5. `cellWarranty` 边距 + `isWarrantyTable()` + `compactSafety` flags

**模板化保留**：
- imt050 (cn/gb/hk/de) + v23 (wevac/vesta/act) — 所有变体验证通过
- brand-themes.json > <brand>.docx 接受 `sizes` / `images` / `margins` override 块
- 文字替换批量交付能力完整

**剩余 3 分差距**：结构性，HTML vs JSON 段落树差异

**含义**：
- 通过 Swiss pipeline 已经能交付 11.74 视觉 + 完整多 SKU 模板化
- 通过 W32 final docx 能交付 8.28 视觉但单一型号
- 客户可以选择交付链：Swiss pipeline（批量 + 视觉 11.74）或 W32 final（单 SKU + 视觉 8.28）
