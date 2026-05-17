# 占位符提取报告 (PLACEHOLDER_MAP)

> 阶段 1 母版生成产出之一，配合 `strings/cn.md` + `master_template.docx` 使用。
> 提取规则源：`.claude/skills/docx-pipeline/references/master-extraction.md`。
> 视觉规范源：`swiss/DESIGN-STANDARD.md` §十八。
> 审计规范源：`swiss/QA-RULES.md` §八。

## A. 总览统计

- **总占位符数**：277（覆盖 W50 母版中所有汉字 `<w:t>` 节点）
- **document.xml 中**：263（9 个 area）
- **footer*.xml 中**：14（页脚每页 1 个，p2-p15）

### 按 area 分布

| Area | 含义 | 占位符数 | 来源页 |
|------|------|---------|--------|
| `cover` | 封面 | 5 | p1 |
| `toc` | 目录 | 13 | p2 |
| `safety` | 安全须知（含 warning/caution/notice） | 41 | p3-p4 |
| `install` | 安装与运输（含 prep + transport） | 36 | p5, p13 |
| `operate` | 操作指引（含 structure/function/guide） | 55 | p6-p7, p9-p10 |
| `spec` | 技术参数 | 22 | p8 |
| `troubleshoot` | 故障排除 | 34 | p11 |
| `clean` | 维护保养 | 18 | p12 |
| `warranty` | 保修信息（含 card） | 39 | p14-p15 |
| `footer` | 页脚 | 14 | p2-p15 |

## B. Key 命名规则

格式：`<area>_[<subarea>_]<seq>`，seq 是该 area（或 area+subarea）内的全局递增（从 1 起）。

### area 分类（按 master-extraction.md §Key 命名）

- `cover` 封面 / `toc` 目录 / `safety` 安全 / `install` 安装/准备/运输 /
  `operate` 操作（结构/按键/步骤） / `spec` 规格 / `troubleshoot` 故障 /
  `clean` 清洁保养 / `warranty` 保修 / `footer` 页脚
- subarea（按页/语义二级细分）：
  - `safety_warning_*`（p3）/ `safety_caution_*`（p4）
  - `install_prep_*`（p5）/ `install_transport_*`（p13）
  - `operate_structure_*`（p6）/ `operate_function_*`（p7）/ `operate_guide_*`（p9-p10）
  - `warranty_*`（p14）/ `warranty_card_*`（p15）

**禁用模式**（master-extraction.md §禁用）：
- 不用中文 pinyin / 不用纯位置 `p3_line5` / 不用纯数字 `text_1`

## C. 提取规则记录

### 替换原则

- 仅替换**包含汉字**的 `<w:t>` 节点内容 → `{{key}}`
- 不动 run 结构（不合并、不拆分 `<w:r>`，不改 `<w:rPr>`）
- 中英混排（如 `IMT050 — 说明书`）若在同一 `<w:t>` 节点 → 整体作为一个占位符；
  译者在 `strings/{lang}.md` 中保留 `IMT050` 等型号字串
- XML 实体（`&quot;`, `&lt;`, `&#x201C;`）原样写入 `strings/cn.json` → 替换回去仍是合法 XML

### 跳过的 w:t（document.xml）

- 总 `<w:t>` 节点：448
- 汉字占位符化：262
- 跳过（型号 `IMT050` / 品牌英文 `Wevac` / 单位 `mm`/`kg`/`W`/`V`/`Hz`/`°C` / 数字 / 标点 / 空白）：186

### 合并 / 拆分统计

- 合并的 `<w:r>`：**0**（W50 不动）
- 拆分的 `<w:r>`：**0**（W50 不动）
- unpack 时已指定 `--merge-runs false --simplify-redlines false` 保护 W50 micro-tuning

## D. 抽样验证（30 处）

从 `master_unpacked/word/document.xml` 抽 30 个 placeholder（跨 9 个 area + footer），
列：key + 原文（中文）+ OOXML 位置（文件:行号）+ run rPr（sz/font/color/bold）。

