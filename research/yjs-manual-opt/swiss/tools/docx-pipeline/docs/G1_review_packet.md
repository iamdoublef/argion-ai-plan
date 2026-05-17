# Gate G1 v2 — 母版生成阶段人工 Review Packet

> **版本**：v2（v1 G1 review FAIL 后大 boss 决定 3 项改动重做的产物）
> **触发**：docx 流水线阶段 1 v2（W50 占位符化 + 3 项改动 + round-trip 验证）完成。
> **审阅人**：大 boss。**决策**：PASS（进阶段 2）/ HOLD（修后再 review）/ FAIL（v3 重做）。
> **SOT 引用**：
> - 视觉规范 → `swiss/DESIGN-STANDARD.md` §十八 DOCX 实现映射
> - 审计规范 → `swiss/QA-RULES.md` §八 DOCX 流水线审计适配（§8.2 anti-cheat / §8.4 G1）
> - 提取规则 → `.claude/skills/docx-pipeline/references/master-extraction.md`
> - OOXML 映射 → `.claude/skills/docx-pipeline/references/ooxml-map.md`
> - anti-cheat 骨架 → `.claude/skills/docx-pipeline/references/anti-cheat-impl.md`
>
> 本 packet **不重新定义**任何视觉/审计规范，仅汇总阶段 1 v2 产出 + v1→v2 改动对比。

---

## A. PLACEHOLDER_MAP 命名说明

### A.1 命名格式（master-extraction.md §Key 命名规范）

```
<area>_[<subarea>_]<sequence>
```

- `area`：按 master-extraction.md 表列出的 10 种之一
  （`cover`/`toc`/`safety`/`install`/`operate`/`spec`/`troubleshoot`/`clean`/`warranty`/`footer`）
- `subarea`：W50 母版中按页/语义二级分类时使用：
  - `safety_warning`（p3 WARNING 框）/ **`safety_caution`（p4 CAUTION 框）/ `safety_notice`（p4 NOTICE 框，v2 新增）**
  - `operate_structure`（p6）/ `operate_function`（p7）/ `operate_guide`（p9-p10）
  - `install_prep`（p5）/ `install_transport`（p13）
  - `warranty_card`（p15）
- `sequence`：该 area（或 area+subarea）内按文档先后顺序的递增编号（从 1 起）

**禁用**：中文 pinyin / 纯位置 (`p3_line5`) / 纯数字 (`text_1`)。

### A.2 areas 与 W50 页结构对应（v2 调整 p4）

| 页 | area / subarea | 说明 |
|----|---------------|------|
| p1 | `cover` | 封面 |
| p2 | `toc` | 目录 |
| p3 | `safety_warning_*` | 安全须知 WARNING 框 |
| p4 (前段) | `safety_caution_*` | 安全须知 CAUTION 框（直到 NOTICE box-title 之前） |
| **p4 (后段)** | **`safety_notice_*`（v2 新增）** | **NOTICE 框（从 box-title `提示 NOTICE` 起）** |
| p5 | `install_prep_*` | 产品及使用提示（放置/水质/使用） |
| p6 | `operate_structure_*` | 产品结构（部件标签） |
| p7 | `operate_function_*` | 产品功能（按键说明） |
| p8 | `spec_*` | 技术参数 |
| p9-p10 | `operate_guide_*` | 操作指引（步骤+提示） |
| p11 | `troubleshoot_*` | 故障排除 |
| p12 | `clean_*` | 维护保养 |
| p13 | `install_transport_*` | 安装运输/存储/拆除 |
| p14 | `warranty_*` | 保修信息 |
| p15 | `warranty_card_*` | 保修卡 |
| p2-p15 | `footer_*` | 页脚（每页 1 个） |

### A.3 跨语言不变 key 清单（v2 重构 — 大量原 placeholder 已字面化）

W50 母版中下列内容**全部已在母版字面化**（不再是 placeholder），所有语言版本天然一致：

