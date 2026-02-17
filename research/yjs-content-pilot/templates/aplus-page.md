# A+页面内容 Prompt模板

> 项目：yjs-content-pilot
> 适用：Amazon A+ Content（Enhanced Brand Content）
> 版本：v1.0

---

## 使用说明

1. 使用与 `product-description.md` 相同的 System Prompt
2. A+页面由5-7个模块组成，每个模块对应Amazon A+的一个内容块
3. 生成文案后，配合图片生成模板（`image-generation.md`）制作配图

---

## Task Prompt — A+页面完整内容

```
Create Amazon A+ Content (Enhanced Brand Content) for the following product:

**Product:** {product_name}
**Brand:** {brand_name}
**Category:** {category}
**Key Specifications:** {key_specs_list}
**Key Benefits:** {key_benefits_list}
**Target Audience:** {target_audience}
**Competitor Advantages to Address:** {competitor_comparison_points}

---

Generate A+ content with the following 7 modules:

### Module 1: Hero Banner (Standard Image & Text Overlay)
- **Headline** (max 60 chars): Bold, benefit-driven statement
- **Subheadline** (max 100 chars): Supporting detail
- **Image direction**: Describe the ideal hero image (product in lifestyle setting)

### Module 2: Brand Story (Standard Company Logo)
- **Brand headline** (max 60 chars)
- **Brand body** (max 450 chars): Brief brand story — who we are, why we do this, 17 years of expertise
- **Image direction**: Brand/factory/team image suggestion

### Module 3: Key Features Grid (Standard Three Images & Text)
Three feature cards, each with:
- **Feature title** (max 50 chars)
- **Feature description** (max 300 chars)
- **Image direction**: What the feature image should show

### Module 4: How It Works (Standard Four Images & Text)
Four steps showing the product in action:
- **Step title** (max 30 chars)
- **Step description** (max 200 chars)
- **Image direction**: What each step image should show

### Module 5: Comparison Chart (Standard Comparison Chart)
Compare this product vs 2-3 other models in the brand lineup (NOT competitors):
- 5-6 comparison dimensions
- Use checkmarks and feature highlights
- Position this product as the premium/best-value option

### Module 6: Use Cases / Lifestyle (Standard Image & Light Text Overlay)
3-4 real-world use cases:
- **Use case title** (max 40 chars)
- **Description** (max 150 chars)
- **Image direction**: Lifestyle scene suggestion

### Module 7: Specifications + Trust (Standard Technical Specifications)
- Key specs in table format
- Certifications listed (ETL, CE, FDA, etc.)
- Warranty information
- What's in the box

---

For each module, also provide:
- **Image direction**: Detailed description for the designer/AI image generator
- **Alt text**: Accessibility text for each image (max 100 chars)
```

---

## 示例输入（Wevac CV10）

```
Product: Wevac CV10 Chamber Vacuum Sealer
Brand: Wevac
Category: Chamber Vacuum Sealer
Key Specifications:
- Dual pump system, -99.9kPa vacuum
- 10" double seal bar
- Stainless steel body
- LCD touch panel
- Liquid Mode, Marinate Mode, Dry Mode, Pulse Mode

Key Benefits:
- Seal liquids without any mess
- Commercial-grade power at home price
- One-touch simplicity
- Built to last 10+ years

Target Audience: Sous vide enthusiasts, meal preppers, home chefs
Competitor Advantages to Address:
- vs FoodSaver: chamber design seals liquids (external sealers can't)
- vs VacMaster VP210: more compact, modern UI, similar power
- vs Anova: dual pump (Anova single pump), faster cycle time
```

---

## Amazon A+ 模块类型参考

| Amazon模块名 | 用途 | 图片尺寸 |
|-------------|------|----------|
| Standard Image & Text Overlay | Hero banner | 970×600 px |
| Standard Company Logo | 品牌故事 | 600×180 px (logo) |
| Standard Three Images & Text | 特性展示 | 300×300 px each |
| Standard Four Images & Text | 步骤/流程 | 220×220 px each |
| Standard Comparison Chart | 产品对比 | 150×150 px each |
| Standard Image & Light Text Overlay | 场景/生活方式 | 970×300 px |
| Standard Technical Specifications | 规格表 | 无图片 |

---

## 质量检查清单

- [ ] 共7个模块，覆盖品牌故事→特性→使用→对比→规格
- [ ] 每个模块的文字长度符合Amazon限制
- [ ] 对比图表只对比自家产品线（不提竞品名）
- [ ] 图片方向描述足够具体，可直接用于图片生成
- [ ] Alt text已为每张图片提供
- [ ] 无夸大宣传或未验证声明
- [ ] 品牌调性一致
