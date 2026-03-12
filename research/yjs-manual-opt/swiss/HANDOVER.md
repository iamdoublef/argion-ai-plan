# Swiss 说明书系统交接文档

**日期**：2026-03-12
**交接范围**：`research/yjs-manual-opt/swiss/` 下的 A5 说明书生产系统

---

## 一、系统定位

Swiss 说明书系统是亚俊氏产品说明书的生产线，采用 JSON 单源驱动、多变体输出（HTML/PDF/DOCX），支持 7 地区 × 3 品牌 = 21 种组合的说明书批量生成。

**详细操作指南**请阅读：`research/yjs-manual-opt/swiss/operation-manual.md`

---

## 二、环境准备

### 2.1 克隆仓库

```bash
git clone <仓库地址>
```

### 2.2 安装 Node.js

要求 Node.js 18+。

### 2.3 安装依赖

在仓库根目录执行：

```powershell
npm install
```

依赖清单（已在根目录 `package.json` 中声明）：

| 包名 | 版本 | 用途 |
|------|------|------|
| `playwright` | ^1.58.2 | PDF 导出 + 视觉审计 |
| `docx` | ^9.6.0 | DOCX 导出 |
| `sharp` | ^0.34.5 | 图片处理 |
| `xlsx` | ^0.18.5 | 翻译工作簿读写 |

### 2.4 安装 Playwright 浏览器

```powershell
npx playwright install chromium
```

### 2.5 验证环境

```powershell
cd research/yjs-manual-opt/swiss

# 构建一个变体
node tools/build-variant.js --product products/v23 --region cn

# 导出 PDF
node tools/export-pdf.js output/v23-wevac-eu-cn.html

# 运行审计
node tools/audit-visual.js output/v23-wevac-eu-cn.html
```

如果以上 3 条命令均无报错，环境准备完成。

---

## 三、交付物清单

### 3.1 核心文件（全部在仓库内）

| 类别 | 路径 | 说明 |
|------|------|------|
| **操作手册** | `swiss/operation-manual.md` | 角色定义、AI 操作指南、命令速查 |
| **视觉标准** | `swiss/DESIGN-STANDARD.md` | 唯一视觉基准（色彩、字体、布局） |
| **审计规则** | `swiss/QA-RULES.md` | 5 阶段审计流程 |
| **生产流程** | `swiss/SOP-new-product.md` | 新产品接入 + 维护流程 |
| **Word 规范** | `swiss/WORD-BASE-TEMPLATE-CN.md` | DOCX 母版规范 |

### 3.2 产品数据

| 产品 | 路径 |
|------|------|
| V23 | `swiss/products/v23/` |
| IMT050 | `swiss/products/imt050/` |

每个产品下包含：
- `product.json` — 产品事实
- `images.json` — 图片映射
- `images/` — 产品图片
- `content/source/` — 章节结构 JSON
- `i18n/compiled/` — 编译后的译文 JSON
- `i18n/workbooks/` — 翻译工作簿 Excel

### 3.3 模板

| 文件 | 说明 |
|------|------|
| `swiss/template/v23-master-{cn,en,de,it}.html` | V23 各语言母版 |
| `swiss/template/imt050-master-{cn,en,de,it}.html` | IMT050 各语言母版 |
| `swiss/template/shared/base/` | 共享 CSS + 品牌主题 |
| `swiss/template/shared/docx/base-template-cn.docx` | Word 基础母版 |

### 3.4 工具链

| 工具 | 路径 | 用途 |
|------|------|------|
| `build-variant.js` | `swiss/tools/` | 单变体 HTML 构建 |
| `build-all.js` | `swiss/tools/` | 批量构建 + 自动审计 |
| `export-pdf.js` | `swiss/tools/` | 单文件 PDF 导出 |
| `export-pdf-batch.js` | `swiss/tools/` | 批量 PDF 导出 |
| `export-docx.js` | `swiss/tools/` | DOCX 导出 |
| `audit-visual.js` | `swiss/tools/` | Playwright 视觉审计 |
| `export-translation-workbook.js` | `swiss/tools/` | JSON → 翻译工作簿 |
| `compile-translation-workbook.js` | `swiss/tools/` | 翻译工作簿 → JSON |
| `sync-json-to-workbook.js` | `swiss/tools/` | compiled JSON → 工作簿反写 |

### 3.5 规范资产

| 文件 | 路径 | 用途 |
|------|------|------|
| 品牌语言指南 | `swiss/standards/brand-language-guide.md` | 品牌文案规范 |
| 术语表 | `swiss/standards/terminology-glossary.json` | 术语统一 |
| 单位规范 | `swiss/standards/unit-and-measurement-policy.md` | 单位格式 |
| 警示语规范 | `swiss/standards/warning-language-policy.md` | 安全措辞 |
| 本地化指南 | `swiss/standards/locale-guides.json` | 各语言本地化 |
| AI 结构 prompt | `swiss/standards/ai-new-product-structure-prompt.md` | 新产品结构草稿 |
| AI 翻译 prompt | `swiss/standards/ai-translation-draft-prompt.md` | 翻译初稿 |
| AI 审计 prompt | `swiss/standards/ai-localization-audit-prompt.md` | 本地化质检 |