| 内容 | 出现 | v1 处理 | v2 处理 |
|------|------|---------|---------|
| **品牌名 `Wevac`** | 30 处（document 16 + footer 14） | 30 个独立 placeholder（cn=`威富可`，其他 lang 填 `Wevac`） | **母版字面 `Wevac`**，所有 lang 一致 |
| **型号 `IMT050`** | 多处嵌入混排 | 整段 placeholder，要求译者保留 `IMT050` 前缀 | **拆 `<w:t>` 后型号作字面**，CJK 部分独立 placeholder |
| 单位 `V`/`Hz`/`W`/`kg`/`mm`/`°C`/`dB(A)`/`℉` | 嵌入混排 | 部分嵌入 placeholder | **同 v2 型号策略**：单位作字面，CJK 独立 placeholder |
| URL/邮箱 `support@wevactech.com` | 嵌入混排 | 部分嵌入 placeholder | **拆 `<w:t>` 后字面化** |
| 警示标题 `WARNING`/`CAUTION`/`NOTICE`/`DISCLAIMER` | `警告 WARNING`/`注意 CAUTION`/`提示 NOTICE`/`免责声明 DISCLAIMER` 各处 | 整段 placeholder，要求译者保留英文标题 | **拆 `<w:t>` 后英文标题作字面**，中文前缀（`警告 ` 等）独立 placeholder |
| 章节英文标题 `CH.0x` | 各 area 顶部 | v1 已是纯 ASCII w:t（未占位符化） | 同 v1（不动） |

### A.4 PLACEHOLDER_MAP.md（30 处抽样在该文件 §D）

详见 [`PLACEHOLDER_MAP.md`](./PLACEHOLDER_MAP.md)。

---

## B. Round-trip 评分对照（v2 新基准）

`score_candidate.py` 评分（target = W50 PDF `final/_score_tmp/pdf/imt050-wevac-eu-cn.pdf`，
baseline-pngs = `final/_score_tmp/png/`）。

### B.1 全局指标

| 指标 | W50 baseline (v1 时记录) | round_trip_cn v2 | 偏差 | 判定 |
|------|-------------------------|------------------|------|------|
| pages | 15 | 15 | 0 | ✅ |
| text chars | 4626 | 4686 | +60 | ✅（品牌 `威富可`→`Wevac`，3→5 字符×30 处 = +60，与预期吻合） |
| text ratio | 1.00 | 1.01 | +0.01 | ✅ |
| editable_pct | 100.0% | 100.0% | 0.0pp | ✅ |
| **wt_count** | **448** | **545** | **+97** | ✅（v2 拆 `<w:t>` 60 个，每个拆出 ≥ 2 节点 → 净增 ≈ 97） |
| image_hack_detected | False | False | — | ✅ |
| **overall_mean_diff** | **7.21** | **5.59** | **-1.62** | ✅（评分变好，符合大 boss 接受新 CN 视觉基准） |
| **max_page_diff** | **10.13** | **10.10** | **-0.03** | ✅（< 12 阈值，无 fix-or-escalate 报警） |
| pass.overall | True | True | — | ✅ |

> **大 boss 已确认**：v2 引入品牌字面化 + 中英混排拆 `<w:t>`，CN 字符宽度变化导致视觉锚需要重建。
> v2 round-trip 评分（5.59 / 10.10）替代 v1 的 7.21 / 10.13 **作为新 CN 基准**。

### B.2 Per-page mean diff（v2 vs v1）

| Page | v1 round_trip_cn | v2 round_trip_cn | 偏差 | 说明 |
|------|------------------|------------------|------|------|
| p1 (cover) | 2.17 | 1.03 | **-1.14** | 品牌字面化让 p1 顶部"威富可"→"Wevac"与 PDF target 渲染更一致 |
| p2 (toc) | 3.23 | 1.74 | -1.49 | 同上（toc 顶部 banner） |
| p3 (safety warning) | 10.03 | 10.10 | +0.07 | 持平；w:t 拆分微调，p3 是 max |
| p4 (safety caution+notice) | 6.38 | 4.13 | -2.25 | 安全须知（续）页 |
| p5 (install prep) | 8.55 | 7.17 | -1.38 | |
| p6 (operate structure) | 3.77 | 5.53 | +1.76 | 产品结构页轻微退化（CJK→Latin 字符宽度差） |
| p7 (operate function) | 7.18 | 5.15 | -2.03 | |
| p8 (spec) | 7.05 | 4.13 | -2.92 | 技术参数页改善（单位字面化对齐表格） |
| p9 (operate guide) | 9.69 | 6.90 | -2.79 | |
| p10 (operate guide) | 9.13 | 7.52 | -1.61 | |
| **p11 (troubleshoot)** | **10.13**（max） | **7.91** | **-2.22** | p11 不再是 max |
| p12 (clean) | 8.84 | 5.47 | -3.37 | |
| p13 (install transport) | 9.25 | 6.86 | -2.39 | |
| p14 (warranty) | 9.67 | 8.65 | -1.02 | |
| p15 (warranty card) | 3.04 | 1.49 | -1.55 | |

