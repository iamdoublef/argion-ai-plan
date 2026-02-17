# 数据采集汇总 & 待采集清单

> 采集日期：2026-02-15
> 采集方式：6个并行Agent（Playwright + WebFetch + WebSearch）

---

## 一、已采集数据清单（按品牌）

### Wevac（文件：wevac-amazon.md）

| 数据项 | 值 | 来源 | 可信度 |
|--------|-----|------|--------|
| Amazon 产品数量 | 16 SKU（1台机器+15款袋/卷） | Amazon搜索页 | ✅ 高 |
| 唯一封口机 | 手持式 B0CTHS1927, $31.99, 4.2星, 97评价 | Amazon搜索页 | ✅ 高 |
| 旗舰产品 | 11x50 Rolls B07TMZDGQ1, $16.84, 4.6星, 65.6K评价 | Amazon搜索页 | ✅ 高 |
| 真空袋评分 | 全线4.6-4.7星 | Amazon搜索页 | ✅ 高 |
| 价格区间 | $9.99-$32.99（袋），$31.99（手持机） | Amazon搜索页 | ✅ 高 |
| 子品牌 | Wevac Lite（2024年推出，经济线） | Amazon搜索页 | ✅ 高 |
| 官网状态 | wevac.com 仅联系表单，无产品页 | Playwright实测 | ✅ 高 |

**关键发现：Wevac在Amazon是真空袋品牌，不是封口机品牌。之前报告的定位完全错误。**

### FoodSaver（文件：foodsaver-amazon.md）

| 数据项 | 值 | 来源 | 可信度 |
|--------|-----|------|--------|
| 官网产品数量 | 10款封口机 | foodsaver.com Playwright采集 | ✅ 高 |
| 价格区间 | $49.99-$349.99 | foodsaver.com | ✅ 高 |
| 旗舰产品 | Elite All-in-One Liquid+, $339.99, 4.3星, 277评价 | foodsaver.com | ✅ 高 |
| 最高评分 | FM2100 4.4星(873评价), Everyday 4.4星(126评价) | foodsaver.com | ✅ 高 |
| 最低评分 | VS3130 3.6星(250评价) | foodsaver.com | ✅ 高 |
| 缺货产品 | v4440, VS3130 | foodsaver.com | ✅ 高 |
| Amazon ASIN | B00LUGK5QW($139.91), B08BDHZ1PV($99.99) | Amazon搜索页 | ✅ 高 |
| 品牌口号 | "the original food vacuum sealer" | foodsaver.com | ✅ 高 |
| 母公司 | Sunbeam Products / Newell Brands | foodsaver.com | ✅ 高 |

**注意：之前报告的VS5880/VS3180/VS0100均已停产，不在当前产品线中。**

### Anova（文件：anova-amazon.md）

| 数据项 | 值 | 来源 | 可信度 |
|--------|-----|------|--------|
| 基础款 | $79.99(Amazon)/$89.00(官网), 4.2星, 2735评分/6251评价 | Amazon+官网 | ✅ 高 |
| Pro款 | $155.00(官网), Amazon数据未采集到 | 官网 | ✅ 高(官网) |
| 腔式机 | $374.00, 4.4星, 79评价 | Amazon+官网 | ✅ 高 |
| 手持式 | Amazon数据未采集到 | - | ❌ 缺失 |
| 基础款规格 | 425x122x79.7mm, 1.04kg, -0.5bar, 4L/min | 官网 | ✅ 高 |
| Pro款规格 | 400x180x108.5mm, 12L/min, 110W | 官网 | ✅ 高 |
| 保修 | 全线2年+100天退款 | 官网 | ✅ 高 |
| Wirecutter评价 | Best Overall | Google摘要 | ⚠️ 中(间接来源) |
| CNET评价 | Best for Sous Vide | CNET页面 | ✅ 高 |

### Mueller（文件：mueller-geryon-amazon.md）

| 数据项 | 值 | 来源 | 可信度 |
|--------|-----|------|--------|
| 主力款 | B07J2SR7YT, $39.99, 4.1星, 12.6K评价 | Amazon搜索页 | ✅ 高 |
| 新款 | B0C6R8QVZ8, $39.99, 3.7星, 70评价 | Amazon搜索页 | ✅ 高 |
| 便携款 | B0DCDJP9CV, $19.72, 3.1星, 33评价 | Amazon搜索页 | ✅ 高 |

