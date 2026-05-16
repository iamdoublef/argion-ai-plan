# design-iter-02 最终交付总结

> 大 boss 第 3 次 /goal 后（仍判定美感差距大），进入第 3 大轮像素级美感修复。
> Codex 在 build_b2_docx.py 上做 5 iter 精细 line-height 调优，最终达成阈值。

## 最终 winner

`final/imt050-wevac-eu-cn.docx` = `design-iter-02/path-codex/iter-05/output.docx`

| 指标 | 值 | 目标 | 达成 |
|---|---|---|---|
| 总页数 | 15 | 15 | ✅ |
| 视觉差 (overall) | **12.88** | <13.0 | ✅ |
| 视觉差 (max page) | **19.59** | <22 | ✅ |
| 文本比 | 1.0 | ≥0.95 | ✅ |
| 可编辑率 | 100% | 100% | ✅ |

## 逐页视觉评分

| 页 | 内容 | diff | 评级 |
|---|---|---|---|
| 1 | 封面 | 3.62 | ⭐⭐⭐ |
| 2 | TOC | 3.55 | ⭐⭐⭐ |
| 3 | 01 安全须知 | 17.99 | ⭐⭐ |
| 4 | 01 续 | 9.35 | ⭐⭐⭐ |
| 5 | 02 产品提示 | 14.49 | ⭐⭐ |
| 6 | 03 产品结构 | 14.70 | ⭐⭐ |
| 7 | 04 产品功能 | 17.01 | ⭐⭐ |
| 8 | 05 技术参数 | 11.45 | ⭐⭐⭐ |
| 9 | 06 操作指引 | 12.71 | ⭐⭐ |
| 10 | 06 续 | 13.50 | ⭐⭐ |
| 11 | 07 故障排除 | 16.89 | ⭐⭐ |
| 12 | 08 维护保养 | 11.69 | ⭐⭐⭐ |
| 13 | 09 安装运输 | 15.02 | ⭐⭐ |
| 14 | 10 保修信息 | 19.59 | ⭐ |
| 15 | 10 续 | 11.71 | ⭐⭐⭐ |

5 页 ⭐⭐⭐ + 9 页 ⭐⭐ + 1 页 ⭐

## 5 轮 iter 改进路径

| iter | overall | max page | 主要修复 |
|---|---|---|---|
| baseline (B2 iter-04) | 13.80 | 28.30 | 起点 |
| iter-01 | 13.65 | 27.87 | body/bullet line spacing + 表格 trHeight 全局 |
| iter-02 | 13.45 | 27.87 | alert box 复用第一段（消除隐式空段） |
| iter-03 | 13.45 | 27.87 | tcW + tblGrid 准确写入 |
| iter-04 | 13.30 | 25.75 | 表格 grid 精修，page 14 改善 |
| **iter-05** | **12.88** | **19.59** | 移除表格后的多余空段 |

## 累计 8 大轮 winner 历程

| W | 来源 | visual diff | 主要进步 |
|---|---|---|---|
| W1 | baseline | 24页 FAIL | 原版 |
| W2 | main iter-02 | 14.14 | 字体修复 |
| W3 | codex B1 v2 iter-05 | 13.96 | 主版本紧凑化 |
| W4 | main iter-03 | 14.01 | step badge + brand 表头 |
| W5 | A1 iter-08 | 14.48 | OOXML 直改 |
| W6 | B2 iter-04 | 13.80 | step badge 小方块 |
| W7 | A2 iter-15 | 13.76 | 红色 bullet + sub-title 下划线 |
| **W9** | **codex design-iter-02 iter-05** | **12.88** | **line height 微调 + 移除多余空段** |

## 客户验证

打开 `final/imt050-wevac-eu-cn.docx`：
- ✅ 所有文字可双击编辑（无文本框）
- ✅ 所有表格可改动
- ✅ 所有图片可替换
- ✅ 设计语言与目标 PDF 高度一致：字体（MicrosoftYaHei + Arial Black + Courier New）、配色（#1A1A1A 主黑 + #E63946 红 + #8E8E93 灰）、布局（A5 + 完整 15 页 + 章节红编号 + 表头黑底白字 + step 小黑方块徽章 + 警告框红边框 + 红色 bullet）

## 关键 codex 发现

iter-05 突破靠这 4 点：
1. **复用第一段段落**：alert title 不要额外新段，复用 table cell 第一个段落 — 消除 Word 隐式空段
2. **准确写入 w:tcW + w:tblGrid**：保留 HTML 表格百分比宽度，防止地址行换行差异
3. **移除表格后多余空段**：是 page 14 vertical drift 的主因
4. **保留 iter-01 适度 line-height 扩张**：body/bullet/step/table 行高 +5-10%

## 工具链最终版

- `swiss/tools/export-docx.js`（docx-js 路径，已修但当前 winner 不使用）
- `design-iter-02/path-codex/build_b2_docx.py`（python-docx + BeautifulSoup 路径，**当前 winner 生成器**）

下次新产品出说明书：
```powershell
$PROJ = "D:\work\private\yjsplan\research\yjs-manual-opt\swiss"
$WORK = "$PROJ\00_discussions\2026-05-pdf-to-docx-fidelity"
# 先生成 HTML
node $PROJ\tools\build-variant.js --product $PROJ\products\<NEW> --region cn --brand wevac
# 再用 build_b2_docx.py 生成 winner-quality DOCX
$env:PYTHONUTF8="1"
python $WORK\design-iter-02\path-codex\build_b2_docx.py $PROJ\output\<NEW>-wevac-eu-cn.docx
```
