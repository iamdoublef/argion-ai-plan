# 3 轮 Fix-or-Escalate 检查清单

> 每次 `generator.py --lang {lang}` 跑完 → 按本清单跑全套检查 → 通过 → 下一语言；不通过 → 单维度 fix → 重跑。
> **3 轮没修通 → 停 + 诊断报告 → 大 boss escalate (QA-RULES §8.4 G4)**。
> 本表对应 QA-RULES §8.1 矩阵的 DOCX 列。

## 一、每轮必跑的检查（按 SOT QA-RULES 顺序）

### Phase 1b — 数据残留（QA §1b）

| 检查 | 工具 | 阈值 |
|------|------|------|
| `strings/{lang}.md` 无空值 | 解析 MD 表格，每行第 2 列非空 | ERROR if 任何空 |
| `master_unpacked/` 中 `{{*}}` 全部替换 | grep `\{\{[^}]+\}\}` on docx 解包后 XML | ERROR if 任何残留 |
| 生成 docx 文本无 `undefined` / `null` / `TODO` | python-docx 读所有 paragraph + cell 文本 grep | ERROR |

### Phase 3c — 文本残留（QA §3c）

| 检查 | 工具 | 阈值 |
|------|------|------|
| 渲染后文本无 `{{*}}` | LO 转 PDF → pdftotext → grep | ERROR |
| 无 `NaN` 字面 | 同上 | ERROR |

### Phase 4a — CJK 残留（QA §4a）

| 目标语言 | 检查 | 阈值 |
|---------|------|------|
| en / de / it | 文本中 `[一-鿿]` 数 = 0 | ERROR if 任意 |
| zh-HK / zh-TW | 与 cn 逐条比对，完全相同条目数 | WARNING（人工抽检）|

### Phase 4b — T1/T2/T3 翻译失败抽检（QA §4b）

按 SOT 定义：
- **T1 Truncation**：翻译后连续多条仍含 CJK → grep 看
- **T2 Wrong key mapping**：A 段翻译落在 B key
- **T3 Key-value swap**：两条互换

T1 自动可查；T2/T3 需要人工抽检 5-10 条（G2 阶段已做 + G3 再抽）。

### Phase 4d — 单位一致性（QA §4d / DESIGN C19）

| 检查 | 阈值 |
|------|------|
| 正文中 `V/Hz/W/kg/mm/°C` 与规格表一致 | ERROR if 冲突 |
| 不混用单位体系（公制/英制） | ERROR if 同变体混用 |
| `spec_unit_*` key 跨语言不变 | ERROR if 任一 lang 变了 |

### QA-RULES §8.2 — anti-cheat 三道闸

| 检查 | 阈值 |
|------|------|
| `wt_count` (w:t 节点数) | ≥ 300 |
| `image_hack` (整页图片替换) | == false |
| `text_ratio` (vs W50) | ∈ [0.95, 1.20] |

### 强制 Word 验证

| 检查 | 工具 | 阈值 |
|------|------|------|
| `validate.py`（官方 docx skill） | 必须通过 | ERROR |
| MS Word COM 打开 | `compare_word.py` 或 `docx2pdf.convert()` 不报错 | ERROR（W28 教训）|

### 页数

| 检查 | 工具 | 阈值 |
|------|------|------|
| 总页数 | LO 转 PDF → pypdf 数页 | 15 (±1) |

### CN 专属

| 检查 | 工具 | 阈值 |
|------|------|------|
| `score_candidate.py` | 评分 vs W50 PDF target | = 7.21/10.13 (±0.01) |

## 二、Fix 决策表

发现某条 ERROR 时，**只允许做表中"fix"列定义的动作**。**不允许** sweep / 探索 lever / 改多维度。

| ERROR | 定位 | Fix（单维度，1 处）| Anti-pattern |
|-------|------|-------------------|--------------|
| `{{*}}` 残留 | 哪个 key | 补 `strings/{lang}.md` 缺失的 key | ❌ 改 master_template / 改 generator 逻辑 |
| CJK 残留 en/de/it | 哪个 key | 补译该 key | ❌ 改 OOXML |
| `undefined`/`null`/`TODO` | 哪段 | 修 generator 模板替换逻辑 或 补 strings | ❌ 加 catch-all |
| 单位不一致 | 哪个 spec_unit_* key | 把该 key 重置为 CN 标准值 | ❌ 让 lang 各自定义 |
| `wt_count < 300` | 比 W50 缺哪些 run | 检查最近 patch 是否合并 run / 删 run → 回滚 | ❌ 加假 `<w:t>` 充数 |
| `image_hack == true` | 哪页变图 | 立即回滚最近 patch | ❌ "重做更细致的图片替换" |
| `text_ratio < 0.95` | 哪段文本丢失 | 补 strings 或回滚漏 key 的 patch | ❌ 加 dummy 文本 |
| `text_ratio > 1.20` | 哪段被重复替换 | 修 generator 幂等性 | ❌ 改 anti-cheat 阈值 |
| validate 失败 | 错误行号 | 修对应 XML 语法（METHODOLOGY §3.1） | ❌ 跳过 validate |
| Word COM 打不开 | 最近 patch | 回滚最近 patch | ❌ 切到 LO 替代 |
| 页数 ≠ 15 | 哪段多/少 | 多 1 页：检查最近 patch 是否拉长某段；少 1 页：检查是否合段了 | ❌ 改 sectPr 强加分页 |
| score（CN）≠ W50 | 哪页 diff 高 | 阶段 1 占位符提取错了，回阶段 1 retry | ❌ 在阶段 3 修 OOXML 让 CN 评分回来 |

