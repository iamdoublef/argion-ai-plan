# yjs-manual-opt

当前正式主链已经收口为：**初稿 Word / 参考手册 -> JSON 结构源 + 译文工作簿 -> DOCX（ODM） / HTML+PDF（自有品牌）**。

## 当前目录

```text
research/yjs-manual-opt/
  INDEX.md
  _inbox/                          -> 原始 Word / 参考手册输入
  swiss/                           -> 正式生产线
```

## 当前正式入口

- 输入源：
  - `research/yjs-manual-opt/_inbox/`
  - `research/yjs-manual-opt/swiss/products/<product>/product.json`
  - `research/yjs-manual-opt/swiss/products/<product>/images.json`
  - `research/yjs-manual-opt/swiss/products/<product>/content/source/manifest.json`
  - `research/yjs-manual-opt/swiss/products/<product>/content/source/chapters/*.json`
  - `research/yjs-manual-opt/swiss/products/<product>/i18n/workbooks/<locale>.xlsx`
  - `research/yjs-manual-opt/swiss/products/<product>/i18n/compiled/<locale>.json`
- 输出：
  - 自有品牌：`HTML + PDF`
  - ODM：`DOCX + PDF`

## 阶段节点

### 2026-03 DOCX 美化方案四方向研究完成，确认"真母版驱动"范式
commit: uncommitted
四方向研究（python-docx/docxtpl、docx npm 高级技巧、HTML→DOCX 转换、行业最佳实践）完成。结论：Word 模板 + 模板引擎注入是行业标准范式，推荐 docxtpl (Python, 免费) 或 docxtemplater Enterprise (Node.js, €3k/yr)。当前 docx npm 程序式生成已触及天花板，HTML→DOCX 转换因 CSS 无法映射到 OOXML 而不可行。与大boss 方向对齐确认。
- ptr: `file:research/yjs-manual-opt/swiss/00_discussions/2026-03-docx-beautification-research.md`
- ptr: `file:.claude/agents/docx-research-pydocx.md`
- ptr: `file:.claude/agents/docx-research-npm.md`
- ptr: `file:.claude/agents/docx-research-convert.md`
- ptr: `file:.claude/agents/docx-research-industry.md`

### 2026-03 swiss-issue-fix Skill 创建
commit: uncommitted
补写了 Swiss 说明书问题修复 skill，覆盖 6 大问题类型（溢出、图片、翻译、分页、DOCX 特有、构建失败）决策树和标准修复流程。含 5 个 eval 测试用例。
- ptr: `file:research/yjs-manual-opt/swiss/skills/swiss-issue-fix/SKILL.md`
- ptr: `file:research/yjs-manual-opt/swiss/skills/swiss-issue-fix/evals/evals.json`

### 2026-03-12 V23 当前批准版反向固化为产品线基线
commit: worktree
当前 `V23` 已确认的中文批准版被固化为产品线基线；产品特征经验沉淀到 `products/v23/README.md`，本次提炼出的图片尺寸、保修分页、rowspan 错位、单位一致性等共性规则回写到公共规范，供后续 `V23` 其他品牌/地区/翻译版本直接复用。
- ptr: `research/yjs-manual-opt/swiss/products/v23/README.md`
- ptr: `research/yjs-manual-opt/swiss/DESIGN-STANDARD.md`
- ptr: `research/yjs-manual-opt/swiss/QA-RULES.md`

### 2026-03-11 Swiss JSON 单源 + 双渲染器正式落地
commit: 9effce9
说明书正式切到 JSON 单源，结构、图片、译文和品牌主题分层；自有品牌走 `HTML + PDF`，ODM 走 `DOCX + PDF`，翻译人员只改译文工作簿，不再碰 HTML。
- ptr: `git:9effce9:research/yjs-manual-opt/swiss/SOP-new-product.md`
- ptr: `git:9effce9:research/yjs-manual-opt/swiss/tools/build-variant.js`
- ptr: `git:9effce9:research/yjs-manual-opt/swiss/tools/export-docx.js`
- ptr: `git:9effce9:research/yjs-manual-opt/swiss/products/imt050/product.json`
- ptr: `git:9effce9:research/yjs-manual-opt/swiss/products/v23/product.json`

### 2026-03-11 中文 Word 母版基线定型
commit: 4c587f0
中文 Word 支线从“PDF 影子稿”改成 A5 可编辑母版支线，固定单一 Word 母版骨架 + 品牌主题包，后续新产品默认在这套骨架上微调内容和图片。
- ptr: `git:4c587f0:research/yjs-manual-opt/swiss/WORD-BASE-TEMPLATE-CN.md`
- ptr: `git:4c587f0:research/yjs-manual-opt/swiss/template/shared/docx/base-template-cn.docx`

### 2025-07-08 QA 生产线工具链 TDD 落地（6 项 Work Item）
commit: a496c44
TDD 方式完成 QA 全链路：DESIGN-STANDARD §十七 内容结构约束（10条规则）+ QA-RULES.md 审计流程；4 个自动化工具（audit-visual / build-all / compile --check-lang / sync-json-to-workbook）；Writer/Auditor agent 指令更新。31 个测试全绿。
- ptr: `git:a496c44:research/yjs-manual-opt/swiss/DESIGN-STANDARD.md`
- ptr: `git:a496c44:research/yjs-manual-opt/swiss/QA-RULES.md`
- ptr: `git:a496c44:research/yjs-manual-opt/swiss/tools/audit-visual.js`
- ptr: `git:a496c44:research/yjs-manual-opt/swiss/tools/build-all.js`
- ptr: `git:a496c44:research/yjs-manual-opt/swiss/tools/compile-translation-workbook.js`
- ptr: `git:a496c44:research/yjs-manual-opt/swiss/tools/sync-json-to-workbook.js`
- ptr: `git:a496c44:research/yjs-manual-opt/swiss/tests/`
- ptr: `git:4c587f0:research/yjs-manual-opt/swiss/tools/export-docx.js`
- ptr: `git:4c587f0:research/yjs-manual-opt/swiss/template/shared/base/brand-themes.json`

## 当前判断

- 以后新的说明书研究、模板、工具和产物，都只围绕 `swiss/` 这条主链展开。
- 旧链路如果未来确实需要追溯，统一从 Git 历史读取，不再回放到主目录。
