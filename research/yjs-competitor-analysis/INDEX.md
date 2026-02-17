# 竞品分析：真空封口设备与耗材市场

> 项目状态：✅ 完成（POC，2026-02-16）
> 分析框架：三层递进（特性矩阵 + 价值曲线 + 数字化竞争力）
> 数据基础：Amazon实采 + 品牌官网 + 权威评测
> 数据审计：B+级（0 ERROR / 3 WARNING / 4 INFO）
> 分析审计：A级（3 ERROR已修 / 7 WARNING已修4个 / 5 INFO）
> 局限性：数据源单一（Amazon为主）、评分主观、建议未验证（详见主报告末尾）

## 核心结论
- Wevac在耗材赛道是头部玩家（旗舰65.6K评价，BSR#3）
- Vesta Precision在封口机赛道存在感极弱（旗舰67评价，不在Amazon搜索Top 20）
- "制造巨人，品牌婴儿"需分赛道修正：耗材=品牌巨人，封口机=品牌婴儿

## 文件索引

### 方法论
- methodology/framework-research.md — 分析框架研究
- methodology/analysis-dimensions.md — 分析维度体系

### 数据文件
- data/argion-products.md — Argion制造能力 + Wevac/Vesta双品牌数据
- data/competitor-1-foodsaver.md — FoodSaver（市场领导者）
- data/competitor-2-anova.md — Anova（智能化标杆）
- data/competitor-3-nesco.md — Nesco（评测之王）
- data/competitor-4-mueller.md — MuellerLiving（性价比品牌）
- data/competitor-5-geryon.md — GERYON（评价数之王）
- data/market-data.md — 市场规模、财报、评测推荐、Amazon搜索排名

### 原始数据（19个文件）
- data/_raw/ — Amazon实采、品牌验证、产品规格等原始数据（15个初始文件）
- data/_raw/mueller-specs-supplement.md — Mueller技术规格+保修+功能补采
- data/_raw/geryon-specs-supplement.md — GERYON技术规格+功能补采（110W/2.2lbs/E2900M）
- data/_raw/vesta-specs-supplement.md — Vesta V22/V23/Pro II技术规格补采
- data/_raw/review-keywords-supplement.md — 6品牌Amazon用户评价关键词补采

### 分析报告
- analysis/competitive-analysis-report.md — 竞品分析主报告（三层递进框架，v2重写+审计修复 2026-02-16）
- analysis/gap-analysis.md — 差距分析（v2，双赛道框架+7个战略机会 2026-02-16）
- analysis/recommendations.md — 战略建议（v2，P0/P1/P2行动矩阵 2026-02-16）

### 审计报告
- analysis/stage1-audit.md — 阶段1数据合并审计（PASS）
- analysis/stage2-audit.md — 阶段2分析报告审计
- analysis/final-audit.md — 最终审计
- analysis/data-completeness-audit.md — 数据完整性审计v1（B级，2 ERROR / 9 WARNING）
- analysis/data-completeness-audit-v2.md — 数据完整性审计v2（B+级，0 ERROR / 3 WARNING）
- analysis/stage6-analysis-audit.md — 分析报告审计（B级→修复后A级，3 ERROR / 7 WARNING / 5 INFO）

### 可视化
- dashboard/competitor-intelligence-dashboard.html — 交互式仪表盘v2（6 Tab，含用户评价分析 2026-02-16）

### 过程记录
- research-log.md — 研究过程日志
