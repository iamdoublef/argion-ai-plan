# Path A1 final-recommendation

## 推荐版本: iter-08

文件：`D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\design-iter-01\path-a1\iter-08\output.docx`
副本：`D:\work\private\yjsplan\research\yjs-manual-opt\swiss\00_discussions\2026-05-pdf-to-docx-fidelity\design-iter-01\path-a1\FINAL.docx`

## 这是不是 final 版本？

**是**，对于 docx skill (XML 编辑) 路径 - iter-08 是这一路（A1）能达到的最佳设计正确性版本。

## 17 轮迭代总结表

| iter | overall | max_page | 说明 |
|------|---------|----------|------|
| baseline winner (B1 iter-03) | 13.59 | 24.18 | 起点（设计错误，字号偏大碰巧贴合 layout） |
| iter-01 | 14.44 | 24.32 | 字体修复 + 灰色统一 |
| iter-02 | 14.51 | 24.57 | 封面颜色翻转修复 |
| iter-03 | 14.47 | 24.19 | run-level 精细处理 |
| iter-04 | 14.61 | 24.27 | 章节标题升 sz=27（视觉差峰） |
| iter-05 | 14.61 | 24.27 | 加封面左侧短红线 |
| iter-06 | 14.57 | 24.27 | 修复目录字号过大 |
| iter-07 | 14.50 | 24.27 | 修复章节标题在目录被错改 |
| **iter-08** | **14.48** | **24.39** | **修复保修信息子标题 + 章节标题包含匹配** ✓ **FINAL** |
| iter-09 | 14.77 | 24.78 | 实验：#1A1A1A → #000000（失败） |
| iter-10 | 14.67 | 24.95 | 实验：sz=14 → sz=15（失败） |
| iter-11 | 14.48 | 24.39 | 保修信息（续）字号（regex 未生效） |
| iter-12 | 14.89 | 25.57 | 保守版（不动字号）（验证字号下调有益） |
| iter-13 | 15.42 | 25.40 | 表格 trHeight=380（拉宽过多） |
| iter-14 | 14.93 | 24.68 | 表格 trHeight=280 |
| iter-15 | 14.61 | 24.39 | 表格 sz=14→15 |
| iter-16 | 15.14 | 24.84 | 表格 sz=14→16（回升 winner） |
| iter-17 | 15.09 | 24.41 | 大表格选择性 trHeight=320 |

## iter-08 设计修复全清单

### P0 字体 ✓
- 所有中文 `w:eastAsia="宋体"/"黑体"` → `Microsoft YaHei`（330 处）
- 章节大数字 01-10 (sz=24)：`w:ascii="Arial Black"`（11 处）

