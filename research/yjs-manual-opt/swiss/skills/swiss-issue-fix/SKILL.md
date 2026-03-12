---
name: swiss-issue-fix
description: "Swiss 说明书问题修复 skill：当 QA 审计、视觉审计、构建错误或用户反馈发现 Swiss A5 说明书存在问题（溢出、图片缺失、翻译残留、分页错位、样式异常、DOCX 损坏等），使用本 skill 定位根因并修复。触发词包括：fix、修复、overflow、溢出、图片丢失、翻译错误、分页问题、audit 报告修复、QA issue、构建失败、DOCX 打不开、样式不对、排版问题。只要涉及 Swiss 说明书修复或 QA 回归，都应使用本 skill。"
---

# Swiss 说明书问题修复 Skill

## 适用场景

当 Swiss A5 说明书出现以下任一情况时，先读本文件：

- QA 审计报告（`audit-visual.js` 或手动审计）发现 ERROR / WARNING
- 构建失败或产生异常输出
- PDF / DOCX 渲染异常（溢出、图片丢失、样式错位）
- 翻译残留（源语言文字出现在非源语言变体中）
- 用户直接报告某页/某块有问题

## 先读哪些文件

修复前必须获取足够上下文，按优先级读取：

1. **审计报告**（如果有）：定位具体的 ERROR / WARNING 条目
2. **本 skill 的修复决策树**（下方 §修复决策树）
3. **`DESIGN-STANDARD.md`** — 确认正确的排版标准
4. **`QA-RULES.md`** — 确认判定标准和检查方法
5. **出问题的产品数据**：
   - `products/<product>/product.json`
   - `products/<product>/images.json`
   - `products/<product>/content/source/manifest.json`
   - `products/<product>/content/source/chapters/*.json`（只读相关章节）
   - `products/<product>/i18n/compiled/<locale>.json`（只读相关 locale）
6. **相关模板和样式**：
   - `template/*-master-*.html`
   - `template/shared/base/*.css`
   - `template/shared/base/brand-themes.json`
7. **构建和导出工具**（需要理解渲染逻辑时）：
   - `tools/build-variant.js`
   - `tools/export-docx.js`
   - `tools/export-pdf.js`

## 修复硬规则

1. **修正式源头，不修产物**：所有修复必须回写到 JSON 结构源 / 译文 catalog / CSS / 模板，禁止只修 HTML 输出或 PDF
2. **最小改动原则**：只修出问题的地方，不顺手重构不相关的代码
3. **修完必须验证**：修改后必须重新构建并确认问题消失，不能只改文件就结束
4. **不破坏其他变体**：修一个 locale / region / brand 后，必须确认未影响其他变体（至少抽检 2 个）
5. **禁止 `html_fragment`**：不能用 `html_fragment` 做修复补丁
6. **禁止打印黑魔法**：不能用 `zoom` / `nth-of-type` 打印补丁

## 修复决策树

遇到问题时，按此树定位根因和修复路径：

### A. 页面溢出 / 内容超出 A5 边界

```
溢出 →
├─ 文字溢出？
│  ├─ 长语种 (EN/DE/IT) → 拆页、加续页（DESIGN-STANDARD 允许）
│  ├─ 中文溢出 → 检查是否文本过长，精简或拆段落
│  └─ 表格溢出 → 检查 table-layout: fixed + word-break 设置
├─ 图片溢出？
│  ├─ 检查 images.json 中 width/height 是否合理
│  ├─ 检查 CSS object-fit: contain 是否生效
│  └─ 检查图片原始尺寸是否过大
└─ 容器溢出？
   ├─ 检查 CSS 中是否有固定高度导致截断
   └─ 检查 page-break 设置是否合理
```

**修复入口**：CSS (`template/shared/base/*.css`) 或 JSON 内容 (`chapters/*.json`)

### B. 图片问题

```
图片问题 →
├─ 图片不显示？
│  ├─ images.json 中 file 路径是否正确？
│  ├─ 文件是否存在于 products/<product>/images/ ？
│  └─ SVG 引用路径是否正确？
├─ 图片变形 / 裁切？
│  ├─ 检查 object-fit 值（应为 contain）
│  ├─ 检查容器宽高比与图片宽高比是否匹配
│  └─ 检查 figure block 的 layout 配置
└─ DOCX 图片问题？
   ├─ 检查 SVG → PNG 光栅化缓存 `_docx_raster_cache/`
   ├─ 检查 export-docx.js 中 fitImageSize 逻辑
   └─ 清除缓存后重新导出
```

**修复入口**：`images.json`、图片文件、CSS 或 `export-docx.js`

### C. 翻译 / 本地化问题

