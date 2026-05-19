# 占位符提取报告 (PLACEHOLDER_MAP)

> 阶段 1 母版生成产出之一，配合 `strings/cn.md` + `master_template.docx` 使用。
> 提取规则源：`.claude/skills/docx-pipeline/references/master-extraction.md`。
> 视觉规范源：`swiss/DESIGN-STANDARD.md` §十八。
> 审计规范源：`swiss/QA-RULES.md` §八。

## A. 总览统计

- **总占位符数**：304（覆盖 W50 母版中所有汉字 `<w:t>` 节点）
- **document.xml 中**：290（9 个 area）
- **footer*.xml 中**：14（页脚每页 1 个，p2-p15）

### 按 area 分布

| Area | 含义 | 占位符数 | 来源页 |
|------|------|---------|--------|
| `cover` | 封面 | 4 | p1 |
| `toc` | 目录 | 12 | p2 |
| `safety` | 安全须知（含 warning/caution/notice） | 43 | p3-p4 |
| `install` | 安装与运输（含 prep + transport） | 46 | p5, p13 |
| `operate` | 操作指引（含 structure/function/guide） | 60 | p6-p7, p9-p10 |
| `spec` | 技术参数 | 23 | p8 |
| `troubleshoot` | 故障排除 | 40 | p11 |
| `clean` | 维护保养 | 17 | p12 |
| `warranty` | 保修信息（含 card） | 45 | p14-p15 |
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

## C. 提取规则记录（v2）

### 替换原则（v2 三项改动）

**改动 1（品牌字面化）**：W50 中 `威富可` 全部 30 处（document.xml 16 + footer 14）
→ 母版直接字面化为 `Wevac`，**不再占位**。所有语言版本（含 CN）统一显示 `Wevac`。
`cn.json` value 中 0 处 `威富可`。

**改动 2（中英混排拆 `<w:t>`）**：W50 中 ASCII + CJK 混排在同一 `<w:t>` 内的节点
（如 `IMT050 — 说明书` / `警告 WARNING` / `提示 NOTICE`）→ 在母版中拆成多个 `<w:t>`：
ASCII 部分作为字面 `<w:t xml:space="preserve">…</w:t>`，CJK 部分作为独立 placeholder。
**`<w:r>` 不拆、`<w:rPr>` 不改、`<w:t>` 节点数增加**（OOXML 允许同一 `<w:r>` 多 `<w:t>`）。

**改动 3（safety subarea 三分）**：p3 → `safety_warning_*`；p4 中 NOTICE box-title
之前 → `safety_caution_*`；p4 中从 NOTICE box-title 起 → `safety_notice_*`。

**通用原则**（v1 沿用）：
- 仅替换含汉字（CJK 范围 `[一-鿿　-〿＀-￯]`）的 `<w:t>` 内容
- 不合并、不拆分 `<w:r>`；不改 `<w:rPr>`
- XML 实体（`&quot;`, `&lt;`, `&#x201C;`）原样写入 `strings/cn.json`

### 拆 `<w:t>` 实施统计

- 因中英混排拆 `<w:t>` 数：**60**
- 含 `威富可` 已字面化的 `<w:t>` 数：**30**
- 字面化的 `威富可` 总出现次数：**30**
- `notice_pivot_pos`（p4 NOTICE box-title 偏移）：61497

### 跳过的 w:t（document.xml）

- W50 原始 `<w:t>` 节点：448
- v1 中汉字占位符化（参考）：262
- v1 跳过（型号 / 单位 / 数字 / 标点 / 空白）（参考）：186
- v2 后 `<w:t>` 节点数会因拆分增加；以 round-trip docx 实测 `wt_count` 为准。

### 合并 / 拆分统计

- 合并的 `<w:r>`：**0**
- 拆分的 `<w:r>`：**0**（v2 仍不拆 `<w:r>`；只拆 `<w:t>` = 60 个）
- 修改的 `<w:rPr>`：**0**
- unpack 时已指定 `--merge-runs false --simplify-redlines false`

