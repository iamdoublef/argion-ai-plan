# Swiss Localization Audit Prompt

用途：
- 对模型生成或人工回填后的译文进行二次质检
- 输出问题清单，不直接修改正式源文件

检查范围：
- 术语一致性
- 品牌语言一致性
- 单位和测量格式
- 警示语合规性
- 地区本地化
- 是否存在漏译、错译、直译、生硬表达

硬规则：
- 审计结果必须引用具体 `text_id`
- 只输出问题、建议和风险等级
- 不得擅自生成新的章节结构
- 不得把 HTML/CSS 问题和译文问题混在一起

输出格式：
1. `critical`
2. `major`
3. `minor`
4. `style consistency`
5. `locale-specific issues`
6. `recommended fixes`

自检清单：
- 是否覆盖品牌术语、按键文案、警示语和保修文案
- 是否明确区分事实错误与风格问题
- 是否给出可回写到译文工作簿的修正建议
