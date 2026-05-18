# 阶段 2-3 Runbook（HTML→cn→lang 映射 + 派单要点）

> SKILL §五/§六 是规则；本文档是**实操步骤**。一份 runbook 服务所有非 CN 语言。
> 阶段 1 v2 已 PASS（304 keys，brand 字面化），本 runbook 以 v2 为基线。

## 一、阶段 2：HTML → docx 字典生成

### 输入清单

| 文件 | 路径 | 用途 |
|------|------|------|
| cn.json (v2) | `swiss/tools/docx-pipeline/strings/cn.json` | docx key 集 + cn value（事实 SOT）|
| HTML cn | `swiss/template/imt050-master-cn.html` | 章节锚（与 lang HTML 对齐用）|
| HTML lang | `swiss/template/imt050-master-{en,de,it}.html` | lang 译文源 |
| PLACEHOLDER_MAP | `swiss/tools/docx-pipeline/docs/PLACEHOLDER_MAP.md` | area / subarea 命名空间 |

### 算法（必须按此顺序）

```
Step 1：解析两份 HTML（cn 和 lang），按 DOM 遍历建立段落序列：
  cn_html_paragraphs[i] ↔ lang_html_paragraphs[i]
  （HTML 模板设计上是结构对齐的，章节顺序、段落数应一致）

Step 2：对每个 i：
  cn_text = cn_html_paragraphs[i].text.strip()
  lang_text = lang_html_paragraphs[i].text.strip()

  # 在 cn.json 中按 value 反查 docx key
  candidates = [k for k, v in cn.items() if v.strip() == cn_text]

  if len(candidates) == 1:
    docx_key = candidates[0]
  elif len(candidates) > 1:
    # 多 key 命中（罕见）：按 area/subarea 消歧
    area = guess_area_from_html_section(cn_html_paragraphs[i])
    docx_key = pick_by_area(candidates, area)
  else:
    # HTML 文案在 cn.json 中找不到完全匹配
    log_to('docs/stage2-{lang}-unmapped.md', cn_text, lang_text)
    continue

  out_strings[docx_key] = lang_text

Step 3：写 strings/{lang}.json：
  - key 集与 cn.json 完全一致（cn 有的 key 都要有，缺译留空字符串）
  - value 是 lang 译文；空字符串触发 generator.py 回退 cn

Step 4：跨语言锁定 keys 校验：
  python tools/check_invariants.py --cn cn.json --lang {lang}.json
  违反 → 强制设回 cn 值
```

### 锁定 keys 自动检测

`check_invariants.py` 扫描 cn.json，按正则识别"必须 = cn"的 keys（详见 `ooxml-map.md` "跨语言锁定 keys"）：

```python
INVARIANT_PATTERNS = [
    (r'^[\d.\-/x×]+$',          'pure_number'),
    (r'https?://',              'url'),
    (r'[\w.\-]+@[\w.\-]+',      'email'),
    (r'^[\+\d\s\-()]{7,}$',     'phone'),
]
INVARIANT_LITERALS = {'WARNING','CAUTION','NOTICE','DANGER'}
```

阶段 2 启动时把识别到的 invariant key 列表写到 `docs/stage2-invariant-keys.json`，G2 review 也带上这份。

### 常见 unmapped 原因

| 原因 | 处理 |
|------|------|
| HTML 文案在 cn.json 没有完全匹配（cn HTML 与母版 cn docx 文案略有出入） | 人工对照原始 W50 docx → 决定补 cn 值或调 HTML |
| HTML 文案被拆/合并（cn 一段对应 lang 两段） | 在 unmapped.md 记录，人工拆词后补 lang.json |
| docx 中含中英混排（v2 已拆 `<w:t>`，cn key 是纯中文部分） | OK，按算法走即可 |

### G2 输出物

```
swiss/tools/docx-pipeline/
├── strings/
│   ├── cn.json                        # SOT（不动）
│   ├── en.json                        # 阶段 2 产出
│   ├── de.json                        # （本次只做 EN，DE/IT 后续）
│   └── it.json
└── docs/
    ├── stage2-en-unmapped.md          # HTML 文案在 cn.json 找不到的清单
    ├── stage2-invariant-keys.json     # 自动识别的锁定 keys 列表
    └── G2_review_packet.md            # 给大 boss 的 review 包
```

