---
name: docx-pipeline
description: 亚俊氏 IMT050 多语言 docx 说明书流水线 — W50 母版 + placeholder 替换 + 3 轮 fix-or-escalate。当大 boss 提到"做 docx 流水线"、"批量产多语言 docx"、"把 IMT050 转成英/德/意/繁/港/台"、"复用 W50 母版"、"docx + 翻译"、"加新语言 docx"，或要求把 PDF 流水线那套搬到 docx 上时，立刻使用本 skill。即使大 boss 没有显式说 "skill"，只要任务涉及 IMT050 docx 多语言生成 / W50 母版复用 / 翻译字典对齐 / docx 视觉验收 这几个动作中的任何一个，就必须用本 skill 而不是从头摸索。本 skill 是生产流水线（不是研究阶段），所有视觉规范和审计要求引用 SOT（`swiss/DESIGN-STANDARD.md` + `swiss/QA-RULES.md`），与 PDF 流水线保持完全一致。
---

# 亚俊氏 docx 多语言流水线（IMT050）

> **生产 ≠ 研究**。W27→W50 那 50 轮 sub-cohort sweep 是研究阶段，已结束。
> 本 skill 是生产流水线：**W50 母版 + placeholder 替换 + 3 轮 fix-or-escalate + 人工 review**。
> 不做 sweep，不探索新 lever，发现具体问题就精准修，3 轮内修不通 → 转人工。

## 一、SOT（必读，本 skill 不重复定义）

| SOT 文档 | 用途 | 路径 |
|---------|------|------|
| **DESIGN-STANDARD.md** | 视觉 + 内容结构规范（双流水线共享）。§十八 DOCX 实现映射 | `research/yjs-manual-opt/swiss/DESIGN-STANDARD.md` |
| **QA-RULES.md** | 5 阶段审计流程（双流水线共享）。§八 DOCX 适配 | `research/yjs-manual-opt/swiss/QA-RULES.md` |
| **设计文档** | docx 流水线整体设计 | `docs/superpowers/specs/2026-05-17-docx-pipeline-design.md` |

> 研究阶段方法论（W27→W50 sub-cohort sweep、lever 库、踩坑教训）**不在本 skill 范围**，已收纳到 `research/yjs-manual-opt/swiss/00_discussions/2026-05-pdf-to-docx-fidelity/METHODOLOGY.md`。本 skill 是生产流水线，不照搬不引用。

**docx 流水线相关 SOT 条款速查**：
- 视觉/内容规范全部 → `DESIGN-STANDARD.md` §一-§十七，**docx 实现映射** → §十八
- 审计流程 → `QA-RULES.md` Phase 1-5，**docx 适配** → §八（含 Phase 共享矩阵、anti-cheat、3 轮 fix-or-escalate、4 个人工 review gate）
- 数据残留检测（C3c） / CJK 残留（C4a） / T1/T2/T3 翻译失败（C4b） / 单位一致性（C4d） — **完全共享语义**
- 批准版派生不漂移（C18） / 单位口径一致（C19） — **完全共享**

任一规范不一致 → 修 SOT，不要在本 skill 中绕过。

## 二、硬规则（违反就废）

