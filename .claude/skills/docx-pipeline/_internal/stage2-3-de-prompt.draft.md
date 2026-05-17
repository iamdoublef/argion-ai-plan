# 阶段 2-3 DE Subagent Prompt 草稿

> 这是 main agent 在 subagent A 跑阶段 1 期间预制的草稿。G1 通过后用此 prompt spawn subagent B。

---

你是亚俊氏 docx 多语言流水线的执行 agent，按 `.claude/skills/docx-pipeline/` skill 走 **阶段 2 翻译对齐 + 阶段 3 DE 生成 + 3 轮 fix-or-escalate**。

## 仓库根目录
`D:\work\private\yjsplan\` — 所有相对路径以此为根，请用绝对路径或先 `cd D:/work/private/yjsplan`。

## 任务范围
完成 DE 一个语言的完整流水线（阶段 2 + 阶段 3）。完成后等大 boss G3 confirm。

## 前置条件（阶段 1 已完成）
- ✅ `swiss/tools/docx-pipeline/master_template.docx` 存在 + validate 通过
- ✅ `swiss/tools/docx-pipeline/master_unpacked/` 存在
- ✅ `swiss/tools/docx-pipeline/strings/cn.md` 含全部占位符
- ✅ `swiss/tools/docx-pipeline/docs/PLACEHOLDER_MAP.md` 含 key 命名 + 跨语言不变 key 清单
- ✅ `swiss/tools/docx-pipeline/generator.py` 工作正常（round-trip cn 评分 = W50）
- ✅ `swiss/tools/docx-pipeline/anti_cheat.py` 工作正常

## 必读文件
1. `D:\work\private\yjsplan\.claude\skills\docx-pipeline\SKILL.md` 阶段 2-3 + 3 轮 fix-or-escalate
2. `D:\work\private\yjsplan\.claude\skills\docx-pipeline\references\fix-checklist.md`（3 轮 fix 操作清单 + Fix 决策表）
3. `D:\work\private\yjsplan\.claude\skills\docx-pipeline\references\ooxml-map.md` SOT → OOXML
4. `D:\work\private\yjsplan\research\yjs-manual-opt\swiss\QA-RULES.md` §八 DOCX 适配（Phase 共享矩阵 + 3 轮 fix）
5. `D:\work\private\yjsplan\research\yjs-manual-opt\swiss\DESIGN-STANDARD.md` §十八 DOCX 映射

## 输入资源
- 德语 HTML 翻译模板：`D:\work\private\yjsplan\research\yjs-manual-opt\swiss\template\imt050-master-de.html`
- 阶段 1 产物：`swiss/tools/docx-pipeline/` 下所有文件
- 官方 docx skill：`C:\Users\iamdo\.claude\skills\docx\scripts\office\{unpack,pack,validate}.py`

## 阶段 2：翻译对齐

### 步骤
1. 解析 `swiss/template/imt050-master-de.html`，提取所有德语文本及其上下文（章节、位置）
2. 用 `docs/PLACEHOLDER_MAP.md` 的 key 命名空间映射 HTML 文案到 docx 占位符
3. 写 `swiss/tools/docx-pipeline/strings/de.md`：
   - 格式严格对齐 `strings/cn.md`（同样的 key 排序、同样的 section 分组、同样的表格头）
   - 跨语言不变 key 保持原值：`IMT050` / `Wevac` / `Argion` / `Vesta` / `mm` / `kg` / `W` / `V` / `Hz` / `°C` / 二维码 URL
   - 警示标题 box-title 跨语言英文不变：WARNING / CAUTION / NOTICE
4. spot-check 关键术语跨语言一致：制冰机 → Eismaschine / 警告 → WARNUNG / 安装 → Installation / 等

## 阶段 3：DE 生成 + 3 轮 fix-or-escalate

```
generator.py --lang de --output output/imt050-wevac-eu-de.docx

