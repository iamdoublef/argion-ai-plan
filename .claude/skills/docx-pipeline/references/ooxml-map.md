# SOT 语义条款 → OOXML 实现映射

> 本表把 `swiss/DESIGN-STANDARD.md` 的语义条款映射到 OOXML 元素。
> **W50 母版已实现这些映射**，本表用于 fix 时定位 OOXML 元素。
> 不要据此从头搭母版 — 母版是 W50 复用，**只改不重建**。

## §二 色彩系统

| SOT 语义 | OOXML 元素 | 备注 |
|---------|-----------|------|
| `--swiss-black` `#000000` | `w:color w:val="000000"` / `w:shd w:fill="000000"` | 表头 shd 必须纯黑（W44：1A1A1A → 000000 是 -0.17 mean） |
| `--swiss-red` `#E63946` | `w:color w:val="E63946"` / `w:pBdr w:color="E63846"` | banner 边线 |
| `--swiss-gray-bg` `#F2F2F7` | `w:shd w:fill="F2F2F7"` | 灰底 |
| `--swiss-gray-text` `#8E8E93` | `w:color w:val="8E8E93"` | 页眉/页脚文字。**必须同步改 footer*.xml**（W44 教训） |

**禁用**（DESIGN §二）：
- `#E30613` / 其他非标准红
- 用 `#1A1A1A` 替代 `#000000`（变量必须是纯黑）
- 用 `#F5F5F5` 替代 `#F2F2F7`

## §三 字号系统

DOCX 单位：`w:sz` 是 half-point。10pt = `w:sz w:val="20"`。

| SOT 语义 | A5 字号 | OOXML | 备注 |
|---------|--------|-------|------|
| `.section-title` 一级标题 | 18px ≈ 13.5pt | `w:sz w:val="27"` | + 红色 chapter-num |
| `.sub-title` 二级标题 | 10px ≈ 7.5pt | `w:sz w:val="15"` | + `w:b` bold |
| 正文 `p` | 10px ≈ 7.5pt | `w:sz w:val="15"` | YaHei + Arial 栈 |
| `.step-text` | 10px | `w:sz w:val="15"` | |
| `td` 表格正文 | 9px ≈ 6.75pt | `w:sz w:val="14"` | |
| `th` 表头 | 8px ≈ 6pt | `w:sz w:val="12"` | + 白字 `w:color="FFFFFF"` |
| 警告框 | 9.4px ≈ 7pt | `w:sz w:val="14"` | |
| `.header-brand` | 9px ≈ 6.75pt | `w:sz w:val="14"` | uppercase |
| `.header-ref` | 7.5px ≈ 5.5pt | `w:sz w:val="11"` | Courier New |
| `.page-footer` | 7px ≈ 5pt | `w:sz w:val="10"` | Courier New, gray |

### 长语言补偿（DE/IT）

PDF 流水线用 CSS line-height/font-size 微调；DOCX 流水线**W50 已包含 baked-in 微调**：

| 属性 | CN/EN | DE/IT |
|------|-------|-------|
| `pPr/w:spacing w:line` | 默认 | 略小（行高 -0.1） |
| 步骤文字 `w:sz` | 15 | 14（10px→9.5px）|

**生产阶段不调这些**：W50 母版已经平衡好。如果 DE/IT 溢出导致页数变化 → fix-or-escalate（精确定位哪段超 → 减字数 / 改 strings），**不要 sweep 字距**。

## §五 标题系统

| SOT 语义 | OOXML 实现 |
|---------|-----------|
| `.section-title` 左侧竖线 4px black | `w:pBdr/w:left w:val="single" w:sz="32" w:color="000000"` |
| `.chapter-num` 红色编号 | `w:r` 含 `w:rPr/w:color w:val="E63946"` |
| `.sub-title` 底部黑线 1.5px | `w:pBdr/w:bottom w:val="single" w:sz="12" w:color="000000"` |
| `.sub-title` uppercase | OOXML 无 text-transform；CN 模板内容直接全大写（如适用） |

## §六 表格系统

| SOT 语义 | OOXML 实现 |
|---------|-----------|
| 表头黑底白字 | `w:tcPr/w:shd w:fill="000000"` + `w:rPr/w:color w:val="FFFFFF"` |
| 交替行色 | 偶数行 `w:tcPr/w:shd w:fill="F2F2F7"` |
| 边线 `#CCC` | `w:tcBorders/* w:val="single" w:sz="4" w:color="D9D9D9"`（W44 提亮到 D9D9D9）|

**禁用**：
- 灰底表头（`#F5F5F5` 等）
- `w:val="nil"` 边框（W46：用 single + FFFFFF 代替）

