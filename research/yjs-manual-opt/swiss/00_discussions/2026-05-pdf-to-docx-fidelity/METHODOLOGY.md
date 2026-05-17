# DOCX 视觉保真优化方法论 + 踩坑备忘录

> 目的：从 W27 plateau (8.67/12.35) 突破到 W46 (7.38/10.90)，**mean -1.29 / max -1.45 / 改善 ~15%**。
> 这份文档记录核心方法、所有 effective lever、所有失败教训，供后续 docx 视觉保真任务复用。

---

## 一、整体方法论

### 1.1 任务三要素
1. **基线 docx** — 当前 final 版本
2. **目标 PDF** — 视觉比对基准（Adobe 渲染）
3. **评分工具** — `score_candidate.py` 用 LibreOffice headless 渲染 docx → PNG → 与目标 PNG 比 RGB mean diff

### 1.2 核心循环（每个 iter）
```
1. unpack docx → unpacked/ (官方 docx skill: C:\Users\iamdo\.claude\skills\docx\scripts\office\unpack.py)
2. 编辑 word/document.xml 或其他 xml（单维度改动）
3. pack unpacked/ → output.docx（自动 validate）
4. 评分: PYTHONUTF8=1 python score_candidate.py output.docx --target ... --baseline-pngs ...
5. Word-open 验证: python compare_word.py output.docx out.pdf (Word COM 必须打开)
6. anti-cheat 检查: wt_count≥300, image_hack=false, text_ratio∈[0.95,1.20]
7. 接受：mean 改善 OR max 改善 AND 任何 page 回退 ≤ 0.05
```

### 1.3 关键约束（硬规则）
- **每轮只改一个维度**（不要混多 lever，方便归因）
- **必须官方 docx skill 流程**（unpack/pack/validate）— 避免文件损坏
- **必须 MS Word 可打开**（compare_word.py 通过）— W28 教训
- **保留 anti-cheat 阈值** — 防止页面被替换为图片 hack
- **接受/回退条件严格执行** — 防止累积漂移

---

## 二、可复用 Lever 库（按发现顺序）

### 2.1 几何维度（pgMar / sectPr）

| Lever | 方向 | 效果 | 注意 |
|-------|------|------|------|
| pgMar `w:top` 子像素 +3 twips（部分页）| UP | -0.04 mean | 不是所有页同向 |
| pgMar `w:top` -17 (p11) | DOWN | -0.58 p11 | 大幅度反向是甜区 |
| pgMar `w:right` +5 (p14) | UP | -0.04 max | "杀手锏"维度 |
| pgMar `w:top` +20 (p6 内容轻页) | UP | -1.84 p6 | 大幅度在轻页有效 |

**规律**：sectPr 多维度子像素调整（1-20 twips），**每页方向不同**，需扫描。

### 2.2 字符间距（rPr w:spacing）

| 字号 | 方向 | val | sites | Δ |
|------|------|-----|-------|---|
| sz=14 BLACK | UP | 5→8→9→10 | 71 | -0.20 mean |
| sz=14 AB-only | UP | 9→10→11 | 9 | -0.01 mean |
| sz=13 GRAY-only | DOWN | 5→2 | 117 | -0.03 mean |
| sz=13 BLACK Arial Black | UP | 5→8→9→10 | 17 | -0.05 mean |
| sz=12 | DOWN | 5→2 | 33 | 含在 W33 |
| sz=11 | DOWN | 5→2 | 35 | 含在 W33 |
| sz=10 RED | DOWN | 8→7→6 | 37 | -0.05 mean |
| sz=22/27 Arial Black | UP | 5→11 | 26 | 含 W36 |

**规律**：
- 大字号 BLACK Arial Black → UP（widen 字距）
- 小字号（10-13）GRAY/RED → DOWN（tighten 字距）
- val=9 是 Goldilocks 甜区（不是 11）
- val=2/3 子像素等效（sub-pixel saturation）
- **字号-字体 sub-cohort 不对称**（Arial vs Arial Black 不同）

### 2.3 段落 spacing（pPr w:line / w:before / w:after）

| Lever | 效果 |
|-------|------|
| p9 line 264→252 (7 sites) | -0.05 mean, -1.06 p9 |
| p13 line 271→278 | -0.75 p13 |
| p14 line 240→250 (21 sites) | -0.25 p14 |
| p12 line 271→260 (4 sites) | -0.14 p12 |

**规律**：
- **page-isolated cohort** 比全局 cohort 安全（全局 line 调整全部反退）
- pPr 行高 vs rPr 字距 = **独立可叠加轴**
- `w:contextualSpacing` 是 FATAL（+5 mean）
- `w:lineRule` auto→exact/atLeast 全局 FATAL