## D. 抽样验证（30 处）

从 `master_unpacked/word/document.xml` 抽 30 个 placeholder（跨 9 个 area + footer），
列：key + 原文（中文）+ OOXML 位置（文件:行号）+ run rPr（sz/font/color/bold）。

| # | Key | 中文文本 | OOXML 位置 | run rPr |
|---|-----|----------|-----------|---------|
| 1 | `cover_1` | 制冰机 | `document.xml:94` | sz=36 font=Calibri bold color=1A1A1A bold |
| 2 | `toc_1` | 说明书 | `document.xml:204` | sz=10 font=Courier New color=F5F5F5 |
| 3 | `safety_warning_1` | 安全须知 | `document.xml:660` | sz=22 font=Calibri bold color=000000 bold |
| 4 | `safety_warning_15` | 禁止在手脚潮湿或未穿鞋的情况下触摸产品电源部件。 | `document.xml:1079` | sz=13 font=Calibri color=000000 |
| 5 | `safety_caution_2` | 注意  | `document.xml:1521` | sz=12 font=Calibri bold color=000000 bold |
| 6 | `install_prep_1` | 产品及使用提示 | `document.xml:1888` | sz=22 font=Calibri bold color=000000 bold |
| 7 | `install_prep_16` | 适用水源：纯净饮用水、 | `document.xml:2132` | sz=14 font=Calibri color=000000 |
| 8 | `install_transport_6` | 运输后需静置  | `document.xml:8544` | sz=14 font=Calibri color=000000 |
| 9 | `operate_structure_1` | 产品结构 | `document.xml:2361` | sz=22 font=Calibri bold color=000000 bold |
| 10 | `operate_structure_11` | 排水孔 | `document.xml:3016` | sz=13 font=Calibri color=1A1A1A |
| 11 | `operate_function_9` | 清洁 | `document.xml:3618` | sz=13 font=Calibri color=1A1A1A |
| 12 | `operate_guide_3` | 务必将产品放置在平整稳固的平面，且产品背部和右侧散热孔处不能放置任何东西，以免阻挡散热。产品与墙或物品之间距离必须  | `document.xml:5411` | sz=14 font=Calibri color=000000 |
| 13 | `operate_guide_13` |  按键，按键显示白灯，产品已处于开机状态。 | `document.xml:5527` | sz=14 font=Calibri color=000000 |
| 14 | `operate_guide_23` |    选择完尺寸后，产品自动开始制作子弹冰。 | `document.xml:6195` | sz=14 font=Calibri color=000000 |
| 15 | `spec_1` | 技术参数 | `document.xml:3890` | sz=22 font=Calibri bold color=000000 bold |
| 16 | `spec_8` | 尺寸（宽 | `document.xml:4333` | sz=13 font=Calibri color=1A1A1A |
| 17 | `spec_15` | 冰块  | `document.xml:4641` | sz=13 font=Calibri color=1A1A1A |
| 18 | `troubleshoot_1` | 故障排除 | `document.xml:6600` | sz=22 font=Calibri bold color=000000 bold |
| 19 | `troubleshoot_14` | 给水箱加水至水位线。 | `document.xml:7070` | sz=13 font=Calibri color=1A1A1A |
| 20 | `troubleshoot_27` | 次冰块偏小 | `document.xml:7450` | sz=13 font=Calibri color=1A1A1A |
| 21 | `clean_1` | 维护保养 | `document.xml:7901` | sz=22 font=Calibri bold color=000000 bold |
| 22 | `clean_9` |    将产品底部的排水孔塞松脱，让内腔的水排干。 | `document.xml:8087` | sz=14 font=Calibri color=000000 |
| 23 | `warranty_1` | 品牌与保修信息 | `document.xml:8933` | sz=22 font=Calibri bold color=000000 bold |
| 24 | `warranty_12` | 网址 | `document.xml:9250` | sz=13 font=Calibri color=1A1A1A |
| 25 | `warranty_23` | 保修信息 | `document.xml:9721` | sz=15 font=Calibri bold color=000000 bold |
| 26 | `warranty_card_2` | 保修卡 | `document.xml:9938` | sz=15 font=Calibri bold color=000000 bold |
| 27 | `footer_1` | 说明书 | `footer2.xml:57` | sz=10 font=Calibri color=E8E8E8 |
| 28 | `footer_4` | 说明书 | `footer5.xml:57` | sz=10 font=Calibri color=E8E8E8 |
| 29 | `footer_7` | 说明书 | `footer8.xml:57` | sz=10 font=Calibri color=E8E8E8 |
| 30 | `footer_10` | 说明书 | `footer11.xml:57` | sz=10 font=Calibri color=E8E8E8 |