## 三、Patches 日志格式（patches/{lang}.md）

```markdown
# {LANG} OOXML / 数据修复日志

> 每条 fix = 1 个 iter，**只改一处**。
> 状态 ✅ Applied / ❌ Rejected。Rejected 必须回滚。

## fix 1 — strings/de.md 第 47 行 safety_warning_5 漏译
- **状态**: ✅ Applied (iter-1, sha:abc1234)
- **触发**: QA Phase 1b 在 master_unpacked/word/document.xml p3 扫到 `{{safety_warning_5}}` 残留
- **定位**: strings/de.md 第 47 行 key `safety_warning_5` value 为空
- **fix**: 补 strings/de.md 第 47 行德文翻译 "Schalten Sie das Gerät vor der Installation aus"
- **验证**: 重跑 generator.py --lang de → grep 无残留 → anti-cheat 通过 → Word COM 通过 → 页数=15

## fix 2 — output/...-de.docx p3 wt_count 降至 285（< 300）
- **状态**: ❌ Rejected (iter-2)
- **触发**: anti-cheat wt_count = 285
- **定位**: fix-1 之后引入。检查发现 generator 把 de 的长德语单词合并到单 run
- **fix**: 改 generator.py 不合并 run（保留 W50 的 run 结构）
- **验证**: 重跑 → wt_count = 372 ✅
- 备注: 标 ❌ Rejected 是因为初次 patch 引入了 wt_count 降，第二次 patch 才修通；patches 留痕便于回查
```

## 四、3 轮上限严格遵守

```
iter-1: 跑全套检查 → 若任一 ERROR：定位 + 单维度 fix → 写 patches/{lang}.md
iter-2: 重跑全套 → 同上
iter-3: 重跑全套 → 若仍有 ERROR：停，**不允许 iter-4**

转 G4：
  - 写 docs/diagnosis-{lang}.md：
    - 每轮 patch 内容 + 验证结果
    - 最终未通过的 ERROR 列表
    - 推测原因（最有用：哪个 SOT 条款冲突，或 W50 母版本身有缺陷）
    - 建议：a) 人工改 strings/{lang}.md / b) 退回阶段 1 改 master / c) 砍该语言交付
  - 暂停该语言；继续跑其他语言
  - 报大 boss
```

## 五、3 轮也修不通的常见原因（背景知识）

| 现象 | 真因 | 应对 |
|------|------|------|
| de 页数永远 16 | 德语长，文本溢出 1 页 | 缩短某段 strings/de.md / 检查 W50 是否有 DE 补偿（DESIGN §三 §十八 18.3） |
| en 评分仍差 W50 0.5+ | W50 母版本身基于 CN 训练，EN 文本宽度差异结构性问题 | 不修，标 ACCEPTANCE_REPORT 为 WARNING（EN 视觉与 CN 有结构性差） |
| zh-HK / zh-TW 大量与 CN 相同 | 翻译团队直接复制了 CN | 转翻译团队补繁体差异，**不动 OOXML** |
| validate 反复挂同一行 | XML schema 不匹配最近改动 | 看 METHODOLOGY §3.1，回滚到上一可通过版本 |
| Word COM 间歇打不开 | OOXML 边缘 case，可能是 W28-类问题 | 立即回滚最近所有 patch，从头重 generator |

3 轮没修通**不是失败**，是该 escalate 的信号。**继续硬刚反而毁掉前面通过的语言**。

## 六、与 QA-RULES Phase 5 全变体验证的衔接

3 轮 fix-or-escalate **per language**。全 7 语言跑完后还要做 QA Phase 5：

- 全部 docx 一起跑 anti-cheat 横扫
- 抽样人工 review（G3）
- 写 ACCEPTANCE_REPORT.md
- commit + 交付
