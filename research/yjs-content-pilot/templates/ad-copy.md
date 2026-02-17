# 广告文案 Prompt模板（PPC / 社媒）

> 项目：yjs-content-pilot
> 适用：Amazon PPC广告（SP/SB）、社交媒体帖子（Instagram/Facebook/TikTok）
> 版本：v1.0

---

## 使用说明

1. 使用与 `product-description.md` 相同的 System Prompt
2. 根据广告类型选择对应的 Task Prompt
3. 每次生成多个变体，用于A/B测试

---

## Task Prompt 1 — Amazon PPC广告

```
Create Amazon PPC ad copy variations for the following product:

**Product:** {product_name}
**Brand:** {brand_name}
**Target Keywords:** {target_keywords_list}
**Key Selling Points:** {key_benefits_list}
**Target Audience:** {target_audience}
**Price:** {price}
**Current Promotions:** {promotions_if_any}

---

Generate the following:

### Sponsored Products (SP) — Custom Headlines
5 headline variations (max 50 characters each):
- Each highlights a different benefit/angle
- Include target keyword naturally
- Create urgency or curiosity without being clickbait

### Sponsored Brands (SB) — Headlines + Custom Images
3 headline variations (max 50 characters each) + 3 taglines (max 45 characters each):
- Headlines: brand-level messaging, not just product features
- Taglines: supporting detail or call-to-action

### Sponsored Brands Video — Script Outline
1 video script outline (15-30 seconds):
- Hook (0-3s): attention-grabbing opening
- Problem (3-8s): customer pain point
- Solution (8-20s): product demo/features
- CTA (20-30s): call to action

For each variation, note:
- **Angle**: What customer motivation it targets (convenience, quality, value, etc.)
- **A/B test suggestion**: What to test against
```

---

## Task Prompt 2 — 社交媒体帖子

```
Create social media content for the following product:

**Product:** {product_name}
**Brand:** {brand_name}
**Platform:** {platform: Instagram / Facebook / TikTok}
**Content Goal:** {goal: awareness / engagement / conversion}
**Key Message:** {key_message}
**Target Audience:** {target_audience}
**Hashtag Strategy:** {existing_hashtags_if_any}

---

Generate:

### Instagram Post (Feed)
- **Caption** (max 2200 chars, ideal 150-300):
  - Hook line (first sentence visible before "more")
  - Body: benefit-focused, conversational tone
  - CTA: clear next step
- **Hashtags** (20-25): mix of high-volume and niche
- **Image direction**: What the post image should show

### Instagram Reel Script (15-30s)
- **Hook** (0-3s): text overlay + action
- **Body** (3-25s): demo or transformation
- **CTA** (25-30s): follow/shop/link in bio
- **Audio suggestion**: trending sound or original

### Facebook Ad Copy
- **Primary text** (max 125 chars visible, full up to 500):
  - Lead with benefit or question
  - Social proof element if available
- **Headline** (max 40 chars)
- **Description** (max 30 chars)
- **CTA button**: Shop Now / Learn More / See More

### TikTok Script (15-60s)
- **Hook** (0-3s): pattern interrupt or question
- **Content** (3-50s): educational or entertaining angle
- **CTA** (last 5s): follow for more / link in bio
- **Text overlays**: key points to display on screen
```

---

## 内容角度库（可复用）

针对亚俊氏产品线，以下角度可反复使用：

| 角度 | 适用场景 | 示例钩子 |
|------|----------|----------|
| 省钱 | 真空保鲜延长食物寿命 | "Stop throwing away $X/month in wasted food" |
| 专业降级 | 商用级设备家用化 | "Restaurant-grade vacuum sealing, now in your kitchen" |
| 对比震撼 | Before/After保鲜效果 | "Day 14: regular bag vs vacuum sealed" |
| 生活方式 | Meal prep / Sous vide | "Sunday meal prep that actually lasts all week" |
| 环保 | 可降解真空袋 | "Vacuum seal without the guilt — 100% compostable bags" |
| 技术解密 | Liquid Mode等专利技术 | "The secret to vacuum sealing soup (yes, soup)" |
| 社交证明 | 用户评价/使用场景 | "Why 10,000+ home chefs switched to chamber sealing" |

---

## 质量检查清单

### PPC广告
- [ ] 标题≤50字符（SP）/ ≤50字符（SB）
- [ ] 无竞品品牌名
- [ ] 无夸大宣传（"best", "#1"）
- [ ] 关键词自然融入
- [ ] 每个变体角度不同

### 社媒帖子
- [ ] 平台格式正确（字数限制、hashtag数量）
- [ ] 品牌调性一致
- [ ] CTA明确
- [ ] 图片/视频方向描述具体
- [ ] 无敏感/争议内容