```
翻译问题 →
├─ 源语言残留？
│  ├─ 检查 i18n/compiled/<locale>.json 是否有空值
│  ├─ 检查 text_id 是否在 catalog 中缺失
│  └─ 修复路径：补充 compiled JSON → 回写 workbooks
├─ 术语不一致？
│  ├─ 对照 standards/terminology-glossary.json
│  └─ 修复路径：更新 compiled JSON + workbook
├─ 变量 {{}} 渲染失败？
│  ├─ 检查变量名拼写
│  ├─ 检查 product.json 中是否有对应值
│  └─ 修复路径：修 compiled JSON 中的变量名或 product.json 中的数据
└─ zh-HK/zh-TW 显示简体？
   ├─ 确认是否有独立 locale catalog
   └─ 禁止运行时逐字简转繁，必须有独立 compiled JSON
```

**修复入口**：`i18n/compiled/<locale>.json`，然后同步回写 `i18n/workbooks/<locale>.xlsx`

### D. 分页 / 排版问题

```
分页问题 →
├─ 保修卡被截断？
│  ├─ warranty_card 是否跨了 page block？ → JSON 结构错误
│  └─ 保修卡允许独立续页，检查 page-break 设置
├─ 章节标题孤页（标题在底部，内容在下页）？
│  ├─ CSS break-after / break-inside 设置
│  └─ 可能需要在 JSON 中调整 block 位置
├─ 目录页码不对？
│  └─ 目录由构建工具自动生成，检查构建逻辑
└─ 空白页过多？
   ├─ 检查 page block 内容是否过少
   └─ 考虑合并相邻 page block
```

**修复入口**：`chapters/*.json`（结构调整）或 CSS（分页规则）

### E. DOCX 特有问题

```
DOCX 问题 →
├─ DOCX 打不开 / 损坏？
│  ├─ 检查 export-docx.js 构建日志
│  ├─ 用 unpack.py 解压检查 XML 结构
│  └─ 检查是否有非法字符或过大的嵌入图片
├─ DOCX 样式丢失？
│  ├─ 检查 base-template-cn.docx 基线是否完整
│  ├─ 检查 brand-themes.json 中 docx 主题配置
│  └─ 对照 WORD-BASE-TEMPLATE-CN.md 规范
├─ DOCX 与 PDF 内容不一致？
│  ├─ 两者共用同一 JSON 源，检查 build-variant.js 加载逻辑
│  └─ 检查 export-docx.js 中是否有条件分支遗漏某些 block
└─ DOCX 图片问题？
   └─ 见上方 §B 图片问题 → DOCX 分支
```

**修复入口**：`export-docx.js`、`base-template-cn.docx`、`brand-themes.json`

### F. 构建失败

```
构建失败 →
├─ JSON 解析错误？
│  ├─ 检查 JSON 语法（多余逗号、缺引号）
│  └─ 用 node -e "JSON.parse(require('fs').readFileSync('...'))" 快速定位
├─ 找不到文件？
│  ├─ 检查 manifest.json 引用的章节文件是否存在
│  ├─ 检查 images.json 引用的图片是否存在
│  └─ 检查路径大小写（区分大小写的系统）
├─ html_fragment 错误？
│  └─ 正式内容禁止 html_fragment，必须转为正式 block 类型
└─ 模板变量未解析？
   ├─ 检查 product.json 中是否缺少必要字段
   └─ 检查 build-variant.js 中 resolveVars 逻辑
```

**修复入口**：JSON 数据文件

## 标准修复流程

```
1. 定位问题
   ├─ 读审计报告 / 用户描述
   ├─ 确认影响范围（哪些 product × region × brand × locale）
   └─ 在决策树中定位到对应分支

2. 分析根因
   ├─ 读取相关源文件（JSON、CSS、模板、工具脚本）
   ├─ 确认是数据问题、样式问题还是工具逻辑问题
   └─ 找到需要修改的最小文件集

3. 执行修复
   ├─ 修改源文件（不修产物）
   ├─ 每次只改一个问题
   └─ 修改前记录原值，便于回滚

4. 验证修复
   ├─ 重新构建：node tools/build-variant.js <product> <region> <brand>
   ├─ 确认问题消失
   ├─ 抽检至少 2 个其他变体未被影响
   └─ 如涉及 DOCX：额外确认 DOCX 可打开、图文完整

5. 回归检查
   ├─ 运行 audit-visual.js 确认无新增 ERROR
   └─ 如修复涉及样式/模板：抽检所有产品的代表变体
```

## 常见陷阱

| 陷阱 | 后果 | 防范 |
|------|------|------|
| 只修了 compiled JSON，没回写 workbook | 下次翻译人员编辑 workbook 后编译会覆盖修复 | 修 compiled 后必须同步 workbook |
| 修 CSS 时用了页序号选择器 | 其他产品或变体页序号不同，样式错位 | 禁止 nth-of-type / zoom 打印补丁 |
| 修了一个 locale 忘了其他 locale | 多语言不一致 | 修完后 grep 检查所有 locale 的同一 text_id |
| 给 DOCX 加了 html_fragment 补丁 | 违反正式 block 白名单 | 只用正式 14 种 block 类型 |
| 修了图片路径但没检查文件是否存在 | 构建通过但图片不显示 | 修路径后 Test-Path 确认文件存在 |
| 修复溢出时压缩字体/缩小间距 | 整体视觉质量下降 | 长语种优先拆页续页，不优先压缩 |
