# yjs-manual-opt

当前正式主链已经收口为：**初稿 Word / 参考手册 -> JSON 结构源 + 译文工作簿 -> DOCX（ODM） / HTML+PDF（自有品牌）**。

## 当前目录

```text
research/yjs-manual-opt/
  INDEX.md
  _inbox/                          -> 原始 Word / 参考手册输入
  swiss/                           -> 正式生产线
```

## 当前正式入口

- 输入源：
  - `research/yjs-manual-opt/_inbox/`
  - `research/yjs-manual-opt/swiss/products/<product>/product.json`
  - `research/yjs-manual-opt/swiss/products/<product>/images.json`
  - `research/yjs-manual-opt/swiss/products/<product>/content/source/manifest.json`
  - `research/yjs-manual-opt/swiss/products/<product>/content/source/chapters/*.json`
  - `research/yjs-manual-opt/swiss/products/<product>/i18n/workbooks/<locale>.xlsx`
  - `research/yjs-manual-opt/swiss/products/<product>/i18n/compiled/<locale>.json`
- 输出：
  - 自有品牌：`HTML + PDF`
  - ODM：`DOCX + PDF`

## 阶段节点

### 2026-03-11 Swiss JSON 单源 + 双渲染器正式落地
commit: 9effce9
说明书正式切到 JSON 单源，结构、图片、译文和品牌主题分层；自有品牌走 `HTML + PDF`，ODM 走 `DOCX + PDF`，翻译人员只改译文工作簿，不再碰 HTML。
- ptr: `git:9effce9:research/yjs-manual-opt/swiss/SOP-new-product.md`
- ptr: `git:9effce9:research/yjs-manual-opt/swiss/tools/build-variant.js`
- ptr: `git:9effce9:research/yjs-manual-opt/swiss/tools/export-docx.js`
- ptr: `git:9effce9:research/yjs-manual-opt/swiss/products/imt050/product.json`
- ptr: `git:9effce9:research/yjs-manual-opt/swiss/products/v23/product.json`

### 2026-03-11 中文 Word 母版基线定型
commit: 4c587f0
中文 Word 支线从“PDF 影子稿”改成 A5 可编辑母版支线，固定单一 Word 母版骨架 + 品牌主题包，后续新产品默认在这套骨架上微调内容和图片。
- ptr: `git:4c587f0:research/yjs-manual-opt/swiss/WORD-BASE-TEMPLATE-CN.md`
- ptr: `git:4c587f0:research/yjs-manual-opt/swiss/template/shared/docx/base-template-cn.docx`
- ptr: `git:4c587f0:research/yjs-manual-opt/swiss/tools/export-docx.js`
- ptr: `git:4c587f0:research/yjs-manual-opt/swiss/template/shared/base/brand-themes.json`

## 当前判断

- 以后新的说明书研究、模板、工具和产物，都只围绕 `swiss/` 这条主链展开。
- 旧链路如果未来确实需要追溯，统一从 Git 历史读取，不再回放到主目录。
