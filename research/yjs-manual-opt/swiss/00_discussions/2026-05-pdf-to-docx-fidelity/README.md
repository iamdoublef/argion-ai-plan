# PDF → DOCX 高保真还原实验

**Goal**: 把 `imt050-wevac-eu-cn.pdf` 复刻为视觉 1:1 的 .docx，并把胜出路径固化为工作流。

## 输入与目标

| 资产 | 路径 | 大小 |
|---|---|---|
| 目标 PDF | `swiss/output/imt050-wevac-eu-cn.pdf` | 914 KB |
| 源 HTML | `swiss/output/imt050-wevac-eu-cn.html` | 46 KB |
| 现有 DOCX | `swiss/output/imt050-wevac-eu-cn.docx` | 571 KB（30/3 生成） |
| 源 JSON 内容 | `swiss/products/imt050/...` | - |
| 现有工具 | `swiss/tools/export-docx.js` | 1646 行 |

PDF 由 HTML + puppeteer 渲染（`export-pdf.js`）。DOCX 由 docx-js 9.6.0 直接从 JSON 构建。二者**完全是两条独立链路**，所以视觉差异预期较大。

## 工具链清单（已验证可用）

- LibreOffice: `C:\Program Files\LibreOffice\program\soffice.exe` ✓
- Node 22 + docx-js 9.6.0 ✓
- Python 3.12 + PyMuPDF 1.26.6 + python-docx 1.2.0 ✓
- pandoc 3.9.0.2 ✓
- Playwright + sharp ✓

需要按需安装：pdf2docx（Codex 路径用）、Aspose / Spire（备用商业转换器）。

## 双路径策略

### 路径 A — Claude 主控（HTML→DOCX 重建优化）
- 走 **JSON → docx-js → DOCX** 重建链路（复用 `export-docx.js`）
- 通过 `/docx` skill 的 unpack/edit/pack 流程做 XML 级精细微调
- 像素级对齐：A5 页面（148×210mm）、字体（Arial + 宋体）、行距、表格样式、figure 尺寸
- 主要解决：分页一致、表格边框、图片定位、页眉页脚

### 路径 B — Codex 副控（PDF 直转 DOCX 新方案）
- 由 `codex-batch-executor` 调度 Codex CLI 独立尝试
- 候选技术：
  1. `pdf2docx` (Python, 直接 PDF→DOCX)
  2. LibreOffice headless 直接 convert-to docx
  3. mammoth.js / docx2pdf 反向
  4. 商业 SDK (Aspose, Spire) 评估
- 与 Claude 路径平行不交叉，最后用同一套对比工具裁决

### 裁决标准
1. 用 LibreOffice 把 DOCX 转 PDF
2. 用 PyMuPDF 把两个 PDF 渲染为 200dpi PNG
3. 逐页生成并排对比图 + 差异热力图
4. 量化指标：页数一致、文本/图片定位、关键样式（色块、accent line、表格边框）

## 目录约定

```
2026-05-pdf-to-docx-fidelity/
├── README.md             # 本文件
├── log.md                # 实验流水
├── baseline/             # 第 1 步：基线（target PDF + 当前 DOCX 渲染图）
├── path-a-claude/        # Claude 路径产物（每个 iteration 一个子目录）
├── path-b-codex/         # Codex 路径产物
├── screenshots/          # 对比图、热力图
└── final/                # 胜出版本 + 复用工作流
```

## 失败兜底

如双路径都无法做到 1:1：
- 回退到"功能等价"——保留可编辑性 + 视觉接近度 ≥85%
- 标注无法还原的元素（如 SVG 渐变、puppeteer 字距）
- 把无法还原项写入"已知限制"列表，方便人工微调

