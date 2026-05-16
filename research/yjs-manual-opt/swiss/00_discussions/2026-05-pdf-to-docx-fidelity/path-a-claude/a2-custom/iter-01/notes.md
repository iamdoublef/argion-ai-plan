# iter-01 — python-docx 直接构建（架构选定）

## 方法
- 抛弃 pandoc HTML→DOCX 路线（pandoc baseline=16 页但完全没视觉接近性，且 reference-doc 锁不住表格/警告框/步骤序号这种 PDF 特有结构）。
- 选择**python-docx 直接构建 OOXML**（候选路径 2），完全控制 A5 页面、字体、段距、表格、边框、底色、Header/Footer、PAGE field。
- 输入：`products/imt050/content/source/chapters/*.json` + `i18n/compiled/zh-CN.json` + `product.json` + `images.json`。
- 输出：每章一个 Word section（独立 header/footer，让 `CH.XX — XXX` 右上角文字随章节变化）。

## 实施
- 见 `build_docx.py`（一个文件，约 700 行，~25 个 helper）。

## 结果
- DOCX→PDF = **21 页**（目标 ≤16，still over）
- 视觉接近度大幅改善：
  - 目录 ★★★★★（接近完美：红色编号+加粗章节名+灰色页码+底部分隔线）
  - 章节标题 ★★★★（红色编号+黑色粗体+左侧黑色竖条）
  - 警告/注意/提示框 ★★★★（红/黑边框+底色+列表）
  - 步骤序号 ★★★★（黑底白字方块）
  - 表格 ★★★★（specs/parts/buttons/troubleshooting）
  - 页眉页脚 ★★★（黑色顶部线+品牌左+章节右 / 灰色品牌IMT050+页码右）
  - 封面 ★★★（红线品牌+图+MODEL+大标题+说明书+红色分隔线，但底部 disclaimer 溢出到 page 2）

## 问题清单（按优先级）

### P0 阻塞（必须修）
1. **caution_box 内联文本乱码**（page 15/18）：`_render_box` 走到 `block.get("text")` 路径时拿到 GBK-as-UTF8 乱码原文，应该先查 `text_id`。
2. **总页数 21 > 16**：主要来自：
   - 封面溢出到 page 2（disclaimer 推到下页）
   - 安全须知 (ch01) 用了 page 4+5 两页装第一组（应单页），page 6 装 page2 内容
   - 步骤流程（ch06）多了 1-2 页
   - 保修信息（ch10）多了 1 页
3. **PAGE 字段从 1 开始**：但目标设计封面/TOC不显示页码，body 页码=3 开始。Word PAGE field 从 1 计数。需要 `<w:pgNumType w:start="1">` 起点和 section 重启策略。

### P1 重要
4. **Parts 表（页 8）排序错**：当前是行优先（1/2, 3/4, 5/6, 7/-），目标是列优先（1/5, 2/6, 3/7, 4/-）。
5. **章节继续页（"安全须知（续）"）丢失"（续）"标识**：因为我把整章 page 1+2 内容合在一个 section 中，所以第 2 个 section_title 实际上是从 page['section_title'] 来的，需要保证它来自 i18n strings（含"（续）"）。看起来代码已经 lookup section_title_id，但渲染出来变成"01 安全须知"——可能 strings.section_title 是同样的字符串没标"（续）"。检查 zh-CN.json 看 `content.chapter.01-safety.page.page2.section_title`。
6. **页码起算**：cover=1 page2=2 但目标设计是 cover=不显示 toc=显示2 ch01p1=3。需要：cover 段不显示页码，TOC 段从 page=2 起。
7. **bullet_list 行距过宽** (1.35) → 收紧到 1.25。

### P2 优化
8. **status-indicator-row** 显示在 page 13，但 NOTICE 框被推到下一页（剩 3 项），需 keep_with_next 或缩小行距。
9. **封面 product image 太大**（max 48mm），目标 PNG 看起来约 35mm 高度。
10. **Heading 章节红色编号字号偏大**（18pt），目标看起来约 14-16pt。
11. **Specs 表行高**：每行 ~5mm 看起来 OK，可尝试 4mm 更紧凑。
12. **Cover MODEL IMT050 字号 8pt 偏小**，目标看 9-10pt。

## 下一步（iter-02）
1. P0/P1 全部修
2. 重点：让总页数 ≤16 后再优化视觉细节
3. 单独的 page-break 控制：每章只在 chapter section 开头分页，不在 chapter 内部强制分页（除非 page['page_id']>=2）
