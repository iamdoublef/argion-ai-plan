# TRO 规范（Index-First）

本仓库采用 Index-First 工作流：
- 你看的是“阶段索引”（摘要），快速知道做过什么。
- AI 用的是“指针”（路径/当时版本），按指针回读源文件还原细节。

目标：
- 防止“研究失忆”：避免重复从零开始。
- 防止“目录熵增”：长期保持研究资料可检索、可定位。

硬约束：
- 保存一次阶段节点必须能在 1 分钟内完成。

## 1）术语

`<project>`（项目 ID）：
- 一个稳定的研究主题 ID，用于在同一个仓库内分组。
- 作为 `research/` 下的目录名。
- 示例：`normalization`、`rag-eval`、`query-engine`。

阶段节点（Stage node）：
- 值得保存的关键点（结果确认、做出决策、准备切换上下文）。
- 随机性 commit/迭代不要求保存阶段节点。

指针（Pointer）：
- 面向 AI 的“定位入口”，用于找到源文件/当时版本。
- 指针不是解释，细节永远在指针指向的文件里。

## 2）目录规则（禁止随便乱放）

研究资料必须放在：
- `research/<project>/...`

允许的临时兜底目录：
- `research/<project>/_inbox/`

如果在 `research/<project>/...` 之外发现研究文档/脚本/输出：
- 视为不合规。
- 必须移动到正确目录（或先在索引里写指针，后续再移动归位）。

建议的实验/POC 目录（一次运行一个目录）：
- `research/<project>/01_experiments/<YYYY-MM-DD>_<slug>/`

每个实验目录的最小建议内容：
- `notes.md`（短即可，3-10 行也可以）
- `outputs/`（至少一个输出文件）
- 可选：`README.md`（如何复现）

阶段索引文件：
- `research/<project>/INDEX.md`

## 3）阶段索引条目（给人看的）

阶段索引只存两类信息：
- 一行摘要（给人看）
- 指针（给 AI 回读）

推荐条目格式（可读性优先，AI 也易解析）：

```md
### YYYY-MM-DD <一句话摘要>
commit: <shortsha|uncommitted|nogit>
- ptr: `git:<commit>:<path>`
- ptr: `git:<commit>:<path>`
```

规则：
- 每条记录用一个 `###` 分隔。
- `commit:` 单独一行，避免第一行过长。
- 指针统一用 `- ptr: ` 开头，指针本体用反引号包起来，便于机器提取。

示例：

```md
### 2026-02-09 类型过滤验证通过，准确率+12%
commit: a83f2c9
- ptr: `git:a83f2c9:research/normalization/01_experiments/2026-02-09_type-filter/`
- ptr: `git:a83f2c9:research/normalization/01_experiments/2026-02-09_type-filter/notes.md`
- ptr: `git:a83f2c9:research/normalization/01_experiments/2026-02-09_type-filter/outputs/metrics.json`
```

## 4）指针格式（给 AI 用的）

首选（稳定，可回读当时版本）：
- `git:<commit>:<path>`
  - 示例：`git:a83f2c9:research/normalization/01_experiments/.../outputs/metrics.json`

允许（不稳定，可能腐烂）：
- `file:<relative-path>`
  - 示例：`file:research/normalization/01_experiments/.../outputs/metrics.json`

外部证据：
- `url:<link>`
  - 示例：`url:https://arxiv.org/abs/...`

其他仓库：
- `repo:<remote>@<commit>:<path>`
  - 示例：`repo:git@github.com:org/poc-repo.git@1a2b3c4:experiments/run_01/`

## 5）AI 行为契约（必须遵守）

### 5.1 当用户说“保存阶段节点：<摘要>”（阶段保存）
AI 必须：
1. 确定 `<project>`：
   - 优先使用用户显式给出的 `project=<project>`。
   - 若用户未给出：默认值为“仓库根目录名”（例如当前仓库目录名）。
   - 如果用户明确在同一仓库内维护多个 project 且本次不明确，则追问确认。