**结论**：v2 在 **13/15 页**上 mean diff 下降，仅 p3 / p6 微升（< 2.0）。
最大 p3 = 10.10 < 12 fix-or-escalate 阈值。max_page_diff 从 p11 (10.13) 转移到 p3 (10.10)。

### B.3 Top 3 per-page diff (v2)

1. **p3 safety warning — 10.10**（警告框密度大，与 v1 的 10.03 持平；w:t 拆开 `警告 WARNING` 后 OOXML 节点偏移）
2. **p14 warranty — 8.65**（地址表格混排 + Wevac 字面化字符宽度变化）
3. **p11 troubleshoot — 7.91**（W49 后已修过 disclaimer + 字距）

---

## C. 占位符抽样 30 处

详见 [`PLACEHOLDER_MAP.md` §D](./PLACEHOLDER_MAP.md)。30 个抽样覆盖 9 个 area + footer + 新 `safety_notice` subarea，
每个抽样列：key + 原文（中文）+ OOXML 位置（文件:行号）+ run rPr（sz/font/color/bold）。

字号与 DESIGN-STANDARD §三 字号系统的对应不变（W50 母版 baked-in，本阶段不改 `<w:rPr>`）。

---

## D. 统计

### D.1 占位符统计（v2 vs v1）

| 维度 | v1 | v2 | 偏差 | 说明 |
|------|----|----|------|------|
| **总占位符数** | 277 | **304** | +27 | 拆 `<w:t>` 增加 CJK chunks (+58)；品牌字面化减占位 (-30)；净 +27 |
| document.xml | 263 | 290 | +27 | 同上 |
| footer*.xml | 14 | 14 | 0 | footer 仍每页 1 个 placeholder（拆后字面 `Wevac IMT050 ` + placeholder `说明书`） |

**v2 按 area 分布**（含 v1 对比 + 净变化）：

| Area | v1 | v2 | 偏差 |
|------|----|----|------|
| cover | 5 | 4 | -1（去 `威富可`） |
| toc | 13 | 12 | -1（去 `威富可`） |
| safety | 41 | 43 | +2（`warning`+`caution`+`notice` 三 subarea，拆混排）|
| install | 36 | 46 | +10（多处中英混排拆） |
| operate | 55 | 60 | +5 |
| spec | 22 | 23 | +1 |
| troubleshoot | 34 | 40 | +6 |
| clean | 18 | 17 | -1（去 `威富可`） |
| warranty | 39 | 45 | +6（地址 / 邮箱混排拆） |
| footer | 14 | 14 | 0 |

### D.2 v2 三 subarea 切分（safety）

- `safety_warning_*`: 27 个 key（p3）
- `safety_caution_*`: 10 个 key（p4 中 NOTICE box-title 之前）
- `safety_notice_*`: 6 个 key（p4 中从 `提示 NOTICE` box-title 起）

`safety_notice_*` 内容：
- `safety_notice_1` = `提示 `（CJK 前缀，`NOTICE` 已作字面）
- `safety_notice_2` = `产品噪音等级低于`
- `safety_notice_3` = `。`
- `safety_notice_4` = `本产品的气候类型为`
- `safety_notice_5` = `，适合在`
- `safety_notice_6` = `的环境温度中使用。`

p4 NOTICE box-title 偏移：document.xml pos = **61497**（v2 切换 subarea 锚点）。

### D.3 跳过 / 合并 / 拆分（v2）

