# V23 产品线说明

本文件只记录 `V23` 产品线自己的基线、派生矩阵和已确认经验，不承载通用规范。通用生成/审计规则统一见：

- [DESIGN-STANDARD.md](/D:/work/private/yjsplan/research/yjs-manual-opt/swiss/DESIGN-STANDARD.md)
- [QA-RULES.md](/D:/work/private/yjsplan/research/yjs-manual-opt/swiss/QA-RULES.md)

未被当前批准版验证通过的页面级修补，不写入本文件；这里只沉淀已经被接受的 `V23` 产品线规则。

## 当前批准版基线

- 当前 `V23` 中文批准版基线：`research/yjs-manual-opt/swiss/output/v23-wevac-eu-cn.html`
- 后续 `V23` 的其他品牌、地区、翻译、单位版本，默认都以这份中文批准版为结构和分页基线
- 不允许反过来以外语版、其他品牌版或历史旧版去修改当前中文基线

## V23 派生矩阵

- 品牌：`wevac / vesta / act`
- 地区：`cn / hk / tw / gb / de / it / za`
- 语言映射：
  - `cn -> zh-CN`
  - `hk -> zh-HK`
  - `tw -> zh-TW`
  - `gb / za -> en`
  - `de -> de`
  - `it -> it`

## V23 当前确认过的页面与分页经验

以下经验只针对 `V23` 产品线成立：

1. `06 操作指引` 的附件使用页，以“减少大面积空白”为优先目标
   - `6.8` 和 `6.9` 应优先合页
   - 相邻附件图应尽量合并承载，不要为了默认分页留下大块空白

2. `07 故障排除` 的附加处理页，以“表格 + 后续步骤说明”连续阅读为优先目标
   - 故障长表后的液体处理说明，若渲染后能容纳，应优先合页
   - 不要把同一小节人为拆成上页留白、下页续写的形态

3. `09 真空包装特性` 的保鲜期限表对 `rowspan` 非常敏感
   - 任意改动分类行数后，必须回看分类列与内容列是否仍对齐
   - 这类表格在 `V23` 中不接受“视觉差不多”的处理方式，必须逐行对齐

4. `10 品牌与保修信息` 当前基线规则
   - `保修信息 + 保修卡` 在 `V23` 中默认同页
   - 若后续文字增长导致必须拆页，先确认是否属于真实内容增长，而不是版式退化

## 产品经验与公共经验的边界

- `V23 README` 只写 `V23` 自己的批准版基线、派生矩阵、分页经验和回写要求。
- 可复用到其他产品的规则，例如图片承载尺寸、保修分页、`rowspan` 防护、单位一致性，统一写回公共规范，不在这里重复展开。

## V23 后续地区 / 翻译 / 单位版本的推荐顺序

1. 先以 `v23-wevac-eu-cn.html` 确认当前结构和分页仍为批准版
2. 只修改 `products/v23/i18n/compiled/<locale>.json` 中的译文、本地化和单位表达
3. 如涉及正式译文修订，再用 `tools/sync-json-to-workbook.js` 把修订同步回 `i18n/workbooks/<locale>.xlsx`
4. 用 `tools/build-all.js --product v23` 重建全部品牌和地区变体
5. 再导出 `PDF / DOCX`
6. 最后跑 visual audit 与翻译质检

## 单位同步范围

`V23` 的单位更新必须视为同一任务，不允许只改一半：

- `product.json` 中 `specs.us / specs.eu`
- `i18n/compiled/*.json` 中正文涉及尺寸、温度、时间、重量、压力等单位的表达
- 必要时同步回 `i18n/workbooks/*.xlsx`

底线规则：

- 正文单位与规格表单位必须一致
- 同一地区版本不得出现双套单位说法互相冲突
- `zh-HK` 和 `zh-TW` 不得回退成逐字简转繁

## Workbook / Compiled 回写要求

- `workbooks/*.xlsx` 是翻译编辑面
- `compiled/*.json` 是当前正式构建输入
- 如果为了快速修复先改了 `compiled/*.json`，必须再用 `tools/sync-json-to-workbook.js` 回写 workbook
- 不允许长期形成“compiled 已更新、workbook 还是旧译文”的双轨状态
