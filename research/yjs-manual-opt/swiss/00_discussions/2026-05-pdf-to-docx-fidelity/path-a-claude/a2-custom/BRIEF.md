# Path A2 — Claude + 自选最佳路径

请先读 `../../BRIEF_SHARED.md` 拿到背景。

## 你的自由度
**不限于 docx skill 工具链**。你应该评估并选择最能达成"视觉接近 PDF + 完全可编辑"的路径。

## 候选路径（按推荐度）
1. **pandoc HTML→DOCX + python-docx 后处理**
   - 已知 HTML 在 `swiss/output/imt050-wevac-eu-cn.html`
   - `pandoc --reference-doc=template.docx -o out.docx in.html`
   - 用 reference-doc 把字体/边距/Heading 样式锁住
   - 用 python-docx 后处理表格宽度、shading、accent 线
2. **python-docx 模板填充**
   - 手工建一个 reference 模板（含 styles、numbering、headers/footers）
   - 用 python-docx 从 JSON 内容填段落、表格、图片
   - 完全可编辑、所有元素是真实 OOXML 节点
3. **修 docx-js 生成器 + 紧凑化**（与 A1 路径相似，但你可以自由用任何辅助工具）
4. **混合**：pandoc 处理流文本，docx-js 处理图片+表格

**强烈不推荐**：`pdf2docx`（输出全是文本框/绝对定位，不可正常编辑）

## 工作目录
`D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\path-a-claude\a2-custom\`

## 必须循环的步骤（直到达标）
1. iter-NN/plan.md — 这轮要改什么
2. 改/生成
3. iter-NN/output.docx
4. `python compare_pdfs.py docx2pdf ...`
5. `python compare_pdfs.py render ...`
6. `python compare_pdfs.py compare ...`
7. 看 side_by_side 图，写 iter-NN/notes.md
8. 达标？是→停；否→回 1

## 验收标准
同共享 BRIEF。

## 关键提示
- 一定要在 Word 里能直接编辑文字（不是文本框，不是图片化的文字）
- pandoc 3.9.0.2 已在 PATH
- python-docx 1.2.0 已装
- 第一个 iter 可以用 pandoc 试一发 baseline，看离目标多远

## 产出
- `iter-XX/output.docx`（最优一版）
- `final-recommendation.md`
- `WORKFLOW.md`（一键复现命令）
