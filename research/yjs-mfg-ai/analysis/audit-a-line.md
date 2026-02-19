# A线审计报告（5场景）

> 审计日期：2026-02-17（第二轮审计，基于v2数据文件）
> 审计员：research-auditor
> 审计对象：a1-film-inspection.md, a2-blown-film-optimization.md, a3-production-scheduling.md, a4-biodegradable-formulation.md, a5-fba-demand-forecast.md
> 交叉比对源：d0-research-brief.md
> 审计方法：URL curl验证 + ROI数学验算 + 跨文件一致性 + 结构完整性 + 估算值标注检查

## 审计摘要

| 指标 | 数量 |
|------|------|
| ERROR（必须修复） | 2 |
| WARNING（建议修复） | 12 |

| 场景 | 评级 | ERROR | WARNING | 说明 |
|------|------|-------|---------|------|
| A1 薄膜质检 | A | 0 | 2 | URL小问题已在文件中标注，ROI三情景计算自洽 |
| A2 吹膜工艺优化 | **C** | **2** | 1 | 先导线和全面推广回收期计算均有错误 |
| A3 排产优化 | A | 0 | 2 | 无精确ROI（已诚实声明数据不足），1个URL超时 |
| A4 配方优化 | B | 0 | 4 | ROI回收期上限偏差，多处数据来源薄弱 |
| A5 需求预测 | A | 0 | 3 | ROI计算自洽，不可达URL均已标注 |

**vs 第一轮审计对比**：v2数据文件修复了第一轮的8个ERROR（URL批量失效、案例空白、ROI计算错误等），本轮新发现2个ERROR（A2回收期计算）和12个WARNING。整体质量显著提升。

---

## A1: 薄膜质检AI

### URL验证（11个URL）

| URL | 文件声称 | 实测(2026-02-17) | 判定 |
|-----|---------|------------------|------|
| isravision.com/en-en/products/plastic-film-foil-sheets | 200 | 200 | PASS |
| bst.elexis.group/en/solutions/surface-inspection/ipq-surface | 200 | 200 | PASS |
| cognex.com/ | 429（已标注） | 429 | PASS |
| keyence.com/ | 200 | 503 | **WARNING** |
| wh.group/ | 200 | 301->200 | PASS |
| lusterinc.com/...软包检测/ | 200 | 200 | PASS |
| daheng-imaging.com/ | 200 | 200 | PASS |
| hexagon.com/ | 403（已标注） | 403 | PASS |
| paddlepaddle.org.cn/ | 200 | 200 | PASS |
| isravision.com/en-en/industries/plastic-film-foil-sheets | -- | 200 | PASS |
| bst.elexis.group/en/industries/film-extrusion | -- | 200 | PASS |

### ROI验算

| 情景 | 投入 | 年收益 | 文件回收期 | 验算 | 判定 |
|------|------|--------|-----------|------|------|
| 最优 | 550万 | 770万 | 0.7年 | 550/770=0.71 | PASS |
| 中间 | 900万 | 530万 | 1.7年 | 900/530=1.70 | PASS |
| 最差 | 1,270万 | 290万 | 4.4年 | 1270/290=4.38 | PASS |

### 问题清单

| # | 级别 | 问题 | 位置 |
|---|------|------|------|
| 1 | WARNING | Keyence官网实测503，文件声称200 | 供应商表 |
| 2 | WARNING | 人工漏检率5-15%无具体来源URL，仅标注行业 | 痛点 |

### 完整性：通过 / 估算标注：通过 / 评级：A

---

## A2: 吹膜工艺参数AI优化

### URL验证（13个URL）

