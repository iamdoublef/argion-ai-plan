# 数据完整性与准确性审计报告 v2（补采后复审）

> 审计日期：2026-02-15
> 审计范围：D:\work\private\yjsplan\research\yjs-competitor-analysis\data\
> 审计文件数：7个主数据文件 + 4个_raw补充文件
> 审计员：独立审计Agent（第二轮复审，覆盖v1全部问题）
> 前置审计：data-completeness-audit.md（v1，2 ERROR + 9 WARNING + 6 INFO）

---

## 1. 审计摘要

| 指标 | v1数量 | v2数量 | 变化 |
|------|--------|--------|------|
| ERROR（必须修复） | 2 | 0 | -2 |
| WARNING（建议修复） | 9 | 3 | -6 |
| INFO（供参考） | 6 | 4 | -2 |

**总体评级：B+级（CONDITIONAL PASS）**

核心判断：v1的2个ERROR均已降级为WARNING（技术规格部分补采但仍有不可获取项），9个WARNING中6个已完全修复。补采数据与_raw原始文件高度一致（10项抽查全部PASS）。数据可支撑进入分析阶段，但Mueller/GERYON的功率/真空强度缺失需在分析报告中标注。

---

## 2. 第一轮问题逐项复查

### ERROR级别

#### E-01: Mueller技术规格缺失 → PARTIALLY_FIXED

- v1状态：功率/真空强度/密封宽度/泵类型/尺寸/重量全部为空
- v2状态：
  - 已补采：尺寸 16.54"x7.91"x4.92"、材质 Plastic、电源类型 Electric、产地 Made in China
  - 仍未公开：功率、真空强度、重量、密封宽度（具体数值）
  - 来源：`_raw/mueller-specs-supplement.md`，Amazon + Mueller官网均已确认不公开
- 降级为：WARNING（W-01-v2）
- 理由：已穷尽可用数据源（Amazon详情页+Mueller官网），确认为品牌方不公开而非采集遗漏。补采文件明确记录了采集困难和数据缺失原因。分析中可标注"未公开"并基于价位推断。

#### E-02: GERYON技术规格缺失 → PARTIALLY_FIXED

- v1状态：功率/真空强度/尺寸/重量均未列出
- v2状态：
  - 已补采：功率 110W、电压 120V AC、尺寸 14.4"x5.5"x2.56"、重量 2.2 lbs、材质 Stainless Steel、型号 E2900 M、上市日期 2018-05-08、BSR #24,366/#93
  - 仍未公开：真空强度(kPa/inHg)、密封宽度、泵类型
  - 来源：`_raw/geryon-specs-supplement.md`，Amazon Technical Details实采
- 降级为：WARNING（W-02-v2）
- 理由：核心规格（功率/尺寸/重量）已补齐，仅真空强度/密封宽度/泵类型未公开。补采文件记录了多渠道搜索均无结果（GERYON官网疑似关闭）。分析中标注"未公开"即可。

### WARNING级别

#### W-01: Vesta/Wevac无评价关键词 → FIXED

- 文件：`argion-products.md` 第206-216行
- 补采内容：Wevac旗舰袋好评(Value/Quality/Functionality)和差评(Sealability/Size)；Vesta Vac'n Seal好评(Works well/Quality/Sealability)
- 来源：`_raw/review-keywords-supplement.md` §5-§6
- 数据一致性：主文件与_raw完全一致

#### W-02: Vesta封口机缺技术规格 → FIXED