## E. 跨语言不变 Key 清单

这些 key（或 key 中嵌入的字串）在所有 `strings/{lang}.md` 中保持相同值。

| Key pattern | 跨语言固定值 | 原因 |
|------------|------------|------|
| 品牌"威富可" → 母版直接字面 `Wevac`（不再占位） | `Wevac` | v2 改动 1：所有 30 处品牌（含 footer / cover / 嵌入）已在母版字面化 |
| 型号 `IMT050` / `IMT060` 等 | `IMT050` | v2 改动 2：中英混排已在母版拆 `<w:t>`，型号作为字面 `<w:t>` 保留 |
| `spec_*` 单位字段 `V`/`Hz`/`W`/`kg`/`mm`/`°C`/`dB(A)` | 跨语言一致 | QA-RULES C19；v1 已字面（原非占位）+ v2 混排拆出更多单位字面 |
| 警示框标题 `WARNING`/`CAUTION`/`NOTICE`/`DISCLAIMER` | 英文不变 | v2 改动 2 后已与中文 box-title 文字拆开：`{{safety_*_1}}` = `提示 ` / `警告 ` / `注意 ` / `免责声明 `，字面后缀保留 |
| 二维码 URL / 邮箱 / 电话 | 同 CN | URL/邮箱不翻；v1/v2 均为字面 |

说明（v2）：W50 母版中所有 ASCII + CJK 混排在同一个 `<w:t>` 内的片段，在
`extract_master.py` v2 中已 **拆 `<w:t>`**（保留同一 `<w:r>`，不改 `<w:rPr>`）：
ASCII 部分作为字面 `<w:t>`，CJK 部分作为独立 placeholder。
译者只需翻译 CJK 部分，不再需要"保留 `IMT050` 字串"这类约束。

## F. Round-trip 闭环验证（v2 新基准）

用 v2 `master_template.docx` + `strings/cn.json` 重生成 `round_trip_cn.docx`，
对照 W50 PDF target 评分：

- pages: target=15 / candidate=15 ratio=1.0
- text chars: target=4626 / candidate=4686 ratio=1.01
- editable_pct: 100.0% / wt_count=545
- visual: overall_mean_diff=5.59 / max_page_diff=10.1
- pass: {'pages': True, 'text': True, 'editable': True, 'visual': True, 'overall': True}

**v1 baseline (7.21/10.13) 不再适用**：v2 引入品牌字面化（30 处汉字 → 拉丁字符，字符宽度变化）+ 中英混排拆 `<w:t>`，
已与大 boss 确认接受 **v2 round-trip 评分作为新 CN 视觉基准**。

## G. 阶段 1 v2 验收清单

- [x] master_template.docx 通过 validate.py（对照 W50 自身基线）
- [x] master_template.docx 中 `威富可` 子串数 = 0
- [x] strings/cn.json 不含 `威富可` 作为 value
- [x] round_trip_cn.docx 通过 anti-cheat 三道闸 + 页数 + Word COM
- [x] PLACEHOLDER_MAP.md 含 30+ 抽样（本文件）
- [x] strings/cn.md 占位符数 = master_template `{*}` 数（304）
- [x] safety_notice_* 已切（v2 改动 3）