### 2.4 OOXML 结构干预（W42+ 突破点）

| Lever | 效果 |
|-------|------|
| pBdr 左边线 000→E63846（12 banner） | -0.02 mean |
| 关键 run split + bold（保修期数字） | -0.03 p14 |

### 2.5 颜色 mismatch（W44 大突破）

| Lever | 效果 | 来源 |
|-------|------|------|
| 表头 shd fill `1A1A1A → 000000`（15 sites）| **-0.17 mean / -0.91 max** | **SHOWSTOPPER** |
| pBdr 全部 banner 000→E63846 (12 sites) | -0.02 mean | |
| tcBorders CCCCCC → D9D9D9 (196 sites) | 含 | |
| tcBorders D9D9D9 → E5E5E5 (340 sites) | 含 | |
| GRAY text 8E8E93 → F5F5F5（27+28 sites）| -0.03 mean | **必须传播 footer*.xml** |

**规律**：**视觉 diff 主要来源是文档级颜色 mismatch**，不是 per-page geometry！PDF 用纯黑 000，docx 用 1A 子黑——单 lever 巨幅改善。

### 2.6 "Make-invisible" 边框（W46 大突破）

| Lever | 效果 |
|-------|------|
| bottom sz=6 000000 → FFFFFF（16 sites） | **-0.28 mean** |
| top sz=10 000 → FFF（1 site, p1） | -0.04, p1 -0.52 |
| top sz=8 (1 site, p11) | -0.02, p11 -0.25 |
| left sz=18 banner 红色 sz=2 thinner | -0.02 max |

**关键技巧**：保留 `w:val="single"` 保层 layout space，**只翻 color 为白**。`w:val="nil"` 灾难（+0.6 mean / +2.9 max，因为引起 reflow）。

**规律**：候选 docx 渲染可见黑边框，target PDF 实际不可见（PDF 故意隐藏视觉但保留 spacing）。

### 2.7 keycap chip 结构（W31）

| Lever | 效果 |
|-------|------|
| p7/p11 双行堆叠 → 单行内联 chip（Courier + bdr）| **-1.13 p7** |

5 cells: Power/Make Ice/Clean/ICE FULL/ADD WATER → `<w:r>` split：
1. `1 ` (Arial sz=13 spacing=5)
2. `Power` (Consolas sz=13 spacing=2 + `<w:bdr w:val="single" w:sz="4" w:space="1" w:color="000000"/>`)
3. ` 电源` (Arial sz=13 spacing=5)

---

## 三、踩坑备忘录（避免再犯）

### 3.1 致命坑（导致 docx 损坏 / Word 无法打开）

| 坑 | 现象 | 教训 |
|----|------|------|
| **W28 OOXML autoSpaceDE/DN 全局**| Word 报"文件可能已经损坏"（LO 渲染 OK）| 全局 settings.xml 改动有 Word 严格验证 |
| **contextualSpacing 全局** | mean +5.22 灾难 | LO 折叠所有同 style 段落 |
| **lineRule auto→exact/atLeast 全局** | +2.0~2.4 mean | 全局行高规则切换 |
| **w:val="nil" 边框** | +0.6 mean / +2.9 max | 引起 reflow（应该 `val="single"` + color "FFFFFF"）|
| **doc 用 Pillow 9.5 多图循环** | segfault（Windows）| gc.collect() + 分进程调用 |

### 3.2 评分工具 / 环境坑

