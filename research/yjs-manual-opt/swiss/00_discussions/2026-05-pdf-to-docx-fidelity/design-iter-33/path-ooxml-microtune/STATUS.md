# OOXML 微调 - W27 plateau 突破 (design-iter-33)

**约束**: Word-safe（W28 因 autoSpaceDE/DN 被 Word 报"文件损坏"）

**W27 baseline**: 8.67 mean / 12.35 max（LibreOffice 评分）

## 最终成果（W29 候选）

**r8-winner.docx: 8.63 mean / 12.30 max（Word-safe，Word COM 渲染 15 页 OK）**

突破策略：每页 sectPr 内 pgMar w:top 子像素位调整（+3/+1 twips），仅作用于评分高位页。

## 迭代日志

| 轮 | 操作 | 文件 | mean | max | 备注 |
|----|------|------|------|-----|------|
| 0 | W27 baseline | — | 8.67 | 12.35 | plateau |
| 1 | 全局 pgSz 8391→8400, 11906→11899 | r1-pgsz.docx | 8.67 | 12.35 | 中性 (LO 自动吸收) |
| 2 | p3/p9/p11/p14 top +3 | r2-pgmar-hard.docx | 8.67 | 12.36 | p3 -0.15, p9 -0.11, p11 +0.22 (劣化), p14 ±0 |
| 3 | p3/p9 top +5, p11/p14 top -3 | r3-pgmar-perpage.docx | 8.68 | 12.47 | 大幅度过冲 |
| 4 | 仅 p3/p9 top +3 | r4-p3p9.docx | **8.65** | 12.35 | 首次突破 |
| 5 | p3/p9 +6, 探针 p5/p10/p12/p13 +3 | r5-explore.docx | 8.65 | 12.35 | 发现 p5(-0.19), p12(-0.16), p13(-0.02) 也吃 +3 |
| 6 | 仅赢家组合 p3/5/9/12/13 各 +3 | r6-best.docx | **8.63** | 12.35 | mean 进一步 |
| 7 | 加 p11/p14 各 +1（最小探针） | r7-probe-p11p14.docx | 8.63 | **12.30** | max 突破！p14 -0.05, p11 +0.05 |
| 8 | 最终：p3/5/9/12/13 +3, p14 +1 | **r8-winner.docx** | **8.63** | **12.30** | 6 页改善 0 页劣化 |

## 关键发现

1. **per-section pgMar w:top 微调可以突破 plateau** — 这是 28 路径迭代历史中未明确尝试的方向（"per-page section margin" 被笼统列入失败清单，但本次实证发现 +3 twips 是最佳量级，原失败可能因为偏移过大）
2. **每页对偏移方向敏感度不同**：p3/p5/p9/p12/p13 全部受益于 +3（向下推 0.15pt），但 p11 受 +3 反向，p14 仅 +1 受益
3. **LibreOffice 渲染对 pgSz 不敏感**：8391→8400 全无影响（噪声层内）
4. **Word 兼容性 100% 保留**：6 个 sectPr 修改全部通过 Word COM 渲染，15 页结构保持

## Word-safe 边界验证

| 项 | 状态 |
|----|------|
| validate.py | PASS（无新错误，仅 W27 已有的 footer/zoom warnings） |
| Word COM 渲染 | PASS（15 页，与 W27 一致） |
| 编辑性（wt_count, image_hack） | PASS（445/false） |
| 文本字符数 | 1.0 ratio |

## r8-winner.docx 偏移详情

```
p3:  w:top  578 → 581 (+3 twips ≈ +0.15pt)
p5:  w:top  578 → 581 (+3)
p9:  w:top  578 → 581 (+3)
p12: w:top  578 → 581 (+3)
p13: w:top  578 → 581 (+3)
p14: w:top  578 → 579 (+1)
```

(1 twip = 1/20 pt = 1/1440 inch ≈ 0.0176 mm)

## 升级行为

r8-winner.docx 替换 `final/imt050-wevac-eu-cn.docx`，并更新 SCORES.md。
</content>
</invoke>