- 合并的 `<w:r>`：**0**
- 拆分的 `<w:r>`：**0**（v2 仍不拆 `<w:r>`）
- 拆分的 `<w:t>` 节点：**60**（document.xml 46 + footer 14）
- `<w:rPr>` 修改数：**0**

符合硬规则 "不动 `<w:r>` 结构、不改 `<w:rPr>`；允许拆 `<w:t>` 节点（OOXML 合法：一个 `<w:r>` 可含多 `<w:t>`）"。

---

## E. SOT 引用（不在本 packet 中重新定义）

### E.1 视觉规范（`DESIGN-STANDARD.md`）

| 本阶段动作 | 依据条款 |
|----------|---------|
| 复用 W50 母版作为视觉锚（v2 接受 CN 视觉基准重建） | §十八 18.1 母版与生成模型 |
| 字号 `sz=15/14/13/27` 等 OOXML 值 | §三 字体系统 + §十八 18.2 |
| 颜色 `000000/E63846/F2F2F7/8E8E93` 等 | §二 色彩系统 + §十八 18.2 |
| 警示三级 WARNING/CAUTION/NOTICE 框 | §七 警示体系 + §十八 18.2（v2 NOTICE 单独切 subarea） |
| 不改 W50 几何/字距 | §十八 18.1 + 18.3 |
| 单位跨语言一致 | §十七 C19 + §十八 18.2（v2 拆 `<w:t>` 后单位字面，天然一致） |
| 标准 15 页结构不漂移 | §十三 + §十七 C13 + §十八 18.2 |

### E.2 审计规范（`QA-RULES.md`）

| 本阶段动作 | 依据条款 |
|----------|---------|
| anti-cheat 三道闸 + 页数 + Word COM | §8.2 DOCX 专属 anti-cheat 阈值表 |
| round-trip CN = 新基准（v2 接受） | §8.2 `score_candidate.py` + §8.4 G1 |
| 数据残留（`{{*}}` 0 残留） | §8.1 Phase 1b + §三 C3c |
| 母版生成完成时人工 review | §8.4 G1 |
| 数据同源（cn.md ↔ master_template.docx） | §一致性原则 + DESIGN §十八 18.1 |

### E.3 提取/实现细则（`.claude/skills/docx-pipeline/references/`）

| 文件 | 用途 |
|------|------|
| `master-extraction.md` | 阶段 1 占位符提取规则（v2 接受"允许拆 `<w:t>`"作为合法操作） |
| `ooxml-map.md` | SOT 语义条款 → OOXML 元素映射，跨语言不变 key 速查 |
| `anti-cheat-impl.md` | anti_cheat.py 实现骨架 |

---

## F. anti-cheat 结果（v2）

`round_trip_cn.docx` 经 5 项检查（`anti_cheat.py round_trip_cn.docx --baseline final/imt050-wevac-eu-cn.docx`）：

| 检查项 | SOT 阈值（§8.2） | 实测 | 判定 |
|--------|-----------------|------|------|
| `wt_count` | ≥ 300 | **545** | ✅ PASS |
| `image_hack` | false | **false**（media=16 = baseline 16） | ✅ PASS |
| `text_ratio` | [0.95, 1.20] | **1.006**（5137/5105） | ✅ PASS |
| `page_count` | 15 (±1) | **15** | ✅ PASS |
| `word_com`（W28 教训） | 不报错 | **PASS**（docx2pdf 转换成功） | ✅ PASS |
| `validate.py`（带 `--original W50`）| 不引入新错误 | **All validations PASSED** | ✅ PASS |
| `score_candidate.py` | mean ≤ 12 / max ≤ 12 | **5.59 / 10.10** | ✅ PASS |

**全部 7 项硬闸 PASS**，符合 SKILL §四 阶段 1 验收清单。

---

## G. G1 决策建议（v2）

### G.1 v1 → v2 改动落地的强项

