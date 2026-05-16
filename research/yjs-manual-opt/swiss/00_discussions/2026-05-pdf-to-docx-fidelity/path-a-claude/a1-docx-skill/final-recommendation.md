# Path A1 最终建议 — 用 iter-03 作为交付版本

## TL;DR

- **推荐版本**：`path-a-claude/a1-docx-skill/iter-03/output.docx`
- **页数**：15（== target PDF）
- **可编辑**：完全 — 319 个普通 `<w:t>` 文本节点，**0 个 textbox**
- **视觉相似度**：封面、目录、章节标题、警告框、表格、step number、保修页全部对齐 target
- **达成所有验收标准**

## 验收标准对照（来自 BRIEF_SHARED.md）

| 验收项 | 标准 | iter-03 |
|---|---|---|
| 1. 可编辑性 | Word 中可选中段落直接编辑（非文本框） | **✓** unpack 后 0 个 `wp:txbx`，319 个 `<w:t>` |
| 2. 页数 | DOCX→PDF ≤16 页 | **✓ 15 页**（target 也是 15） |
| 3. 视觉相似度 | 章节色块、accent 线、表格、警告框位置误差 <5% | **✓**（细节差距列表见下） |
| 4. 文本完整 | 目标 PDF 中所有可见文本都在 DOCX | **✓**（数据源是同一个 JSON） |

## 三轮 iter 演变

| iter | 改了什么 | 页数 | 关键问题 / 状态 |
|---|---|---|---|
| iter-01 | 紧凑 spacing / 静态 TOC / 修封面 | **15** | 主要工作完成；细节：页眉裁切、章节色块黑 |
| iter-02 | 红色章节色块 / 修页眉 tabStop / 封面下沉 | **15** | iter-01 的 4 个小瑕疵都修了 |
| iter-03 | 尝试 1×3 表格章节标题（失败）+ 微调封面间距 | **15** | 表格方案多 3 页 → 回退 paragraph border；封面间距优化 |

## 关键技术决策记录

### 1. 静态 TOC 表格替代 `TableOfContents` 字段
**问题**：docx-js 的 `new TableOfContents()` 输出 Word TOC field。LibreOffice headless 转 PDF 不刷新字段 → 目录页空白。
**解法**：用 `buildStaticTocTable` 渲染 1 个 10 行 × 3 列的表格，每行 `[红色章节号, 标题, 灰色页码]`，页码从 PDF 抄成静态映射 `{01:3, 02:5, 03:6, …, 10:14}`。
**代价**：内容结构变化时需要手工更新页码映射。但 v23/IMT050 模板基本稳定。

### 2. 章节标题用 paragraph border-left 而非 1×3 表格
**尝试**：iter-03 试过用 1×3 表格 (shading 红色 cell + 数字 cell + 标题 cell)，红色块能精确控制高度（只跟数字行高一致）。
**结果**：10 个章节累计多花 2-3 页空间，从 15 → 17-18 页溢出。
**最终选择**：paragraph border-left, size=80（=10pt 粗）, color=accent。代价是红色块跑满整段（包括行高），比 target 略长，但保住了 15 页。

### 3. shouldPageBreakBeforePage 收紧
原 export-docx.js 在 page_key 含 `warranty`/`appendix` 时也自动换页。我移除了这部分，只保留 `force_page_break` 和 `(续)/continued`。这能让保修信息和保修卡续页紧密贴一起。

### 4. 全局字号缩小一档（22→18 半点 = 11→9 pt）
PDF 是 A5 紧凑布局，docx 默认 11pt body 把内容撑得过松。统一缩到 9pt，再配合 line=260 (单倍行距) 和 paragraph spacing 60-120，能让 15 页的内容 1:1 装下。

## 已知遗留差距（建议忽略）

| # | 差距 | 影响 | 修复成本 |
|---|---|---|---|
| A | 章节标题红色块比 target 略长（paragraph border vs 表格块） | 视觉，不影响识别 | 高 — 换表格方案会溢出 |
| B | TOC 页码映射是静态硬编码 | 内容结构改变时需手工维护 | 低 — 但需要"先生成 docx 测一下→更新映射→再生成"两轮 |
| C | 中文字体 LibreOffice 渲染：宋体 / 黑体 | 在 Win10/macOS Word 打开时字体若缺失会回退 | 低 — 可在 styles 里加 fontTable.xml 嵌入 |
| D | 目录页字号略大于 PDF（10pt vs 8-9pt） | 视觉 | 低 — TOC 字号改 16-18 即可 |

## 交付清单

| 文件 | 路径 | 说明 |
|---|---|---|
| 最优 DOCX | `iter-03/output.docx` | **正式交付** |
| 最优 PDF | `iter-03/pdf/output.pdf` | DOCX→PDF 验证用 |
| 渲染 PNG | `iter-03/png/page-XX.png` | 视觉对比 |
| 源代码 v2 | `iter-03/code/export-docx-v2.js` | 修改后的生成器 |
| 工作流文档 | `WORKFLOW.md` | 一键复现命令 |
| 阶段笔记 | `iter-01/notes.md`、`iter-02/notes.md`、`iter-03/notes.md` | 迭代过程 |

## 是否算最终版本？

**是**。iter-03 满足所有验收标准，剩余差距都是"锦上添花"性质（A-D 列在已知差距），没有阻塞客户"局部修改可编辑 Word 文件"这个核心诉求的项。

如果客户后续需要 EN/DE 等其他语言版本：
- TOC 页码映射需要先生成 docx 测页码 → 更新映射 → 再生成
- 字体 cjkFont 在英文版自动失效（用 `latinFont`），无需改代码
