# CLAUDE.md

## 项目背景

本仓库为亚俊氏（Argion）AI转型规划项目。

### 企业信息
- 全称：广州亚俊氏真空科技股份有限公司
- 英文名：Guangzhou Argion Electric Appliance Co., Ltd.
- 品牌：Argion（官网）、Wevac、Vesta（自有品牌）
- 行业：真空厨房设备（真空封口机、低温烹饪、制冷设备、真空袋）
- 模式：ODM代工 + 自有品牌并行
- 规模：约600人，2024年营收2.92亿元
- 生产基地：广州（17,000㎡）、佛山（25,600㎡）、新加坡（4,000㎡）
- 证券：新三板 874106
- 详细资料：`research/yjs-ai-transform/_inbox/01-company-profile.md`

### 人员称呼规范（硬规则）
- 企业负责人/创始人统一称"管理者"，禁止使用"老板"
- 用户（本项目协助者）不是管理者的家属，是独立的技术协助方
- 禁止在任何文档中出现"老板""儿子""家属"等称呼
- 涉及用户角色时，使用"技术协助方"或"项目协助方"

## 项目规则（Claude Code）

本仓库遵循 `ops/policy.md`（Index-First 规范）。

硬规则：
- 执行任何工作前，必须先读取并遵守 `ops/policy.md`。
- 研究资料必须放在 `research/<project>/...`（临时兜底：`research/<project>/_inbox/`）。
- 保存阶段节点时，必须更新 `research/<project>/INDEX.md`：一行摘要 + 至少一个指针。
- 回忆/复盘/总结时，必须沿指针读取源文件（优先 `git:<commit>:<path>`），禁止猜测与编造。

自然语言触发：
- 用户说"保存阶段节点"（或类似表达）时，按 `ops/policy.md` 的"阶段保存"流程执行。
- 用户说"检查合规/目录是不是乱了"（或类似表达）时，按 `ops/policy.md` 的"合规检查"流程执行。

## 网络访问策略（三级降级）

本项目通过Kiro API代理访问，WebSearch可能不可用。获取网络信息时必须按以下顺序尝试：

1. **优先：WebSearch + WebFetch** — 先尝试内置工具，如果返回空结果或报错，立即降级
2. **降级：Playwright MCP** — WebSearch/WebFetch失败时，使用 `.mcp.json` 中配置的 Playwright 工具访问网页：
   - 用 `mcp__playwright__browser_navigate` 打开页面
   - 用 `mcp__playwright__browser_snapshot` 获取页面内容
   - 用完后 `mcp__playwright__browser_close` 关闭浏览器
3. **兜底：标注缺失** — 如果Playwright也失败，在文档中标注 `⚠️ 来源URL待补充` 并继续工作，不要阻塞

判定"失败"的标准：
- WebSearch返回空结果（无搜索结果）
- WebFetch返回403/500或其他错误
- 连续2次不同查询都返回空 → 直接跳到Playwright，本次会话不再尝试WebSearch