## §七 警示三级体系

| SOT 类 | OOXML 实现 |
|--------|-----------|
| `.warning-box` 红边 2px | `w:pBdr` 四边 `w:val="single" w:sz="16" w:color="E63946"` |
| `.warning-box .box-title` 红色 uppercase | run `w:color="E63946"` + `w:b` + 文本全大写 |
| `.caution-box` 黑边 2px | `w:pBdr` 四边 `w:val="single" w:sz="16" w:color="000000"` |
| `.note-box` 灰底 + 左边线灰 | `w:shd w:fill="F2F2F7"` + `w:pBdr/w:left w:val="single" w:sz="24" w:color="8E8E93"` |
| 红色 bullet `•` | `w:numPr` 列表 + 自定义 numFmt 含 red bullet |

**禁用**：emoji（⚠/⚡/📝）替代文字标题。

## §八 步骤列表

OOXML 实现：黑底白字方块编号 + `w:tab` 缩进文本。

| SOT | OOXML |
|-----|-------|
| `.step-num` 18×18 黑底白字 | 表格单元格 `w:tcW` + `w:tcPr/w:shd w:fill="000000"` + run `w:color="FFFFFF" w:b` |
| `.step-text` 缩进 28px | `w:ind w:left` |

## §九 普通列表

| SOT | OOXML |
|-----|-------|
| 红色 bullet `•` | `w:numPr/w:numId` 引用 `numbering.xml` 中定义的红色 bullet 列表 |

## §十 图片

| SOT | OOXML |
|-----|-------|
| `max-height: 54mm` | `<wp:extent cy="..."/>` EMU 单位（1 mm = 36000 EMU） |
| `object-fit: contain` | 默认 `xfrm`，不要 `stretch` |
| `.fig-caption` 灰色小字 Courier | `w:r` 含 `w:rFonts w:ascii="Courier New"` + `w:color w:val="8E8E93"` + `w:sz w:val="11"` |

**禁用**：拉伸（`xfrm` 不等比缩放）。

## §十二 页脚

| SOT | OOXML |
|-----|-------|
| `bottom: 4mm` | `sectPr/w:pgMar w:footer` |
| Courier 7px gray | `footer*.xml` 中 run 用 `w:rFonts="Courier New"` + `w:sz="10"` + `w:color="8E8E93"` |
| 双 flex 布局 | 单段落用 `w:tab` 分左右；或表格 1×2 |

**W44 教训**：GRAY 颜色 mismatch 修复时必须同步改 footer*.xml，否则视觉不对齐。

## §十三 内容结构

| SOT | DOCX 实现 |
|-----|----------|
| 总页数 11-14（PDF）/ 15 ±1（DOCX W50） | `sectPr` 分节符控制；**不要改总页数** |
| 标准页面序列 | W50 已固定，**不允许重排** |
| C13 调图不增页 | 改图尺寸时验证 `pkg validate` 后页数不变 |

## §十七 内容结构约束（DOCX 适配）

| SOT 条款 | DOCX 实现 / 替代 | 备注 |
|---------|----------------|------|
| C1 warranty_card 不跨页 | W50 母版已固定；strings 改文本不动结构 | 文本超长会破，提前 spot-check 长度 |
| C3 step 不跨页 | LO 渲染 PNG 抽样人工 review | DOCX 无 Playwright |
| C5 图片右边界 | W50 固定 | 不改图 |
| C8 页面溢出 | **anti-cheat text_ratio + 页数变化** 代理 | 详 §8.2 |
| C9 DE/IT 文本溢出 | 页数变化检测 + 必要时 fix（改 strings 缩短，不动 OOXML） | 不做 sweep |
| C11/C12 图片标注可辨认 | W50 母版固定，人工抽样 | |
| C13 调图不增页 | 不允许调图 | 母版锁定 |
| C14/C15 留白失衡 | LO PNG 人工抽样 | |
| C17 rowspan 一致 | 表格 `w:vMerge` 校验 | W50 已对齐 |
| C18 批准版不漂移 | 7 语言 docx 视觉与 W50 CN 对齐 | **核心** |
| C19 单位一致 | 跨语言锁定 keys 强制 = cn 值（见本文 "跨语言锁定 keys" 段） | strings/{lang}.json 由 `tools/check_invariants.py` 校验 |

## 跨语言锁定 keys（v2 实地版本）

