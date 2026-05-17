# Design-iter-38 / path-keycap-chip — STATUS

## 基线
W30 (final iter-37 系列): overall_mean_diff = **8.57**, max_page_diff = **12.26** (current re-score; iter-37 STATUS 报告 8.54/12.24 是旧版 scorer 数据)

## 最终 (W31)
**iter-8: overall_mean_diff = 8.49, max_page_diff = 12.26**
- Delta: mean **-0.08**, max **±0.00**
- p7 单页贡献: **7.81 → 6.68 (-1.13)**
- 升级到 `final/imt050-wevac-eu-cn.docx`

## 任务范围澄清
FIX_LIST 说"p7 + p11 共 7 个 cell"，但实际查看 target PDF p11，故障表里 `(ADD WATER亮红灯)` 是**纯文本+小括号**，**没有** chip 样式。所以本轮只对 **p7 的 5 个按键说明 cell** 做结构重构。

## XML 改动方案（iter-8 chip 实现）

### 旧结构（W30 基线，每个 cell）
```xml
<w:r>
  <w:rPr>
    <w:rFonts w:ascii="Arial" .../>
    <w:b w:val="0"/> <w:sz w:val="13"/> <w:color w:val="1A1A1A"/> <w:spacing w:val="5"/>
  </w:rPr>
  <w:t>1</w:t>
  <w:br/>
  <w:t>Power</w:t>
  <w:br/>
  <w:t>电源</w:t>
</w:r>
```

### 新结构（W31 iter-8，单 cell 拆分为 3 个 run）
```xml
<!-- Prefix: 数字 + 空格 -->
<w:r>
  <w:rPr> ... Arial sz=13 spacing=5 ... </w:rPr>
  <w:t xml:space="preserve">1 </w:t>
</w:r>
<!-- Chip: Consolas + 单线黑边框 -->
<w:r>
  <w:rPr>
    <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas" w:eastAsia="Consolas"/>
    <w:b w:val="0"/> <w:sz w:val="13"/> <w:color w:val="1A1A1A"/>
    <w:spacing w:val="2"/>
    <w:bdr w:val="single" w:sz="4" w:space="1" w:color="000000"/>
  </w:rPr>
  <w:t>Power</w:t>
</w:r>
<!-- Suffix: 空格 + 中文标签 -->
<w:r>
  <w:rPr> ... Arial sz=13 spacing=5 ... </w:rPr>
  <w:t xml:space="preserve"> 电源</w:t>
</w:r>
```

5 个 cell 都同样改造：Power/电源, Make Ice/制冰, Clean/清洁, ICE FULL/冰满, ADD WATER/加水。

## 每轮迭代记录

| Iter | chip 实现 | mean | max | p7 | 备注 |
|------|-----------|------|-----|-----|------|
| baseline (W30) | 堆叠 3 行 | 8.57 | 12.26 | 7.81 | — |
| iter-1 | Courier New + bdr sz=4 + space=0 | 8.51 | 12.26 | 6.91 | 单线 + chip 初见效 |
| iter-2 | Courier + space=4 (宽 padding) | 8.54 | 12.26 | — | **拒绝** — 推后续 cell 内容右移 |
| iter-3 | Courier + sz=12 (6pt) | 8.51 | 12.26 | 6.95 | **拒绝** — 字号变小反退 |
| iter-4 | Consolas + space=1 | 8.49 | 12.26 | 6.69 | **大进步** — Consolas glyph 更紧 |
| iter-5 | Consolas + bdr sz=6 (粗边) | 8.50 | 12.26 | 6.86 | **拒绝** — 边框过粗 |
| iter-6 | Consolas + bdr sz=2 (细边) | 8.51 | 12.26 | 6.93 | **拒绝** — 边框过细 |
| iter-7 | Lucida Console | — | — | — | **soffice 失败** — 字体不支持 |
| iter-8 | Consolas + spacing=2 + bdr sz=4 space=1 | **8.49** | **12.26** | **6.68** | **最终接受** |
| iter-9 | iter-4 + spacing val=5 | — | — | — | **soffice 失败** |
| iter-10 | 控制实验: 单行无 chip | 8.51 | 12.26 | 6.93 | 验证: chip styling 贡献 0.25, 单行结构贡献 0.88 |
| iter-11 | iter-8 + bold | 8.49 | 12.26 | 6.69 | **持平** — bold 无增益 |

## 关键发现

1. **chip 字体选择**: Consolas 显著优于 Courier New（p7 6.91→6.68）。Consolas 的字符宽度对 6.5pt 渲染更准；Courier New 在小 size 下渲染权重略重。

2. **chip padding**: bdr sz=4 + space=1（0.5pt 边 + 1pt 内距）是最优组合。更宽 padding (space=4) 把后续 Chinese tag 推右，破坏 cell 对齐。更窄/无 padding（space=0）chip 显得拥挤。

3. **letter spacing**: chip 内 spacing val=2（不是正文的 5）能让 chip 字符稍微展开但不破坏其紧凑感。

4. **chip styling 与单行重构各贡献一半**:
   - 单行重构（iter-10 控制）: p7 7.81→6.93 (-0.88)
   - chip styling 增量: p7 6.93→6.68 (-0.25)
   - 合计 -1.13，符合审计预测的"~1.0pt"

5. **p11 不需要 chip**: target PDF p11 故障表中 `(ADD WATER亮红灯)` 是普通 ASCII 括号 + 文本，**无** chip 样式。审计 FIX_LIST 关于 "p11 也用 chip" 的描述错误。

## 接受条件验证

- ✅ mean 8.49 < 8.54 (baseline)
- ✅ max 12.26 = 12.26 (无回退)
- ✅ wt_count = 445 (≥300)
- ✅ editable_pct = 100%
- ✅ text ratio = 1.0
- ✅ pages 15:15
- ✅ Word COM 转 PDF 成功（iter-8_word.pdf）
- ✅ validate.py: document.xml 6 errors (与 baseline 同数，无新增)

## 下一推荐角度

1. **p3 (11.86) / p9 (11.87) / p13 (11.57) / p14 (12.26)** — 仍是高 diff 页，但都是字号/行距 sub-pixel 矛盾，难再突破。
2. **p11 (11.56) 故障表内容布局** — 列宽不均导致解决方案列 wrap 不同；可调整 tcW 比例。
3. **p5 (10.75) / p10 (10.01)** — 安全/操作页 list spacing，需 micro-tune `<w:p>` 的 before/after。
4. **跳出 LO 渲染优化局部最优** — 直接以 Word COM 渲染做 baseline 选最优字号/间距，绕开 LO 渲染偏差。

## 工作文件
- 最优 docx: `iter-8.docx`
- chip 实施脚本: `apply_iter1.py` + `apply_iter4.py` + `apply_iter8.py`
- Word 渲染验证: `iter-8_word.pdf` + `iter-8_word_p7.png`