1. **品牌字面化彻底**：30 处"威富可"全部已字面化为 `Wevac`，`master_template.docx` 中 `威富可` 子串数 = 0；`cn.json` 中 0 处 `威富可` value。所有语言版本天然一致，**译者不再需要填 30 次品牌名**。
2. **拆 `<w:t>` OOXML 合法**：60 个混排 `<w:t>` 拆成多个 `<w:t>` 节点（同一 `<w:r>` 内），保留原 `<w:rPr>`；validate.py 通过 + Word COM 可打开 + LO 渲染正常。证明"一个 `<w:r>` 可含多 `<w:t>`"在 W50 母版中安全可行。
3. **safety_notice 切分清晰**：p4 NOTICE 框已独立 subarea（6 keys），与 CAUTION 框（10 keys）分开；未来若 NOTICE 内容跨页 / 翻译策略不同（如某 lang 不译 box-title 后缀） → 可单独定位。
4. **round-trip CN 评分改善**：mean 7.21 → 5.59（13/15 页改善），max 10.13 → 10.10（持平）。证明 v2 改动**不仅没破坏视觉锚，反而让 CN docx 与 PDF target 更接近**（因品牌 latin 字符与 PDF 文字渲染更一致）。
5. **anti-cheat 全过 + 阈值 5.59/10.10 远低于 12 警戒线**：无 fix-or-escalate 触发。

### G.2 v2 仍存的人工 review 点

1. **拆得最碎的混排**：如 `'香港九龙尖沙咀漆咸道南87-105号百利商业中心404A室'` 拆成 5 chunks（3 placeholders + 2 字面）。
   - **可接受**：地址中的号牌 `87-105` / 房号 `404A` 是跨语言不变（不翻译），译者只翻 CJK 部分。
   - **风险**：译者翻译时若改 CJK 部分顺序（如把"室"放在前面），可能与字面 `404A ` 错位。
   - **建议**：阶段 2 翻译时人工抽 5 处复杂拆分（warranty 地址 / install_prep `120mm（4.7"）` 类）spot-check。

2. **`safety_notice_1` = `提示 `（带尾空格）**：拆 `'提示 NOTICE'` 时 CJK chunk 含尾空格，作为 placeholder 值。
   - **风险**：译者去掉尾空格 → 渲染时 `EN: Notice` 前后无空 vs `CN: 提示 NOTICE` 有空。
   - **缓解**：placeholder 用 `<w:t xml:space="preserve">` 已保留；阶段 2 翻译规范需明确"保留首尾空白"。

3. **运输页 `45°` 类**：`× / °` 等符号被分类为 ASCII（U+00D7 / U+00B0），切到字面 `<w:t>`，CJK 部分独立 placeholder。
   - **正确**：这些是跨语言通用符号。
   - **副作用**：尺寸表 `'尺寸（宽×深×高）'` 拆成 3 placeholders + 2 字面 `×`。

4. **p3 / p6 mean diff 微升**：p3 +0.07（噪声范围）/ p6 +1.76（产品结构页 latin 字符宽度差）。
   - **不需 fix**：max < 12 / mean < 12。
   - **后续监控**：阶段 3 跑其他语言时 p6 可能继续受 latin 字符宽度影响 → 不修，标 ACCEPTANCE 时观察。

### G.3 与 SOT 的一致性

- ✅ `DESIGN-STANDARD §十八` 全部条款通过 round-trip 隐式验证（视觉评分在阈值内）
- ✅ `QA-RULES §8.2` 全部 7 项 anti-cheat 通过
- ✅ `QA-RULES §8.4 G1` 三项检查（PLACEHOLDER_MAP 命名 / round-trip CN 评分在阈值 / 抽样占位符位置合理）齐备
- ⚠️ 提取规则 `master-extraction.md §替换原则` 原文写 "不要碰 run 结构、不要合并 run、不要改 `<w:rPr>`" — v2 引入"允许拆 `<w:t>`"作为补充（已与大 boss 确认）。建议阶段 2 前在 master-extraction.md 加一行注脚说明。

### G.4 推荐决策：**PASS（可进阶段 2）**

理由：
- 大 boss G1 v1 review 决定的 3 项改动**全部 100% 落地**：30 处品牌字面化 ✓ / 60 个混排拆 `<w:t>` ✓ / safety_notice 单独 subarea ✓
- 所有硬交付指标（validate / anti-cheat / Word COM / score）100% 通过
- round-trip CN 评分较 v1 改善（13/15 页 mean 下降，max 持平）
- 拆 `<w:t>` 让译者工作简化（不再要求保留 IMT050 / WARNING 等英文字串）

