# SOT 边界清理执行 Plan

> **触发时机**：subagent A 跑完 + G1 review 通过后执行（避免 subagent 中途读到不一致版本）。
> **目标**：按大 boss "一致放一起，不一致分开" 原则，把 SOT 文档里的 DOCX 实现细节剥离到 docx-pipeline skill 内。

## 一、原则

| 内容性质 | 归属 |
|---------|------|
| 双流水线**完全共享**的语义条款（颜色/字号/警示三级/内容结构/翻译质检语义/单位口径） | **SOT 主体**（DESIGN-STANDARD / QA-RULES） |
| 双流水线**对照说明**（哪个 Phase 谁负责、哪些自动谁人工） | **SOT 主体**（保留作为治理） |
| **PDF 特定实现**（CSS 选择器、border-left/right、Playwright 工具调用） | **SOT 标 [PDF 实现]**，目前留 SOT（PDF skill 尚未结构化拆出） |
| **DOCX 特定实现**（OOXML 元素映射、anti-cheat 阈值、3 轮 fix-or-escalate、4 个 review gate） | **docx-pipeline skill 内**（不在 SOT 主体） |

## 二、DESIGN-STANDARD.md 改动

### 2.1 删 §十八（DOCX 流水线实现映射）
- §18.1 母版与生成模型 → 已在 `SKILL.md` 二、八，**确认已覆盖即删**
- §18.2 条款映射速查表 → 已在 `references/ooxml-map.md` 顶部表格，**确认已覆盖即删**
- §18.3 DOCX 语言补偿 → 已在 `references/ooxml-map.md` §"长语言补偿"，**已覆盖**
- §18.4 3 轮 fix-or-escalate → 已在 `SKILL.md` 六 + `references/fix-checklist.md`，**已覆盖**
- §18.5 哪些条款不在 DOCX 自动验证 → 已在 `references/ooxml-map.md` 末尾 + `fix-checklist.md`，**已覆盖**

### 2.2 顶部声明调整
- 保留 SOT 双流水线声明
- 删掉 "[DOCX 实现] 标签" 这一类（DOCX 实现整体移走，标签无意义）
- 改成："本文含 [语义]（双方共享）+ [PDF 实现]（PDF 流水线专属）。DOCX 实现细则在 `.claude/skills/docx-pipeline/` 内。"

### 2.3 末尾加 DOCX 实现指针
```markdown
---
## DOCX 流水线实现指针

DOCX 流水线的所有实现细则（母版生成、OOXML 映射、anti-cheat、3 轮 fix-or-escalate、4 个 review gate）在：
- `.claude/skills/docx-pipeline/SKILL.md` — 流水线 4 阶段总览
- `.claude/skills/docx-pipeline/references/ooxml-map.md` — SOT 条款 → OOXML 元素
- `.claude/skills/docx-pipeline/references/fix-checklist.md` — 3 轮 fix-or-escalate
- `.claude/skills/docx-pipeline/references/master-extraction.md` — 阶段 1 提取规则
- `.claude/skills/docx-pipeline/references/anti-cheat-impl.md` — anti-cheat.py 实现

本 SOT 文档变动时，docx-pipeline skill 内的实现映射必须同步更新（双流水线一致性原则）。
```

### 2.4 变更记录加 v1.7
```
| v1.7 | 2026-05-17 | 边界清理：剥离 §十八（DOCX 实现细节）回 docx-pipeline skill，按"一致放一起，不一致分开"原则 |
```

## 三、QA-RULES.md 改动

### 3.1 保留 §八 但只留对照说明
原 §八 4 小节：
- §8.1 Phase 共享/替代矩阵 → **保留**（双流水线对照说明，是 SOT 治理）
- §8.2 DOCX 专属 anti-cheat → **移到 docx-pipeline skill**（细节阈值是 DOCX 实现）
- §8.3 3 轮 fix-or-escalate → **移到 docx-pipeline skill**
- §8.4 4 个人工 review gate → **移到 docx-pipeline skill**

§八 改成只剩 §8.1 矩阵 + 末尾指针 "详细 DOCX 实现见 docx-pipeline skill"。