| URL | 文件声称 | 实测(2026-02-17) | 判定 |
|-----|---------|------------------|------|
| wh.group/int/en/.../blown_film_lines/ | 200 | 200 | PASS |
| wh.group/int/en/.../automation_assistance/ | 200 | 200 | PASS |
| wh.group/int/en/.../reduce_material_waste/ | 200 | 200 | PASS |
| reifenhauser.com/.../blown-film-lines/ | 200 | 200 | PASS |
| reifenhauser.com/.../evo-fusion | 200 | 200 | PASS |
| reifenhauser.com/.../blown-film-extrusion-enhancing-conversion | 200 | 200 | PASS |
| doi.org/10.1016/j.applthermaleng.2014.04.036 | 200 | 302->200 | PASS |
| hammer-ims.com/ | 200 | 200 | PASS |
| hammer-ims.com/news/westlake-plastics... | 200 | 200 | PASS |
| hammer-ims.com/news/federal-eco-foam... | 200 | 200 | PASS |
| sightmachine.com/ | 200 | 200 | PASS |
| corporate.davis-standard.com/ | 200 | 200 | PASS |
| jinming.com/ | 200 | 200 | PASS |

### ROI验算

**先导线（2-3条线）：**

- 年收益加法：(15-40)+(10-30)+(5-15) = 30-85万 -- 正确
- 回收期验算：

| 情景 | 投入 | 年收益 | 回收期 |
|------|------|--------|--------|
| 最优 | 100万 | 85万 | 100/85=**1.18年** |
| 最差 | 250万 | 30万 | 250/30=**8.33年** |

文件声称1.5-3.5年。最优应为1.18年（非1.5），最差应为8.33年（非3.5）。**ERROR**。

**全面推广（24条线）：**

- 年收益加法：(150-400)+(100-300)+(50-100) = 300-800万 -- 正确
- 回收期验算：

| 情景 | 投入 | 年收益 | 回收期 |
|------|------|--------|--------|
| 最优 | 500万 | 800万 | 500/800=**0.63年** |
| 最差 | 1200万 | 300万 | 1200/300=**4.0年** |

文件声称1-2.5年。最差应为4.0年（非2.5）。**ERROR**。

### 问题清单

| # | 级别 | 问题 | 位置 |
|---|------|------|------|
| 1 | **ERROR** | 先导线回收期声称1.5-3.5年，实为1.18-8.33年 | ROI-先导线 |
| 2 | **ERROR** | 全面推广回收期声称1-2.5年，实为0.63-4.0年 | ROI-全面推广 |
| 3 | WARNING | A1提到吹膜线速度100-200m/min，A2未引用此数据 | 跨文件 |

### 完整性：通过 / 估算标注：通过 / 评级：C（2 ERROR）

---

## A3: 排产优化AI

### URL验证（18个URL）

| URL | 文件声称 | 实测(2026-02-17) | 判定 |
|-----|---------|------------------|------|
| oee.com/world-class-oee/ | 200 | 200 | PASS |
| siemens.com/en-us/products/opcenter/ | 200 | 200 | PASS |
| 3ds.com/products/delmia/ortems | 200 | 200 | PASS |
| asprova.com/ | 200 | 200 | PASS |
| asprova.com/en/case-studies-sort-by-productss-name.html | 200 | 200 | PASS |
| asprova.com/.../case_study_20_panasonic... | 200 | 200 | PASS |
| asprova.com/.../case_study_15_bridgestone... | 200 | 200 | PASS |
| planettogether.com/ | 200 | 200 | PASS |
| andafa.com/ | 200 | 200 | PASS |
| andafa.com/product/aps/aps_index-flm.html | 200 | 200 | PASS |
| andafa.com/kehuanli/kehuanli_index-flm.html | 200 | 200 | PASS |
| blacklake.cn/ | 200 | 200 | PASS |
| shanshu.ai/ | 200 | 200 | PASS |
| flexciton.com/ | 200 | 200 | PASS |
| flexciton.com/about-us | 200 | 200 | PASS |
| flexciton.com/resources/seagate-case-study-2-0 | 200 | 200 | PASS |
| flexciton.com/resources/renesas-electronics-case-study | 200 | 200 | PASS |
| developers.google.com/optimization | -- | 超时(000) | **WARNING** |

