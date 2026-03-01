# V23 手册完整审计报告（2026-03-01）

## 1. 审计范围

本次审计基于最新阅读版与 booklet 产物，覆盖 5 套文档：

- `output/v23-manual-cn.html` + `output/V23-Manual-CN-Wevac.pdf`
- `output/v23-manual-en.html` + `output/V23-Manual-EN-Wevac.pdf`
- `experiments/2026-02-26_top-tier-styles/v23-mi-2.0-full.html` + `v23-mi-2.0-full-fixed.pdf`
- `experiments/2026-02-26_top-tier-styles/v23-lifestyle-complete.html` + `v23-lifestyle-complete-fixed.pdf`
- `experiments/2026-02-26_top-tier-styles/v23-swiss-complete.html` + `v23-swiss-complete-fixed.pdf`

审计依据：

- `data/d5-manual-standard.md`（已补充 12.8 / 12.9）
- `.claude/agents/manual-auditor.md`（已补充 F/G/H/I）

审计产物目录（新路径，不覆盖旧报告）：

- `audits/2026-03-01_full-layout-audit-v1/`
- 指标：`audit-metrics.json`
- 图片加载检查：`playwright-image-check.json`
- 证据图：`evidence/*.png`

## 2. 审计结论（总览）

整体评级：**C（需较大修正后再作为最终交付）**

- ERROR: 3
- WARNING: 3
- INFO: 2

## 3. 关键发现（按严重级别）

### ERROR-01（Swiss）章节分页溢出，出现“孤立续页 + 大面积留白”

现象：

- `v23-swiss-complete-fixed.pdf` 在第 9/10 页（PDF 物理页）之间出现异常拆分：
- 页 9 底部未完整结束，页 10 仅承接一小段注释并留下大面积空白。

证据：

- `evidence/swiss-style_p09.png`
- `evidence/swiss-style_p10.png`
- `evidence/swiss-style_p11.png`

源位置（同一 `.page` 内容过满）：

- `v23-swiss-complete.html:346`（06 操作续页容器起始）
- `v23-swiss-complete.html:395`（6.5 末尾 note）
- `v23-swiss-complete.html:396`（页脚）

判定：违反新增规范 12.8（分页最小块、留白门禁）。

---

### ERROR-02（全版本）图内 callout 编号未提供对应编号映射

现象：

- 控制面板图（`image10.svg`）包含 1..7 编号。
- 下方功能表未提供 1..7 的显式对应关系（仅按按钮名称列出）。

证据：

- `evidence/en-main_p06.png`
- `evidence/swiss-style_p06.png`

源位置：

- `v23-manual-en.html:460`（控制面板图）
- `v23-manual-cn.html:459`
- `v23-mi-2.0-full.html:468`
- `v23-lifestyle-complete.html:221`
- `v23-swiss-complete.html:246`

判定：违反新增规范 12.8（callout 编号必须有完整映射）。

---

### ERROR-03（全版本）存在无页脚品牌线/页码的物理页（由溢出造成）

现象：

- 每份 PDF 均出现 1 个“无 `WEVAC V23 ...` 页脚”的物理页。
- 对应页：
  - CN: p18
  - EN: p10
  - MI: p18
  - Lifestyle: p18
  - Swiss: p9

证据：

- `evidence/cn-main_p18.png`
- `evidence/en-main_p10.png`
- `evidence/mi-style_p18.png`
- `evidence/life-style_p18.png`
- `evidence/swiss-style_p09.png`

判定：违反页脚连续性与分页稳定性要求（12.2 / 12.8）。

## 4. 次级问题（WARNING）

### WARNING-01（EN）6.6~6.10 章节标题与纵向节奏不一致

现象：

- `v23-manual-en.pdf` 中 6.8 被单独挤到下一物理页（页面首行直接是 `6.8 ...`），导致与前后页的章节标题节奏不一致。

证据：

- `evidence/en-main_p10.png`
- `evidence/en-main_p11.png`
- `evidence/en-main_p12.png`

源位置：

- `v23-manual-en.html:601-700`（6.6~6.10 同页规划，实际打印溢出拆分）

---

### WARNING-02（全版本）图注策略混用

现象：

- 6.6~6.9 的操作示意图（`image18/20/22/24/26`）无图注。
- 6.10 的 `image28/30` 有 `Fig./图 11/12` 图注。

证据：

- `evidence/en-main_p10.png`（无图注）
- `evidence/en-main_p12.png`（有图注）

源位置：

- EN: `v23-manual-en.html:605-680`（无） vs `692-697`（有）
- CN: `v23-manual-cn.html:604-679`（无） vs `691-696`（有）
- MI/Lifestyle/Swiss 同构。

判定：不满足新增 12.8 的“同层级图注策略一致”。

---

### WARNING-03（流程）booklet 被当作阅读审查对象，容易误判“分页错位”

现象：

- booklet 首几页天然不是阅读顺序（拼版逻辑），在双页预览中会出现“封面/目录/末页交错”。

证据：

- `audit-metrics.json` 中各 booklet `first_lines` 非阅读顺序。

判定：需按新增 12.9 执行“阅读版与 booklet 分离验收”。

## 5. 通过项（INFO）

- Playwright 图片加载检查全部通过：5 个 HTML 均 `failed=0`、`nonzeroNatural=15`、`zero=0`。
  - 见 `playwright-image-check.json`
- 全部 booklet 页数正确：5 份均为 10 页。
  - 见 `audit-metrics.json`

## 6. 修复优先级建议

1. 先修分页容器容量（ERROR-01/03）
- 把超长 `.page` 拆分为更细粒度页面，尤其是 Swiss 06 续页、各版本 10 章保修信息页。
- 对 `sub-title + steps + figure` 采用“最小块同页”策略，空间不足即整块换页。

2. 再修控制面板编号映射（ERROR-02）
- 在控制面板图下新增 1..7 对照表（编号、按钮名、功能）并与图中 callout 一一对应。

3. 再统一图注策略（WARNING-02）
- 方案 A：给 6.6~6.9 的操作图补图注；
- 方案 B：取消 6.10 的 Fig.11/12 图注，仅保留标题性小节说明。

4. 固化验收口径（WARNING-03）
- 阅读版审计只看 `*-fixed.pdf` / 主输出 PDF；
- booklet 仅做拼版检查，不做阅读顺序判定。

---

> 本报告仅为审计，不修改现有页面内容；后续修订请在新版本目录进行。