### GERYON（文件：mueller-geryon-amazon.md）

| 数据项 | 值 | 来源 | 可信度 |
|--------|-----|------|--------|
| 主力款(银) | B0F8LJNDHM, $38.99, 4.3星, 30.4K评价 | Amazon搜索页 | ✅ 高 |
| 经典款(黑) | B07CXKMGTK, $37.99, 4.3星, 30.4K评价(共享) | Amazon搜索页 | ✅ 高 |
| 银色变体 | B07B4W5PMB, $41.99, 4.3星, 30.4K评价(共享) | Amazon搜索页 | ✅ 高 |
| 真空袋 | 3款, $19.99-$29.99, 4.7星, 2.1K-4.4K评价 | Amazon搜索页 | ✅ 高 |

### Nesco（文件：nesco-amazon.md）

| 数据项 | 值 | 来源 | 可信度 |
|--------|-----|------|--------|
| VS-12 Deluxe | B01KCK9W1K, $128.99, 4.3星, 14.5K评价, "Overall Pick" | Amazon搜索页 | ✅ 高 |
| VS-15 FreshLock Pro | B0DKV752SY, $89.99, 4.8星, 11评价(新品) | Amazon搜索页 | ✅ 高 |
| VS-02 | B00IUAK39A, $76.79, 4.2星, 2.3K评价 | Amazon搜索页 | ✅ 高 |
| VS-22LB Premium | B0DJRL4R8Z, $239.99, 4.6星, 113评价 | Amazon搜索页 | ✅ 高 |
| VS-01 | B00IUAK0E8, $62.99, 4.1星, 179评价 | Amazon搜索页 | ✅ 高 |
| VS-74S | B0F9X95YDL, $42.13, 3.5星, 11评价 | Amazon搜索页 | ✅ 高 |
| Preserve Plus | B0DJRN26VQ, $67.93, 4.1星, 11评价 | Amazon搜索页 | ✅ 高 |

### 行业市场数据（文件：market-and-reviews.md）

| 数据项 | 值 | 来源 | 可信度 |
|--------|-----|------|--------|
| 全球真空包装市场(2015) | $15.0B | TMR报告摘要 | ✅ 高 |
| 全球真空包装市场(2024预测) | $22.8B | TMR报告摘要 | ⚠️ 中(预测值) |
| CAGR | 4-5% | TMR/GVR/M&M三源交叉 | ✅ 高 |
| Newell H&CS部门FY2025营收 | $3.772B, -7.3% YoY | Newell IR官方 | ✅ 高 |
| Newell H&CS营业利润 | $252M (6.7%) | Newell IR官方 | ✅ 高 |
| Wirecutter Best Overall | Anova Pro, $119 | Google摘要 | ⚠️ 中 |
| CNET Best Overall | Nesco VS-12 | CNET页面 | ✅ 高 |
| Anova YouTube | 1.46万订阅, 195视频, 1391万总观看 | YouTube页面 | ✅ 高 |

---

## 二、待采集清单（未能获取的关键数据）

### 优先级 P0（影响核心分析结论）

| # | 数据项 | 原因 | 建议采集方式 |
|---|--------|------|-------------|
| 1 | Wevac 台式封口机是否存在 | Amazon上只有手持式，需确认Argion是否通过Wevac品牌卖过台式机 | **需客户确认**：Wevac品牌下是否有/曾有台式真空封口机在Amazon销售？ |
| 2 | Anova Pro Amazon价格/评分/评价数 | Amazon反爬重定向 | 手动访问 amazon.com/dp/B08F8SMSC4 |
| 3 | FoodSaver Amazon评分/评价数（当前在售款） | Amazon反爬，官网评价数偏少 | 手动访问Amazon搜索"FoodSaver vacuum sealer"记录前5款的评分和评价数 |
| 4 | Wevac真空袋 Best Seller Rank | 判断品类排名 | 手动访问 amazon.com/dp/B07TMZDGQ1 查看BSR |