### ROI验算

文件明确声明数据不足，暂无法给出精确的ROI计算，仅引用Panasonic案例（排产工时减少75%、提前期缩短50%）作为参考。无自行计算的数字，无需验算。处理方式诚实合理。

### 问题清单

| # | 级别 | 问题 | 位置 |
|---|------|------|------|
| 1 | WARNING | Google OR-Tools URL超时不可达，建议替换为github.com/google/or-tools | 3.3 |
| 2 | WARNING | 投入和ROI均无具体数字，决策支撑力偏弱（但已诚实标注） | 5.2-5.3 |

### 完整性：通过 / 估算标注：通过 / 评级：A

---

## A4: 可降解材料配方AI优化

### URL验证（15个URL，含2个已标注失效）

| URL | 文件声称 | 实测(2026-02-17) | 判定 |
|-----|---------|------------------|------|
| european-bioplastics.org/.../standards-certifications-and-labels/ | 200 | 200 | PASS |
| citrine.io/ | 200 | 200 | PASS |
| citrine.io/resources/case-studies/ | 200 | 200 | PASS |
| citrine.io/who-we-help/plastics/ | 200 | 200 | PASS |
| citrine.io/who-we-help/packaging/ | 200 | 200 | PASS |
| citrine.io/why-citrine/ | 200 | 200 | PASS |
| uncountable.com/ | 200 | 200 | PASS |
| uncountable.com/case-studies | 200 | 200 | PASS |
| botorch.org/ | 200 | 200 | PASS |
| nature.com/articles/s41578-022-00490-5 | 200 | 303(auth) | PASS |
| nature.com/articles/s41524-020-00429-w | 200 | 303(auth) | PASS |
| kingfa.com/ | 200 | 200 | PASS |
| sciencedirect.com/.../S0032386122008199 | 403（已标注） | 403 | PASS |
| ~~citrine.io/success-stories/~~ | 404（已标注删除） | -- | PASS |
| ~~tuv-at.be/.../ok-compost-industrial/~~ | 404（已标注删除） | -- | PASS |

### ROI验算

| 项目 | 文件数值 | 验算 | 判定 |
|------|---------|------|------|
| 年原料采购额 | 3000-6000万 | 24x(150-300)=3600-7200万，保守取3000-6000万 | PASS |
| 原料节省5% | 150万 | 3000x5%=150万 | PASS |
| 保守年节省 | 230万 | 150+80=230万 | PASS |
| 首年投入(方案A) | 95-220万 | (60-150)+(20-40)+(15-30)=95-220万 | PASS |
| 回收期 | 6-18个月 | 最优=95/230=0.41年约5月，最差=220/230=0.96年约12月 | **WARNING** |

问题：文件声称回收期上限18个月，但按文件自身数字最差为约12个月。18个月需假设实施期间无收益，但文件未说明此假设。

### 问题清单

| # | 级别 | 问题 | 位置 |
|---|------|------|------|
| 1 | WARNING | 回收期上限18个月无法从文件数字推导（最差应为约12个月） | 5.4 |
| 2 | WARNING | ML配方优化可节省原料成本5-15%无单一可验证来源 | 5.1 |
| 3 | WARNING | Citrine定价100K-300K美元/年、Uncountable 50K-200K美元/年均为估算，无官方定价页 | 2.3 |
| 4 | WARNING | Nature论文URL返回303重定向（Nature常见行为，不影响论文存在性） | 3, 6.3 |

### 完整性：通过 / 估算标注：通过 / 评级：B（0 ERROR，4 WARNING）

---

## A5: Amazon FBA需求预测AI

### URL验证（16个URL）

