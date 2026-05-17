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

格式：`<area>_<subarea>_<sequence>`

| Area | 含义 | 示例 |
|------|------|------|
| `cover` | 封面 | `cover_brand`, `cover_model`, `cover_tagline` |
| `toc` | 目录 | `toc_chapter_1`, `toc_chapter_2` |
| `safety` | 安全章节 | `safety_warning_1`, `safety_caution_3` |
| `install` | 安装章节 | `install_step_1`, `install_diagram_label_a` |
| `operate` | 操作章节 | `operate_button_start`, `operate_mode_normal` |
| `clean` | 清洁保养 | `clean_step_1`, `clean_warning` |
| `spec` | 规格表 | `spec_voltage_label`, `spec_dim_label` |
| `troubleshoot` | 故障排查 | `troubleshoot_q1`, `troubleshoot_a1` |
| `warranty` | 保修 | `warranty_terms`, `warranty_period` |
| `footer` | 页脚 | `footer_copyright`, `footer_url` |

**序号**：sequence 是文档内出现顺序，从 1 起。

**禁用**：
- 不要用中文 pinyin（如 `anquan_jinggao_1`）
- 不要用纯位置（`p3_line5`），因为页码会变
- 不要用纯数字（`text_1`），看不出语义

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

### 2. `strings/cn.md`
```markdown
# IMT050 中文翻译字典

> 总占位符数：347 个（来自 W50）
> 来源：final/imt050-wevac-eu-cn.docx
> 评分锚：7.21/10.13（round-trip 必须复现）

## 封面
| Key | 中文文本 | 位置 | 备注 |
|-----|---------|------|------|
| cover_brand | Wevac | p1 顶部 | 跨语言不变（**别替换**）|
| cover_model | IMT050 | p1 中央 | 跨语言不变（**别替换**）|
| cover_tagline_1 | 自动制冰机 | p1 副标 | |
| cover_subtitle | 使用说明书 | p1 底部 | |

## 第 1 章 安全注意事项 (p3-p4)
| Key | 中文文本 | 位置 | 备注 |
|-----|---------|------|------|
| safety_intro | 请仔细阅读本说明书并妥善保管以备参考 | p3 章首 | |
| safety_warning_1 | 本产品仅供家庭使用 | p3 警告框 | |
| safety_warning_2 | 安装前请关闭电源 | p3 警告框 | |
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

## 跨语言不变 key 清单
（这些 key 在所有 strings/{lang}.md 中保持原值）
- cover_brand: Wevac
- cover_model: IMT050
- spec_unit_v: V
- spec_unit_hz: Hz
- spec_unit_w: W
```

## 阶段 1 验收清单

- [ ] master_template.docx 通过 validate
- [ ] master_template.docx 通过 MS Word COM
- [ ] strings/cn.md 占位符数 = master_template.docx 中 `{{*}}` 数
- [ ] PLACEHOLDER_MAP.md 抽样 30 处人工 review 通过
- [ ] generator.py --lang cn → 评分 = W50 (7.21/10.13 零误差) ← **硬指标**
- [ ] 跨语言不变 key 清单已列出
- [ ] 大 boss 人工 review 通过

通过才进阶段 2。**round-trip ≠ W50 就退回重做，绝不带病前进**。
