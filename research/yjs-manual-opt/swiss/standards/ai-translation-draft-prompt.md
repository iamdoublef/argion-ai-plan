# Swiss Translation Draft Prompt

用途：
- 基于结构化 source content 和语言规范资产，生成目标语言译文初稿

输入要求：
- source language strings
- locale guide
- terminology glossary
- brand language guide
- warning language policy
- unit and measurement policy

硬规则：
- 不得改变 `text_id`
- 不得改动章节结构、block 结构或图片绑定
- 所有术语、单位、警示语必须优先服从规范资产
- `zh-HK` 与 `zh-TW` 必须分别输出，不得做逐字简转繁
- 不确定时保留原意并标记 `needs_review`

输出要求：
1. 目标语言 `strings` 草稿
2. 术语冲突列表
3. 本地化注意项
4. 需要人工复核的文本清单

自检清单：
- 品牌名、型号、按键名是否统一
- 单位和数值格式是否符合 locale 规范
- 警示语气和安全措辞是否符合规范
- 是否存在逐字翻译痕迹
- `zh-HK` / `zh-TW` 是否体现本地化差异
