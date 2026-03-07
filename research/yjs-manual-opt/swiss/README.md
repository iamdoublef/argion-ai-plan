# Swiss 说明书模板系统

基于 V23 Swiss 风格说明书（已审计 PASS）的模板化生产系统。

## 目录结构

```
swiss/
├── template/           ← 母版 HTML（含 {{占位符}}）
├── products/v23/       ← 产品配置 + 图片
├── output/             ← 构建输出（HTML + PDF）
├── tools/              ← 构建脚本
└── README.md
```

## 快速使用

### 场景 1：切换品牌（WEVAC → Vesta）

```bash
node tools/build-variant.js --brand vesta
```

### 场景 2：切换市场（欧标 → 美标）

```bash
node tools/build-variant.js --market us
```

### 场景 3：组合切换

```bash
node tools/build-variant.js --brand act --market us
```

### 场景 4：导出 PDF

```bash
node tools/export-pdf.js output/v23-wevac-eu-cn.html
```

## 新产品流程

1. 复制 `products/v23/` → `products/{新型号}/`
2. 修改 `config.json`（型号、参数、图片、按键等）
3. 替换 `images/` 目录下的产品图片
4. 复制母版 HTML，编辑 `@CONTENT` 区域内容
5. 运行 `build-variant.js` → `export-pdf.js` → 审计

## 模板占位符说明

- `{{brand.display_name}}` — 品牌显示名
- `{{product.model}}` — 产品型号
- `{{product.name_cn}}` — 中文产品名
- `{{#SPECS_TABLE_ROWS}}` — 技术参数表（从 config 生成）
- `{{#PARTS_TABLE_ROWS}}` — 零件表（从 config 生成）
- `{{#BUTTONS_TABLE_ROWS}}` — 按键功能表（从 config 生成）
- `{{#BRAND_INFO_ROWS}}` — 品牌商信息表
- `{{#MANUFACTURER_INFO_ROWS}}` — 制造商信息表
- `<!-- @CONTENT:xxx:start/end -->` — 人工编辑区域标记