for iter in 1..3:
  # 跑全套检查（QA-RULES §8.1 矩阵）
  Phase 1b: 数据残留（{{*}}/undefined/null/TODO）
  Phase 4a: CJK 残留（不许有汉字）
  Phase 4b: T1/T2/T3 翻译失败抽检
  Phase 4d: 单位一致性
  anti-cheat 三道闸（wt_count/image_hack/text_ratio）
  validate.py
  Word COM 打开（compare_word.py / docx2pdf；无 MS Word 可标 skip）
  页数 = 15 (±1)

  if 全通过:
    标 PASS，跳出
  else:
    精准定位（哪页/哪段/哪 key）
    单维度 fix（一轮只改一处）
    写 patches/de.md 日志（按 fix-checklist.md §三 格式）
    重跑

if iter == 3 且未通过:
  写 docs/diagnosis-de.md：
    - 每轮 patch 内容 + 验证结果
    - 最终未通过的 ERROR 列表
    - 推测原因（哪个 SOT 条款冲突 / W50 母版结构性问题）
    - 建议（人工改 strings / 退阶段 1 改 master / 砍 DE 交付）
  停，转人工
```

### Fix 决策表（严格遵守 fix-checklist.md §二）

| ERROR | 单维度 Fix |
|-------|-----------|
| `{{*}}` 残留 | 补 strings/de.md 缺失 key |
| CJK 残留 | 补译该 key |
| `undefined`/`null`/`TODO` | 修 generator 模板替换 或 补 strings |
| 单位不一致 | 把 spec_unit_* key 重置为 CN 标准值 |
| `wt_count < 300` | 检查最近 patch 是否合并/删 run → 回滚 |
| `image_hack == true` | 立即回滚最近 patch |
| `text_ratio` 越界 | 补漏 key 或修 generator 幂等 |
| validate 失败 | 修对应 XML 语法 |
| Word COM 打不开 | 回滚最近 patch |
| 页数 ≠ 15 | 查哪段多/少，fix 或转 G4 |

### 禁用 lever（W28/W33/W46 教训）
- `w:contextualSpacing`
- `w:val="nil"` 边框（用 `single` + `FFFFFF` 代替）
- 全局 `w:lineRule="auto"→"exact"`

### 禁止行为
- 不做 sub-cohort sweep
- 不超过 3 轮
- 不探索性试 lever（必须有具体 SOT ERROR 才 fix）
- 不重新定义视觉/审计规范（全部引用 SOT）

## 输出物清单

```
swiss/tools/docx-pipeline/
├── strings/
│   └── de.md                           ← 阶段 2 产物
├── output/
│   └── imt050-wevac-eu-de.docx         ← 阶段 3 产物
├── patches/
│   └── de.md                           ← fix 日志（≤ 3 条）
└── docs/
    ├── diagnosis-de.md                 ← 仅当 3 轮未过时
    └── G3_review_packet.md             ← Gate G3 review 材料
```

`docs/G3_review_packet.md` 内容：
- A. 阶段 2 翻译对齐摘要（key 数、跨语言不变 key spot-check）
- B. 阶段 3 生成结果（anti-cheat 三道闸、validate、Word COM、页数、CJK 残留）
- C. patches/de.md 摘要（每条 fix 一句话）
- D. 翻译失败模式 T1/T2/T3 抽检（5-10 条）
- E. 单位一致性核查（spec_unit_* 横向对照）
- F. SOT 条款引用（QA §8.2 / §4 / §十八）
- G. 给大 boss 的 G3 决策建议（PASS / HOLD / FAIL）

## 硬规则

1. 官方 docx skill 是唯一 I/O 入口（W28 教训）
2. anti-cheat 三道闸 + Word COM + 页数 = 15 是 ERROR 底线
3. 3 轮上限严格遵守
4. 单 lever per patch
5. 不动 OOXML 除非有具体 SOT ERROR
6. 引用 SOT 不重定义
7. commit msg 中文
8. 称呼：大 boss / 管理者；禁止 "老板"/"儿子"/"家属"

## 返回格式

完成后简要总结（≤ 500 字）：
1. strings/de.md 占位符数 + 跨语言不变 key 数
2. DE docx anti-cheat 三道闸结果
3. 页数 + Word COM 结果
4. patches/de.md 条目数（≤ 3）+ 状态
5. 是否需要 G4 escalate
6. commit sha

阻塞立即停 + 报告。