## 二、阶段 3：流水线生成 + 3 轮 fix-or-escalate

### 起手三步

```bash
cd research/yjs-manual-opt/swiss/tools/docx-pipeline

# 1. 生成
python generator.py --lang en --output output/imt050-wevac-eu-en.docx

# 2. 跑 anti-cheat 全套（Linux dev：跳过 Word COM）
python anti_cheat.py output/imt050-wevac-eu-en.docx \
  --baseline final/imt050-wevac-eu-cn.docx \
  --skip-word-com

# 3. validate
python ${DOCX_SKILL_ROOT}/scripts/office/validate.py output/imt050-wevac-eu-en.docx
```

### 3 轮循环执行清单

每轮按 `fix-checklist.md` "一、每轮必跑的检查"跑全套，发现 ERROR 按"二、Fix 决策表"处理。

**ERROR 优先级**（同 1 轮内并行修同类）：

```
P0（不通过整个循环停）：validate 失败 / wt_count<300 / image_hack=true / Word COM 打不开
P1（必修，同类一轮）：{{*}} 残留 / CJK 残留 / 跨语言锁定 keys 偏移 / undefined/null/TODO 残留
P2（修，同类一轮）：text_ratio 越界 / 页数越界 / T1/T2/T3 抽检失败
```

P0 出现立即回滚最近 patch 不消耗轮数；P1/P2 各自记 1 轮。

### `patches/{lang}.md` 模板

每条 fix 一段，**严格按字段**：

```markdown
## fix N — <一句话症状>
- **状态**: ✅ Applied / ❌ Rejected (iter-N, sha:abcdef)
- **触发**: QA-RULES Phase X / SOT 条款编号
- **定位**: <key 列表 / 页 / 哪个 xml part>
- **fix**: <动作 — 改 strings 哪几行 / 改 OOXML 哪个元素>
- **验证**: <重跑结果：哪些检查 PASS、之前 FAIL 的现在 PASS>
```

### 3 轮没修通 → escalate G4

写 `docs/diagnosis-{lang}.md`：

```markdown
# {LANG} G4 Escalate 诊断报告

## 已跑轮次
- iter-1: 修 X 类 ERROR（<sha>）→ 验证 <结果>
- iter-2: 修 Y 类 ERROR（<sha>）→ 验证 <结果>
- iter-3: 修 Z 类 ERROR（<sha>）→ 验证 <结果>

## 仍未通过的 ERROR 列表
- ERROR A：<现象 / 定位 / 已尝试 fix / 为什么没修通>
- ERROR B：...

## 推测原因（必填一项）
- [ ] 缺译多到非 1 轮可补（建议人工 strings/{lang}.json 全量 review）
- [ ] W50 母版结构性问题（建议回研究阶段补强 master）
- [ ] 翻译团队 HTML 模板与 docx 母版不一致（建议先对齐 HTML）
- [ ] 该语言不适合复用 W50 母版（建议砍交付 / 单独建 master）

## 建议下一步
<具体动作 + 责任人>
```

## 三、派单到 subagent 时的提示词要点

把 subagent 视作不带上下文的同事；prompt 必须自带：

1. **工作目录**：`research/yjs-manual-opt/swiss/tools/docx-pipeline/`（绝对/相对都行，但写清楚）
2. **任务范围**：本次只做哪个 lang（如 EN），DE/IT/HK/TW 暂缓
3. **必读文件**：本 skill SKILL.md / 本 runbook / `fix-checklist.md` / `ooxml-map.md` / 阶段 1 G1_review_packet
4. **输入资源**：cn.json 路径、HTML 模板路径
5. **执行边界**：3 轮上限 / 一轮一类 / 优先改 strings 不改 OOXML / 禁用 lever 列表
6. **产出清单**：`strings/{lang}.json` + `output/*-{lang}.docx` + `patches/{lang}.md` + `docs/G2_review_packet.md`（如阶段 2）/ `docs/G3_*` 段落（如阶段 3）
7. **何时停**：3 轮未过 → 写 `docs/diagnosis-{lang}.md` 后停，不要"再试一轮"
8. **称呼规则**：管理者 / 大 boss；**禁** 老板 / 儿子 / 家属
