# Argion（亚俊氏）全线产品与品牌数据

> 数据来源：argiontechnology.com 官网、vestaprecision.com 官网、Amazon产品页
> 采集日期：2026-02-15
> 合并自：原 argion-products.md + `_raw/brand-positioning.md` + `_raw/vesta-amazon.md` + `_raw/wevac-amazon.md` + `_raw/argion-brands-verification.md`

---

## 品牌关系树

```
Guangzhou Argion Electric Appliance Co., Ltd. (广州亚俊氏真空科技股份有限公司)
├── 制造实体: ODM/OEM 制造商 (argiontechnology.com)
├── 美国运营实体: Precision Appliance Technology, Inc. (PAT), Seattle
├── 消费品牌 1: Wevac
│   ├── 定位: 耗材品牌（真空袋为核心，B2B/Amazon渠道）
│   ├── Tagline: "Waste Less, Enjoy More"
│   ├── 官网: wevac.com（仅B2B联系表单，无DTC商城）
│   ├── Amazon Store: 57个产品
│   ├── 价格带: .99-2.99
│   └── 子线: Wevac Lite（2024年推出，经济定位）
└── 消费品牌 2: Vesta Precision
    ├── 定位: 设备+耗材全线品牌（封口机+低温烹饪+制冷+袋子）
    ├── Tagline: "It'''s not just a matter of degrees..."
    ├── 官网: vestaprecision.com（完整Shopify DTC商城）
    ├── Amazon品牌名: V Vesta Precision
    ├── 价格带: .99-,397
    └── 子线: VestaEco（可降解）、Neovide（无水低温）、Skyra（透明冰）、Imersa（浸入式）
```

### 品牌定位对比

| 维度 | Wevac | Vesta Precision |
|------|-------|----------------|
| 核心品类 | 真空袋（占95%+ SKU） | 封口机 + 低温烹饪器 + 真空袋 |
| 价格带 | .99-2.99 | .99-,397 |
| Amazon BSR | #948 Kitchen & Dining（旗舰） | #23,683 Kitchen & Dining（旗舰） |
| 评价量级 | 旗舰 65,600+ 评价 | 旗舰封口机 67 评价（手持857） |
| 官网 | 仅联系表单（B2B） | 完整 Shopify DTC 商城 |
| 品牌叙事 | 无（纯功能导向） | 有（25年研发、精准温控、创新） |
| 社交媒体 | 无可见账号 | Facebook, Twitter, Pinterest, YouTube, LinkedIn, Instagram, TikTok |
| 目标客户 | 家庭用户（走量） | 家庭 + 商用（走价值） |

### SKU 编码交叉验证（Argion-Vesta 关联铁证）

来源：vestaprecision.com/products.json + argiontechnology.com 产品目录。采集日期 2026-02-15。

| Vesta Precision 产品 | Vesta SKU | Argion 对应型号 | 证据 |
|---------------------|-----------|----------------|------|
| Vac '''n Seal Pro I 托盘 | TRAY-YJS604 | YJS604cfm | SKU 含 YJS604 |
| Vac '''n Seal Pro II 托盘 | TRAY-YJS780 | YJS780cf | SKU 含 YJS780 |
| 手持封口机替换头 | TIP-YJS60 | YJS70/71 系列 | SKU 含 YJS60 前缀 |
| V30 Chamber Vac Elite | BAR-V30, GSKT-V30 | V30 | Argion 目录有 V30 |
| OP10 油泵腔式 | C09af | C10af | Argion 有 C10af |
| OP12 油泵腔式 | C17af | C17f | Argion 有 C17f |
| Perfecta (SV202) | LID-SV202 | SV202 | Argion 有 SV202 |

> 结论：YJS 前缀 = 亚俊氏内部型号编码体系。Vesta 产品 SKU 直接使用 Argion 内部型号，确认为同一公司。

---

## 一、Vesta Precision Amazon 销售数据

来源：Amazon搜索页 + 产品详情页（Playwright采集）
采集日期：2026-02-15

### 1.1 封口机产品线（4款）

| ASIN | 产品 | 价格 | 评分 | 评价数 | 库存 |
|------|------|------|------|--------|------|
| B07GVPTY5B | 手持式封口机 | $29.99 | 4.1 | 857 | In Stock |
| B0BVG33PWR | Vac'''n Seal 12" 外置式 | $299.00 | 4.0 | 67 | In Stock |
| B0BVG374W9 | Vac'''n Seal Pro II 16" 外置式 | $329.99 | 4.0 | 67* | In Stock |
| B0C3VRSVS2 | OP10 油泵腔式 10" | $799.00 | 4.8 | 7 | Only 9 left |