1. **官方 docx skill 是唯一文件 I/O 入口**：unpack/pack/validate 必须用官方 docx skill 下的 `scripts/office/{unpack,pack,validate}.py`。路径通过环境变量 `DOCX_SKILL_ROOT` 解析，默认值：Windows = `C:\Users\iamdo\.claude\skills\docx`，Linux/Mac = `~/.claude/skills/docx`。理由：W28 教训 — 绕过 validate 的 OOXML 改动会让 MS Word 报"文件损坏"。
2. **每一个生成的 docx 必须通过 Word COM 验证**：用 `anti_cheat.py` 的 `check_word_com()`（基于 docx2pdf）。Linux/Mac dev 环境允许 `--skip-word-com`，但 **G3 验收前必须在 Windows 工位上跑过一次 Word COM**，未跑不发布。
3. **anti-cheat 三道闸**（QA-RULES §8.2）：`wt_count ≥ 300` / `image_hack == false` / `text_ratio ∈ [0.95, 1.20]`。任一道挂立即拒收 + 回滚。
4. **3 轮 fix-or-escalate**：单语言生成后跑全套检查，发现错误最多 3 轮内修，**3 轮未通过转人工**。**禁止** 5+ 轮迭代 / sub-cohort sweep / 探索式 lever。
5. **一轮 = 一类 ERROR**：同一类 ERROR（如所有 `{{*}}` 残留）允许在一轮内一并补齐（多 key 同改）；不同类 ERROR 算不同轮。**禁止** 把 OOXML 微调和 strings 缺译揉在一轮。每轮 patch 写入 `patches/{lang}.md` 日志。
6. **称呼**：项目 owner 叫"管理者"，提问者叫"大 boss"。**禁止**"老板""儿子""家属"。生成的文档、注释、commit 全部遵守。
7. **commit msg 中文**。
8. **流水线工作根目录**：所有阶段 1-4 的产物落在 `research/yjs-manual-opt/swiss/tools/docx-pipeline/` 下（不是 `template-system/`，那是 v1 弃用代码）。
9. **Linux 渲染必须配 Calibri 字体替换**：母版 OOXML 写的是 `Calibri`（正文+标题），Windows 自动拿真 Calibri，**Linux 默认 fallback 到 DejaVu Sans 度量不一致会排版偏移**。Linux dev 工位首次跑流水线前**必须**执行 `bash setup_linux_fonts.sh`，配 fontconfig 别名 `Calibri → Carlito`（Google 出品的 metrics-equivalent 开源替代）。不改任何 docx OOXML，仅影响 Linux 端 LO/PDF 预览。

## 三、流水线 4 阶段总览

```
W50 docx（事实批准版；CN baseline 评分 7.21/10.13）
   │
   │  阶段 1：母版生成（AI 做）— 产物落 swiss/tools/docx-pipeline/
   │      └→ 人工 review gate G1 ⚠️
   ▼
master_template.docx + master_unpacked/ + strings/cn.{json,md} + docs/PLACEHOLDER_MAP.md
   │
   │  阶段 2：翻译对齐（AI 做，复用 swiss/template/imt050-master-{lang}.html）
   │      └→ 人工 review gate G2 ⚠️
   ▼
strings/{cn,en,de,it,gb,hk,tw}.json（同 key 跨语言对齐）
   │
   │  阶段 3：流水线生成 + 3 轮 fix-or-escalate
   │      └→ 任意语言 3 轮未过 → G4 人工 escalate ⚠️
   ▼
output/imt050-wevac-eu-{lang}.docx × 7   +   patches/{lang}.md
   │
   │  阶段 4：批量验收（QA-RULES Phase 1+3+4+5 全套）
   │      └→ 人工 review gate G3 ⚠️
   ▼
ACCEPTANCE_REPORT.md + 7 个 docx 交付
```

4 个 gate 全部在 `QA-RULES §8.4`。**阶段 1 是分水岭，母版抽错后面全错**。

> **阶段 1 v2 已 G1 PASS**（2026-05-17）：brand `威富可` → `Wevac` 字面化（30 处）+ 中英混排拆 `<w:t>`（60 处）+ safety_notice subarea 三分；304 个 `{{key}}`，round-trip CN mean 5.59 / max 10.10。本 skill 的"事实基线"是 v2，不再是 v1 的 7.21/10.13。新任务不要重做阶段 1，除非走 v3 重做流程。

## 四、阶段 1：母版生成

> **若 v2 母版已存在且 G1 PASS（默认情况），跳过本节，直接进阶段 2**。本节仅适用于：① 新 SKU（如 V23）首次建母版；② v2 母版被大 boss 否决要求 v3 重做。

### 步骤
1. 工作目录 `swiss/tools/docx-pipeline/`。unpack W50 到 `master_unpacked/`：
   `python ${DOCX_SKILL_ROOT}/scripts/office/unpack.py --merge-runs false <W50.docx> master_unpacked/`