### 3.2 顶部声明调整
- 保留 SOT 双流水线声明
- 改成："Phase 1（pre-render）+ Phase 4（翻译质检）+ Phase 5（全变体验证）是双流水线**共享语义**。Phase 2/3 由各自实现：PDF 用 audit-visual.js，DOCX 见 docx-pipeline skill。"

### 3.3 §8.1 矩阵保留
Phase 共享/替代矩阵是双流水线对照表，本身就是治理用，不算"DOCX 特定"。**保留在 SOT**。

### 3.4 末尾加 DOCX 实现指针
```markdown
---
## DOCX 流水线实现指针

DOCX 流水线的 anti-cheat 阈值、3 轮 fix-or-escalate 流程、4 个人工 review gate (G1-G4) 详见：
- `.claude/skills/docx-pipeline/SKILL.md`
- `.claude/skills/docx-pipeline/references/fix-checklist.md`
- `.claude/skills/docx-pipeline/references/anti-cheat-impl.md`
```

### 3.5 变更记录加 v1.4
```
| v1.4 | 2026-05-17 | 边界清理：剥离 §8.2/8.3/8.4（DOCX 实现细节）回 docx-pipeline skill；§8.1 双流水线对照矩阵留 SOT |
```

## 四、docx-pipeline skill 内同步检查

### 4.1 SKILL.md
- §一 SOT 表格不引 §十八 / §八（已移走）→ 改引用 SOT 内对应**语义条款**（C18/C19/Phase 1b/4a 等）
- 在 §一 加一句："本 skill 内部 references/ 是 DOCX 实现细节，与 SOT 语义条款一一对应"

### 4.2 references/ooxml-map.md
- 顶部明确："本文是 DOCX 流水线对 SOT 语义条款（DESIGN-STANDARD §一-§十七 + QA-RULES Phase 1-5）的 OOXML 实现映射。SOT 变动必须同步本文。"

### 4.3 references/fix-checklist.md
- 顶部已经 ref "QA-RULES §8.1"，改成 ref "QA-RULES §八 双流水线对照表" 即可
- §"QA-RULES §8.2 — anti-cheat 三道闸" 改成 "本 skill `anti-cheat-impl.md` — anti-cheat 三道闸"（既然 §8.2 内容移到了这边）

### 4.4 references/anti-cheat-impl.md
- 顶部 "规范定义在 swiss/QA-RULES.md §8.2 (SOT)" 改成 "anti-cheat 阈值由本 skill 定义（SOT 中只保留 anti-cheat 概念引用）"
- 把 §8.2 阈值表完整搬过来（wt_count / image_hack / text_ratio / validate / Word COM / 页数 / score）

### 4.5 references/master-extraction.md
- 保持不变（一直就是 DOCX 特定）

## 五、执行顺序

1. **等 subagent A 完成 + G1 review 通过**（先确保 subagent 看到的是稳定 SOT）
2. **改 docx-pipeline skill 内**（先把要从 SOT 移过来的内容补齐 / 调引用）
3. **改 SOT 文档**（删 §十八整段、删 §8.2/8.3/8.4、加指针、加变更记录）
4. **commit**（中文 msg："SOT 边界清理：DOCX 实现剥离回 docx-pipeline skill"）
5. **subagent B 阶段 2-3 跑时已在新边界上**（subagent B 也会读 SOT，要看新版）

## 六、验收

- [ ] DESIGN-STANDARD.md 内无 OOXML 元素描述（`w:`/`w:sz`/`w:color` 等）
- [ ] QA-RULES.md 内无 `wt_count ≥ 300` / `text_ratio ∈ [0.95, 1.20]` 等 DOCX 阈值
- [ ] DESIGN-STANDARD.md / QA-RULES.md 末尾都有 DOCX 实现指针
- [ ] docx-pipeline skill 内 references/ 覆盖原 §十八 / §8.2/8.3/8.4 全部信息
- [ ] subagent B 读 SOT 不会读到 DOCX 实现细节
- [ ] PDF 流水线（build-variant.js 等）功能不受影响（SOT 内 [PDF 实现] 标签内容未动）