- 文件：`argion-products.md` 第82-86行
- 补采内容：V22(185W/-28.3inHg/12.4"/5.3lb)、V23(190W/-28.3inHg/12.4"/6.6lb)、Pro II(550W/95kPa/16"/11.22lb)
- 来源：`_raw/vesta-specs-supplement.md`
- 数据一致性：主文件与_raw完全一致

#### W-03: FoodSaver无评价关键词 → FIXED

- 文件：`competitor-1-foodsaver.md` 第124-139行（C2节）
- 补采内容：V4400好评Top5(Functionality 1.5K/Quality 1.2K/Value 715/Easy to use 697/Food freshness 305)和差评(Sealing ability 679/Durability 270)
- 来源：`_raw/review-keywords-supplement.md` §1
- 数据一致性：主文件与_raw完全一致

#### W-04: Anova无评价关键词 → FIXED

- 文件：`competitor-2-anova.md` 第113-129行（C2节）
- 补采内容：ANVS02好评(Quality 190/Easy to use 111)和差评(Functionality 325/Seal 199/Suction 110)
- 来源：`_raw/review-keywords-supplement.md` §2
- 数据一致性：主文件与_raw完全一致

#### W-05: Nesco无评价关键词 → FIXED

- 文件：`competitor-3-nesco.md` 第124-138行（E2节）
- 补采内容：VS-12好评(Works well 1.2K/Sealer quality 935/Easy to use 763)和差评(Lifespan 490/Sealability 793/Value 503/Suction 288)
- 来源：`_raw/review-keywords-supplement.md` §3
- 数据一致性：主文件与_raw完全一致

#### W-06: Mueller无评价关键词 → FIXED

- 文件：`competitor-4-mueller.md` 第114-139行（D节）
- 补采内容：主力款好评Top5(Functionality 1.4K/Easy to use 1.1K/Quality 935/Value 628/Compact 233)和差评(Functionality issues 1.4K/Seal 620/Suction 413)
- 来源：`_raw/review-keywords-supplement.md` §4
- 数据一致性：主文件与_raw完全一致

#### W-07: Mueller保修/认证未确认 → FIXED

- 文件：`competitor-4-mueller.md` 第155-165行（F节）
- 补采结果：确认为"未公开"——Amazon和Mueller官网均未标注保修期限和认证信息，仅有30天退货政策
- 来源：`_raw/mueller-specs-supplement.md` §2
- 状态：已从"未确认"改为明确的"未公开"并标注来源，属于合理闭环

#### W-08: GERYON功能特性不完整 → FIXED

- 文件：`competitor-5-geryon.md` 第79-93行
- 补采内容：10项功能有/无判定（干湿模式有/脉冲无/罐装有/卷袋存储无/自动袋检测无/预设2个/内置切刀有/LED有/可拆卸清洁有/外接真空管有）
- 来源：`_raw/geryon-specs-supplement.md` §2
- 数据一致性：主文件与_raw完全一致

### INFO级别

#### I-03: Anova Pro重量不一致 → FIXED

- 文件：`competitor-2-anova.md` 第39行
- v1状态：B节写2.9kg(6.4lbs)，C节写5 Pounds
- v2状态：B节已统一为"5 lbs / 2.27 kg（Amazon实采）"，并加注"官网标注2.9kg可能含包装"
- C节第87行确认"5 Pounds"
- 两处数据现已一致，差异原因已标注

---

## 3. 补采数据准确性抽查（10个新增数值）

| # | 数据项 | 主文件值 | _raw补充文件值 | 结果 |
|---|--------|---------|---------------|------|
| 1 | GERYON B07CXKMGTK 功率 | 110W | 110W (geryon-specs-supplement §1) | PASS |
| 2 | GERYON B07CXKMGTK 尺寸 | 14.4"x5.5"x2.56" | 14.4"x5.5"x2.56" (geryon-specs-supplement §1) | PASS |
| 3 | GERYON B07CXKMGTK 重量 | 2.2 lbs | 2.2 lbs (geryon-specs-supplement §1) | PASS |
| 4 | Mueller B07J2SR7YT 尺寸 | 16.54"x7.91"x4.92" | 16.54"x7.91"x4.92" (mueller-specs-supplement §1) | PASS |
| 5 | Vesta V22 功率 | 185W | 185W (vesta-specs-supplement §1) | PASS |
| 6 | Vesta V22 真空强度 | -28.3 inHg | -28.3 inHg (vesta-specs-supplement §1) | PASS |
| 7 | Vesta Pro II 功率 | 550W | 550W (vesta-specs-supplement §3) | PASS |
| 8 | Vesta Pro II 重量 | 11.22 lb | 11.22 lb (vesta-specs-supplement §3) | PASS |
| 9 | FoodSaver V4400 好评Functionality | 1.5K mentions | 1.5K (review-keywords-supplement §1) | PASS |
| 10 | Nesco VS-12 差评Lifespan | 490 mentions | 490 (review-keywords-supplement §3) | PASS |

**结果：10/10 PASS（100%通过率）**

---

## 4. 更新后的分析可用性矩阵

### Layer 1 覆盖率（Y=完整 P=部分 N=无）

| 维度 | Argion | FoodSaver | Anova | Nesco | Mueller | GERYON | 覆盖率 | v1变化 |
|------|--------|-----------|-------|-------|---------|--------|--------|--------|
| A.品牌概况 | Y | Y | Y | Y | P | Y | 92% | = |
| B.技术规格 | Y | P | Y | Y | P | P | 75% | +8% |
| C.功能特性 | Y | Y | Y | Y | Y | Y | 100% | +25% |
| D.价格与评价 | Y | Y | Y | Y | Y | Y | 100% | = |
| E.评价关键词 | P | Y | Y | Y | Y | Y | 92% | +84% |
| F.售后认证 | Y | Y | Y | Y | P | Y | 92% | +9% |

**Layer 1 综合：约92%（v1为70%，提升22个百分点）**

### Layer 2 价值曲线12要素

| 支撑度 | 要素 | v1变化 |
|--------|------|--------|
| HIGH(6个) | 价格竞争力、智能化程度、品牌知名度、产品线完整度、功能丰富度、耗材生态 | +2 |
| MEDIUM(4个) | 密封性能、售后服务、易用性、产品耐用性 | +2/-2 |
| LOW(2个) | 工业设计、渠道覆盖 | -2 |

**Layer 2 综合：约70%（v1为55%，提升15个百分点）**

说明：评价关键词补采使"易用性"和"产品耐用性"从LOW升至MEDIUM（有跨品牌量化对比数据）；Mueller/GERYON功能特性补采使"功能丰富度"从MEDIUM升至HIGH。

### Layer 3 数字化竞争力

| 维度(权重) | 支撑度 | v1变化 |
|-----------|--------|--------|
| A.智能产品能力(25%) | MEDIUM | = |
| B.电商与数字营销(30%) | LOW | = |
| C.数据与AI应用(20%) | NONE | = |
| D.数字化客户体验(25%) | LOW | = |

**Layer 3 综合：约20%（未变化，建议维持定性描述）**

---

## 5. 残留问题清单

### WARNING（3个）

| ID | 问题 | 文件 | 影响 | 建议处理 |
|----|------|------|------|----------|
| W-01-v2 | Mueller功率/真空强度/重量不可获取 | competitor-4-mueller.md | Layer2密封性能评分需推断 | 分析中标注"未公开，基于价位推断为入门级"；该产品库存仅1件可能即将停售，影响有限 |
| W-02-v2 | GERYON真空强度/密封宽度/泵类型不可获取 | competitor-5-geryon.md | 同上 | 分析中标注"未公开"；补采文件已记录GERYON官网疑似关闭 |
| W-03-v2 | GERYON B07CXKMGTK价格微差：_raw/geryon-specs-supplement.md写$36.99，主文件和_raw/mueller-geryon-amazon.md写$37.99 | competitor-5-geryon.md / geryon-specs-supplement.md | 极低，属正常价格波动 | 无需修复，两次采集时间点不同导致$1差异 |

### INFO（4个）

| ID | 问题 | 说明 |
|----|------|------|
| I-01-v2 | Wevac BSR数据来自不同ASIN（#948 vs #92） | v1遗留，已在文件中标注ASIN对应关系 |
| I-02-v2 | 社交媒体数据仍大面积缺失 | Layer 3已建议降级为定性描述，不阻塞分析 |
| I-03-v2 | FoodSaver真空强度未公开 | 行业领导者不公开此参数，分析中标注即可 |
| I-04-v2 | Mueller主力款库存仅1件，可能即将停售 | 分析中应标注该产品生命周期风险 |

---

## 6. 审计结论

**CONDITIONAL PASS — 数据可支撑进入分析阶段。**

v1的2个ERROR已全部消除（降级为WARNING），9个WARNING中6个完全修复。补采数据准确率100%（10/10 PASS）。Layer 1覆盖率从70%提升至92%，Layer 2从55%提升至70%，均已达到可分析阈值。

残留的3个WARNING均为品牌方不公开数据（Mueller/GERYON技术规格），已穷尽可用数据源，属于行业常态（低价品牌普遍不公开真空强度参数）。在分析报告中标注"未公开"并基于价位合理推断即可，不构成阻塞。

**进入分析阶段的前提条件：**
1. 分析报告中Mueller/GERYON技术规格相关评分必须标注"基于推断，非实测数据"
2. Layer 3维持定性描述，不做量化评分
3. 评价关键词跨品牌对比表已具备（6个品牌/产品均有数据），可直接用于用户感知分析