### 优先级 P1（补充分析深度）

| # | 数据项 | 原因 | 建议采集方式 |
|---|--------|------|-------------|
| 5 | FoodSaver产品详细规格（真空强度、功率、泵类型） | 官网详情页未能加载 | 手动访问foodsaver.com各产品详情页 |
| 6 | Nesco VS-12详细规格 | Amazon详情页被重定向 | 手动访问 amazon.com/dp/B01KCK9W1K |
| 7 | Instagram粉丝数（FoodSaver、Anova、Wevac） | 平台动态渲染限制 | 手动打开Instagram App查看 |
| 8 | Facebook粉丝数（FoodSaver、Anova） | 平台封锁 | 手动打开Facebook查看 |
| 9 | Wirecutter完整推荐列表（3款） | 仅获取Google摘要 | 手动访问 nytimes.com/wirecutter/reviews/best-vacuum-sealer/ |
| 10 | Amazon "vacuum sealer" 搜索结果Top 20排名 | 判断各品牌搜索可见度 | 手动搜索并截图 |

### 优先级 P2（锦上添花）

| # | 数据项 | 原因 | 建议采集方式 |
|---|--------|------|-------------|
| 11 | 家用真空封口机细分市场规模 | 需付费报告 | 购买GVR/TMR报告，或标注为"无公开数据" |
| 12 | FoodSaver品牌独立营收 | Newell未单独披露 | 标注为"无公开数据，仅知H&CS部门$3.772B" |
| 13 | Sous vide市场规模 | 报告页面不可用 | 购买报告或标注为"无公开数据" |
| 14 | 各品牌Amazon广告投放数据 | 非公开数据 | 需第三方工具（Jungle Scout/Helium 10） |
| 15 | 各品牌月销量估算 | Amazon不公开 | 需第三方工具（Jungle Scout/Helium 10） |

---

## 三、之前报告中需要纠正的错误数据

| # | 错误内容 | 正确数据 | 来源 |
|---|---------|---------|------|
| 1 | "Wevac是封口机品牌，价格$55-90" | Wevac在Amazon主要卖真空袋，唯一封口机是手持式$31.99 | wevac-amazon.md |
| 2 | "FoodSaver VS5880旗舰$179.99" | VS5880已停产，当前旗舰是Elite Liquid+ $339.99 | foodsaver-amazon.md |
| 3 | "FoodSaver VS3180紧凑款$79.99" | VS3180已停产，最接近的是VS3130 $199.99(缺货) | foodsaver-amazon.md |
| 4 | "Mueller评价25K+" | Mueller主力款B07J2SR7YT实际12.6K评价 | mueller-geryon-amazon.md |
| 5 | "GERYON评价18K+" | GERYON实际30.4K评价(共享评价池) | mueller-geryon-amazon.md |
| 6 | "Nesco VS-12评价12K+, $89.99" | 实际14.5K评价, $128.99 | nesco-amazon.md |
| 7 | "Anova Pro Amazon $119.99" | Amazon数据未采集到，官网$155.00 | anova-amazon.md |
| 8 | "Wevac评分4.5-4.7" | 这是真空袋的评分，唯一封口机评分4.2 | wevac-amazon.md |
| 9 | "FoodSaver市占率35-45%" | 无公开精确数据，仅知被广泛认为是市场领导者 | market-and-reviews.md |
| 10 | "FoodSaver评价8K-80K+" | 官网最高873评价(FM2100)，Amazon数据未完整采集 | foodsaver-amazon.md |

---

## 四、数据采集方法论说明

### 采集工具限制
- **Amazon反爬**：搜索结果页可提取基础数据（名称/价格/评分/评价数），但产品详情页频繁被重定向
- **Instagram/Facebook**：动态渲染+平台封锁，自动化工具无法采集粉丝数
- **付费报告**：市场规模细分数据需购买GVR/TMR/M&M报告（$3000-$5000/份）

### 数据可信度分级
- ✅ 高：直接从一手来源（品牌官网、Amazon搜索页）采集的精确数值
- ⚠️ 中：间接来源（Google摘要、评测文章引用）或预测值
- ❌ 缺失：未能采集到，需手动补充或标注为"无公开数据"