2. 用 `extract_master.py` 扫 `master_unpacked/word/{document,header*,footer*}.xml`，按 `references/master-extraction.md` 规则提取占位符。
3. pack 出 `master_template.docx`（不 validate；后续 generator 会 validate 实际产物）；同时输出 `strings/cn.json` + `strings/cn.md` + `docs/PLACEHOLDER_MAP.md` + `docs/_extraction_meta.json`。
4. **round-trip 自检**：`python generator.py --lang cn --output round_trip_cn.docx`，跑 `score_candidate.py`：
   - **硬阈值**：mean ≤ 12 / max ≤ 12（QA-RULES §8.2 anti-cheat 评分门槛）
   - **不再要求** = W50 (7.21/10.13) 零误差 — brand 字面化等结构性改动会让评分偏移，G1 packet 已认可
   - 跑完所有 anti-cheat 三道闸 + validate.py + Word COM（可 `--skip-word-com`，但 G1 packet 必须含一次 Windows Word COM 结果）
5. 不闭合 → 修提取逻辑重做，**不带病前进**。
6. 写 `docs/G1_review_packet.md` 给大 boss（参考 v2 已有版本）。

### Gate G1（QA-RULES §8.4）
交大 boss review：
- `docs/PLACEHOLDER_MAP.md`（key 命名 + area 分布合理吗）
- `round_trip_cn.docx` + `round_trip_cn.score.json`（视觉评分 mean/max 在阈值内）
- `master_unpacked/word/document.xml` 抽样 30 行（占位符位置合理吗，混排是否正确拆 `<w:t>`）
- 7 项 anti-cheat 全 PASS（wt_count / image_hack / text_ratio / page_count / word_com / validate / score）

通过才进阶段 2。

## 五、阶段 2：翻译字典对齐

### 输入
- 母版：`swiss/tools/docx-pipeline/strings/cn.json`（304 keys，事实 SOT）
- HTML 模板：`research/yjs-manual-opt/swiss/template/imt050-master-{cn,en,de,it}.html`
- 命名空间：`swiss/tools/docx-pipeline/docs/PLACEHOLDER_MAP.md`

### 算法（HTML 不含 docx key，必须 cn 文本反查）

详细 runbook 见 `references/stage2-3-runbook.md`。一句话流程：

```
HTML 中 lang 文案 ── 按章节/段落对齐 ──▶ cn 同位置文案 ── 反查 cn.json ──▶ docx key
                                                                            │
                                                                            ▼
                                                          写入 strings/{lang}.json[key]
```

### 步骤
1. 解析 `imt050-master-cn.html` 与 `imt050-master-{lang}.html`，按章节/段落顺序对齐 → (cn_text, lang_text) 对。
2. 对每对：在 `strings/cn.json` 中按 value 反查 key（**完全相等**优先；多 key 命中按 area 消歧；找不到记 WARNING 进 `docs/stage2-{lang}-unmapped.md`）。
3. 写 `strings/{lang}.json`：key 与 cn.json 完全一致；value 是 lang 译文；缺译留空字符串（generator.py 自动回退 cn）。
4. 跨语言锁定 keys（详见 `references/ooxml-map.md` "跨语言锁定 keys"）：spec 数字行、URL、box-title 等强制 = cn 值；用 `tools/check_invariants.py` 校验。
5. T1/T2/T3 抽检（QA-RULES §4b）：从 cn.json 随机抽 10 条，对照 lang.json 人工确认无 truncation / wrong-key / swap。
6. **gb/hk/tw**：现 swiss/template 缺；先与大 boss 确认走哪条路（翻译团队补 / OpenCC 简繁转换 + 港台习语 patch）。本 skill 不替决策。

### Gate G2
交大 boss：
- `strings/{en,de,it}.json`（key 集与 cn.json 完全对齐）
- `docs/stage2-{lang}-unmapped.md`
- T1/T2/T3 抽检 10 条对照清单
- spot-check 关键术语：`IMT050` / `Wevac`（已母版字面化，跨语言不变）/ 单位 `V/Hz/W/kg/mm/°C` / box-title `WARNING/CAUTION/NOTICE`