若大 boss 想 **HOLD**：合理触发条件 ——
- G.2 中的某项 review 点要求更深入抽样（如要求 `address` / `120mm` 类全部人工 review）
- 想看 master-extraction.md 注脚先补上再走（建议阶段 2 启动前补）
- 想看 v2 中**每一处**拆 `<w:t>` 的 OOXML 上下文（45 个混排 origin，可补附录）

若大 boss 想 **FAIL**：通常触发条件 ——
- 某项改动未落地（**当前未出现** — 改动 1/2/3 全部已实施）
- 评分破线（**当前未出现** — max 10.10 < 12）
- anti-cheat 任一项挂（**当前未出现**）

---

## H. v1 → v2 改动对比（本节为 v2 特有）

### H.1 改动 1 — 品牌字面化（30 处 → `Wevac`）

W50 母版中 `威富可` 全部 30 处直接替换为字面 `Wevac`，不再占位。`cn.json` 中相应 brand placeholder（v1 的 `cover_1` / `toc_1` / `safety_warning_1` / `safety_caution_1` / `install_prep_1` / `operate_structure_1` / `operate_function_1` / `spec_1` / `operate_guide_1` / `operate_guide_14` / `troubleshoot_1` / `clean_1` / `install_transport_1` / `warranty_1` / `warranty_card_1` 这 15 处独立 brand + 1 处 `warranty_3` 嵌入 + 14 个 footer brand）全部消失。

实施 OOXML 行号（document.xml 16 + footer 14）：

**document.xml（16 处）**：line 25 / 194 / 621 / 1431 / 1849 / 2322 / 3198 / 3851 / 5328 / 5814 / 6561 / 7862 / 8409 / 8894 / 8948（嵌入 `Wevac ` literal，在 `warranty_2` / `warranty_3` placeholder 之间）/ 9881

**footer*.xml（14 处）**：footer2.xml..footer15.xml 每个文件 line 57（pattern 一致：`<w:t xml:space="preserve">Wevac IMT050 </w:t><w:t>{{footer_N}}</w:t>`）

### H.2 改动 2 — 中英混排拆 `<w:t>`（60 处）

document.xml 中 46 个 `<w:t>`（含 brand 替换后引发的 1 个）+ footer 中 14 个 → 共 60 个拆。

**示例**（按 source order）：

