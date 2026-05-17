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

1. **官方 docx skill 是唯一文件 I/O 入口**：unpack/pack/validate 必须用 `C:\Users\iamdo\.claude\skills\docx\scripts\office\{unpack,pack,validate}.py`。理由：W28 教训 — 绕过 validate 的 OOXML 改动会让 MS Word 报"文件损坏"。
2. **每一个生成的 docx 必须通过 `compare_word.py`**：Word COM 打不开的 docx 一律拒收，无例外。
3. **anti-cheat 三道闸**（QA-RULES §8.2）：`wt_count ≥ 300` / `image_hack == false` / `text_ratio ∈ [0.95, 1.20]`。任一道挂立即拒收 + 回滚。
4. **3 轮 fix-or-escalate**：单语言生成后跑全套检查，发现错误最多 3 轮内修，**3 轮未通过转人工**。**禁止** 5+ 轮迭代 / sub-cohort sweep / 探索式 lever。
5. **每轮单维度修**：一轮 patch 只改一处，写入 `patches/{lang}.md` 日志。
6. **称呼**：项目owner 叫"管理者"，提问者叫"大 boss"。**禁止**"老板""儿子""家属"。生成的文档、注释、commit 全部遵守。
7. **commit msg 中文**。

## 三、流水线 4 阶段总览

```
W50 docx（评分 7.21/10.13，事实批准版）
   │
   │  阶段 1：母版生成（AI 做）
   │      └→ 人工 review gate G1 ⚠️
   ▼
master_template.docx (200-400 个 {{key}})  +  strings/cn.md  +  PLACEHOLDER_MAP.md
   │
   │  阶段 2：翻译对齐（AI 做，复用 swiss/template/imt050-master-{lang}.html）
   │      └→ 人工 review gate G2 ⚠️
   ▼
strings/{cn,en,de,it,gb,hk,tw}.md（同 key 跨语言对齐）
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

## 四、阶段 1：母版生成

### 步骤
1. unpack W50：`python C:\Users\iamdo\.claude\skills\docx\scripts\office\unpack.py final/imt050-wevac-eu-cn.docx → master_unpacked/`
2. 扫 `master_unpacked/word/document.xml` + `header*.xml` + `footer*.xml`，提取占位符。规则见 `references/master-extraction.md`。
3. pack 出 `master_template.docx`；输出 `strings/cn.md` + `docs/PLACEHOLDER_MAP.md`。
4. **round-trip 自检**：用 master + cn.md 重新生成 CN docx，必须 **`score_candidate.py` 评分 = W50 (7.21/10.13) 零误差**。
5. 不闭合 → 修提取逻辑重做，**不带病前进**。

### Gate G1（QA-RULES §8.4）
交大 boss review：
- `docs/PLACEHOLDER_MAP.md`（key 命名 + 提取范围合理吗）
- round-trip CN docx + score json（视觉 = W50 吗）
- `master_unpacked/word/document.xml` 抽样 30 行（占位符位置合理吗）

通过才进阶段 2。

## 五、阶段 2：翻译字典对齐

1. 解析 `swiss/template/imt050-master-{de,en,it}.html`（HTML 模板，不是目录）。
2. 用 PLACEHOLDER_MAP.md 的 key 把 HTML 占位符对应到 docx 占位符。
3. 写 `strings/{en,de,it}.md`，格式严格对齐 `strings/cn.md`。
4. **gb/hk/tw 现 swiss/template 缺**：先跟大 boss 确认走哪条路（翻译团队补 / 自动繁简转换 + 港台习语 patch）。
5. spot-check 跨语言术语一致（IMT050 / Wevac / Argion / 制冰机 / 警告 / 单位）— `DESIGN-STANDARD §十八 18.2` 跨语言不变 key 清单。

### Gate G2
大 boss spot-check 关键术语。

## 六、阶段 3：流水线生成 + 3 轮 fix-or-escalate

### 核心循环（每个非 CN 语言独立跑）

```
generator.py --lang {lang}
   → output/imt050-wevac-eu-{lang}.docx

for iter in 1..3:
  # 跑全套检查（QA-RULES §8.1 矩阵）
  Phase 1b: 数据残留扫描（{{*}} / undefined / null / TODO）
  Phase 4a: CJK 残留（en/de/it 不许有汉字）
  Phase 4b: T1/T2/T3 翻译失败抽检
  Phase 4d: 单位一致性（C19）
  anti-cheat 三道闸（wt_count / image_hack / text_ratio）
  validate.py
  Word COM 打开（compare_word.py）
  页数 = 15 (±1)

  if 全通过:
    标记 PASS，跳出
  else:
    定位具体错误（哪页/哪段/哪 key）
    单维度 fix（参考 references/ooxml-map.md 找对应 OOXML 元素）
    写 patches/{lang}.md（selector / before / after / 触发 / 效果）
    重跑

if iter == 3 且未通过:
  停 + 写诊断报告 → 大 boss escalate G4
```

### 关键约束

- **一轮一处**：不允许同一 patch 改多个维度。
- **不做研究式 sweep**：发现"de 版 mean diff 14.2 偏高"这种**总体劣化**信号 → **不是触发自修复**，是 W50 母版方法论问题，回到研究阶段补强母版（不在本流水线范围）。
- **触发 fix 的合法理由**：必须是 QA-RULES §一-§五 + §8.2 anti-cheat 中某条**具体**ERROR。
- **禁用 lever**：`w:contextualSpacing`（W28）/ `w:val="nil"` 边框（W46）/ 全局 `w:lineRule=auto→exact`（W33）。
- **3 轮上限就是 3 轮**，不允许"再试一轮"。

### `patches/{lang}.md` 格式
```markdown
# {LANG} OOXML 修复日志

