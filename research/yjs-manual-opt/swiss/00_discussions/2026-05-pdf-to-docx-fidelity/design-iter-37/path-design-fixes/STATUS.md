# Design-iter-37 / path-design-fixes — STATUS

## 基线
W29 (final iter-30 系列): overall_mean_diff = **8.63**, max_page_diff = **12.30**

## 最终 (W30)
**iter-9: overall_mean_diff = 8.54, max_page_diff = 12.24**
- Delta: mean **-0.09**, max **-0.06**
- 升级到 `final/imt050-wevac-eu-cn.docx`

## 执行的 FIX 实施（每条单独验证）

| Iter | FIX | 改动 | mean | max | 状态 |
|------|-----|------|------|-----|------|
| baseline | — | W29 (复制自 final) | 8.63 | 12.30 | 起点 |
| iter-1 | FIX#1 styles BodyText3 sz 16→14 | styles.xml | 8.63 | 12.30 | **N/A** — W29 字号已 inline 控制，styles 无效 |
| iter-2 | FIX#7 zebra F2F2F7→F0F0F0 | document.xml 57 处 | 8.71 | 12.38 | **拒绝** — target 实际 F1F1F6 而非 F0F0F0 |
| iter-2b | zebra F2F2F7→F1F1F6 (实测 target) | document.xml 57 处 | 8.60 | 12.24 | **接受** -0.03 |
| iter-3 | FIX#6 trHeight 215→280, 225→290 | document.xml 57 trH | 9.14 | 16.09 | **拒绝** — 行高增加打破对齐 |
| iter-3b | trHeight +20 (215→235, 225→245) | 同上 | 8.83 | 15.37 | **拒绝** — 仍退化 |
| iter-4 | FIX#3 WARNING 边: 4 边→仅 top | document.xml 1 处 | 8.59 | 12.24 | **接受** -0.01 |
| iter-5 | FIX#3 CAUTION 边: 4 边→仅 top | document.xml 2 处 | 8.54 | 12.24 | **接受** -0.05 (单次最大 delta) |
| iter-6 | FIX#B2 红 E63946→E63846 | document.xml 100 处 | 8.54 | 12.24 | **接受** 持平 (品质修正) |
| iter-7 | FIX#5 TOC line 240→320 | document.xml 10 处 | 8.56 | 12.24 | **拒绝** — p2 反退 3.25→3.48 |
| iter-7b | TOC line 240→280 | 同上 | 8.56 | 12.24 | **拒绝** |
| iter-8 | p9-p10 sz=14→15 (7→7.5pt) | document.xml 27 处 | 8.71 | 12.81 | **拒绝** — 字号上调破坏 plateau |
| iter-9 | FIX#8 p1 footer split 2 段 | document.xml 1 处 | 8.54 | 12.24 | **接受** p1 2.93→2.88 |
| iter-10 | p9-p10 sz=13→14 (6.5→7pt) | document.xml 3 处 | 8.66 | 12.85 | **拒绝** |
| iter-11 | FIX#B1 top margin +60 twips | document.xml 15 处 | 11.45 | 17.83 | **拒绝** 大退化 |

## 关键发现

1. **审计基线过时**：FIX_LIST.md 基于 W27 (8.67) 编写，但当前 W29 (8.63) 已经隐式完成了 FIX #1 (字号 8→6.5/7pt) 和 FIX #9 (• bullet)。30+ 轮像素优化器其实把 styles.xml 字号绕过了，**改用 inline `<w:sz w:val=...>`**, 所以审计建议改 styles.xml 完全无效。

2. **审计 FIX #7 色值错误**：审计说 zebra 改 F0F0F0，但 PIL 取样 target PNG 显示实际是 **F1F1F6 (241,241,246)**。F2F2F7 (W29) 已经很接近；F1F1F6 仅 -1 step 但够拿 -0.03。

3. **审计 FIX #3 关于 fill 错误**：target 实测 p3 WARNING/CAUTION 区是**纯白 + 黑/红 top accent**，**无 fill**。审计说有 #F9EFEF / #FDECEC 是错觉。但 **边框去掉 (4 边→仅 top)** 是对的，accept -0.06 累计。

4. **审计 FIX #6 trHeight 完全错误**：增加行高会推动表格内容下移，**打破 30 iter 对齐**，反而退化。

5. **W29 已经撞 plateau**：top margin, 字号变动 (任何方向)、TOC line 都会推动整体位移失败。剩余 8.54 主要是 **p3/p5/p9/p11/p13/p14 字号、行间距、ink density** 的 sub-pixel 反向矛盾 — 现有审计未捕捉的更深层问题。

## 实施的 FIX 合计接受 (5 条)
- FIX #7 (zebra F2F2F7 → F1F1F6, 用实测值)
- FIX #3 部分 (WARNING/CAUTION 去掉 left/right/bottom 边框)
- FIX #B2 (红 E63946 → E63846)
- FIX #8 (p1 footer split 2 段)

## 拒绝/无效的 FIX (5 条)
- FIX #1 (改 styles.xml 无效 — W29 已用 inline sz)
- FIX #5 (TOC line spacing — 反退化)
- FIX #6 (trHeight 加高 — 大退化)
- FIX #B1 (top margin — 大退化)
- p9/p10 字号上调 (sz=13→14 或 sz=14→15) — 均退化

## 下一推荐角度
1. **FIX #2 keycap chip** (p7 + p11) — 高难度但审计预测 +1.0pt，目前未尝试（结构性修改）
2. **p14 数据表格深度审查** — max diff 12.24 都来自 p14，可能需要重做 brand info table 的字号/行高 micro-tuning
3. **p3/p5/p13 安全段落 list spacing** — 增加 `<w:p w:before w:after>` 在 CAUTION/WARNING 内的逐段，但需要精细 (FIX #4)
4. **跳出 LO 渲染优化局部最优** — 改用 Word 原生渲染做 baseline 重新选择字号/间距