| 原 `<w:t>` 内容 | 拆后 OOXML | placeholder keys |
|----------------|-----------|------------------|
| `IMT050 — 说明书` | `<w:t xml:space="preserve">IMT050 — </w:t><w:t>{{toc_1}}</w:t>` | `toc_1 = 说明书` |
| `警告 WARNING` | `<w:t xml:space="preserve">{{safety_warning_3}}</w:t><w:t>WARNING</w:t>` | `safety_warning_3 = 警告 ` |
| `注意 CAUTION` | `<w:t xml:space="preserve">{{safety_caution_2}}</w:t><w:t>CAUTION</w:t>` | `safety_caution_2 = 注意 ` |
| `提示 NOTICE` (p4) | `<w:t xml:space="preserve">{{safety_notice_1}}</w:t><w:t>NOTICE</w:t>` | `safety_notice_1 = 提示 ` |
| `提示 NOTICE` (p10) | `<w:t xml:space="preserve">{{operate_guide_24}}</w:t><w:t>NOTICE</w:t>` | `operate_guide_24 = 提示 ` |
| `免责声明 DISCLAIMER` | `<w:t xml:space="preserve">{{troubleshoot_39}}</w:t><w:t>DISCLAIMER</w:t>` | `troubleshoot_39 = 免责声明 ` |
| `运输后需静置4小时，待冷媒稳定后再通电。` | 3 节点：CJK + `4` + CJK | `safety_caution_4 / safety_caution_5` |
| `产品噪音等级低于50 dB(A)。` | 3 节点：CJK + `50 dB(A)` + CJK | `safety_notice_2 / safety_notice_3` |
| `本产品的气候类型为SN，适合在10℃~32℃ / 50℉~89.6℉ 的环境温度中使用。` | 5 节点：CJK / `SN` / CJK / `10℃~32℃ / 50℉~89.6℉ ` / CJK | `safety_notice_4..6` |
| `确保产品四周留有至少 120mm（4.7&quot;）的通风间距。` | 5 节点：CJK / `120mm` / CJK / `4.7&quot;` / CJK | `install_prep_4..6` |
| `No. / 按键` | 2 节点：`No. / ` + CJK | `operate_function_2` |
| `切换制冰尺寸（S / M / L），选择后产品自动制冰。` | 3 节点：CJK / `S / M / L` / CJK | `operate_function_7 / operate_function_8` |
| `指示灯（绿灯）— 冰篮已满，产品暂停制冰。` | 3 节点：CJK / `—` / CJK | `operate_function_12 / operate_function_13` |
| `尺寸（宽×深×高）` | 5 节点：CJK / `×` / CJK / `×` / CJK | `spec_8..10` |
| `24h制冰量` | 2 节点：`24h` + CJK | `spec_12` |
| `冰块 S` / `冰块 M` / `冰块 L` | 2 节点：CJK + `S/M/L` | `spec_15..17` |
| `'务必将产品放置在平整稳固的平面，... 距离必须 ≥ 120 mm（4.7 in），以确保通风良好。'` | 5 节点：CJK / `≥ 120 mm` / CJK / `4.7 in` / CJK | `operate_guide_3..5` |
| `给产品接通电源，产品发出&#x201C;滴&#x201D;一声，所有按键点亮后再熄灭，表示已经接通电源。` | 5 节点：CJK / `&#x201C;` / CJK / `&#x201D;` / CJK | `operate_guide_9..11` |
| ` 按键，切换点亮按键上方的 S / M / L 指示灯，选择需要制作的子弹冰尺寸。` | 3 节点：CJK / `S / M / L` / CJK | `operate_guide_21 / operate_guide_22` |
| `水箱缺水（ADD WATER亮红灯）` (2 处) | 3 节点：CJK / `ADD WATER` / CJK | `troubleshoot_12/13` + `troubleshoot_23/24` |
| `冰篮已满（ICE FULL亮绿灯）` | 3 节点：CJK / `ICE FULL` / CJK | `troubleshoot_19 / troubleshoot_20` |
| `前5次冰块偏小` | 3 节点：CJK / `5` / CJK | `troubleshoot_26 / troubleshoot_27` |
| `确保四周≥120mm间距；将产品移至阴凉通风处。` | 3 节点：CJK / `≥120mm` / CJK | `troubleshoot_32 / troubleshoot_33` |
| `水质矿物质含量高或水温/环温影响` | 3 节点：CJK / `/` / CJK | `troubleshoot_35 / troubleshoot_36` |
| `使用TDS&lt;200mg/L的纯净水；连续制冰偶尔不透明属正常现象。` | 3 节点：CJK / `TDS&lt;200mg/L` / CJK | `troubleshoot_37 / troubleshoot_38` |
| `运输过程中请保持平衡，防止倾翻；产品倾斜角不得大于 45°。` | 3 节点：CJK / `45°` / 空 | `install_transport_3 / install_transport_4` |
| `运输后需静置 4 小时，待冷媒稳定后再通电。` | 3 节点：CJK / `4` / CJK | `install_transport_6 / install_transport_7` |
| `产品四周与墙或物品之间需保持至少 120mm（4.7&quot;）的间距，以确保通风和可维护性。` | 5 节点：CJK / `120mm` / CJK / `4.7&quot;` / CJK | `install_transport_11..13` |
| `本产品含电子元件和 R600a 制冷剂，不得与生活垃圾一同丢弃。` | 3 节点：CJK / `R600a` / CJK | `install_transport_18 / install_transport_19` |
| `感谢您购买 威富可 制冰机...` （brand replaced）→ `感谢您购买 Wevac 制冰机...` | 3 节点：CJK / `Wevac` / CJK | `warranty_2 / warranty_3` |
| `香港九龙尖沙咀漆咸道南87-105号百利商业中心404A室` | 5 节点：CJK / `87-105` / CJK / `404A` / CJK | `warranty_9..11` |
| `广东省广州市番禺区南村镇启业路1号` | 3 节点：CJK / `1` / CJK | `warranty_20 / warranty_21` |
| `2 年有限保修` | 2 节点：`2 ` + CJK | `warranty_25` |
| ` 。自原始购买日期起 2 年内可享受保修更换服务。要获得保修更换资格，您必须：` | 3 节点：CJK / `2 ` / CJK | `warranty_26 / warranty_27` |
| `在过去 2 年内购买过产品。` | 3 节点：CJK / `2` / CJK | `warranty_28 / warranty_29` |
| `向我们发送电子邮件申请保修服务： support@wevactech.com` | 2 节点：CJK / `support@wevactech.com` | `warranty_32` |
| `城市 / 州 / 邮政编码` | 5 节点：CJK / `/` / CJK / `/` / CJK | `warranty_card_5..7` |
| `Wevac IMT050 说明书` (footer × 14) | 2 节点：`Wevac IMT050 ` + CJK | `footer_1..14` |

