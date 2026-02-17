# 产品图片生成 Prompt模板

> 项目：yjs-content-pilot
> 适用：Midjourney / Ideogram / DALL-E 产品场景图、生活方式图
> 版本：v1.0

---

## 使用说明

1. 产品主图（白底图）仍建议使用实拍照片，AI生成图用于辅助场景图和生活方式图
2. 以下Prompt针对Midjourney V6优化，其他工具需微调语法
3. 生成后需人工检查产品外观准确性，必要时用Photoshop修正细节

---

## Prompt结构

```
[主体描述], [场景/环境], [光线], [构图], [风格], [技术参数]
```

---

## 模板1：产品场景图（Kitchen Setting）

适用：Amazon A+页面、社媒帖子

```
A {product_name} placed on a {surface_material} kitchen countertop, {action_description}, surrounded by {food_items}, modern kitchen background with {kitchen_style} cabinets, soft natural window light from the left, shallow depth of field, editorial product photography style, 4K, photorealistic --ar 16:9 --v 6 --s 200
```

### 变量示例（Wevac CV10）

```
A Wevac CV10 chamber vacuum sealer placed on a white marble kitchen countertop, sealing a bag of fresh salmon fillets, surrounded by fresh herbs rosemary and thyme and lemon slices, modern kitchen background with light oak cabinets, soft natural window light from the left, shallow depth of field, editorial product photography style, 4K, photorealistic --ar 16:9 --v 6 --s 200
```

---

## 模板2：生活方式图（Lifestyle）

适用：Amazon主图辅助、社媒、广告

```
A {person_description} in a {setting} using a {product_name} to {action}, {emotional_context}, {food_items} visible on the counter, warm ambient lighting, lifestyle photography, candid feel, 4K, photorealistic --ar 4:5 --v 6 --s 150
```

### 变量示例

```
A young couple in a bright modern kitchen using a Wevac chamber vacuum sealer to prepare meal prep containers for the week, smiling and enjoying the process together, colorful vegetables and portioned chicken breasts visible on the counter, warm ambient lighting, lifestyle photography, candid feel, 4K, photorealistic --ar 4:5 --v 6 --s 150
```

---

## 模板3：Before/After对比图

适用：A+页面、社媒

```
Split image comparison, left side: {food_item} stored in regular plastic bag showing {deterioration_signs} after {time_period}, right side: same {food_item} vacuum sealed in clear bag looking perfectly fresh after {time_period}, clean white background, studio lighting, informational product photography, text overlay space at top --ar 16:9 --v 6 --s 100
```

### 变量示例

```
Split image comparison, left side: fresh strawberries stored in regular plastic bag showing mold and wilting after 7 days, right side: same strawberries vacuum sealed in clear bag looking perfectly fresh after 7 days, clean white background, studio lighting, informational product photography, text overlay space at top --ar 16:9 --v 6 --s 100
```

---

## 模板4：使用步骤图（How-to）

适用：A+页面 Module 4

```
Step {step_number} of using a vacuum sealer: {action_description}, close-up shot of hands {hand_action}, {product_name} visible in frame, clean bright kitchen background, instructional photography style, clear and well-lit, 4K --ar 1:1 --v 6 --s 100
```

### 四步示例

```
Step 1: Place food in vacuum bag, close-up of hands placing marinated chicken into a clear vacuum bag, bright kitchen counter --ar 1:1 --v 6

Step 2: Place bag in chamber, close-up of hands placing the filled bag into the Wevac CV10 chamber, LCD panel visible --ar 1:1 --v 6

Step 3: Close lid and press start, close-up of hand pressing the touch panel on the Wevac CV10, lid closed --ar 1:1 --v 6

Step 4: Perfectly sealed, close-up of hands holding a perfectly vacuum-sealed bag of chicken, no wrinkles, tight seal visible --ar 1:1 --v 6
```

---

## 模板5：Sous Vide场景图

适用：低温烹饪产品线

```
A perfectly cooked {food_item} being removed from a sous vide water bath, {food_description}, vacuum sealed bag partially open, steam rising, {garnish} on a {plate_type}, restaurant-quality plating, dramatic side lighting, food photography style, appetizing, 4K --ar 4:5 --v 6 --s 250
```

---

## 模板6：环保主题图

适用：可降解真空袋产品

```
{brand_name} compostable vacuum bags arranged artfully with fresh {food_items}, surrounded by green leaves and natural elements, earth-toned background, eco-friendly aesthetic, soft diffused lighting, sustainability-focused product photography, clean and natural feel --ar 16:9 --v 6 --s 200
```

---

## Midjourney 参数速查

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `--ar` | 宽高比 | 16:9（横幅）、4:5（社媒）、1:1（方图） |
| `--v 6` | 模型版本 | 始终用V6 |
| `--s` | 风格化程度 | 100（写实）、200（略有风格）、250（艺术感） |
| `--q` | 质量 | 默认1即可，2用于最终出图 |
| `--no` | 排除元素 | `--no text, watermark, logo`（排除文字） |

---

## Amazon图片规范

| 图片类型 | 尺寸要求 | 背景 | 说明 |
|----------|----------|------|------|
| 主图 | ≥1000×1000px | 纯白(RGB 255,255,255) | 建议实拍，不用AI |
| 辅助图 | ≥1000×1000px | 不限 | AI场景图适用 |
| A+页面 | 按模块不同 | 不限 | AI生成+后期处理 |

---

## 质量检查清单

- [ ] 产品外观与实物基本一致（形状、颜色、比例）
- [ ] 无AI伪影（多余的手指、扭曲的文字、不合理的阴影）
- [ ] 食物看起来新鲜、有食欲
- [ ] 场景真实可信（厨房布局合理、光线自然）
- [ ] 图片分辨率≥1000×1000px
- [ ] 无品牌logo/文字（除非刻意添加）
- [ ] 人物多样性（不同肤色、年龄、性别）
- [ ] 无版权风险元素（其他品牌产品、名人肖像）