*B0BVG33PWR 与 B0BVG374W9 共享评价池

#### 1.1a Vesta封口机技术规格

来源：_raw/vesta-specs-supplement.md | 采集日期：2026-02-15

| 型号 | 功率 | 真空强度 | 密封宽度 | 泵类型 | 尺寸(LxWxH) | 重量 | 特色功能 |
|------|------|----------|----------|--------|-------------|------|----------|
| V22 | 185W | -28.3 inHg | 12.4" | 干泵 | 15.4x9x4.3" | 5.3 lb | Normal/Gentle/Liquid三模式, 罐装密封, 切刀, 卷袋存储(20'), Smart Seal连续密封专利 |
| V23 | 190W | -28.3 inHg | 12.4" | 干泵 | 15x8.1x6.1" | 6.6 lb | 同V22功能 + 双卷存储(50'单卷或2x20') |
| Pro II | 550W | 95 kPa | 16" | 双泵 | 21.3x10.31x5.59" | 11.22 lb | 不锈钢, 5年保修, 风冷散热, 磁吸锁手柄 |

来源URL：
- https://www.amazon.com/dp/B07GVPTY5B
- https://www.amazon.com/dp/B0BVG33PWR
- https://www.amazon.com/dp/B0BVG374W9
- https://www.amazon.com/dp/B0C3VRSVS2

### 1.2 低温烹饪器产品线（5款）

| ASIN | 产品 | 价格 | 评分 | 评价数 | 库存 |
|------|------|------|------|--------|------|
| B0C8JDRLMJ | Neovide NSV100 3L 无水低温 | $399.99 | 3.9 | 75* | Only 7 left |
| B0C8JCQW23 | Neovide NSV500 8.6L 无水低温 | $569.24 | 3.9 | 75* | Only 14 left |
| B07DRRL2KG | Imersa Elite WiFi 浸入式 | $119.00 | 4.0 | 182* | In Stock |
| B07RDM2BNL | Imersa Pro NSF 浸入式 | $299.00 | 4.0 | 182* | In Stock |
| B07RHQ338J | Imersa Expert 50L/1500W | $399.00 | 4.4 | 5 | Only 13 left |

*共享评价池：NSV100+NSV500共享75评价；Imersa Elite+Pro共享182评价

来源URL：
- https://www.amazon.com/dp/B0C8JDRLMJ
- https://www.amazon.com/dp/B0C8JCQW23
- https://www.amazon.com/dp/B07DRRL2KG
- https://www.amazon.com/dp/B07RDM2BNL
- https://www.amazon.com/dp/B07RHQ338J

### 1.3 Vesta Precision 官网产品目录（Shopify）

来源：https://www.vestaprecision.com/products.json | 采集日期：2026-02-15

#### 封口机

| 型号 | 类型 | 官网价格 | 库存 |
|------|------|---------|------|
| V22 | 外置式 | $129.99 | 缺货 |
| V23 | 外置式（大卷仓） | $159.99 | 缺货 |
| V513 | 腔式（干泵，小腔） | $349.00 | 缺货 |
| V553 | 腔式（干泵，大腔） | $599.00 | 缺货 |
| OP10 | 腔式（油泵，10"） | $799.00 | 有货 |
| OP12 | 腔式（油泵，12"） | $899.00 | 缺货 |

#### 低温烹饪器

| 型号 | 类型 | 官网价格 | 库存 |
|------|------|---------|------|
| NSV100 | Neovide 无水低温（3L） | $449.00 | 有货 |
| NSV500 | Neovide 无水低温（8.6L） | $749.00 | 有货 |

#### 透明冰制冰机

| 型号 | 类型 | 官网价格 | 库存 |
|------|------|---------|------|
| IMT200 | Skyra 单托盘 | $5,399-$5,898 | 缺货 |
| IMT300 | Skyra 双托盘 | $6,399-$7,397 | 有货 |

#### 真空袋

| 产品 | 官网价格 | 库存 |
|------|---------|------|
| VestaEco 可降解卷装 Combo | $36.99 | 有货 |
| VestaEco 可降解预切袋 50ct | $15.99-$29.99 | 部分有货 |
| 8"x50''' Embossed Rolls 2pk | $17.99 | 有货 |
| 5mil Heavy Duty Rolls | $28.99 | 有货 |
| Combo Bags 100ct (6x10+8x12) | $23.99 | 有货 |

---

## 二、Wevac Amazon 销售数据

来源：Amazon搜索页 + 产品详情页（Playwright采集）
采集日期：2026-02-15

### 2.1 真空袋核心产品线（Top 5 by 评价数）

| 排名 | ASIN | 产品 | 价格 | 评分 | 评价数 |
|------|------|------|------|------|--------|
| 1 | B07TMZDGQ1 | 11x50 Rolls 2 pack（旗舰） | $16.84 | 4.6 | 65.6K |
| 2 | B07TV4KRCL | 100 Gallon 11x16 | $24.99 | 4.7 | 17.9K |
| 3 | B07QXKJ43N | 100 Pint 6x10 | $13.99 | 4.7 | 17.9K |
| 4 | B07TV5RNQL | 100 Quart 8x12 | $16.19 | 4.7 | 15.3K |
| 5 | B096MBL1GJ | 11" x 150''' Roll Keeper with Cutter | $31.99 | 4.7 | 13.1K |

BSR数据（B096M9GZNJ 8"x150''' Roll）：#948 in Kitchen & Dining, #9 in Vacuum Sealer Bags
来源：https://www.amazon.com/dp/B096M9GZNJ

### 2.2 全部 Wevac Amazon 产品

| ASIN | 产品 | 价格 | 评分 | 评价数 |
|------|------|------|------|--------|
| B07TMZDGQ1 | 11x50 Rolls 2pk | $16.84 | 4.6 | 65.6K |
| B07TV4KRCL | 100 Gallon 11x16 | $24.99 | 4.7 | 17.9K |
| B07QXKJ43N | 100 Pint 6x10 | $13.99 | 4.7 | 17.9K* |
| B07TV5RNQL | 100 Quart 8x12 | $16.19 | 4.7 | 15.3K |
| B096MBL1GJ | 11" x 150''' Roll Keeper | $31.99 | 4.7 | 13.1K |
| B096M9GZNJ | 8" x 150''' Roll Keeper | $24.29 | 4.7 | 13.1K* |
| B0BX9NS6WL | 8"x100''' & 11"x100''' 2 Rolls Keeper | $32.99 | 4.7 | 13.1K* |
| B096RBVQ8Z | 8"x12" 200ct PreCut Quart | $26.99 | 4.7 | 8K |
| B096RD36H8 | 6"x10" 200ct PreCut Pint | $20.99 | 4.7 | 8K* |
| B0BXKK9ZFB | 6"x10" & 8"x12" 300ct Combo | $27.99 | 4.7 | 8K* |
| B0CS9NKVM3 | Wevac Lite 8"x50''' 3 Rolls | $19.99 | 4.4 | 2.6K |
| B0CTHMSZ1F | 衣物收纳真空袋 10 Pack | $19.99 | 4.3 | 2.5K |
| B0CTHS1927 | 手持式封口机 | $31.99 | 4.2 | 97 |
| B0FLQ1ZC7T | 50ct 8x12 新品 | $9.99 | 4.7 | 126 |
| B0FVSPRZMB | 8"x16''' 2 Rolls 新品 | $9.99 | 4.6 | 31 |
| B0DD7DNXL3 | Wevac Lite 8"x12" 200ct | $21.99 | 4.3 | 66 |

*标注：带*的评价数为同一产品家族共享的评价池

来源URL：各产品 https://www.amazon.com/dp/{ASIN}

### 2.3 Wevac 产品线分析

- **核心产品**：真空袋（卷装+预切装），占全部SKU的绝大多数
- **旗舰产品**：B07TMZDGQ1 (11x50 Rolls 2pk) 以 65.6K 评价遥遥领先
- **子品牌**：Wevac Lite（2024年推出，经济定位，评分略低 4.3-4.4）
- **品类扩展**：衣物收纳真空袋、手持式封口机
- **无台式封口机**（已确认）

### 2.4 用户评价关键词

来源：_raw/review-keywords-supplement.md | 采集日期：2026-02-15

**Wevac 旗舰袋 11x50 Rolls 2pk (ASIN: B07TMZDGQ1)** | 评价数：~65,600+
- 好评：Value for money (1.2K), Quality (1.2K), Functionality (1K)
- 差评：Sealability (773 mentions, mixed) - 部分无法保持真空密封; Size (608 mentions, mixed) - 卷太大放不进封口机

**Vesta Vac'n Seal (ASIN: B0BVG33PWR)** | 评价数：~67（极少）
- 好评：Works well, Quality (9 mentions), Sealability (12 mentions)
- 差评：评价数太少(67条)，Amazon未生成负面关键词摘要

---

## 三、Argion 制造能力

来源：https://www.argiontechnology.com | 采集日期：2026-02-15

### 公司概况

| 项目 | 数据 |
|------|------|
| 公司全称 | 广州亚俊氏真空科技股份有限公司 (Guangzhou Argion Electric Appliance Co., Ltd.) |
| 成立时间 | 2007年 |
| 总部地址 | 广州市番禺区企业路1号，邮编511440 |
| 定位 | ODM/OEM 厨房电器制造商 |
| 研发团队 | 约100名工程师 |
| 认证体系 | ETL、CE、RoHS、GS、SAA、FDA、LFGB |
| 荣誉 | Metro Sourcing 铂金供应商（全球仅3家） |

### 生产基地

| 基地 | 面积 | 产线 |
|------|------|------|
| 广州 | 17,000 sqm | 10条组装线 + 15条注塑线 |
| 佛山 | 25,600 sqm | 16条真空袋产线 + 16条制冷产线 |
| 新加坡 | 4,000 sqm | 3条设备产线 + 8条真空袋产线 |

---

## 四、Argion 产品目录（制造端）

来源：https://www.argiontechnology.com | 采集日期：2026-02-15

### 产品数量统计

| 品类 | 型号数量 | 定位 |
|------|----------|------|
| 外置式真空封口机 | 21款 | 入门到专业级 |
| 腔式真空封口机 | 19款 | 家用到商用 |
| 手持式真空封口机 | 1+款 | 便携日常 |
| 浸入式低温烹饪器 | 9款 | 家用到商用 |
| 水浴式低温烹饪机 | 5款 | 家用到商用 |
| 急速冷冻机 | 4款 | 商用 |
| 透明冰制冰机 | 2款 | 商用（酒吧/餐饮） |
| 真空袋/卷 | 5大类8+袋型 | 全场景覆盖 |
| 封袋机 | 2+款 | 商用包装 |

### 外置式封口机（21款）

#### YJS系列（主力产品线）

YJS741（旗舰级）详细规格：
- 来源：https://www.argiontechnology.com/product-item/external-vacuum-sealer-yjs741/
- 功率 550W | 泵压 -28.3"Hg / -958mbar | 双泵 | 最大袋宽 406mm | 封口线宽 5mm
- 尺寸 495x301x162mm | 重量 5.6kg | 认证 CE, RoHS, GS, ETL

其他YJS外置式型号：YJS780cf, YJS770f, YJS614, YJS604cfm, YJS608, YJS601, YJS460, YJS260f, YJS215, YJS210f, YJS150f, YJS120f, YJS111f, YJS90

#### V系列（Vesta品牌线）

V21, V20f, V15f, V08, V07, V05

### 腔式封口机（19款）

C10af 详细规格：
- 来源：https://www.argiontechnology.com/product-item/c10af/
- 功率 1000W | 泵压 -29.9"Hg / -1012mbar | 油泵 | 最大袋宽 260mm
- 腔体 265x330x130mm | 重量 21kg | 认证 CE, RoHS, GS, ETL

C17f 详细规格：
- 来源：https://www.argiontechnology.com/product-item/chamber-vacuum-sealer-c17f/
- 功率 370W | 泵压 -0.1MPa | 油泵 | 最大袋宽 350mm | 重量 26kg

C20f 详细规格：
- 来源：https://www.argiontechnology.com/product-item/c20f/
- 功率 1150W | 泵压 -29.9"Hg | 油泵 | 最大袋宽 410mm | 双封口线 | 重量 44kg

其他腔式型号：C25, C30, C45, C50, C701, C801, V30, V50f, V60f, V70f, V86f, YJS801, YJS803, YJS820f, YJS822f, YJS890

### 低温烹饪设备

浸入式（9款）：SV96, SV95, SV85, SV84, SV330, SV300, SV130, SV111, SV100
水浴式（5款）：SV200, SV202, SV210, SV250, SV251

### 制冷设备

急速冷冻机（4款）：BF110, BF210, BF310, BF610
透明冰制冰机（2款）：IMT310, IMT210

### 真空袋

5大类：传统真空袋、可降解真空袋（OK Compost + BPI 双认证，全球首家）、真空储物袋、可降解食品储物袋、塑料食品储物袋

### 核心技术优势

1. SmartVac 一键智能操作系统
2. 油泵系统，最高泵压 -29.9"Hg / -1012mbar
3. 可降解真空袋（OK Compost + BPI 双认证，全球首家）
4. 精确温控（低温烹饪 0.1°C 精度）
5. 透明冰制冰技术（23-28小时，节省95%成本）
6. 全品类覆盖：从真空封口到低温烹饪到制冷到耗材
