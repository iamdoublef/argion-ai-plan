# 阶段 2-3 EN Subagent Prompt（正式版）

> SKILL §五/§六 是规则，`references/stage2-3-runbook.md` 是步骤，本文件是**派单 prompt**。
> 阶段 1 v2 已 G1 PASS（304 keys / round-trip mean 5.59 max 10.10），可直接派单走 EN。

---

你是亚俊氏 docx 多语言流水线的执行 agent，按 `.claude/skills/docx-pipeline/` skill 走 **阶段 2 翻译对齐 + 阶段 3 EN 生成 + 3 轮 fix-or-escalate**。

## 仓库根目录
仓库根 = 当前工作目录（Linux：`/root/projects/yjsplan/`；Windows：`D:\work\private\yjsplan\`）。所有路径相对仓库根。

## 任务范围
完成 **EN 一个语言** 的完整流水线（阶段 2 + 阶段 3）。完成后等大 boss G3 confirm。
DE/IT/GB/HK/TW 暂缓。

## 前置（v2 已就位）
- ✅ `research/yjs-manual-opt/swiss/tools/docx-pipeline/master_template.docx`（brand 字面化 / 拆 w:t / safety_notice subarea）
- ✅ `swiss/tools/docx-pipeline/strings/cn.json`（304 keys，无 brand placeholder）
- ✅ `swiss/tools/docx-pipeline/generator.py` + `anti_cheat.py`
- ✅ `swiss/tools/docx-pipeline/docs/PLACEHOLDER_MAP.md`

## 必读
1. `.claude/skills/docx-pipeline/SKILL.md`
2. `.claude/skills/docx-pipeline/references/stage2-3-runbook.md` ← 算法步骤
3. `.claude/skills/docx-pipeline/references/fix-checklist.md`
4. `.claude/skills/docx-pipeline/references/ooxml-map.md` ← 跨语言锁定 keys
5. `research/yjs-manual-opt/swiss/QA-RULES.md` §八
6. `research/yjs-manual-opt/swiss/DESIGN-STANDARD.md` §十八
7. v2 阶段 1 产物：`swiss/tools/docx-pipeline/docs/G1_review_packet.md`

## 输入
- EN HTML：`research/yjs-manual-opt/swiss/template/imt050-master-en.html`
- CN HTML（对齐锚）：`research/yjs-manual-opt/swiss/template/imt050-master-cn.html`
- 官方 docx skill：环境变量 `${DOCX_SKILL_ROOT}`（Linux 默认 `~/.claude/skills/docx`，Windows 默认 `C:\Users\iamdo\.claude\skills\docx`）

## 阶段 2：翻译对齐

按 `references/stage2-3-runbook.md` 一、阶段 2 算法走（HTML 段落对齐 → cn 文本反查 cn.json → 写 lang.json）。

关键点：
- brand `Wevac` / 型号 `IMT050` / 单位 `V/Hz/W/kg/mm/°C` 已母版字面化，不出现在 cn.json，**译者无需处理**
- 阶段 1 v2 已拆中英混排 `<w:t>`，cn key 是纯中文部分（如 `cover_2 = "说明书"` → en `"User Manual"`），不要保留型号前缀
- 跨语言锁定 keys 自动检测：`tools/check_invariants.py --cn cn.json --lang en.json`，违反一并修
- HTML 实体（`&#x2014;` 等）转 Unicode 字符再写入 strings/en.json
- 找不到 cn 匹配的 HTML 段落记入 `docs/stage2-en-unmapped.md`，不要硬编

## 阶段 3：EN 生成 + 3 轮 fix-or-escalate

按 `references/stage2-3-runbook.md` 二、阶段 3 起手三步 + 循环执行清单走。

```
python generator.py --lang en --output output/imt050-wevac-eu-en.docx
python anti_cheat.py output/imt050-wevac-eu-en.docx \
    --baseline final/imt050-wevac-eu-cn.docx --skip-word-com
python ${DOCX_SKILL_ROOT}/scripts/office/validate.py output/imt050-wevac-eu-en.docx
```

**Linux dev 环境**用 `--skip-word-com`，**G3 验收前必须在 Windows 工位补一次 Word COM 验证**。

3 轮一类 ERROR 一轮（fix-checklist.md §二粒度）。3 轮未过 → `docs/diagnosis-en.md` → 大 boss G4。

EN 特殊关注：
- `text_ratio` 通常 1.10-1.18（英文较长），阈值上限 1.20 有缓冲
- 页数溢出风险：盯 p3/p9/p14（W50 已经吃满）

禁用 lever（W28/W33/W46）：`w:contextualSpacing` / `w:val="nil"` 边框 / 全局 `w:lineRule="auto"→"exact"`。

## 输出物

```
swiss/tools/docx-pipeline/
├── strings/en.json                     ← 阶段 2 产物
├── output/imt050-wevac-eu-en.docx      ← 阶段 3 产物
├── patches/en.md                       ← fix 日志 ≤ 3 条
└── docs/
    ├── stage2-en-unmapped.md           ← HTML 找不到对应 cn 文案的清单
    ├── stage2-invariant-keys.json      ← 自动识别的锁定 keys
    ├── G2_review_packet.md             ← 阶段 2 review 包
    ├── G3_review_packet.md             ← 阶段 3 review 包
    └── diagnosis-en.md                 ← 仅 3 轮未过时
```

`docs/G3_review_packet.md` 含：
- A. EN 翻译对齐摘要（key 数 = cn.json + 抽检 10 处）
- B. EN docx 生成结果（anti-cheat 5 项 + validate + Word COM(skipped 标记) + 页数 + CJK 扫描）
- C. patches/en.md 摘要
- D. T1/T2/T3 抽检 5-10 条
- E. 跨语言锁定 keys 横向对照（cn vs en）
- F. SOT 引用（QA §8.2 / §4 / §十八）
- G. EN vs CN 视觉对比（LO PNG p1/p3/p9/p14）
- H. G3 决策建议（PASS / HOLD / FAIL）

## 硬规则
1. 官方 docx skill 唯一 I/O 入口（`${DOCX_SKILL_ROOT}`）
2. anti-cheat 三道闸 + 页数 = 15 是 ERROR 底线；Word COM Linux 阶段可 skip 但必须 G3 前补 Windows
3. 3 轮上限严格；一轮 = 一类 ERROR
4. 优先改 strings 不改 OOXML
5. 引用 SOT 不重定义
6. commit msg 中文
7. 称呼大 boss / 管理者；禁老板/儿子/家属

## 返回格式（≤ 500 字）
1. strings/en.json keys 数（应 = 304 = cn.json）
2. unmapped 数 + invariant keys 数
3. EN docx anti-cheat 6 项（wt_count / image_hack / text_ratio / page_count / word_com / validate）
4. patches/en.md 条目数 + 状态（每条一句）
5. 是否需要 G4 escalate
6. commit sha

阻塞立即停 + 报告。