### 3.6 AI Agent & Skill

| 类型 | 名称 | 路径 | 用途 |
|------|------|------|------|
| Agent | `swiss-manual-writer` | `.claude/agents/swiss-manual-writer.md` | 生成/重构/修复 |
| Agent | `swiss-content-auditor` | `.claude/agents/swiss-content-auditor.md` | 内容与版式审计 |
| Skill | `swiss-manual-a5` | `swiss/skills/swiss-manual-a5/SKILL.md` | 主技能定义 |
| Skill | `swiss-issue-fix` | `swiss/skills/swiss-issue-fix/SKILL.md` | 问题修复决策树 |

### 3.7 路由配置

| 文件 | 路径 | 说明 |
|------|------|------|
| AGENTS.md | 仓库根目录 | Swiss 路由规则在"Swiss 说明书 Skill 路由"章节 |

---

## 四、AI 工具使用（给接手人）

### 4.1 使用 Claude Code（推荐）

在仓库目录下启动 Claude Code，Agent 和 Skill 会自动被识别。

**示例对话**：
```
用户：使用 swiss-manual-writer agent，帮我给 V23 的中文版重建 HTML。
AI：（自动读取 SKILL.md → DESIGN-STANDARD.md → 产品数据 → 构建）
```

### 4.2 使用 VS Code Copilot Chat

1. 打开仓库文件夹
2. `.claude/agents/` 下的 agent 文件会被 Copilot Chat 自动识别
3. 在 Chat 中可以 `@swiss-manual-writer` 或直接描述任务

### 4.3 使用其他 AI 工具

如果使用不支持 Agent/Skill 自动加载的工具：

1. 先手动把以下文件内容喂给模型：
   - `swiss/skills/swiss-manual-a5/SKILL.md`（主技能）
   - `swiss/DESIGN-STANDARD.md`（视觉标准）
   - `swiss/QA-RULES.md`（审计规则）
2. 然后描述你的任务
3. 模型会按 SKILL.md 中定义的流程执行

---

## 五、日常维护流程

### 5.1 产品内容更新

```
定位要改的 JSON → 修改 → 编译译文 → 构建 HTML → 导出 PDF → 审计 → 抽检
```

详见 `operation-manual.md` §四 B 节。

### 5.2 新产品接入

```
准备源稿 → AI 生成结构草稿 → 人工确认事实 → 建立 JSON → 导出工作簿 → 翻译 → 编译 → 构建 → 审计 → 批量生成
```

详见 `operation-manual.md` §四 A 节。

### 5.3 翻译更新

```
翻译人员改工作簿 → 编译 → 构建 → 导出 PDF → 审计
```

详见 `operation-manual.md` §四 D 节。

---

## 六、注意事项

### 6.1 关键风险

| 风险 | 说明 | 对策 |
|------|------|------|
| 译文覆盖 | `compile-translation-workbook.js` 以工作簿为准覆盖 compiled JSON | 修改 JSON 后先用 `sync-json-to-workbook.js` 反写 |
| PDF hotfix 断链 | 直接改 PDF 而不回写 JSON | 所有 hotfix 必须登记并回写结构源 |
| DE/IT 溢出 | 德语/意大利语文本比中文长 20-30% | 语言补偿 CSS + compact 类 + 拆页 |
| 审计退出码不可靠 | Playwright stderr 可能触发非零退出码 | 判定以 stdout 中 `ALL CHECKS PASSED` 为准 |

### 6.2 禁止事项

- ❌ 在模板里直接写正文（必须来自 JSON）
- ❌ 使用 `html_fragment` block 类型
- ❌ 用 `width:100%` 设置封面图尺寸（用 `max-width`）
- ❌ 把 `zh-HK`/`zh-TW` 做成 `zh-CN` 的简转繁
- ❌ 缩减三级警示体系（WARNING / CAUTION / NOTICE 缺一不可）
- ❌ 按产品复制 Word 模板（统一用 `base-template-cn.docx`）

### 6.3 联系方式

如遇到无法解决的问题，操作手册 FAQ 无法覆盖的场景，请联系[原维护人]。

---

## 七、阅读顺序建议

刚接手建议按以下顺序阅读：

1. **本文件**（交接文档，了解全貌）
2. `swiss/operation-manual.md`（操作手册，了解怎么用）
3. `swiss/SOP-new-product.md`（标准流程，了解怎么做）
4. `swiss/DESIGN-STANDARD.md`（视觉标准，了解长什么样）
5. `swiss/QA-RULES.md`（审计规则，了解怎么验收）
6. `swiss/skills/swiss-manual-a5/SKILL.md`（AI 技能，了解 AI 怎么工作）
