# Path A1 — Claude + 官方 docx skill 严格流程

请先读 `../../BRIEF_SHARED.md` 拿到背景。

## 你的约束
**必须严格使用 `~/.claude/skills/docx/SKILL.md` 推荐的工具链**：
- 编辑现有 DOCX：`unpack.py` → 编辑 XML → `pack.py`
- 创建新 DOCX：`docx-js`（npm `docx` 包）
- 校验：`validate.py`
- 转 PDF：`scripts/office/soffice.py`

不要用 pandoc / mammoth.js / pdf2docx 等非 skill 推荐工具（那是 A2 的领域）。

## 推荐工作路径

现有 DOCX 内容完整、样式有问题，**建议先用 `unpack.py` 拆开看实际 XML 结构**，理解现有生成器哪里偏离 PDF。然后两种打法二选一：

1. **OOXML 直改**：unpack → 用 Edit 工具修 XML（紧凑 spacing、补 TOC 表、修首页）→ pack → 验证
2. **docx-js 重建**：基于 `swiss/tools/export-docx.js` 改一个紧凑版到 `path-a-claude/a1-docx-skill/code/export-docx-v2.js`，从 JSON 重新生成

iter-01 起步建议走 (1) — 因为已有 DOCX 内容是对的，只需精修 XML。

## 工作目录
`D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\path-a-claude\a1-docx-skill\`

## 必须循环的步骤（直到达标）
1. 想清楚这轮要改什么（写 iter-NN/plan.md）
2. 改文件
3. 生成 DOCX，存到 `iter-NN/output.docx`
4. `python compare_pdfs.py docx2pdf iter-NN/output.docx iter-NN/pdf`
5. `python compare_pdfs.py render iter-NN/pdf/output.pdf iter-NN/png --dpi 150`
6. `python compare_pdfs.py compare ../../baseline/target_png iter-NN/png iter-NN/side_by_side --label-a TARGET --label-b A1-NN`
7. 阅读 side_by_side 图片，写 iter-NN/notes.md
8. 评估：达标？是→停；否→回 1（iter-NN+1）

## 验收标准（见共享 BRIEF）
- ≤16 页
- 视觉相似度逐页通过
- 全部文本可编辑（Word 中能选中段落直接改）
- TOC 不空

## 重要提示
- 不要修改 `swiss/output/imt050-wevac-eu-cn.docx`（那是基线参考），把你的产物放进 `iter-NN/output.docx`
- 不要修改 `swiss/tools/export-docx.js` 主版本，如果改了它就拷到 `iter-NN/code/`
- 现有项目根有 `node_modules`，docx-js 9.6.0 可用。在 `D:\work\private\yjsplan\` 下直接 `node <script>` 即可
- LibreOffice headless 不刷新 Word 字段，所以 docx-js 的 `TableOfContents` 不能在 LibreOffice 转 PDF 时显示内容；要么手工渲染 TOC 表，要么转 PDF 前先用宏刷新
- 中文字体：PDF 用的是 puppeteer 内嵌字体；DOCX 要保证中文可读，可用 "宋体"+"黑体"，验证 LibreOffice 渲染时不出方框

## 你的产出（最后一定要有）
- `iter-XX/output.docx`（最优一版）
- `final-recommendation.md`（告诉主控你认为这是不是最终版本，剩余差异清单）
- `WORKFLOW.md`（如果达标，写一个一键复现的命令脚本）