## 六、阶段 3：流水线生成 + 3 轮 fix-or-escalate

### 核心循环（每个非 CN 语言独立跑）

```
python generator.py --lang {lang} --output output/imt050-wevac-eu-{lang}.docx

for iter in 1..3:
  # 跑全套检查（QA-RULES §8.1 矩阵 + fix-checklist 清单）
  Phase 1b: 数据残留扫描（{{*}} / undefined / null / TODO）
  Phase 4a: CJK 残留（en/de/it 不许有汉字）
  Phase 4b: T1/T2/T3 翻译失败抽检
  Phase 4d: 单位一致性 + 跨语言锁定 keys（C19）
  anti_cheat.py 三道闸（wt_count / image_hack / text_ratio）+ page_count + word_com
  validate.py（官方 docx skill）
  页数 = 15 (±1)

  if 全通过:
    标记 PASS，跳出
  else:
    定位 ERROR 类别（哪类、哪 key、哪页）
    单类别 fix（参考 references/fix-checklist.md "Fix 决策表"）
    写 patches/{lang}.md（触发 / 定位 / fix / 验证）
    重跑

if iter == 3 且未通过:
  停 + 写 docs/diagnosis-{lang}.md → 大 boss escalate G4
```

### 关键约束

- **一轮 = 一类 ERROR**：1 轮内可批量修同一类 ERROR（如所有 `{{*}}` 残留一并补译，不算多轮）；不同类 ERROR 算不同轮。**禁止** OOXML 微调和 strings 缺译揉在一轮。
- **优先改 strings 而非 OOXML**：90% 的 ERROR 是缺译/错译，应改 `strings/{lang}.json`；只有 anti-cheat / validate / Word COM 类 ERROR 才允许改 OOXML，且必须按 `references/ooxml-map.md` 找对应元素。
- **不做研究式 sweep**：发现"de 版 mean diff 14.2 偏高"这种**总体劣化**信号 → **不是触发自修复**，是 W50 母版方法论问题，回研究阶段补强母版（不在本流水线范围）。
- **触发 fix 的合法理由**：必须是 QA-RULES §一-§五 + §8.2 anti-cheat 中某条**具体**ERROR。
- **禁用 lever**：`w:contextualSpacing`（W28）/ `w:val="nil"` 边框（W46）/ 全局 `w:lineRule=auto→exact`（W33）。
- **3 轮上限就是 3 轮**，不允许"再试一轮"。

### `patches/{lang}.md` 格式
详见 `references/fix-checklist.md` §三。每条 fix 写明：状态 / 触发（哪条 QA SOT）/ 定位（key + 页 + xml 路径）/ fix（动作）/ 验证（重跑结果）。

## 七、阶段 4：批量验收

跑 QA-RULES Phase 5 全变体验证（已交付的所有语言 docx）：

| 检查 | 来源 | 工具 |
|------|------|------|
| 全部 anti-cheat 通过 | QA-RULES §8.2 | `anti_cheat.py` |
| 全部 validate.py 通过 | QA-RULES §8.2 | 官方 docx skill |
| 全部 Word COM 可打开 | QA-RULES §8.2 / W28 | `anti_cheat.py`（必须 Windows，**不允许 `--skip-word-com`**） |
| 数据残留 0 / undefined 0 / TODO 0 | QA-RULES §3c | `tools/scan_residue.py` |
| 非 CN 无 CJK 残留 | QA-RULES §4a | `tools/scan_cjk.py` |
| 翻译失败模式 T1/T2/T3 抽检 | QA-RULES §4b | 人工 10 条 |
| 单位一致性 + 跨语言锁定 keys | QA-RULES §4d / C19 | `tools/check_invariants.py` |
| LO 渲染 PNG 抽样视觉对照 W50 | QA-RULES §3a（DOCX 适配） | `soffice --headless` |

写 `docs/ACCEPTANCE_REPORT.md`：每语言一段，列 anti-cheat 7 项 / validate / Word COM / patches 数 / 残余 WARNING。