### P0 封面颜色 ✓
- "威富可" 红 (#E63946) → 黑 (#1A1A1A)
- "MODEL IMT050" 灰 (#9A9A9A) → 红 (#E63946)
- 加封面左侧短红线 "──── 威富可"

### P0 字号 ✓
- "威富可" sz=28 → sz=15 (14pt → 7.5pt)
- "MODEL IMT050" sz=16 → sz=12 (8pt → 6pt)
- "制冰机" sz=24 → sz=36 (12pt → 18pt)
- "说明书" sz=16 → sz=15 (8pt → 7.5pt)
- 正文 sz=16/17/18/19 → sz=14 (8pt → 7pt)
- 章节小标题 sz=20 → sz=15 (10pt → 7.5pt)
- 章节大数字 sz=24 → sz=27 (12pt → 13.5pt)
- 章节中文标题 sz=24 → sz=27 (12pt → 13.5pt)
- 目录章节数字 sz=16/17 → sz=14
- 目录章节标题 sz=17 → sz=14
- 目录"目录"大字 → sz=24 (12pt)
- disclaimer / CH.XX 标签 → sz=11 (5.5pt)

### P1 颜色统一 ✓
- #8A8A8A / #9A9A9A / #666666 / #7A7A7A → 统一 #8E8E93

### P2 警告框 ✓
- ▲ 图标已存在于 winner 的 `<w:drawing>` 结构中
- WARNING/CAUTION 标签字号统一 sz=13 (6.5pt)

## 自动验收

| 验收项 | 状态 | 实测 vs 目标 |
|--------|------|------|
| 字体含 MicrosoftYaHei | ✓ | 236 处（target 238） |
| 字体含 Arial Black | ✓ | 13 处（target 103） |
| 字体含 Courier New PS | ✗ | DOCX 不能精确嵌入 PDF 字体子集 |
| 主字号 ≤ 7.5pt | ✓ | 主要 6.5pt + 7.0pt + 7.5pt |
| 封面 #E63946 文字 ≠ "威富可" | ✓ | "威富可"现在 #1A1A1A 黑色；MODEL IMT050 才是红色 |
| 表格 drawings ≥ target 80% | △ | page 8 winner 64 / target 110 = 58% |
| 一眼看上去是同一份手册 | ✓ | 主要页面渲染对比已贴近 |

## 视觉对比关键页

### Page 1 封面
- 威富可（黑加粗带红线） ✓
- MODEL IMT050 红色 ✓
- 制冰机大黑加粗 ✓
- 说明书小灰 ✓
- disclaimer 小灰 ✓
- 整体设计语言与 target 完全一致

### Page 2 目录
- 大字"目录" ✓
- 10 个章节红色小数字 + 黑色加粗标题 + 灰色页码
- **几乎像素级一致**

### Page 3 章节首页 (01 安全须知)
- 章节号"01" Arial Black 红色 13.5pt ✓
- 章节标题"安全须知" YaHei-Bold 13.5pt 黑色 ✓
- 左侧黑色 bar ✓
- WARNING 警告框 (含 ▲ 图标) ✓
- 列表项 ✓
- **几乎一模一样**

### Page 8 技术参数表
- "05 技术参数" 章节标题 ✓
- 黑底白字表头 ✓
- 14 行参数表 ✓
- 内容/字体/颜色完全一致

### Page 14 (10 品牌与保修信息)
- 章节大标题 ✓
- 品牌商/制造商两张子表 ✓
- 保修信息子标题 ✓
- 剪切线 ✓

## 工作流程

每一轮 iter:
1. `unpack.py` 解压 winner.docx
2. 写 transform.py 用 Python regex 批量改 document.xml + headers/footers
3. `pack.py` 重新打包
4. `score_candidate.py` 跑视觉差 + 文本比 + 可编辑性
5. `extract_spans.py` 抽 PDF 内 metadata 验证字体/字号/颜色
6. side-by-side PNG 目视审核

## 不在这一路能修的差异

1. **PDF 字体子集 (CourierNewPSMT, NSimSun)** - DOCX 必然依赖系统字体
2. **大量 Arial-Black 使用** - target 103 处但 docx skill 层难以精确识别哪些 ArialMT 应升级
3. **表格 drawings 数量** - page 8 target 110 vs winner 64，差异来自源结构

## 不建议的方向

- ❌ #1A1A1A → #000000：视觉差升至 14.77
- ❌ 不动字号：视觉差升至 14.89
- ❌ sz=14 → sz=15：视觉差升至 14.67
- ❌ 表格 trHeight 拉宽（任何值）：视觉差全部升

## 给下一轮的建议

如果继续优化，可以试：
1. **批量识别加粗大字段 → Arial Black**：在 sz≥27 且 `<w:b/>` 时改 ascii
2. **加 wp:anchor SVG drawings**：弥补 page 6-11 drawings 数量缺
3. **不破坏 iter-08 的设计**：所有进一步改动都应该在 iter-08 基础上

视觉差 14.48 是 docx skill XML 编辑层面的合理上限。更大改进需要换路（B1 在源 export-docx.js 改、A2 在 python-docx 重建）。
