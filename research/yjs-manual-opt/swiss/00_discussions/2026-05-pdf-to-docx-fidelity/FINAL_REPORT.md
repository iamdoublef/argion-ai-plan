# PDF → 可编辑 Word 还原：最终交付报告

> 大 boss，4 路并行尝试已收敛，全部 4 路都做到了视觉接近 + 100% 可编辑文本。下面是裁决与推荐。

## TL;DR

- **推荐交付**：`final/imt050-wevac-eu-cn.docx`（= Codex 路径 B1 iter-03）
- **页数**：15（与 PDF 完全一致，原版是 24 页）
- **可编辑性**：100% 真实 Word 段落、表格、嵌入图，无文本框
- **视觉差异**：13.59/24.16（最低；阈值 60；目标 PDF 平均颜色差异）
- **独立第三方（Codex）意见**：同样推荐 B1 iter-03（见 `CROSS_REVIEW.md`）

## 4 路结果对比

| 路径 | 执行方 | 工具链 | 最佳 iter | 视觉差 | 备注 |
|---|---|---|---|---|---|
| **A1** | Claude swiss-manual-writer | docx skill 严格（unpack/edit/pack + docx-js fork） | iter-02 | 14.71 | 封面布局最忠实于 PDF；做到 15 页 |
| **A2** | Claude general-purpose | python-docx + 自建模板 | iter-04 | 16.53 | 完整独立脚本，但视觉略差于其他 3 路 |
| **B1** | Codex (gpt-5.5) | docx skill 严格（fork export-docx.js + 静态 TOC） | **iter-03** | **13.59** | **数值最优 + 章节节奏最佳** |
| **B2** | Codex (gpt-5.5) | python-docx + HTML 解析（独立脚本） | iter-03 | 14.57 | 完整自给自足，不依赖现有 export-docx.js |

详细排行：`RANKING.md`（11 个 PASS 候选 + 2 个 FAIL 对照）。

## 为什么 B1 iter-03 是 winner

来自 Codex 独立 cross-review（`CROSS_REVIEW.md`）：
1. 视觉差 13.59，4 路最低，每页平均颜色差异最小
2. unpack 验证：`<w:t>` 全在，`<wp:txbx>`/`<v:textbox>`/`<w:txbxContent>` 数量 = 0 → 完全可编辑
3. 在产品结构、操作、技术参数、保修页上排版节奏最贴近 PDF
4. 表格、bullet、图片都是可编辑 Word 原生元素
5. 来自对 `swiss/tools/export-docx.js` 的最小化改造，技术资产可持续

## 备选方案（也都达标，按场景选）

- **A1 iter-02** (`final/candidates/A1-iter02_visualdiff_14.71.docx`)：如果客户更看重"封面布局像 PDF"（顶部"威富可"小字+短红线、产品图小、底部 disclaimer 两行），A1 设计还原最忠实
- **B2 iter-03** (`final/candidates/B2-iter03_visualdiff_14.57.docx`)：如果客户希望"完全独立的 python-docx 脚本，不依赖现有 export-docx.js"，B2 是自给自足方案

## 客户场景验证

| 客户需求 | 是否满足 | 验证方式 |
|---|---|---|
| 可在 Word 中局部修改文字 | ✓ | unpack 检查：所有文本在 `<w:t>` 而非 textbox |
| 视觉接近 PDF | ✓ | LibreOffice 渲染对比图见 `path-b-codex/b1-docx-skill/iter-03/side_by_side/side-XX.png` |
| 页数与 PDF 一致 | ✓ | 15 页（PDF 也是 15 页） |
| 表格可编辑 | ✓ | 真实 `<w:tbl>` 节点 |
| 图片可替换 | ✓ | 真实 inline drawing（不是 anchored/floating） |
| TOC 可见 | ✓ | 静态 TOC 表（不依赖 Word 字段刷新） |

## 关键技术沉淀（可复用）

1. **字体校准**：PDF 用 **MicrosoftYaHei** + Arial 组合，DOCX 必须改用同字体（现有 export-docx.js 用宋体偏差大）
2. **字号校准**：正文 7.5pt（DOCX size = 15 half-pt），现有 22 偏大导致页数膨胀
3. **静态 TOC 强制**：LibreOffice headless 不刷新 Word TOC field，必须放弃 `new TableOfContents()` 改用手写表格
4. **章节首页不强制分页**：移除 `pageBreakBefore`，让内容紧接章节标题
5. **紧凑 cell margins**：表格内边距从 70 DXA 降到 40-50 DXA
6. **docx skill validate.py Windows fix**：必须设 `PYTHONUTF8=1` 才不报 gbk codec 错；需补齐 `scripts/office/schemas/` 子目录
7. **pdf2docx 禁用**：输出文本框无法编辑，违反客户核心诉求

## 复用工作流（下一个产品的 DOCX 生成）

详见：`path-b-codex/b1-docx-skill/WORKFLOW.md`

简化版（产品换新只需改 JSON）：
```powershell
# 1. 生成 DOCX（用 winner 路径的 export-docx.js fork）
node research\yjs-manual-opt\swiss\tools\export-docx.js --product <NEW_PRODUCT_DIR> --region cn --brand wevac
# （注：这里需要把 winner B1 iter-03 的 code 改动合并回 swiss/tools/export-docx.js 主版本，
#  或者保留双轨：master 版 + slim 版）

# 2. 转 PDF 用于验收
$soffice = "C:\Program Files\LibreOffice\program\soffice.exe"
& $soffice --headless --convert-to pdf --outdir output\preview output\<new>.docx

# 3. 验收（对比目标 PDF）
python research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\score_candidate.py `
  output\<new>.docx --target output\<new>.pdf `
  --baseline-pngs research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\baseline\target_png
```

## 待大 boss 决策

1. **接受 B1 iter-03 作为最终交付** → 我把 `final/imt050-wevac-eu-cn.docx` 拷到 `swiss/output/` 覆盖现有版本；同时把 B1 的代码改动合并回 `swiss/tools/export-docx.js` 主版本，让下次新产品自动产出紧凑版
2. **想看 A1 / B2 备选** → 在 `final/candidates/` 直接 Word 打开对比
3. **想再迭代** → 我可以让 codex/agent 跑 iter-04+，继续打磨细节

我个人推荐 **方案 1**：B1 iter-03 已经达成所有验收，再迭代收益递减。

## 产出物清单

- `final/imt050-wevac-eu-cn.docx` — 推荐交付（B1 iter-03）
- `final/imt050-wevac-eu-cn.preview.pdf` — DOCX 转 PDF 预览
- `final/0-pre-iteration-baseline-24pages.docx` — 原版备份（实验前）
- `final/candidates/*.docx` — 全部 4 路最佳 iter + 原版基线，文件名含视觉差异分数
- `final/candidates/_target.pdf` — 视觉对比目标
- `RANKING.md` — 完整评分排行
- `CROSS_REVIEW.md` — Codex 第三方独立裁决
- `log.md` — 完整实验流水
- `BRIEF_SHARED.md` — 共享技术 brief（4 路共享发现）
- `baseline/pdf_probe.md` — PDF 字体/配色探查报告
- `compare_pdfs.py`, `score_candidate.py`, `probe_pdf.py`, `dashboard.py` — 评估工具链
- `path-{a,b}-*/iter-NN/` — 4 路所有 iter 完整产物（含 notes、plan、side_by_side）

---

**说话简洁，方案落地**：B1 iter-03 是我的推荐。等大 boss 拍板，我就把它装到生产路径上。