## fix 1 — p3 数据残留：{{safety_warning_5}} 未替换
- **状态**: ✅ Applied (iter-1, sha:abc1234)
- **触发**: QA-RULES Phase 1b 扫到 master_unpacked/word/document.xml p3 残留 `{{safety_warning_5}}`
- **定位**: strings/de.md 第 47 行 key `safety_warning_5` 漏写
- **fix**: 补 strings/de.md 第 47 行德文翻译
- **验证**: 重 generator.py → 再扫无残留 → anti-cheat 通过
```

## 七、阶段 4：批量验收

跑 QA-RULES Phase 5 全变体验证（7 个 docx）：

| 检查 | 来源 |
|------|------|
| 全部 anti-cheat 通过 | QA-RULES §8.2 |
| 全部 validate.py 通过 | QA-RULES §8.2 |
| 全部 Word COM 可打开 | QA-RULES §8.2 |
| 数据残留 0 / undefined 0 / TODO 0 | QA-RULES §3c |
| 非 CN 无 CJK 残留 | QA-RULES §4a |
| 翻译失败模式 T1/T2/T3 抽检 | QA-RULES §4b |
| 单位一致性 | QA-RULES §4d |
| LO 渲染 PNG 抽样视觉对照 W50 | QA-RULES §3a（DOCX 适配） |

写 `ACCEPTANCE_REPORT.md`：每语言一段，列 anti-cheat / validate / Word COM / patches 数 / 残余 WARNING。

### Gate G3
大 boss review ACCEPTANCE_REPORT.md + 抽样看 PNG → 通过 → commit + 交付。

## 八、错误处理速查（哪条 SOT 触发，立即如何应对）

| 症状 | SOT 条款 | 处理 |
|------|---------|------|
| 占位符漏字段（round-trip ≠ W50） | DESIGN §十八 18.1 | 阶段 1 retry，**不进阶段 2** |
| `{{*}}` 残留 | QA §1b / §3c | strings/{lang}.md 补漏 → 重 generator |
| CJK 残留（en/de/it） | QA §4a | strings/{lang}.md 补译 → 重 generator |
| undefined / null / TODO 残留 | QA §3c | 修 strings 或 generator 逻辑 |
| 单位不一致 | C19 / QA §4d | 锁定 spec_unit_* key 跨语言不变 |
| wt_count < 300 | QA §8.2 | 立即拒，怀疑文本被合并/压成图片 |
| text_ratio 越界 | QA §8.2 | 立即拒，怀疑占位符没替换完 / 重复替换 |
| Word COM 打不开 | QA §8.2 / W28 | 立即拒，回滚最近 patch |
| validate 失败 | QA §8.2 | 读错误 → METHODOLOGY § 3.1 → 修 XML → 重 pack |
| 页数 ≠ 15 | C13 / QA §8.2 | 单维度查（哪页多/少了），fix 或转 G4 |
| 3 轮没修通 | QA §8.4 G4 | 停，写诊断报告，转人工 |
| 翻译失败 T1/T2/T3 | QA §4b | 抽检 → 改 strings/{lang}.md，**不动 OOXML** |

## 九、决策边界

- **AI 做**：占位符提取 / 翻译对齐 / fix 定位 / 写 patches 日志
- **Python helper 做**（确定性）：XML 替换 / pack / validate / scoring / anti-cheat
- **人工 review gate**：G1 母版 / G2 翻译 / G3 验收 / G4 escalate（QA §8.4）
- **本 skill 不做**：sub-cohort sweep / 探索性 lever / 5+ 轮调优（那是研究阶段的事，已结束）

## 十、参考（按重要性）

1. `swiss/DESIGN-STANDARD.md` — 视觉/内容规范 SOT（§十八 DOCX 映射）
2. `swiss/QA-RULES.md` — 审计流程 SOT（§八 DOCX 适配）
3. `docs/superpowers/specs/2026-05-17-docx-pipeline-design.md` — 流水线设计文档
4. `references/master-extraction.md` — 阶段 1 占位符提取规则细则
5. `references/ooxml-map.md` — SOT 语义条款 → OOXML 元素映射
6. `references/fix-checklist.md` — 3 轮 fix-or-escalate 检查清单
7. `references/anti-cheat-impl.md` — anti-cheat.py Python 实现骨架

## 十一、何时不用本 skill

- **单纯改 CN 版 OOXML**（不涉及多语言）：研究阶段任务，走 METHODOLOGY.md 那套手动 sweep
- **新 SKU 母版**（V23/Vesta/Act）：本 skill 假设 master = W50 IMT050；新 SKU 先做自己的 W50 等价物（先是研究阶段）
- **HTML/PDF 流水线问题**：跟本 skill 无关，看 `swiss/tools/build-variant.js` + `swiss/QA-RULES.md` Phase 2-3
- **PDF/HTML 与 DOCX 规范不一致**：修 SOT（`DESIGN-STANDARD.md` / `QA-RULES.md`），不要在本 skill 中绕过