> **重要变更（v2 阶段 1）**：brand `威富可` / `Wevac` 已**字面化在母版 OOXML 内**，不再是 placeholder。型号 `IMT050`、单位 `V/Hz/W/kg/mm/°C` 大多本来就是字面值，不在 cn.json 中。
>
> 因此 `cover_brand` / `cover_model` / `spec_unit_*` 这类**虚构 key 不存在**于 v2 cn.json。真正需要锁定的是 **cn.json 中已存在的、跨语言必须等于 cn 值的 key**。

### A. 字面化在母版（无 placeholder，自动跨语言一致）

下列字面值在 W50 母版 OOXML 中直接固化，所有语言自动一致：

| 字面值 | 出现位置 | 备注 |
|--------|---------|------|
| `Wevac` | document.xml + footer*.xml 共 30 处 | v2 阶段 1 改动 1 强制字面化 |
| `IMT050` | 封面 + footer + spec 表 | 型号，原 W50 已字面 |
| `V` / `Hz` / `W` / `kg` / `mm` / `°C` / `Hz/V` | spec 表单元、技术参数行 | 单位字面 |

**生产规则**：阶段 2 翻译对齐时，这些字面值不应出现在任何 `strings/{lang}.json` 的 value 中（否则属于"占位符提取失误"，回阶段 1 retry）。

### B. cn.json 内必须跨语言锁定的 keys（强制 = cn 值）

下列 keys 在 `strings/{en,de,it,gb,hk,tw}.json` 中必须**等于 cn.json 的 value**。`tools/check_invariants.py` 在阶段 2/3 自动校验，违反 = ERROR。

| key 模式 | cn 值（示例） | 锁定理由 |
|---------|-------------|---------|
| `spec_2` | "220-240" | 电压数字范围（C19 单位口径） |
| `spec_3` | "50/60" | 频率数字 |
| `spec_4` | "150" | 功率数字 |
| `spec_5` | "26" | 净重数字 |
| `spec_6` | "12" / "24" | 制冰量数字 |
| `spec_7..23` 中**纯数字行** | 数字 | C19 |
| `cover_*` 中含 `IMT050` 字符串的（混排已拆 `<w:t>`，纯数字若有） | 数字 | 型号附属 |
| `troubleshoot_*` 中故障代码 (E1/E2/E3) | 代码 | 维修一致性 |
| `warranty_*_url` 任何 URL | URL | 不翻译 |
| `warranty_*_email` 邮箱 | 邮箱 | 不翻译 |
| `warranty_*_phone` 电话 | 电话 | 不翻译 |
| `safety_*_box_title` 若 cn 是 "WARNING"/"CAUTION"/"NOTICE"（英文） | 英文 box-title | 跨语言 box-title 用英文 |

> **运行时**：`tools/check_invariants.py` 读 `cn.json` 与 `{lang}.json` 比对，列出违反 keys → 进 fix 循环（一类 ERROR）。
>
> **现状**：v2 阶段 1 完成时 cn.json 304 keys 用的是 `<area>_<seq>` 位置式命名（如 `spec_1..spec_23`、`troubleshoot_1..40`）。具体哪些 seq 是数字行 / URL / 邮箱 / 电话，需要在阶段 2 启动时根据 cn.json 实际 value **生成锁定 keys 清单**（不是预设）。`tools/check_invariants.py` 的实现思路：扫描 cn.json value，匹配纯数字 / URL 正则 / 邮箱正则 / 电话正则 → 自动入锁定列表。

### C. 锁定 keys 自动检测正则（参考实现）

```python
import re, json
def is_invariant(value: str) -> bool:
    if not value or not value.strip(): return False
    # 纯数字 / 数字范围 / 频率
    if re.fullmatch(r'[\d.\-/x×]+', value.strip()): return True
    # URL
    if re.search(r'https?://', value): return True
    # email
    if re.search(r'[\w.\-]+@[\w.\-]+', value): return True
    # phone (含国家码或长数字)
    if re.fullmatch(r'[\+\d\s\-()]{7,}', value.strip()): return True
    # 英文 box-title
    if value.strip() in {'WARNING', 'CAUTION', 'NOTICE', 'DANGER'}: return True
    return False
```

## 母版动 vs 不动决策树

```
有需要调整 OOXML 吗？
├── 单语言 N=1/2/3 fix-or-escalate 中？
│   ├── 是 ERROR 级具体错误（QA-RULES §一-§五）？
│   │   ├── 是 → 改一处 OOXML，单维度，写 patches/{lang}.md
│   │   └── 否 → 不动 OOXML（regression 报警）
│   └── 是总体劣化（mean diff 偏高 / 视觉感"不太对"）？
│       └── 不动 OOXML。回 master 阶段（研究模式），不在本 skill
└── 不在 fix 流程中？
    └── 不动 OOXML。母版 = W50 v2，锁定不重建
```