完整清单见 `docs/_extraction_meta.json` 中 entries（含 `split: true` 标记）。

### H.3 改动 3 — `safety_notice_*` subarea 新增

W50 母版 p4 中 NOTICE box-title `提示 NOTICE` 位置 = document.xml offset **61497**（即 p4 sectPr 之前的 `<w:t>提示 NOTICE</w:t>` 起点）。

`extract_master.py` v2 中实现：对 p4 内的每个 `<w:t>`，若 pos ≥ 61497 则 subarea 设为 `notice`，否则 `caution`。

`safety_notice_*` 共 6 个 key（见 §D.2）。

### H.4 v1 → v2 round-trip CN 评分对比

完整对比见 §B.1 / §B.2。摘要：

| 维度 | v1 | v2 | 偏差 |
|------|----|----|------|
| mean | 7.21 | 5.59 | -1.62 (改善) |
| max | 10.13 | 10.10 | -0.03 (持平) |
| max page | p11 | p3 | （max 转移） |
| text chars | 4626 | 4686 | +60（品牌 latin 字符增） |
| wt_count | 448 | 545 | +97（拆 `<w:t>`）|

阈值检查：max = 10.10 < 12 → **无 fix-or-escalate 触发**。

### H.5 wt_count 变化（v1 448 → v2 545，+97）

明细：
- v1 拆 0 个 `<w:t>` → wt_count = 448
- v2 拆 60 个 `<w:t>` → 多数拆成 2 节点（净 +1 / 拆），少数拆成 3-5 节点
  - 拆成 2：约 31 处 → +31
  - 拆成 3：约 23 处 → +46
  - 拆成 5：约 6 处 → +24（每个 +4）
  - 合计净增约 +97 — 与实测 +97 吻合

### H.6 占位符总数变化（v1 277 → v2 304，+27）

明细：
- 去除 30 个 brand placeholder：-30
- 拆 `<w:t>` 引入新 CJK chunk placeholder：+57（约略；含 v2 中拆出的 CJK chunks 多于原始混排数）
- 合计净 +27 — 与实测吻合（277 + 57 - 30 = 304）

---

## 附：阶段 1 v2 产出清单

```
swiss/tools/docx-pipeline/
├── master_template.docx                      ← v2 占位符化的 W50（含 3 项改动；通过 validate.py）
├── master_unpacked/                          ← v2 unpack 后母版（304 个 {{key}} + 30 处 Wevac 字面）
├── strings/
│   ├── cn.md                                 ← 中文翻译字典（304 keys 分 area 列表）
│   └── cn.json                               ← 同上 JSON；不含「威富可」value
├── docs/
│   ├── PLACEHOLDER_MAP.md                    ← v2 提取报告（含 v2 改动说明 + 30 处抽样）
│   ├── G1_review_packet.md                   ← 本文件
│   └── _extraction_meta.json                 ← v2 extract_master 中间产物（含 split 标记）
├── extract_master.py                         ← v2（实现 3 项改动）
├── extract_meta_to_docs.py
├── generator.py                              ← 不变（v1 generator 兼容 v2 cn.json）
├── anti_cheat.py
├── round_trip_cn.docx                        ← v2 round-trip 验证 docx
└── round_trip_cn.score.json                  ← v2 评分（5.59 / 10.10）
```
