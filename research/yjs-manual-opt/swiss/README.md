# Swiss 说明书系统

A5 竖版产品说明书生产系统 —— JSON 单源驱动、多变体输出。

## 快速了解

| 你想做什么 | 看哪个文件 |
|-----------|-----------|
| **刚接手，从零开始** | [HANDOVER.md](HANDOVER.md) |
| **日常操作（角色、AI 指令、命令）** | [operation-manual.md](operation-manual.md) |
| **新产品接入 / 内容维护流程** | [SOP-new-product.md](SOP-new-product.md) |
| **视觉设计标准** | [DESIGN-STANDARD.md](DESIGN-STANDARD.md) |
| **审计规则与流程** | [QA-RULES.md](QA-RULES.md) |
| **DOCX 母版规范** | [WORD-BASE-TEMPLATE-CN.md](WORD-BASE-TEMPLATE-CN.md) |
| **系统架构全景** | [SYSTEM-DESIGN.md](SYSTEM-DESIGN.md) |

## 系统概览

```
                    ┌─────────────┐
                    │  JSON 内容源  │  product.json + images.json + chapters/*.json
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │  译文 Catalog │  i18n/compiled/*.json ← i18n/workbooks/*.xlsx
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ HTML 构建 │ │ PDF 导出  │ │ DOCX 导出 │
        └──────────┘ └──────────┘ └──────────┘
              │            │            │
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ 技术预览  │ │ 自有品牌  │ │ ODM 客户  │
        │ + 定位问题│ │ 正式交付  │ │ 可编辑交付│
        └──────────┘ └──────────┘ └──────────┘
```

## 变体矩阵

- **页面**：A5 竖版 148mm × 210mm
- **地区**：cn / hk / tw / gb / za / de / it（7 个）
- **品牌**：wevac / vesta / act（3 个）
- **最多**：7 × 3 = 21 种变体

## 当前产品

| 产品 | 目录 | 说明 |
|------|------|------|
| V23 | `products/v23/` | 真空封口机 |
| IMT050 | `products/imt050/` | 制冰机 |

## 常用命令

```powershell
cd research/yjs-manual-opt/swiss

# 构建单变体 HTML
node tools/build-variant.js --product products/v23 --region cn

# 导出 PDF
node tools/export-pdf.js output/v23-wevac-eu-cn.html

# 导出 DOCX（ODM 用）
node tools/export-docx.js --product products/v23 --region cn

# 视觉审计
node tools/audit-visual.js output/v23-wevac-eu-cn.html

# 批量构建全矩阵 + 审计
node tools/build-all.js --product v23
```

## AI Agent

| Agent | 用途 | 触发方式 |
|-------|------|---------|
| `swiss-manual-writer` | 生成 / 重构 / 修复 | "使用 swiss-manual-writer agent" |
| `swiss-content-auditor` | 内容与版式审计 | "使用 swiss-content-auditor agent" |

## 目录结构

```
swiss/
├── README.md              ← 本文件
├── HANDOVER.md            ← 交接文档
├── operation-manual.md    ← 操作手册
├── DESIGN-STANDARD.md     ← 视觉标准
├── QA-RULES.md            ← 审计规则
├── SOP-new-product.md     ← 生产流程
├── WORD-BASE-TEMPLATE-CN.md ← Word 规范
├── SYSTEM-DESIGN.md       ← 系统设计
├── products/              ← 产品数据（JSON + 图片 + 译文）
├── template/              ← HTML 母版 + 共享 CSS + Word 母版
├── tools/                 ← 构建 / 导出 / 审计工具链
├── standards/             ← 术语、品牌、单位、警示语规范
├── skills/                ← AI Skill 定义
├── tests/                 ← 测试套件
├── output/                ← 生成产物（HTML/PDF/DOCX）
└── _archived/             ← 归档文件
```
