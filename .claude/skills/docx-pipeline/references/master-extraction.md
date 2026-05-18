# 母版占位符提取规则（阶段 1 最关键步骤）

> W50 docx 是 50 轮微调累积出来的视觉锚。模板化的核心约束：**不破坏 W50 OOXML 微调**。
> 占位符提取错了，后面全错。这步必须严格。

## 替换原则

### 要替换 → 变成 `{{key}}`
- 所有汉字字串（含标点）
- 例：`<w:t>本产品仅供家庭使用</w:t>` → `<w:t>{{safety_warning_1}}</w:t>`

### 不要替换 → 保持原样
- 型号：`IMT050` / `IMT060` 等
- 品牌：`Wevac` / `Argion` / `Vesta`
- 单位：`mm` / `kg` / `W` / `V` / `Hz` / `°C` / `Hz/V`
- 版本号 / 二维码 URL / 邮编 / 电话号
- 表格中的纯数字
- 所有 OOXML 属性（`w:val`, `w:fill`, `w:color` 等）

### 中英混排注意
W50 部分段落中英混排（型号 + 中文描述）。中英混排在 OOXML 里通常是 **两个 run**：

```xml
<w:r>
  <w:rPr><w:rFonts w:ascii="Arial Black"/></w:rPr>
  <w:t xml:space="preserve">IMT050 </w:t>      ← 不替换（型号）
</w:r>
<w:r>
  <w:rPr><w:rFonts w:ascii="Microsoft YaHei"/></w:rPr>
  <w:t>自动制冰机</w:t>                          ← 替换 → {{cover_tagline}}
</w:r>
```

**只换中文 run 的 `<w:t>` 内容**，不要碰 run 结构、不要合并 run、不要改 `<w:rPr>`。

## Key 命名规范

格式：`<area>[_<subarea>]_<sequence>`（v2 实地：`<area>_<seq>` 位置式即可，多数 area 不分 subarea）

| Area | 含义 | v2 实例（位置式 seq） |
|------|------|---------------------|
| `cover` | 封面 | `cover_1` ~ `cover_4` |
| `toc` | 目录 | `toc_1` ~ `toc_12` |
| `safety` | 安全（v2 三 subarea） | `safety_warning_*` (p3) / `safety_caution_*` (p4 前) / `safety_notice_*` (p4 后) |
| `install` | 安装（v2 二 subarea） | `install_prep_*` (p5) / `install_transport_*` (p13) |
| `operate` | 操作（v2 三 subarea） | `operate_structure_*` (p6) / `operate_function_*` (p7) / `operate_guide_*` (p9-p10) |
| `clean` | 清洁保养 | `clean_1` ~ `clean_17` (p12) |
| `spec` | 规格表 | `spec_1` ~ `spec_23` (p8) |
| `troubleshoot` | 故障排查 | `troubleshoot_1` ~ `troubleshoot_40` (p11) |
| `warranty` | 保修（v2 二 subarea） | `warranty_*` (p14) / `warranty_card_*` (p15) |
| `footer` | 页脚 | `footer2_001` ~ `footer15_001`（每页一个，按页号）|

**v2 实际 304 keys 分布**：cover 4 / toc 12 / safety 43 / install 46 / operate 60 / spec 23 / troubleshoot 40 / clean 17 / warranty 45 / footer 14。

**序号**：sequence 是该 area（或 area+subarea）内文档先后顺序，从 1 起。

**禁用**：
- 不要用中文 pinyin（如 `anquan_jinggao_1`）
- 不要用纯位置（`p3_line5`），因为页码会变
- 不要用纯数字（`text_1`），看不出语义

> **brand `Wevac` / 型号 `IMT050` / 单位 `V/Hz/W/kg/mm/°C` 不进 placeholder**（v2 已字面化在母版 OOXML 内）。详见 `references/ooxml-map.md` "跨语言锁定 keys §A 字面化在母版"。

## 提取算法

```python
# pseudocode
def extract_master(w50_unpacked_dir):
    placeholder_map = {}        # key → 原中文
    section_order = []          # 按文档顺序记录 key
    sequence_counter = {}       # area → 当前序号

    for xml_file in [document.xml, header*.xml, footer*.xml]:
        for run in iter_runs(xml_file):
            text = run.text
            if not contains_chinese(text):
                continue                # 跳过纯英数 run

            # 判断 area（看 run 所在 paragraph 的 sectPr 或最近 heading）
            area = classify_area(run.context)

            # 生成 key
            sequence_counter[area] = sequence_counter.get(area, 0) + 1
            subarea = classify_subarea(run.context)
            if subarea:
                key = f'{area}_{subarea}_{sequence_counter[area]}'
            else:
                key = f'{area}_{sequence_counter[area]}'

            placeholder_map[key] = text
            section_order.append(key)
            run.text = f'{{{{{key}}}}}'

    return placeholder_map, section_order
```