2. 采集事实（不猜测）：
   - 若是 Git 仓库：branch、commit（以及 shortsha）。
   - 可选：最近变更文件列表。
   - 若存在：`research/<project>/01_experiments/` 下最新实验目录。
   - 若工作区存在未提交变更（dirty），必须 WARN：建议先 commit 以生成稳定的 `git:` 指针。
     - 若用户选择不 commit：允许退化为 `file:` 指针，并在条目中写 `commit: uncommitted`（标注“未锚定版本”）。
3. 做轻量合规检查（见第 6 节）。
4. 向 `research/<project>/INDEX.md` 追加 1 条新条目：
   - 包含日期与摘要。
   - 至少包含 1 个指针。
   - 若存在 commit：优先写 `git:<commit>:<path>` 指针。
   - 若无 commit（dirty 或非 Git）：写 `file:`/`url:`/`repo:` 指针，并明确标注原因（例如 `commit: uncommitted` / `commit: nogit`）。
5. 如果关键产物缺失（如没有 `notes.md` 或 `outputs/`），默认不阻断：
   - 清晰 WARN。
   - 给出需要创建/补齐的准确路径。
   - 只有在用户明确要求时才创建占位文件。

### 5.2 当用户说“检查合规 / 目录是不是乱了”（合规检查）
AI 必须：
1. 扫描不合规放置：
   - 在 `research/` 之外出现的研究类文件（合理范围内：md、ipynb、csv、json、png 等）。
   - 说明：为了避免噪声，合规扫描应忽略工具/配置/规划类目录（例如 `ops/`、`design/`、`.git/`）。
2. 检查每个 `research/<project>/` 是否有：
   - `INDEX.md`（没有则建议创建）。
3. 检查最近实验目录是否具备最小建议内容。
4. 输出：
   - 按 WARN/ERROR 分组的发现（默认全部 WARN，除“索引条目没有任何指针”可为 ERROR）。
   - 明确的修复动作：移动路径、创建缺失文件、补指针。

### 5.3 当用户要“回忆/复盘”过往工作
AI 必须：
- 从 `INDEX.md` 读取指针，并按指针读取源文件（`git:` 指针必须回读当时 commit 内容）。
- 每条结论至少引用 1 个指针作为来源。
- 禁止编造指标、文件、命令输出。无法确认则标记 unknown，并要求补充指针/证据。

## 6）合规清单（轻量，1 分钟友好）

默认执行策略：
- 尽量 WARN，不阻断。
- 阶段保存的唯一默认阻断条件：新写入的索引条目不包含任何指针。

清单：
1. `research/<project>/INDEX.md` 存在（或可创建）。
2. 本次索引条目至少包含 1 个指针。
3. 若存在 Git commit，指针优先为 `git:<commit>:<path>`。
4. 若存在实验目录，建议（不强制）包含 `notes.md` 与 `outputs/`。
5. 若发现研究类文件在 `research/<project>/...` 之外，WARN 并建议移动（或先放入 `_inbox/`）。

## 7）研究过程日志（必须记录）

每次研究/实验/POC 完成后，必须在项目目录下创建 `research-log.md`，记录完整的研究过程。

文件路径：
- `research/<project>/research-log.md`

必须包含的内容：

### a）研究目标
- 输入是什么、输出是什么、为什么做这个研究

### b）执行过程
- 每个阶段/步骤做了什么
- 使用了哪些工具/Agent
- 每步的结果：✅ 成功 / ⚠️ 部分成功 / ❌ 失败
- 大致耗时

### c）关键决策
- 做了哪些选择、为什么这样选、有哪些替代方案

### d）失败与教训（最重要）
- 哪些步骤失败了或出了问题
- 失败的现象、原因、教训
- 如何修复的（或为什么没修复）
- 这些教训对后续研究的启示

### e）成果评估
- 验证清单（计划中的验证项是否通过）
- 总体评价（各维度打分）
- 已知局限

### f）后续待办
- 按优先级列出待办项

规则：
- 研究过程日志不是给人看的摘要，是给 AI 和未来的自己看的详细记录。
- 失败和教训比成功更重要——防止重复踩坑。
- 每条失败记录必须包含：现象、原因、教训、修复状态。
- INDEX.md 中必须包含指向 `research-log.md` 的指针。