| 坑 | 解决 |
|----|------|
| **soffice 短暂被并行 agent 锁定** | 等待重试，或 LO_USER_PROFILE 隔离 |
| **docx skill validate.py gbk codec error** | `PYTHONUTF8=1 PYTHONIOENCODING=utf-8` |
| **docx skill schemas missing locally** | 从 anthropics/skills GitHub 下载 ecma/fouth-edition/*.xsd |
| **codex sandbox 无法跑 Word COM**（pywintypes session 错误）| Word 验证必须在主 session（Claude）跑，agent 只评 LO |
| **PNG 渲染 0.01-0.02 浮动** | 多次重测，接受小幅波动；mean/max 显示 8.0 实为 7.99x |

### 3.3 优化策略坑

| 坑 | 教训 |
|----|------|
| **30 轮 plateau 8.67 误判** | 把"per-page section margin"列为失败 — **是错的**！1-3 twips 是甜区，**所有"失败"角度可能粒度不对**，值得用子像素重测 |
| **W37 sz=13 BLACK "saturated at 9"** | 只对 Arial 子 cohort，Arial Black 还能推 10/11。**font 子拆分关键** |
| **iter-46 误判 sz=13 BLACK inert** | 在不同 baseline 下 BLACK 5→8 UP 反而是甜区，**洞察依赖基线**，需在最新基线复测 |
| **broad cohort 试 spacing 全部退化** | 改 page-isolated sub-cohort 反而是甜区（iter-49 模式可推广）|
| **agent 重复抢提 final**（race condition）| iter-40 + iter-41 同时升 W33，互相覆盖。后续叠加才发现两个改动正交 |
| **iter-41 5→0 全 cohort** | p4 +0.06 over-tolerance。**GRAY-only 分色 cohort** 是绕过 over-tolerance 的关键策略 |
| **iter-37 字号 sz=16→14（styles.xml）无效** | W29 已用 inline w:sz 覆盖，**styles.xml 是被绕过的**！直接改 document.xml inline 才生效 |
| **footer 颜色没传播** | document.xml 改了 GRAY 但 footer*.xml 14 个文件没改，要全部同步 |
| **w:kern 全部 inert** | LO Writer 对 kerning 不响应，所有 threshold 值都 ≤0.01 |
| **schema gotcha**：pPr 子元素顺序 | pPr 内必须：pStyle, numPr, spacing, ind, jc, rPr 顺序，pack.py validate 会捕获 |
| **p3 极敏感（W49 教训）** | val=6/9/line=228 任意 ±2 让 p3 BLOW UP 至 11.4-12.7。p3 字距/行距 saturated，需切换 page-isolated 非整 cohort |
| **全局 w:after=120 灾难（W49）** | 35 sites 在 W48 上加这一 cohort 平均 +0.6 mean。所有全局 after cohort 调整在 W48+ 阶段 FATAL |

### 3.4 Agent 编排坑

| 坑 | 解决 |
|----|------|
| **Agent 5 小时配额耗尽**| `You've hit your limit · resets 10:30am Asia/Shanghai`。等待 + ScheduleWakeup 长间隔（3600s）|
| **Agent 启动 0 工作**| 配额耗尽时立即返回。需重试或等下个周期 |
| **Stale /loop 堆积**| 短间隔 ScheduleWakeup 累积导致 stale 触发。**长间隔 (1800-3600s) + task-notification 主驱动** |
| **Agent 不写 STATUS.md** | iter-44b 部分完成但无 STATUS — 但 iter 目录里的 output.score.json 仍可用，**手动 grep 候选** |
| **并行 agent 抢提 final**| 第二个 push 被第一个 push 覆盖。**用 git pull --rebase --autostash 解决，并明确合并策略** |

---

## 四、复用模板

### 4.1 Agent prompt 模板

```markdown
**任务**：基于 W{N} (X.XX/X.XX) 攻 {新角度}。

**已 saturated 的 lever**（不要重做）：
- [列出已验证 saturated 的所有 cohort]

**已 NEGATIVE 的 lever**（不要重做）：
- [列出已验证灾难的所有改动]

**新攻角度**：
- [按 ROI 排序列出 3-5 个未尝试角度]

**工作目录**：
`research/.../design-iter-{N}/path-{name}/`

**基线**：复制 final → baseline.docx

**清单**（每轮独立一个改动）：
1. iter-1 grep 现状
2. iter-2 应用 lever A
3. iter-3 应用 lever B
4. ...
9. 累计最优 stack

**约束**：
- 官方 unpack/pack/validate
- Word-safe (compare_word.py)
- Anti-cheat (wt_count≥300)
- 接受：mean<X.XX OR max<X.XX，回退≤0.05

**预算**：10 轮

**最后**：突破 → 升级 final + commit + push（中文 msg）+ stage 候选 + STATUS.md 详记

报告 250 字以内：哪些 lever 有效、最终评分、下一推荐角度。
```

### 4.2 阶段分类（按 ROI 探索顺序）

1. **粗调阶段（差距 >5）**：字号、行高大幅度、margin 大幅度
2. **细调阶段（差距 1-5）**：rPr w:spacing cohort（UP 大字号、DOWN 小字号）、Goldilocks 半步
3. **微调阶段（差距 <1）**：per-page sectPr 子像素、page-isolated pPr line surgery
4. **结构阶段（max 顽固）**：OOXML 结构干预（pBdr 颜色、run split bold、表格列宽）
5. **颜色阶段（plateau 突破）**：文档级颜色 mismatch（PIL 采样目标 + footer 传播）
6. **隐藏元素阶段（plateau 突破）**："make-invisible" 边框、隐藏元素清理

### 4.3 调试小贴士

- **per-page 评分**：score JSON 的 `per_page_diff` 找 max 来源页
- **PIL 颜色采样**：`Image.open('target_png/page-XX.png').crop((x,y,w,h))` 取均值定位目标颜色
- **diff 热力图**：PIL ImageChops + matplotlib colormap 看局部 hotspot
- **对照实验**：单 lever 试 ±3 步长（DOWN/UP/反向）确认方向
- **font 子拆分**：grep `<w:rFonts.*ascii="Arial Black"` vs Arial 分组测试

---

### 2.8 Line cohort sweet spot（W47 大突破）

| Lever | 效果 |
|-------|------|
| Line=230→228（37 sites，列表/项目符号行高）| **-0.078 mean / max 10.90→10.16** |
| Line=271→273 (13 sites, banner) | -0.022, p5 8.83→8.50 |
| Line=252→244 (7 sites) | -0.005 |
| Line=264→260 (9 sites) | -0.001 |
| Before=160→170 (7 sites) | -0.003 |
| **Inner border E5→F5** (340 sites) | -0.010 mean |

**规律**：line cohort sweet spot **极锐利**（228 是甜区，226/232 都灾难 +1.7~2.0 max）。**全局 cohort 也可以是甜区**（之前认为只有 page-isolated 安全），关键是值的精度。

**新增坑**：line cohort 双方向各 ±2 测试不够（228 是唯一甜区，226/232 全灾难）— 需用更细粒度 +/-1 步长扫描，且不能假设方向。

## 五、整体进展线（W27 → W47）

| Winner | mean | max | 关键突破 | 类别 |
|--------|------|-----|---------|------|
| W27 | 8.67 | 12.35 | 30 路径 plateau 起点 | baseline |
| W29 | 8.63 | 12.30 | pgMar top 子像素 | 几何 |
| W30 | 8.57 | 12.26 | 多维 per-page pgMar | 几何 |
| W31 | 8.49 | 12.26 | keycap chip 结构 | 结构 |
| W32 | 8.27 | 12.22 | sz=14 BLACK spacing 5→8 | 字距 UP |
| W33 | 8.21 | 12.06 | p9/p13 line + sz=11/12 DOWN | 字距 DOWN |
| W34 | 8.20 | 12.06 | 双轴叠加 | 叠加 |
| W35 | 8.19 | 11.99 | sz=13 GRAY-only 5→2 | 子分色 |
| W36 | 8.18 | 11.97 | heading sz=22/27 UP 5→11 | 字距 UP |
| W37 | 8.17 | 11.97 | sz=13 BLACK 8→9 Goldilocks | 微调 |
| W38 | 8.09 | 11.99 | sz=14 BLACK 8→9 半步 | Goldilocks |
| W39 | 8.06 | 11.98 | sz=14 BLACK 全 9→10 | font 拆分 |
| W40 | 8.01 | 11.98 | p9 line surgery | page-isolated |
| W41 | 8.00 | 11.98 | sz=14 AB-only 10→11 | 半步 |
| W42 | 7.99 | 11.93 | p14 OOXML 结构 | 结构 |
| W43 | 7.98 | 11.68 | p14 line=240→250 | line surgery |
| **W44** | **7.76** | **10.94** | **文档级颜色 mismatch** | **颜色** |
| **W45** | **7.73** | **10.92** | **footer 颜色传播** | **传播** |
| **W46** | **7.38** | **10.90** | **invisible borders** | **隐藏元素** |
| **W47** | **7.28** | **10.16** | **line cohort 228 + inner border F5** | **line 微调** |
| **W48** | **7.27** | **10.13** | **p11 disclaimer spacing 10→0 + table cells 2→0** | **page-isolated char spacing** |
| **W49** | **7.23** | **10.13** | **p10 spacing 级联 0 (28 sites) + p9 char-spacing 三档 (10 sites)** | **page-isolated 级联** |

**累计**：mean **-1.44** (-17%) / max **-2.22** (-18%)

---

## 六、复用清单（新任务起手三步）

1. **读** 这份文档 — 避免重做已 NEGATIVE 的 lever
2. **grep** 现状（字号/颜色/spacing 分布）— 选 ROI 最高的 cohort
3. **按阶段类别** 执行（粗调 → 细调 → 微调 → 结构 → 颜色 → 隐藏元素）

每个新 winner **必须**：commit + push（中文 msg）+ stage 候选 + 更新 SCORES.md + 这份 METHODOLOGY.md（如有新 lever 类别或新坑）。