| URL | 文件声称 | 实测(2026-02-17) | 判定 |
|-----|---------|------------------|------|
| sell.amazon.com/fulfillment-by-amazon | 200 | 200 | PASS |
| sellercentral.amazon.com/.../G200285580 | 302（已标注） | 302 | PASS |
| sostocked.com/ | 200 | 200 | PASS |
| inventory-planner.com/ | 200 | 200 | PASS |
| ecomengine.com/restockpro | 200 | 200 | PASS |
| flieber.com/ | 200 | 200 | PASS |
| junglescout.com/pricing/ | 200 | 200 | PASS |
| helium10.com/pricing/ | 200 | 200 | PASS |
| sellerboard.com/ | 200 | 200 | PASS |
| aws.amazon.com/forecast/ | 200 | 200 | PASS |
| docs.aws.amazon.com/forecast/...what-is-forecast.html | 200 | 200 | PASS |
| lokad.com/ | 200 | 200 | PASS |
| arxiv.org/abs/1704.04110 | 200 | 200 | PASS |
| mckinsey.com/.../supply-chain-4-0 | 超时（已标注） | 超时(000) | PASS |
| gartner.com/.../demand-planning | 403（已标注） | 403 | PASS |
| facebook.github.io/prophet/ | -- | 200 | PASS |

### ROI验算

| 项目 | 文件数值 | 验算 | 判定 |
|------|---------|------|------|
| 保守库存成本 | 400K美元 | 5Mx8%=400K | PASS |
| 乐观库存成本 | 1.2M美元 | 10Mx12%=1.2M | PASS |
| 保守AI节省 | 80K美元 | 400Kx20%=80K | PASS |
| 乐观AI节省 | 360K美元 | 1.2Mx30%=360K | PASS |
| 保守净收益 | 74K美元 | 80K-6K=74K | PASS |
| 乐观净收益 | 354K美元 | 360K-6K=354K | PASS |
| 保守ROI | 12x | 74K/6K=12.3约12x | PASS |
| 乐观ROI | 59x | 354K/6K=59x | PASS |

### 问题清单

| # | 级别 | 问题 | 位置 |
|---|------|------|------|
| 1 | WARNING | Wevac年销售额5M-10M美元推断链较长，误差可能较大 | 5.3 |
| 2 | WARNING | McKinsey报告URL超时不可达，仅以标题+年份溯源 | 3.2, 4.1 |
| 3 | WARNING | FBA费率标注为2025年费率表，2026年可能已调整 | 4.2 |

### 完整性：通过 / 估算标注：通过 / 评级：A

---

## 跨文件一致性检查

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 产线数量24条（佛山16+新加坡8） | A1/A2/A3/A4/A5全部一致 |
| 2 | OK Compost+BPI双认证 | A1/A2/A3/A4一致 |
| 3 | 生产流程（原料配混-吹膜-印刷-制袋-质检-包装） | A1/A2/A3一致 |
| 4 | Amazon评价数65,600条 | A5与d0一致 |
| 5 | 技术成熟度梯度（A5=4.5 > A1=4 = A3=4 > A2=3.5 = A4=3.5） | 合理 |
| 6 | A3声明与A1/A2/A5的协同关系 | 逻辑合理 |
| 7 | A2可降解材料描述 vs A4详细展开 | 互补无矛盾 |

未发现跨文件数据矛盾。

---

## 修复建议

### 必须修复（ERROR）

1. **A2 先导线回收期**：将1.5-3.5年修正为三情景表（最优1.2年/中间3.0年/最差8.3年），与A1处理方式保持一致
2. **A2 全面推广回收期**：将1-2.5年修正为三情景表（最优0.6年/中间1.4年/最差4.0年）

### 建议修复（WARNING）

3. A1 Keyence URL：标注实测503，或更换为具体产品页
4. A3 Google OR-Tools URL：替换为 github.com/google/or-tools
5. A4 回收期上限：将6-18个月修正为5-12个月，或说明18个月含过渡期
6. A4 Citrine/Uncountable定价：标注为需向供应商确认
7. A5 FBA费率：标注需查阅2026年最新Seller Central公告
