# DOCX 美化方案研究报告

**日期**：2026-03  
**项目**：yjs-manual-opt / Swiss 说明书 DOCX 输出升级  
**研究分支**：`research/docx-generation-logic`（worktree: `.worktrees/research-docx-gen`）

---

## 1. 背景与问题

当前 Swiss 说明书的 DOCX 输出使用 `docx` npm 包（@9.6.0）在 `tools/export-docx.js`（1536 行）中程序式生成。产出物存在以下不可接受的质量问题：

| 问题 | 根因 |
|------|------|
| 封面无设计元素 | docx npm 不支持 DrawingML / 文本框 / 浮动图形 |
| 默认蓝色标题 (#2E74B5) 与品牌色 (#E63946) 不匹配 | 代码中硬编码了默认颜色，brand-themes.json 的 docx 主题未充分生效 |
| 宋体字体，显得廉价 | 未嵌入品牌字体，docx npm 无字体嵌入能力 |
| 无视觉层次，排版扁平 | 纯"文档流"生成，无法做文本框、渐变填充、多栏浮动等排版 |
| 图片/文字布局单调 | 所有内容线性堆叠，无法实现 figure-row 并排等复杂布局 |

**使用场景**：ODM 客户交付（可编辑 Word/WPS 文件），不要求 1:1 还原 PDF，但必须"可编辑且体面"。

---

## 2. 当前 DOCX 生成链路（已分析）

```
JSON 数据源                    构建工具                      输出
─────────────                ──────────                   ─────
product.json        ─┐
images.json          │
manifest.json        ├─→  build-variant.js  ─→  统一数据对象
chapters/*.json      │     (共享加载模块)
compiled/*.json     ─┘
brand-themes.json                │
                                 ▼
                          export-docx.js
                          (1536 行，14 种 block 渲染器)
                                 │
                      ┌──────────┼──────────┐
                      ▼          ▼          ▼
                  SVG→PNG     构建 OOXML    写入 .docx
                  (sharp)    (docx npm)   (writeBufferWithRetry)
```

### 关键函数清单（export-docx.js）

| 函数 | 职责 |
|------|------|
| `buildDocx()` | 主入口，组装整个文档 |
| `buildCoverBlock()` | 封面页（当前极简） |
| `renderParagraphBlock()` | 普通段落 |
| `renderSubTitle()` | 副标题 |
| `renderBulletList()` | 项目符号列表 |
| `renderAlertBox()` | 警告/注意/提示框 |
| `renderStepFlow()` | 操作步骤 |
| `renderFigureBlock()` | 单图 |
| `renderFigureRow()` | 并排图 |
| `renderSplitPanel()` | 左右分栏 |
| `renderTableRef()` | 表格引用 |
| `renderQaList()` | 问答列表 |
| `renderContactBlock()` | 联系信息 |
| `renderWarrantyCard()` | 保修卡 |
| `renderCustomTable()` | 自定义表格 |
| `renderSpecsTable/PartsTable/ButtonsTable/BrandInfoTable/ManufacturerTable()` | 结构化数据表 |
| `prepareImagesManifestForDocx()` | SVG→PNG 光栅化（220dpi，缓存到 `_docx_raster_cache/`） |
| `fitImageSize()` / `makeImageRun()` | 图片尺寸适配与嵌入 |
| `parseTextTokens()` / `resolveVars()` | 文本解析与变量替换 |

### 数据依赖

- build-variant.js 导出：`loadProductConfig`, `loadContentDocument`, `loadImagesManifest`, `loadLocaleCatalog`, `buildLocalizedRuntimeData`, `resolveBrandTheme`, `langSuffix`, `resolveTemplateIncludes`
- 输出格式：A5 portrait (148×210mm)，10mm 四边距，PAGE_W=8379 DXA, PAGE_H=11906 DXA, CONTENT_W=7245 DXA
- 变体矩阵：7 regions × 3 brands = 21 种组合

---

## 3. 四方向研究结论

### 方向 A：python-docx / docxtpl 模板注入（推荐 - 免费方案）

**核心范式**：在 Word 中设计好母版（A5 封面、页眉页脚、标题样式、品牌色），用 Jinja2 标签标记占位符，运行时 docxtpl 注入数据。

**优势**：
- **Word 专业设计保真**：设计师在 Word 中做好的排版（文本框、渐变、形状、SmartArt）完整保留
- **OOXML 100% 保留**：docxtpl 只替换文本/图片节点，不触碰其他 XML，不会丢失样式
- **免费开源**：MIT 许可，无商业费用
- python-docx 底层稳定，docxtpl 在其上做模板扩展

**关键能力**：
- `{{variable}}` — 文本替换
- `{%for item in items%}...{%endfor%}` — 循环（列表、表格行）
- `{{image_key}}` — `InlineImage()` 图片注入
- `{%if condition%}...{%endif%}` — 条件段落
- RichText 对象 — 加粗/颜色/超链接混排
- 子文档合并 — `subdoc` 机制

**局限**：
- Python 生态，需要从当前 Node.js 工具链切换或桥接
- 复杂的嵌套循环（表格内嵌循环）需要仔细设计模板
- 无法动态创建"从未在模板中出现过"的样式

### 方向 B：docx npm 高级技巧

**结论：不推荐继续**

docx npm 的架构是"程序式文档流"，天花板已到：
- 不支持 DrawingML（文本框、形状、渐变）
- 不支持浮动图片
- 不支持字体嵌入
- 不支持从现有 .docx 模板读取和注入

虽然理论上可以通过 raw XML 注入 hack 部分功能，但维护成本极高，且一旦 docx npm 升级可能全部失效。

### 方向 C：HTML → DOCX 转换

**结论：不推荐**

| 工具 | 问题 |
|------|------|
| Pandoc | CSS 完全不解析，输出是纯文本+标题层级，致命缺陷 |
| LibreOffice headless | 需要本地安装，跨平台一致性差，CSS 支持不完整 |
| html-docx-js / docx-html | 玩具级，不支持 A5 页面设置 |
| Aspose.Words | 商业 $1.2k+，CSS 支持最好但仍有限 |

HTML→DOCX 的核心问题：CSS 在 OOXML 中没有对等映射，转换永远是有损的。

### 方向 D：行业最佳实践

**行业共识**：Word 模板 + 模板引擎注入是标准范式。

| 方案 | 类型 | 价格 | 生态 | 推荐度 |
|------|------|------|------|--------|
| docxtpl (Python) | 开源 | 免费 | Python | ⭐⭐⭐⭐⭐ |
| docxtemplater Enterprise (Node.js) | 商业 | €3k/yr | Node.js | ⭐⭐⭐⭐ |
| Carbone.io | 商业 | 按量计费 | Node.js | ⭐⭐⭐ |
| Aspose.Words | 商业 | $1.2k+ | 多语言 | ⭐⭐⭐ |
| python-docx (纯底层) | 开源 | 免费 | Python | ⭐⭐（需要自己写渲染逻辑） |

---

## 4. 最终推荐：真母版驱动

### 核心思路

```
Word 设计师模板 (.docx)     JSON 数据源        docxtpl 引擎
─────────────────────     ──────────        ────────────
封面（品牌色+Logo+文本框）  product.json       ┌─ 读模板 .docx
目录页（占位符）            images.json        ├─ 注入 JSON 数据
章节页（样式+占位符）        chapters/*.json    ├─ 替换文本/图片/表格
├─ 标题样式                compiled/*.json    ├─ 处理循环/条件
├─ 正文样式                brand-themes.json  └─ 输出最终 .docx
├─ 表格样式
├─ 图片占位符
├─ 警告框样式
├─ 步骤样式
└─ 保修卡样式
```

### 为什么选 docxtpl

1. **完全匹配当前架构**：JSON 单源已经存在，只需要换渲染器
2. **设计与代码分离**：设计师用 Word 做模板，开发者只写数据注入脚本
3. **品牌定制零代码**：换品牌 = 换模板文件，不改任何代码
4. **免费**：MIT 许可
5. **稳定**：python-docx 底层经过大量生产验证

### 迁移路径

1. **Phase 1**：设计 A5 Word 母版模板（1 个中文基线 + 品牌色变量位）
2. **Phase 2**：写 Python 渲染脚本读取现有 JSON 数据 → docxtpl 注入
3. **Phase 3**：用 V23 CN Wevac 做 PoC 验证
4. **Phase 4**：全变体覆盖（7 regions × 3 brands）
5. **Phase 5**：替换现有 export-docx.js

### 与用户（大boss）方向对齐确认

大boss 提出的"真母版驱动"愿景：
> 用户在 Word 中设计好包含品牌元素的专业模板，程序只负责往里面注入内容数据

**结论**：与四方向研究结论 100% 一致。行业标准范式就是如此。

---

## 5. 国内方案补充调研

### 5.1 poi-tl（poi-template-language）⭐⭐⭐⭐⭐

- **出处**：中国开发者 Sayi（深圳），GitHub 5k+ stars，Apache 2.0 许可
- **仓库**：https://github.com/Sayi/poi-tl
- **生态**：Java，基于 Apache POI
- **最新版**：v1.12.2（2024-01）
- **中文文档**：http://deepoove.com/poi-tl

**核心能力**：
- `{{variable}}` — 文本替换（保留模板样式）
- `{{@image}}` — 图片替换
- `{{#table}}` — 表格渲染
- `{{*list}}` — 项目符号/编号列表
- `{{?section}}...{{/section}}` — 条件/循环（类似 Mustache）
- `{{+nested}}` — 子文档合并（模板嵌套）
- **文本框内支持标签**
- **支持 SpringEL 表达式**，可扩展 OGNL、MVEL
- **支持自定义插件**，可在文档任意位置执行自定义函数
- **Markdown → Word 插件**
- **代码高亮插件**

**与 docxtpl (Python) 对比**：

| 维度 | poi-tl (Java) | docxtpl (Python) |
|------|--------------|-----------------|
| 模板语法 | Mustache 风格 `{{}}` | Jinja2 风格 `{{}}` |
| 文本框支持 | ✅ 原生支持 | ✅ 支持 |
| 图片注入 | ✅ `{{@img}}` | ✅ `InlineImage()` |
| 循环/条件 | ✅ Section 语法 | ✅ Jinja2 for/if |
| 子文档 | ✅ `{{+nested}}` | ✅ `subdoc` |
| 自定义插件 | ✅ 强大的插件体系 | ❌ 无 |
| 社区活跃度 | 5k stars，活跃 | 2k stars，活跃 |
| 中文文档 | ✅ 完整中文文档 | ❌ 英文为主 |
| 语言生态 | Java（需 JVM） | Python |

**评估**：poi-tl 是国内最成熟的 Word 模板引擎，中文文档完善，社区活跃，功能比 docxtpl 更强大（尤其是插件体系和子文档合并）。但需要 Java 运行环境。

### 5.2 冰蓝科技 Spire.Doc ⭐⭐⭐

- **出处**：成都冰蓝科技（E-iceblue），国产商业软件
- **官网**：https://www.e-iceblue.cn/Introduce/Spire-Doc-JAVA.html
- **生态**：Java / .NET / Python / C++ / JavaScript 全覆盖
- **授权**：商业付费（免费版有限制：转换≤3页，文档≤500段落等）

**核心能力**：
- 独立运行，不需要 Microsoft Office
- 兼容国产操作系统（中标麒麟、中科方德）
- 支持 WPS 格式（.wps / .wpt）
- 邮件合并（Mail Merge）— 类似 Word 原生邮件合并
- 查找替换、书签操作、域操作
- Word → PDF / HTML / Image / XPS / EPUB / SVG / OFD 转换
- 表单域创建和填充
- 文档比较、数字签名、加密解密

**评估**：功能全面，是真正的"Word SDK"级别产品。但作为商业产品价格不透明（需要询价），且核心场景是"文档处理"而非"模板引擎"。邮件合并功能可以做模板注入，但不如 poi-tl 的模板语法灵活。适合需要在服务端做 Word 全系列操作的企业场景。

### 5.3 WPS 开放平台

- **出处**：金山办公（Kingsoft）
- **官网**：https://open.wps.cn
- **定位**：SaaS 平台，非本地 SDK

**核心能力**：
- 文档在线预览和编辑（WebOffice）
- 多人实时协同编辑
- WPS 客户端二次开发（加载项 / 宏）
- WPS 文档中台

**评估**：WPS 开放平台主要面向"在线协同办公"场景，不适合我们的"本地批量生成 DOCX"需求。如果未来有"让 ODM 客户在线编辑说明书"的需求，可以考虑集成。但当前阶段不适用。

### 5.4 其他国内方案概览

| 名称 | 类型 | 语言 | 特点 | 适合性 |
|------|------|------|------|--------|
| EasyPoi | 开源 | Java | 主打 Excel，Word 功能弱 | ❌ 不适合 |
| Hutool OfficeUtil | 开源 | Java | 工具集中的轻量 Word 封装 | ❌ 太轻量 |
| 永中 Office SDK | 商业 | Java | 国产全套 Office SDK | 💰 价格不透明，生态小 |
| 万兴 PDF 元素 | 商业 | 多语言 | 主打 PDF，非 DOCX | ❌ 非目标 |
| OpenKM/Alfresco | 开源 | Java | 文档管理系统，非模板引擎 | ❌ 不适合 |

### 5.5 国内方案总结

**国内首选**：**poi-tl**。理由：
1. 功能最强大的开源 Word 模板引擎（全球范围内也是 top 级）
2. 完整中文文档，国内社区活跃
3. 模板语法直觉友好，设计师可以直接在 Word 中编辑
4. 插件体系支持高级定制
5. Apache 2.0 许可，完全免费

**唯一的考量**：poi-tl 是 Java 生态。当前工具链是 Node.js（export-docx.js）。如果要用 poi-tl，有两条路：
- **A. Java 独立脚本**：写一个 Java 命令行工具，Node.js 通过 child_process 调用
- **B. 切到 Python 的 docxtpl**：Python 也可以通过 child_process 调用，且 Python 在项目中已有使用

---

## 6. 最终方案比较矩阵（国内外合并）

| 方案 | 语言 | 授权 | 价格 | 模板保真 | 中文支持 | 推荐度 |
|------|------|------|------|---------|---------|--------|
| **poi-tl** | Java | Apache 2.0 | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **🥇** |
| **docxtpl** | Python | MIT | 免费 | ⭐⭐⭐⭐ | ⭐⭐⭐ | **🥈** |
| docxtemplater Enterprise | Node.js | 商业 | €3k/yr | ⭐⭐⭐⭐⭐ | ⭐⭐ | 🥉 |
| Spire.Doc | 多语言 | 商业 | 询价 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Carbone.io | Node.js | 商业 | 按量 | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Aspose.Words | 多语言 | 商业 | $1.2k+ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| docx npm（当前） | Node.js | MIT | 免费 | ⭐⭐ | ⭐⭐ | ❌ 已到天花板 |

---

## 7. 未确定事项

- [ ] 工具链选择：poi-tl (Java) vs docxtpl (Python) vs docxtemplater Enterprise (Node.js, €3k/yr)？
- [ ] 是否需要同时支持多套品牌模板（Wevac / Vesta / Act 各一套 Word 模板）？
- [ ] 模板中的图片占位符格式：用 Jinja2 标签还是用特定占位图？
- [ ] 目录页是否需要自动生成真正的 Word TOC 字段？
- [ ] 迁移期间 export-docx.js 是否保留作为 fallback？

---

## 8. 附：研究过程

- 创建了 git worktree：`.worktrees/research-docx-gen`（branch: `research/docx-generation-logic`）
- 用 `scripts/office/unpack.py` 解压现有 DOCX 检查 XML 结构
- 创建 4 个临时研究 agent 分别调研 4 个方向：
  - `docx-research-pydocx.md` — python-docx / docxtpl 模板注入
  - `docx-research-npm.md` — docx npm 高级技巧
  - `docx-research-convert.md` — HTML→DOCX 转换工具
  - `docx-research-industry.md` — 行业最佳实践
- 每个 agent 返回 11-17KB 研究报告，综合后形成本文档