## 输出 3 个文件

### 1. `master_template.docx`
W50 的占位符化版本。所有中文 run 的 `<w:t>` 被替换为 `{{key}}`。

### 2. `strings/cn.json` + `strings/cn.md`

cn.json 是事实 SOT（generator.py 读这个），cn.md 是给人看的对照表（手改任何一份后必须同步）：

```markdown
# IMT050 中文翻译字典 (v2)

> 总占位符数：304（来自 W50 v2 母版）
> 来源：swiss/output/imt050-wevac-eu-cn.docx → 阶段 1 v2 提取
> Round-trip CN 评分：mean 5.59 / max 10.10（不再是 v1 的 7.21/10.13；brand 字面化导致结构性偏移）

## 封面
| Key | 中文文本 | 位置 | 备注 |
|-----|---------|------|------|
| cover_1 | 制冰机 | p1 副标 | |
| cover_2 | 说明书 | p1 标题 | |
| cover_3 | 使用产品前请仔细阅读本说明书，并妥善保管。 | p1 提示 | |
| cover_4 | 说明书中的产品、配件等插图均为示意图... | p1 免责 | |

> brand `Wevac` 与型号 `IMT050` 已字面化在母版 OOXML 内，不在 cn.json 中。

## 第 1 章 安全须知 (p3-p4)
| Key | 中文文本 | 位置 | 备注 |
|-----|---------|------|------|
| safety_warning_1 | 本机仅供家庭使用... | p3 WARNING 框 | |
| safety_warning_2 | 安装前请关闭电源 | p3 WARNING 框 | |
| safety_caution_1 | ... | p4 CAUTION 框 | |
| safety_notice_1 | ... | p4 NOTICE 框 | v2 新增 subarea |
```

### 3. `docs/PLACEHOLDER_MAP.md`
```markdown
# 占位符提取报告

## 统计
- 总占位符数：347
- 按 area 分布：
  - cover: 8
  - safety: 42
  - install: 56
  - operate: 89
  - clean: 28
  - spec: 35
  - troubleshoot: 48
  - warranty: 30
  - footer: 11

## 提取规则记录
- 跳过的 run：型号 12 处、品牌 18 处、单位 24 处、URL 3 处
- 合并的 run：0（**不允许合并**）
- 拆分的 run：0（**不允许拆分**）

## 抽样验证（30 处）
| Key | OOXML 位置 | 中文 | run rPr |
|-----|-----------|------|---------|
| safety_warning_1 | document.xml:1247 | 本产品仅供家庭使用 | sz=14 BLACK Microsoft YaHei |
| ... | | | |

## 跨语言锁定 keys 清单
（这些 key 在所有 strings/{lang}.json 中保持原 cn 值；详见 `ooxml-map.md` "跨语言锁定 keys"）
- 自动识别：cn value 匹配纯数字 / URL / email / 电话 / 英文 box-title 的 keys（由 `tools/check_invariants.py` 输出 `docs/stage2-invariant-keys.json`）
- 字面值不进 cn.json：brand `Wevac` / 型号 `IMT050` / 单位 `V/Hz/W/kg/mm/°C` 已母版字面化
```

## 阶段 1 验收清单

- [ ] master_template.docx 通过 validate
- [ ] master_template.docx 通过 MS Word COM（Linux dev 可用 `--skip-word-com`，但 G1 packet 必须含一次 Windows 验证）
- [ ] strings/cn.json 占位符数 = master_template.docx 中 `{{*}}` 数（v2 = 304）
- [ ] PLACEHOLDER_MAP.md 抽样 30 处人工 review 通过
- [ ] generator.py --lang cn → round-trip CN docx 评分 mean ≤ 12 / max ≤ 12（v2 baseline 5.59/10.10）
- [ ] 跨语言锁定 keys 已自动识别并写入 `docs/stage2-invariant-keys.json`
- [ ] 大 boss 人工 review 通过

通过才进阶段 2。**round-trip 越界（mean>12 或 max>12）就退回重做，绝不带病前进**。