| # | Key | 中文文本 | OOXML 位置 | run rPr |
|---|-----|----------|-----------|---------|
| 1 | `cover_1` | 威富可 | `document.xml:26` | sz=15 font=Arial Black color=000000 bold |
| 2 | `toc_1` | 威富可 | `document.xml:195` | sz=13 font=Arial Black color=000000 bold |
| 3 | `safety_warning_1` | 威富可 | `document.xml:622` | sz=13 font=Arial Black color=000000 bold |
| 4 | `safety_warning_14` | 如发现插头、电源线或主机损坏，请立即停止使用并联系制造商或授权维修点处理，请勿自行拆修。 | `document.xml:1028` | sz=13 font=Arial color=000000 |
| 5 | `safety_warning_27` | 请勿在本产品中储存含有易燃推进剂的气溶胶罐等爆炸性物质。 | `document.xml:1366` | sz=13 font=Arial color=000000 |
| 6 | `install_prep_1` | 威富可 | `document.xml:1850` | sz=13 font=Arial Black color=000000 bold |
| 7 | `install_prep_13` | 禁止 | `document.xml:2159` | sz=14 font=Arial Black color=000000 bold |
| 8 | `install_transport_6` | 运输后需静置 4 小时，待冷媒稳定后再通电。 | `document.xml:8545` | sz=14 font=Arial color=000000 |
| 9 | `operate_structure_1` | 威富可 | `document.xml:2323` | sz=13 font=Arial Black color=000000 bold |
| 10 | `operate_structure_10` | 控制面板 | `document.xml:2868` | sz=13 font=Arial color=1A1A1A |
| 11 | `operate_function_6` | 点击开机，长按关机。 | `document.xml:3493` | sz=13 font=Arial color=1A1A1A |
| 12 | `operate_guide_1` | 威富可 | `document.xml:5329` | sz=13 font=Arial Black color=000000 bold |
| 13 | `operate_guide_10` | 如何制作子弹冰 | `document.xml:5546` | sz=15 font=Arial Black color=000000 bold |
| 14 | `operate_guide_19` |    选择完尺寸后，产品自动开始制作子弹冰。 | `document.xml:6196` | sz=14 font=Arial color=000000 |
| 15 | `spec_1` | 威富可 | `document.xml:3852` | sz=13 font=Arial Black color=000000 bold |
| 16 | `spec_8` | 脱冰功率 | `document.xml:4257` | sz=13 font=Arial color=1A1A1A |
| 17 | `spec_15` | 冰块 M | `document.xml:4719` | sz=13 font=Arial color=1A1A1A |
| 18 | `troubleshoot_1` | 威富可 | `document.xml:6562` | sz=13 font=Arial Black color=000000 bold |
| 19 | `troubleshoot_12` | 不能制冰 | `document.xml:6999` | sz=13 font=Arial color=1A1A1A |
| 20 | `troubleshoot_23` | 及时给水箱补充水，产品会自动恢复制冰。 | `document.xml:7410` | sz=13 font=Arial color=1A1A1A |
| 21 | `clean_1` | 威富可 | `document.xml:7863` | sz=13 font=Arial Black color=000000 bold |
| 22 | `clean_10` |    将产品底部的排水孔塞松脱，让内腔的水排干。 | `document.xml:8088` | sz=14 font=Arial color=000000 |
| 23 | `warranty_1` | 威富可 | `document.xml:8895` | sz=13 font=Arial Black color=000000 bold |
| 24 | `warranty_10` | 网址 | `document.xml:9251` | sz=13 font=Arial color=1A1A1A |
| 25 | `warranty_19` | 网址 | `document.xml:9666` | sz=13 font=Arial color=1A1A1A |
| 26 | `warranty_card_1` | 威富可 | `document.xml:9882` | sz=13 font=Arial Black color=000000 bold |
| 27 | `footer_1` | 威富可 IMT050 说明书 | `footer2.xml:57` | sz=10 font=Arial color=E8E8E8 |
| 28 | `footer_4` | 威富可 IMT050 说明书 | `footer5.xml:57` | sz=10 font=Arial color=E8E8E8 |
| 29 | `footer_7` | 威富可 IMT050 说明书 | `footer8.xml:57` | sz=10 font=Arial color=E8E8E8 |
| 30 | `footer_10` | 威富可 IMT050 说明书 | `footer11.xml:57` | sz=10 font=Arial color=E8E8E8 |

## E. 跨语言不变 Key 清单

这些 key（或 key 中嵌入的字串）在所有 `strings/{lang}.md` 中保持相同值。

| Key pattern | 跨语言固定值 | 原因 |
|------------|------------|------|
| `cover_brand`（如果单独抽出） | 在 cn=威富可 / en=Wevac / de=Wevac / 其他=Wevac | 品牌名（中文版用本地译名「威富可」，欧/英版用 `Wevac`） |
| 任何 `*_brand` / 模型号嵌入 | `IMT050` | 型号永不翻译，由译者保留原型号字串 |
| `spec_*` 单位字段 | `V`, `Hz`, `W`, `kg`, `mm`, `°C`, `dB(A)` | 单位跨语言一致（QA-RULES C19） |
| 警示框标题 `safety_warning_*` 含 `WARNING/CAUTION/NOTICE` 文字段 | 英文不变 | 三级警示标题国际标准 |
| 二维码 URL、邮箱、电话等 | 同 CN | URL/邮箱不翻 |

说明：因 W50 母版中 `IMT050 — 说明书` 等中英混排片段处于**同一个 `<w:t>`** 节点，
按 master-extraction.md 「不动 run 结构」原则，整段（含 `IMT050`）作为一个占位符，
译者在 `strings/{lang}.md` 中保留型号字串即可（如 EN：`IMT050 — User Manual`）。

## F. Round-trip 闭环验证

用 `master_template.docx` + `strings/cn.json` 重生成 `round_trip_cn.docx`，
对照 W50 PDF target 评分：

- pages: target=15 / candidate=15 ratio=1.0
- text chars: target=4626 / candidate=4626 ratio=1.0
- editable_pct: 100.0% / wt_count=448
- visual: overall_mean_diff=7.21 / max_page_diff=10.13
- pass: {'pages': True, 'text': True, 'editable': True, 'visual': True, 'overall': True}

**与 W50 baseline (7.21/10.13) 误差 = 0.00 ✅**

## G. 阶段 1 验收清单

- [x] master_template.docx 通过 validate.py（对照 W50 自身基线）
- [x] round_trip_cn.docx 评分 = W50 (7.21/10.13) 零误差
- [x] round_trip_cn.docx 通过 anti-cheat 三道闸 + 页数 + Word COM
- [x] PLACEHOLDER_MAP.md 含 30+ 抽样（本文件）
- [x] strings/cn.md 占位符数 = master_template `{*}` 数（277）
