# SOP：Swiss 说明书 JSON 单源生产流程

## 目的

把 Swiss 说明书统一到一条稳定生产线：

- 源头只认 JSON 和图片
- 正式输出只认 HTML 和 PDF
- PDF 用于审稿和交付
- 若发生 PDF hotfix，下一版必须回写 JSON

本 SOP 适用于 `research/yjs-manual-opt/swiss/` 当前 A5 共享母版体系。

## 当前范围

- 本 SOP 适用于现有产品线维护和新产品首版接入
- 本轮不包含 Excel 主源
- 本轮不包含 DOCX 主链
- 本轮不包含 AI 自动生产导入
- 如果后续引入模型，只允许生成草稿，不允许绕过人工确认直接发布

## 正式输入

每个产品只认下面 4 类正式输入：

- `products/<product>/product.json`
- `products/<product>/images.json`
- `products/<product>/content/<lang>/manifest.json`
- `products/<product>/content/<lang>/chapters/*.json`

说明：

- `product.json`：品牌、型号、参数、按钮、部件、区域/语言矩阵等扁平事实
- `images.json`：语义图片清单与文件映射
- `manifest.json`：章节顺序、目录标题、页眉引用、启用状态
- `chapters/*.json`：单章正文结构

不再使用：

- `config.json`
- `content.<lang>.json`
- 模板内正文
- `CONTENT_BODY`

## 正式输出

- `output/*.html`
- `output/*.pdf`
- `output/*audit*`

说明：

- HTML 只用于技术预览和排错
- PDF 才是业务审稿和交付界面
- booklet 不再是硬验收项，只作为兼容性附加产物

## 目录结构

```text
products/<product>/
├─ product.json
├─ images.json
├─ images/
└─ content/
   ├─ cn/
   │  ├─ manifest.json
   │  └─ chapters/
   ├─ en/
   │  ├─ manifest.json
   │  └─ chapters/
   ├─ de/
   │  ├─ manifest.json
   │  └─ chapters/
   └─ it/
      ├─ manifest.json
      └─ chapters/
```

## 内容规则

### 1. 章节来源

- 章节顺序、目录文字、页眉引用只认 `manifest.json`
- 每章正文只认 `chapters/*.json`
- 章节数量和顺序由内容数据决定，不写死在模板里

### 2. block 类型

正式内容只允许：

- `paragraph`
- `bullet_list`
- `warning_box`
- `caution_box`
- `notice_box`
- `sub_title`
- `figure`
- `figure_row`
- `step_flow`
- `table_ref`
- `qa_list`
- `contact_block`
- `warranty_card`
- `split_panel`

禁止：

- `html_fragment`
- 原始 HTML 片段

### 3. 文本 token

文本字段只允许：

- `**粗体**`
- `[btn:按钮名]`
- `\n`

不允许：

- `<b>...</b>`
- `<span>...</span>`
- 任何其他原始 HTML 标签

### 4. 图片规则

- `images.json` 使用语义图片 ID，不直接在正文里写 `image14.png`
- 程序性图片必须标记：
  - `kind: "procedural"`
  - `usage_ref`
- `usage_ref` 格式固定为：
  - `chapter_id.page_key.step_id`
  - 或 `chapter_id.page_key.block_id`
- shared 装饰图单独标记为 `kind: "shared"`

## 新产品首版流程

### Step 1：准备事实资料

准备以下材料：

- 简版 Word / 源稿
- 产品图片
- 参数资料
- 品牌与售后信息

### Step 2：建立产品目录

创建：

- `product.json`
- `images.json`
- `content/<lang>/manifest.json`
- `content/<lang>/chapters/*.json`
- `images/`

### Step 3：录入产品事实

在 `product.json` 中填写：

- 型号
- 品牌信息
- 区域/语言矩阵
- 规格参数
- 按钮表
- 部件表
- 保修年限

### Step 4：录入正文内容

在 `manifest.json` 中定义：

- `chapter_id`
- `chapter_no`
- `title`
- `toc_title`
- `header_ref`
- `enabled`
- `file`

在 `chapters/*.json` 中定义：

- 页面
- block
- 步骤
- 图片绑定

### Step 5：录入图片映射

在 `images.json` 中登记：

- 语义图片 ID
- 实际文件名
- alt
- kind
- usage_ref

### Step 6：构建 HTML

```powershell
cd D:\work\private\yjsplan\research\yjs-manual-opt\swiss
node tools/build-variant.js --product products/<product> --region cn
```

### Step 7：导出 PDF

```powershell
node tools/export-pdf.js output/<product>-<brand>-<market>-<region>.html
```

### Step 8：运行视觉审计

```powershell
node tools/_audit-visual.js output/<product>-<brand>-<market>-<region>.html
```

### Step 9：人工抽检 PDF

必须抽检这些关键页：

- 封面
- 目录
- 安全第一页
- 结构 / 控制面板页
- 操作页
- 保修页
- 保修卡续页

### Step 10：批量导出

确认单变体通过后，再跑全矩阵：

```powershell
node tools/build-variant.js --product products/<product> --all
node tools/export-pdf-batch.js
```

## 旧产品修改流程

旧产品维护只改：

- `product.json`
- `images.json`
- `content/<lang>/manifest.json`
- `content/<lang>/chapters/*.json`
- 产品图片目录

不改：

- 模板正文
- 旧 `config.json`
- 旧 `content.<lang>.json`

改完后固定走：

1. 重建 HTML
2. 重导 PDF
3. 跑视觉审计
4. 抽检关键页

## PDF hotfix 规则

- 允许在临出货前对 PDF 做极少量应急修补
- 但 PDF 不是正式源头
- 所有 hotfix 必须登记，并在下一版回写 JSON

禁止形成：

- PDF 一套
- JSON 一套
- 模板又一套

## 验收标准

- A5 共享母版视觉统一
- 所有内容来自 JSON 单源
- 无旧入口依赖
- 无 raw HTML
- 无 `html_fragment`
- 无横向顶出
- 无图片变形
- 无保修卡裁切
- 程序性图片与步骤一一对应