### Gate G3
大 boss review `docs/ACCEPTANCE_REPORT.md` + 抽样看 PNG → 通过 → commit + 交付。

## 八、错误处理速查（哪条 SOT 触发，立即如何应对）

| 症状 | SOT 条款 | 处理 |
|------|---------|------|
| 占位符漏字段（round-trip mean/max 越界） | DESIGN §十八 18.1 | 阶段 1 retry，**不进阶段 2** |
| `{{*}}` 残留 | QA §1b / §3c | strings/{lang}.json 补漏 → 重 generator |
| CJK 残留（en/de/it） | QA §4a | strings/{lang}.json 补译 → 重 generator |
| undefined / null / TODO 残留 | QA §3c | 修 strings 或 generator 逻辑 |
| 跨语言锁定 keys 偏移 | C19 / QA §4d | 强制设回 cn 值（见 `references/ooxml-map.md` "跨语言锁定 keys"） |
| wt_count < 300 | QA §8.2 | 立即拒，怀疑文本被合并/压成图片，回滚最近 patch |
| text_ratio 越界 | QA §8.2 | 立即拒，怀疑占位符没替换完 / 重复替换 |
| Word COM 打不开 | QA §8.2 / W28 | 立即拒；Linux dev 阶段允许 `--skip-word-com`，G3 前必须补一次 Windows 验证 |
| validate 失败 | QA §8.2 | 读错误 → METHODOLOGY § 3.1 → 修 XML → 重 pack |
| 页数 ≠ 15 | C13 / QA §8.2 | 单维度查（哪页多/少了），fix 或转 G4 |
| 3 轮没修通 | QA §8.4 G4 | 停，写 `docs/diagnosis-{lang}.md`，转人工 |
| 翻译失败 T1/T2/T3 | QA §4b | 抽检 → 改 strings/{lang}.json，**不动 OOXML** |

## 九、决策边界

- **AI 做**：占位符提取 / 翻译对齐 / fix 定位 / 写 patches 日志 / 写 G1/G2/G3 review packet
- **Python helper 做**（确定性）：XML 替换 / pack / validate / scoring / anti-cheat / 残留扫描 / 锁定 keys 校验
- **人工 review gate**：G1 母版 / G2 翻译 / G3 验收 / G4 escalate（QA §8.4）
- **本 skill 不做**：sub-cohort sweep / 探索性 lever / 5+ 轮调优（那是研究阶段的事，已结束）

## 十、参考（按使用顺序）

1. `swiss/DESIGN-STANDARD.md` — 视觉/内容规范 SOT（§十八 DOCX 映射）
2. `swiss/QA-RULES.md` — 审计流程 SOT（§八 DOCX 适配）
3. `docs/superpowers/specs/2026-05-17-docx-pipeline-design.md` — 流水线设计文档
4. `references/master-extraction.md` — 阶段 1 占位符提取规则细则
5. `references/stage2-3-runbook.md` — 阶段 2 HTML→cn→lang 映射 + 阶段 3 派单要点
6. `references/ooxml-map.md` — SOT 语义条款 → OOXML 元素 + 跨语言锁定 keys（v2 真实 keys）
7. `references/fix-checklist.md` — 3 轮 fix-or-escalate 检查清单 + 一轮粒度
8. `references/anti-cheat-impl.md` — anti_cheat.py Python 实现骨架

## 十一、何时不用本 skill

- **单纯改 CN 版 OOXML**（不涉及多语言）：研究阶段任务，走 METHODOLOGY.md 那套手动 sweep
- **新 SKU 母版**（V23/Vesta/Act）：本 skill 假设 master = W50 IMT050；新 SKU 先做自己的 W50 等价物（先是研究阶段）
- **HTML/PDF 流水线问题**：跟本 skill 无关，看 `swiss/tools/build-variant.js` + `swiss/QA-RULES.md` Phase 2-3
- **PDF/HTML 与 DOCX 规范不一致**：修 SOT（`DESIGN-STANDARD.md` / `QA-RULES.md`），不要在本 skill 中绕过
