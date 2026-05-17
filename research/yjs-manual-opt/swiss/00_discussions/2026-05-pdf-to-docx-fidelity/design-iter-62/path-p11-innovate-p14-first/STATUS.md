# iter-62 path-p11-innovate-p14-first STATUS

**基线 W49**: mean=7.23 / max=10.13 (p11=10.13, p14=9.67, p9=9.69, p10=9.48, p3=10.03)

**结果 W50**: mean=**7.21** / max=**10.13**
- p10: 9.48 → **9.13** (-0.35) 
- p11: 10.13 (无变化)
- p14: 9.67 (无变化)
- Δ mean: -0.02
- 候选: iter-13 `p10 line=228 -> 216 (4 sites)`

## 每轮记录

| iter | lever | result | 评语 |
|------|-------|--------|------|
| 1 | grep 现状 | — | 确认 p11=10.13 max, p14=9.67, p9 line=244×7, p10 line=228×4 |
| 2 | p14 line=250→260 (21 sites) | mean 7.26 (+0.03), p14 10.14 (+0.47) | REJECT — p14 line UP 反向 |
| 3 | p14 line=250→240 (21 sites) | mean 7.25 (+0.02), p14 9.99 (+0.32) | REJECT — p14 line 双向都坏，250 是甜区 |
| 4 | p14 char-spc 级联 (11→9, 10→8, 8→6) | mean 7.26 (+0.03), p14 10.10 (+0.43) | REJECT — p14 char-spc tighten 灾难 |
| 5 | p11 tcMar 32→16 top/bot (30+30 sites) | mean 7.44 (+0.21), max 13.34 (+3.21) | **BLOW UP** — p11 tcMar saturated |
| 6 | p11 tcMar 32→48 top/bot | mean 7.51, max 14.32 | **BLOW UP** — 双向都灾难 |
| 7 | p9 line=244→248 (7 sites) | mean 7.25, p9 9.93 (+0.24) | REJECT — p9 line UP 坏 |
| 8 | p9 line=244→240 (7 sites) | mean 7.26, p9 10.17 (+0.48) | REJECT — p9 line 双向都坏，244 是甜区 |
| 9 | p10 line=228→230 (4 sites) | mean 7.24, p10 9.56 (+0.08) | REJECT — +2 反向 |
| 10 | p10 line=228→226 (4 sites) | mean 7.23, p10 9.45 (-0.03) | 小幅好转 |
| 11 | p10 line=228→224 (4 sites) | mean 7.22, p10 9.38 (-0.10) | **CANDIDATE** |
| 12 | p10 line=228→220 (4 sites) | mean 7.22, p10 9.32 (-0.16) | 更好 |
| 13 | p10 line=228→216 (4 sites) | **mean 7.21**, **p10 9.13 (-0.35)** | **WINNER** ← W50 |
| 14 | p10 line=228→208 (4 sites) | mean 7.22, p10 9.36 | 退回 — 过头 |
| 15 | p10 line=228→212 (4 sites) | mean 7.22, p10 9.31 | 退回 — 不如 216 |

## Word-safe 验证

iter-13 output.docx → Word COM 打开 + PDF 导出 OK（compare_word.py 通过）

## 关键洞察 / 新 lever

**新 lever：p10 line=228→216 (4 sites page-isolated)**
- iter-61b 已合并了全局 line=230→228 (37 sites)，p10 是其中 4 个
- 在 W49 基线上，p10 这个 4-site sub-cohort 还能继续 sweep
- 216 是甜区（220 也好，212/208 略退），212-220 都比 228 优
- **page-isolated sub-cohort 在全局已饱和后仍可探索** — 强方法论延伸

## 已新增 saturated lever（更新到 METHODOLOGY）

- **p14 line=250 saturated**（双向 ±10 都灾难，250 是甜区）
- **p14 char-spc tighten 灾难**（cascade 11→9/10→8/8→6 = p14 +0.43）
- **p11 tcMar 32 saturated**（32→16 +3.21 max；32→48 +4.19 max）
- **p9 line=244 saturated**（双向 ±4 都灾难）

## 下一推荐角度

- 继续 p10 page-isolated line sweep（其他 line 值也试 sub-page）
- p9 char-spacing UP 方向（W49 已 DOWN，UP 未试）
- p11 颜色 / 边框深扫（结构 lever 没动过）
- p3 line=228 子集（同 page-isolated 思路）

## 升级 final

- `final/imt050-wevac-eu-cn.docx` ← W50 (iter-13)
- `final/imt050-wevac-eu-cn.W49-backup.docx` ← W49 备份
- `final/imt050-wevac-eu-cn.score.json` ← 更新
- `output/imt050-wevac-eu-cn.docx` ← 同步
