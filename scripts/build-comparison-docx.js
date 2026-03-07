const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, PageNumber, PageBreak, LevelFormat } = require("docx");

const PW = 11906, PH = 16838, MG = 1134, CW = PW - MG * 2;
const F = "Microsoft YaHei";
const ACCENT = "FF6900";
const bd = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const bds = { top: bd, bottom: bd, left: bd, right: bd };
const cm = { top: 60, bottom: 60, left: 100, right: 100 };

const h1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 360, after: 200 },
  children: [new TextRun({ text: t, bold: true, size: 32, font: F })] });
const h2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 280, after: 160 },
  children: [new TextRun({ text: t, bold: true, size: 28, font: F })] });
const tx = (t, o) => new TextRun({ text: t, size: 22, font: F, ...o });
const pr = (t, o) => new Paragraph({ spacing: { after: 120 }, ...o,
  children: Array.isArray(t) ? t : [tx(t)] });
const bp = t => new Paragraph({ numbering: { reference: "bl", level: 0 }, spacing: { after: 80 },
  children: [tx(t)] });
const PB = () => new Paragraph({ children: [new PageBreak()] });

function mkR(cs, ws, hd) {
  return new TableRow({ children: cs.map((c, i) => new TableCell({
    borders: bds, margins: cm, width: { size: ws[i], type: WidthType.DXA },
    shading: hd ? { fill: "F2F2F2", type: ShadingType.CLEAR } : undefined,
    children: [new Paragraph({ children: [new TextRun({ text: c, size: 20, font: F, bold: !!hd })] })],
  })) });
}
function tbl(hds, rows, ws) {
  ws = ws || hds.map(() => Math.floor(CW / hds.length));
  return new Table({ width: { size: CW, type: WidthType.DXA }, columnWidths: ws,
    rows: [mkR(hds, ws, true), ...rows.map(r => mkR(r, ws))] });
}

const C = [];

// Cover
C.push(new Paragraph({ spacing: { before: 4800 }, children: [] }));
C.push(pr([tx("\u4EA7\u54C1\u8BF4\u660E\u4E66\u5236\u4F5C\u65B9\u6848\u5BF9\u6BD4\u5206\u6790", { size: 48, bold: true, color: "1A1A1A" })], { alignment: AlignmentType.CENTER }));
C.push(pr([tx("\u4E9A\u4FCA\u6C0F\u771F\u7A7A\u79D1\u6280 \u00B7 \u5185\u90E8\u51B3\u7B56\u53C2\u8003", { size: 28, color: "666666" })], { alignment: AlignmentType.CENTER }));
C.push(pr([tx("2026\u5E743\u6708", { size: 24, color: "999999" })], { alignment: AlignmentType.CENTER }));
C.push(PB());

// 1. Background
C.push(h1("1. \u80CC\u666F"));
C.push(pr("\u4E9A\u4FCA\u6C0F\uFF08Argion\uFF09\u5F53\u524D\u4F7F\u7528 Word \u624B\u5DE5\u6392\u7248\u5236\u4F5C\u4EA7\u54C1\u8BF4\u660E\u4E66\u3002\u968F\u7740\u81EA\u6709\u54C1\u724C\uFF08WEVAC/Vesta/ACT\uFF09\u51FA\u6D77\u4E1A\u52A1\u6269\u5C55\uFF0C\u8BF4\u660E\u4E66\u7248\u672C\u7BA1\u7406\u538B\u529B\u6025\u5267\u589E\u5927\uFF1A"));
C.push(bp("3\u4E2A\u54C1\u724C \u00D7 2\u79CD\u8BED\u8A00\uFF08\u4E2D/\u82F1\uFF09\u00D7 2\u4E2A\u5E02\u573A\u6807\u51C6\uFF08\u7F8E\u6807110V/\u6B27\u6807220V\uFF09= \u6700\u591A12\u4E2A\u7248\u672C/\u4EA7\u54C1"));
C.push(bp("\u6BCF\u5E74\u7EA610\u6B3E\u4EA7\u54C1\u9700\u8981\u8BF4\u660E\u4E66\uFF0C\u5E74\u7EF4\u62A4\u91CF\u53EF\u8FBE120\u4EFD\u6587\u6863"));
C.push(bp("\u5F53\u524D\u75DB\u70B9\uFF1A\u6392\u7248\u89C6\u89C9\u5DEE\u3001\u7FFB\u8BD1\u8D28\u91CF\u4F4E\u3001\u66F4\u65B0\u6EDE\u540E\u3001\u7248\u672C\u6DF7\u4E71"));
C.push(pr("\u672C\u6587\u6863\u5BF9\u6BD4\u56DB\u79CD\u4E3B\u6D41\u65B9\u6848\uFF0C\u5E2E\u52A9\u7BA1\u7406\u5C42\u505A\u51FA\u51B3\u7B56\u3002"));
C.push(PB());

// 2. Overview table
C.push(h1("2. \u56DB\u79CD\u65B9\u6848\u603B\u89C8\u5BF9\u6BD4"));
const w5 = [1800, 1960, 1960, 1960, 1958];
C.push(tbl(
  ["\u7EF4\u5EA6", "Word \u624B\u5DE5", "InDesign", "HTML+AI", "SaaS"],
  [
    ["\u8F6F\u4EF6\u6210\u672C", "\u5DF2\u6709(Office)", "\uFFE54,500/\u5E74/\u5E2D", "\u514D\u8D39(\u5F00\u6E90)", "$200-500/\u6708"],
    ["\u4EBA\u529B\u6210\u672C", "\u9AD8(\u7EAF\u624B\u5DE5)", "\u9AD8(\u9700\u8BBE\u8BA1\u5E08)", "\u4E2D(\u642D\u5EFA\u540E\u4F4E)", "\u4E2D"],
    ["\u5B66\u4E60\u95E8\u69DB", "\u4F4E(\u4EBA\u4EBA\u4F1A)", "\u9AD8(3-6\u6708)", "\u4E2D(\u9700HTML\u57FA\u7840)", "\u4F4E(\u62D6\u62FD\u5F0F)"],
    ["\u8C01\u80FD\u7F16\u8F91", "\u4EFB\u4F55\u4EBA", "\u4EC5\u8BBE\u8BA1\u5E08", "\u6280\u672F+AI\u8F85\u52A9", "\u4EFB\u4F55\u4EBA"],
    ["\u54C1\u724C\u5207\u6362", "\u624B\u52A8(2-4h)", "\u6A21\u677F(30min)", "JSON(5min)", "\u6A21\u677F(15min)"],
    ["\u591A\u8BED\u8A00\u540C\u6B65", "\u624B\u52A8\u590D\u5236\u7C98\u8D34", "\u624B\u52A8/\u63D2\u4EF6", "AI\u7FFB\u8BD1+\u81EA\u52A8", "\u90E8\u5206\u652F\u6301"],
    ["\u7F8E\u6807/\u6B27\u6807\u5207\u6362", "\u624B\u52A8\u6539\u53C2\u6570", "\u624B\u52A8\u6539\u53C2\u6570", "JSON\u81EA\u52A8\u5207\u6362", "\u4E0D\u652F\u6301"],
    ["\u7248\u672C\u7BA1\u7406", "\u6587\u4EF6\u540D+\u6587\u4EF6\u5939", "\u6587\u4EF6\u540D+\u6587\u4EF6\u5939", "Git\u7248\u672C\u63A7\u5236", "\u4E91\u7AEF\u7248\u672C"],
    ["\u7CBE\u7F8E\u5EA6", "\u2605\u2605\u2606\u2606\u2606", "\u2605\u2605\u2605\u2605\u2605", "\u2605\u2605\u2605\u2605\u2606", "\u2605\u2605\u2605\u2606\u2606"],
    ["\u4E13\u4E1A\u5EA6", "\u2605\u2605\u2606\u2606\u2606", "\u2605\u2605\u2605\u2606\u2606", "\u2605\u2605\u2605\u2605\u2605", "\u2605\u2605\u2606\u2606\u2606"],
    ["\u8D28\u68C0\u80FD\u529B", "\u65E0(\u7EAF\u4EBA\u5DE5)", "\u65E0(\u7EAF\u4EBA\u5DE5)", "\u81EA\u52A8\u5BA1\u8BA1", "\u57FA\u7840\u6821\u9A8C"],
    ["\u65B0\u54C1\u4E0A\u7EBF", "3-5\u5929", "2-3\u5929", "2-3\u5C0F\u65F6", "1-2\u5929"],
    ["\u5173\u952E\u98CE\u9669", "\u7248\u672C\u6DF7\u4E71", "\u4EBA\u5458\u4F9D\u8D56\u6210\u672C\u9AD8", "\u9996\u6B21\u642D\u5EFA\u6295\u5165\u5927", "\u4F9B\u5E94\u5546\u9501\u5B9A"],
  ], w5));
C.push(PB());

// 3. Visual quality comparison
C.push(h1("3. \u7CBE\u7F8E\u5EA6\u5BF9\u6BD4"));

C.push(h2("3.1 Word \u624B\u5DE5\u6392\u7248"));
C.push(bp("\u89C6\u89C9\u6548\u679C\uFF1A\u57FA\u7840\u6392\u7248\uFF0C\u56FE\u6587\u6DF7\u6392\u80FD\u529B\u6709\u9650"));
C.push(bp("\u5B57\u4F53\u63A7\u5236\uFF1A\u7CFB\u7EDF\u5B57\u4F53\uFF0C\u6E32\u67D3\u6548\u679C\u4E00\u822C"));
C.push(bp("\u5370\u5237\u54C1\u8D28\uFF1A\u5BFC\u51FAPDF\u540E\u53EF\u63A5\u53D7\uFF0C\u4F46\u7EC6\u8282\u7C97\u7CD9"));
C.push(bp("\u6574\u4F53\u89C2\u611F\uFF1A\u50CF\u201C\u5185\u90E8\u6587\u6863\u201D\uFF0C\u4E0E Dyson/Breville \u7B49\u56FD\u9645\u54C1\u724C\u6709\u660E\u663E\u5DEE\u8DDD"));
C.push(pr("\u8BC4\u5206\uFF1A\u2605\u2605\u2606\u2606\u2606\uFF08\u7EA640\u5206/100\uFF09", { run: { bold: true } }));

C.push(h2("3.2 InDesign \u4E13\u4E1A\u6392\u7248"));
C.push(bp("\u89C6\u89C9\u6548\u679C\uFF1A\u4E13\u4E1A\u5370\u5237\u7EA7\uFF0C\u7CBE\u786E\u52300.1mm\u7684\u6392\u7248\u63A7\u5236"));
C.push(bp("\u5B57\u4F53\u63A7\u5236\uFF1AOpenType\u5168\u7279\u6027\u652F\u6301\uFF0C\u5B57\u8DDD\u5FAE\u8C03\u3001\u8FDE\u5B57\u5904\u7406"));
C.push(bp("\u5370\u5237\u54C1\u8D28\uFF1A\u51FA\u8840\u7EBF\u3001\u8272\u5F69\u7BA1\u7406\u3001CMYK\u5206\u8272\uFF0C\u5370\u5237\u5382\u76F4\u51FA"));
C.push(bp("\u6574\u4F53\u89C2\u611F\uFF1A\u53EF\u4EE5\u505A\u51FA\u548C Dyson/Breville \u540C\u7EA7\u522B\u7684\u8BF4\u660E\u4E66"));
C.push(pr("\u8BC4\u5206\uFF1A\u2605\u2605\u2605\u2605\u2605\uFF0895\u5206/100\uFF09", { run: { bold: true } }));

C.push(h2("3.3 HTML+AI \u81EA\u52A8\u5316"));
C.push(bp("\u89C6\u89C9\u6548\u679C\uFF1ASwiss\u8BBE\u8BA1\u98CE\u683C\uFF0C\u7B80\u6D01\u4E13\u4E1A\uFF0C\u63A5\u8FD1\u4E13\u4E1A\u6C34\u5E73"));
C.push(bp("\u5B57\u4F53\u63A7\u5236\uFF1AWeb\u5B57\u4F53\uFF08HarmonyOS Sans SC\uFF09\uFF0C\u6E32\u67D3\u4E00\u81F4\u6027\u597D"));
C.push(bp("\u5370\u5237\u54C1\u8D28\uFF1ACSS\u63A7\u5236\u7CBE\u5EA6\u7EA60.5mm\uFF0C\u51FA\u8840\u7EBF\u63A7\u5236\u4E0D\u5982InDesign"));
C.push(bp("\u6574\u4F53\u89C2\u611F\uFF1A\u7EA6InDesign\u768485-90%\uFF0CCSS\u7EDF\u4E00\u63A7\u5236\u4E00\u81F4\u6027\u597D\uFF0C\u6240\u6709\u7248\u672C\u98CE\u683C\u5B8C\u5168\u7EDF\u4E00"));
C.push(pr("\u8BC4\u5206\uFF1A\u2605\u2605\u2605\u2605\u2606\uFF0882\u5206/100\uFF09", { run: { bold: true } }));

C.push(h2("3.4 SaaS \u5E73\u53F0\uFF08\u5982 Canva/Lucidpress\uFF09"));
C.push(bp("\u89C6\u89C9\u6548\u679C\uFF1A\u6A21\u677F\u597D\u770B\u4F46\u5343\u7BC7\u4E00\u5F8B"));
C.push(bp("\u5B57\u4F53\u63A7\u5236\uFF1A\u5E73\u53F0\u5185\u7F6E\u5B57\u4F53\uFF0C\u9009\u62E9\u6709\u9650"));
C.push(bp("\u5370\u5237\u54C1\u8D28\uFF1A\u5BFC\u51FAPDF\u8D28\u91CF\u53EF\u63A5\u53D7"));
C.push(bp("\u6574\u4F53\u89C2\u611F\uFF1A\u7CBE\u7EC6\u63A7\u5236\u80FD\u529B\u5F31\uFF0C\u96BE\u4EE5\u505A\u51FA\u5DEE\u5F02\u5316\u8BBE\u8BA1\uFF0C\u201C\u6A21\u677F\u611F\u201D\u660E\u663E"));
C.push(pr("\u8BC4\u5206\uFF1A\u2605\u2605\u2605\u2606\u2606\uFF0860\u5206/100\uFF09", { run: { bold: true } }));
C.push(PB());

// 4. Professionalism comparison
C.push(h1("4. \u4E13\u4E1A\u5EA6\u5BF9\u6BD4"));

C.push(h2("4.1 Word \u624B\u5DE5\u6392\u7248"));
C.push(bp("\u89C4\u8303\u7EA6\u675F\uFF1A\u65E0\u5185\u7F6E\u89C4\u8303\uFF0C\u683C\u5F0F\u4E00\u81F4\u6027\u5B8C\u5168\u9760\u4EBA"));
C.push(bp("\u5B89\u5168\u8B66\u793A\uFF1A\u5199\u6CD5\u56E0\u4EBA\u800C\u5F02\uFF0C\u65E0\u6807\u51C6\u4F53\u7CFB"));
C.push(bp("\u7ED3\u6784\u5316\u7A0B\u5EA6\uFF1A\u65E0\uFF0C\u6BCF\u4EFD\u6587\u6863\u72EC\u7ACB"));
C.push(bp("\u8D28\u68C0\u80FD\u529B\uFF1A\u65E0\u81EA\u52A8\u5316\u8D28\u68C0"));
C.push(pr("\u8BC4\u5206\uFF1A\u2605\u2605\u2606\u2606\u2606", { run: { bold: true } }));

C.push(h2("4.2 InDesign \u4E13\u4E1A\u6392\u7248"));
C.push(bp("\u89C4\u8303\u7EA6\u675F\uFF1A\u6392\u7248\u4E13\u4E1A\u5EA6\u9AD8\uFF0C\u4F46\u5185\u5BB9\u89C4\u8303\u4ECD\u9760\u4EBA\u5DE5\u628A\u63A7"));
C.push(bp("\u5B89\u5168\u8B66\u793A\uFF1A\u53EF\u505A\u7CBE\u7F8E\u8B66\u793A\u6846\uFF0C\u4F46\u65E0\u81EA\u52A8\u5316\u6821\u9A8C"));
C.push(bp("\u7ED3\u6784\u5316\u7A0B\u5EA6\uFF1A\u6A21\u677F+\u6837\u5F0F\u8868\uFF0C\u4E2D\u7B49"));
C.push(bp("\u8D28\u68C0\u80FD\u529B\uFF1A\u65E0\u81EA\u52A8\u5316\u8D28\u68C0\uFF0C\u9760\u8BBE\u8BA1\u5E08\u7ECF\u9A8C"));
C.push(pr("\u8BC4\u5206\uFF1A\u2605\u2605\u2605\u2606\u2606", { run: { bold: true } }));

C.push(h2("4.3 HTML+AI \u81EA\u52A8\u5316"));
C.push(bp("\u89C4\u8303\u7EA6\u675F\uFF1A\u5185\u7F6E\u5B89\u5168\u8B66\u793A\u4E09\u7EA7\u4F53\u7CFB\uFF08WARNING/CAUTION/NOTICE\uFF0C\u53C2\u7167IEC 82079\uFF09"));
C.push(bp("\u5B89\u5168\u8B66\u793A\uFF1A\u7ED3\u6784\u5316\u5B9A\u4E49\uFF0CAI\u81EA\u52A8\u751F\u6210\uFF0C\u5BA1\u8BA1\u81EA\u52A8\u6821\u9A8C"));
C.push(bp("\u7ED3\u6784\u5316\u7A0B\u5EA6\uFF1A8\u6807\u51C6\u7AE0\u8282\uFF0CJSON\u914D\u7F6E\u9A71\u52A8\uFF0C\u6700\u63A5\u8FD1DITA/CCMS"));
C.push(bp("\u8D28\u68C0\u80FD\u529B\uFF1A\u81EA\u52A8\u5BA1\u8BA1\u2014\u2014\u56FE\u7247\u52A0\u8F7D\u3001\u5206\u9875\u5B8C\u6574\u6027\u3001\u54C1\u724C\u4E00\u81F4\u6027\u3001\u591A\u8BED\u8A00\u540C\u6B65"));
C.push(pr("\u8BC4\u5206\uFF1A\u2605\u2605\u2605\u2605\u2605", { run: { bold: true } }));

C.push(h2("4.4 SaaS \u5E73\u53F0"));
C.push(bp("\u89C4\u8303\u7EA6\u675F\uFF1A\u65E0\u884C\u4E1A\u89C4\u8303\u652F\u6301"));
C.push(bp("\u5B89\u5168\u8B66\u793A\uFF1A\u65E0\u6807\u51C6\u4F53\u7CFB"));
C.push(bp("\u7ED3\u6784\u5316\u7A0B\u5EA6\uFF1A\u6A21\u677F\u7EA7\uFF0C\u65E0\u6DF1\u5EA6\u7ED3\u6784\u5316"));
C.push(bp("\u8D28\u68C0\u80FD\u529B\uFF1A\u57FA\u7840\u62FC\u5199\u68C0\u67E5"));
C.push(pr("\u8BC4\u5206\uFF1A\u2605\u2605\u2606\u2606\u2606", { run: { bold: true } }));
C.push(PB());

// 5. Cost estimation
C.push(h1("5. \u8BE6\u7EC6\u6210\u672C\u4F30\u7B97"));
C.push(pr("\u573A\u666F\uFF1A10\u6B3E\u4EA7\u54C1/\u5E74\uFF0C\u6BCF\u6B3E\u4EA7\u54C1\u9700\u8981\u4E2D\u82F1\u53CC\u8BED\u7248\u672C"));
const cw = [2000, 1910, 1910, 1910, 1908];
C.push(tbl(
  ["\u6210\u672C\u9879", "Word \u624B\u5DE5", "InDesign", "HTML+AI", "SaaS"],
  [
    ["\u8F6F\u4EF6\u8D39(\u5E74)", "\uFFE50(\u5DF2\u6709)", "\uFFE59,000(2\u5E2D)", "\uFFE50", "\uFFE518k-42k"],
    ["\u9996\u6B21\u642D\u5EFA", "\uFFE50", "\uFFE50", "\uFFE530k-50k", "\uFFE55,000"],
    ["\u5355\u4EA7\u54C1\u9996\u7248", "\uFFE51,500-2,500", "\uFFE51,600-2,400", "\uFFE5250", "\uFFE5500-1,000"],
    ["\u54C1\u724C\u53D8\u4F53(\u00D73)", "\uFFE53k-6k", "\uFFE51.2k-2.4k", "\uFFE550", "\uFFE5500-1k"],
    ["10\u6B3E\u5E74\u5236\u4F5C", "\uFFE545k-85k", "\uFFE528k-48k", "\uFFE53k-5k", "\uFFE510k-20k"],
    ["\u5E74\u7EF4\u62A4\u66F4\u65B0", "\uFFE520k-40k", "\uFFE510k-20k", "\uFFE52k-5k", "\uFFE55k-10k"],
    ["\u9996\u5E74\u603B\u6210\u672C", "\uFFE565k-125k", "\uFFE547k-77k", "\uFFE535k-60k", "\uFFE538k-77k"],
    ["\u7B2C\u4E8C\u5E74\u8D77", "\uFFE565k-125k", "\uFFE547k-77k", "\uFFE55k-10k", "\uFFE533k-72k"],
  ], cw));
C.push(pr(""));
C.push(pr([new TextRun({ text: "\u5173\u952E\u53D1\u73B0\uFF1A", size: 22, font: F, bold: true }),
  new TextRun({ text: "HTML+AI\u65B9\u6848\u9996\u5E74\u6210\u672C\u4E0E\u5176\u4ED6\u65B9\u6848\u76F8\u5F53\uFF0C\u4F46\u7B2C\u4E8C\u5E74\u8D77\u6210\u672C\u65AD\u5D16\u5F0F\u4E0B\u964D\uFF08\u4EC5\uFFE55,000-10,000/\u5E74\uFF09\uFF0C\u957F\u671F\u7ECF\u6D4E\u6027\u6700\u4F18\u3002", size: 22, font: F })]));
C.push(PB());

// 6. Industry reference
C.push(h1("6. \u884C\u4E1A\u505A\u6CD5\u53C2\u8003"));
const iw = [1600, 1600, 3438, 3000];
C.push(tbl(
  ["\u4F01\u4E1A\u89C4\u6A21", "\u8425\u6536\u533A\u95F4", "\u5178\u578B\u505A\u6CD5", "\u4EE3\u8868\u4F01\u4E1A"],
  [
    ["\u5C0F\u5382", "<1\u4EBF", "Word\u6392\u7248 + \u5370\u5237\u5382\u7CBE\u6392", "\u5927\u91CF\u767D\u724C/OEM\u5382\u5546"],
    ["\u4E2D\u5382", "1-5\u4EBF", "Word + \u5916\u5305\u8BBE\u8BA1 \u6216 \u5185\u90E8\u8BBE\u8BA1\u5E08", "\u4E9A\u4FCA\u6C0F\u5F53\u524D\u4F4D\u7F6E"],
    ["\u4E2D\u5927\u5382", "5-10\u4EBF", "InDesign + \u5185\u90E8\u8BBE\u8BA1\u56E2\u961F", "Nesco\u3001Mueller"],
    ["\u5927\u5382", ">10\u4EBF", "DITA/CCMS + \u4E13\u4E1A\u6280\u672F\u5199\u4F5C\u56E2\u961F", "FoodSaver(Newell)\u3001Dyson"],
    ["\u79D1\u6280\u5DE8\u5934", ">100\u4EBF", "\u5168\u81EA\u52A8\u5316\u6587\u6863\u7CFB\u7EDF + \u591A\u8BED\u8A00\u7BA1\u7406\u5E73\u53F0", "\u5C0F\u7C73\u3001Apple"],
  ], iw));
C.push(pr(""));
C.push(pr([new TextRun({ text: "\u4E9A\u4FCA\u6C0F\uFF082024\u5E74\u8425\u65362.92\u4EBF\uFF09\u5904\u4E8E\u201C\u4E2D\u5382\u201D\u533A\u95F4\u3002HTML+AI\u65B9\u6848\u7684\u5B9A\u4F4D\u662F\uFF1A\u7528\u4E2D\u5382\u7684\u6210\u672C\uFF0C\u83B7\u5F97\u63A5\u8FD1\u5927\u5382\u7684\u4E13\u4E1A\u5EA6\u548C\u6548\u7387\u3002", size: 22, font: F, bold: true })]));
C.push(PB());

// 7. Recommended solution
C.push(h1("7. \u63A8\u8350\u65B9\u6848\uFF1AWord + AI\u81EA\u52A8\u5316\u8F85\u52A9"));

C.push(h2("7.1 \u6838\u5FC3\u601D\u8DEF"));
C.push(pr("\u4FDD\u7559Word\u4F5C\u4E3A\u5185\u5BB9\u7F16\u8F91\u5165\u53E3\uFF08\u4EBA\u4EBA\u53EF\u7528\uFF09\uFF0C\u5F15\u5165AI\u81EA\u52A8\u5316\u5904\u7406\u591A\u7248\u672C\u8F93\u51FA\u548C\u8D28\u68C0\u3002"));
C.push(pr([new TextRun({ text: "\u5DE5\u4F5C\u6D41\uFF1AWord\u7BA1\u5185\u5BB9 \u2192 JSON\u7BA1\u914D\u7F6E \u2192 AI\u7BA1\u8F93\u51FA \u2192 \u4EBA\u5DE5\u7EC8\u5BA1", size: 22, font: F, bold: true })]));

C.push(h2("7.2 \u5404\u89D2\u8272\u5206\u5DE5"));
const rw = [1800, 2600, 2600, 2638];
C.push(tbl(
  ["\u89D2\u8272", "\u804C\u8D23", "\u5DE5\u5177", "\u6280\u80FD\u8981\u6C42"],
  [
    ["\u4EA7\u54C1\u7ECF\u7406/\u5DE5\u7A0B\u5E08", "\u63D0\u4F9B\u4EA7\u54C1\u89C4\u683C\u3001\u529F\u80FD\u63CF\u8FF0", "Excel/JSON", "\u65E0\u7279\u6B8A\u8981\u6C42"],
    ["\u5185\u5BB9\u7F16\u8F91", "\u7F16\u5199/\u5BA1\u6838\u8BF4\u660E\u4E66\u6587\u5B57\u5185\u5BB9", "Word", "\u57FA\u7840Word\u64CD\u4F5C"],
    ["\u6280\u672F\u534F\u52A9\u65B9", "\u7EF4\u62A4\u6A21\u677F\u3001\u914D\u7F6E\u3001\u81EA\u52A8\u5316\u6D41\u7A0B", "HTML/CSS/Python", "\u524D\u7AEF+\u811A\u672C\u57FA\u7840"],
    ["AI\u7CFB\u7EDF", "\u7FFB\u8BD1\u3001\u591A\u7248\u672C\u751F\u6210\u3001\u683C\u5F0F\u8F6C\u6362\u3001\u8D28\u68C0", "Claude API", "\u81EA\u52A8\u8FD0\u884C"],
    ["\u7BA1\u7406\u8005", "\u7EC8\u5BA1\u3001\u7B7E\u53D1", "PDF\u9605\u8BFB\u5668", "\u65E0\u7279\u6B8A\u8981\u6C42"],
  ], rw));

C.push(h2("7.3 \u843D\u5730\u6B65\u9AA4\uFF085\u6B65\uFF09"));
C.push(pr([new TextRun({ text: "\u7B2C\u4E00\u6B65\uFF1A\u7ED3\u6784\u5316\u4EA7\u54C1\u4FE1\u606F\uFF081-2\u5468\uFF09", size: 22, font: F, bold: true })]));
C.push(bp("\u5EFA\u7ACBproduct-config.json\u914D\u7F6E\u4F53\u7CFB"));
C.push(bp("\u5305\u542B\uFF1A\u54C1\u724C\u4FE1\u606F\u3001\u7535\u538B\u89C4\u683C\u3001\u8BA4\u8BC1\u6807\u5FD7\u3001\u5BA2\u670D\u4FE1\u606F"));
C.push(bp("\u6548\u679C\uFF1A\u53D8\u91CF\u4ECEWord\u4E2D\u5265\u79BB\uFF0C\u6539\u914D\u7F6E\u4E0D\u6539\u6587\u6863"));

C.push(pr([new TextRun({ text: "\u7B2C\u4E8C\u6B65\uFF1A\u5EFA\u7ACB\u8BF4\u660E\u4E66\u7F16\u5199\u89C4\u8303\uFF08\u5DF2\u5B8C\u6210\uFF09", size: 22, font: F, bold: true })]));
C.push(bp("8\u6807\u51C6\u7AE0\u8282\u7ED3\u6784"));
C.push(bp("\u5B89\u5168\u8B66\u793A\u4E09\u7EA7\u4F53\u7CFB\uFF08WARNING/CAUTION/NOTICE\uFF09"));
C.push(bp("\u6392\u7248\u89C4\u8303\uFF08\u5B57\u4F53\u3001\u989C\u8272\u3001\u95F4\u8DDD\uFF09"));

C.push(pr([new TextRun({ text: "\u7B2C\u4E09\u6B65\uFF1A\u642D\u5EFAAI\u751F\u6210\u6D41\u6C34\u7EBF\uFF082-3\u5468\uFF09", size: 22, font: F, bold: true })]));
C.push(bp("Word\u539F\u7A3F \u2192 AI\u89E3\u6790 \u2192 HTML\u6E32\u67D3 \u2192 PDF\u8F93\u51FA"));
C.push(bp("\u591A\u54C1\u724C\u53D8\u4F53\u81EA\u52A8\u751F\u6210\uFF08\u6539JSON\u914D\u7F6E\u5373\u53EF\uFF09"));
C.push(bp("\u4E2D\u82F1\u53CC\u8BED\u81EA\u52A8\u7FFB\u8BD1+\u672F\u8BED\u8868\u7BA1\u7406"));
C.push(bp("\u6548\u679C\uFF1A\u5355\u4EA7\u54C1\u4ECE3-5\u5929\u7F29\u77ED\u52302-3\u5C0F\u65F6"));

C.push(pr([new TextRun({ text: "\u7B2C\u56DB\u6B65\uFF1A\u5EFA\u7ACB\u81EA\u52A8\u8D28\u68C0\u4F53\u7CFB\uFF081\u5468\uFF09", size: 22, font: F, bold: true })]));
C.push(bp("\u56FE\u7247\u52A0\u8F7D\u9A8C\u8BC1\u3001\u5206\u9875\u5B8C\u6574\u6027\u68C0\u67E5"));
C.push(bp("\u54C1\u724C\u4E00\u81F4\u6027\u6821\u9A8C\u3001\u591A\u8BED\u8A00\u540C\u6B65\u68C0\u67E5"));
C.push(bp("\u6548\u679C\uFF1A\u8D28\u91CF\u95EE\u9898\u5728\u4EA4\u4ED8\u524D\u81EA\u52A8\u53D1\u73B0"));

C.push(pr([new TextRun({ text: "\u7B2C\u4E94\u6B65\uFF1A\u8BD5\u70B9\u8FD0\u884C+\u8FED\u4EE3\uFF08\u6301\u7EED\uFF09", size: 22, font: F, bold: true })]));
C.push(bp("\u90091-2\u6B3E\u4EA7\u54C1\u8BD5\u70B9\uFF0C\u6536\u96C6\u53CD\u9988\uFF0C\u4F18\u5316\u6D41\u7A0B"));
C.push(bp("\u9010\u6B65\u8986\u76D6\u5168\u4EA7\u54C1\u7EBF"));

C.push(h2("7.4 \u5DF2\u9A8C\u8BC1\u7684\u6210\u679C"));
C.push(pr("V23\u771F\u7A7A\u5C01\u53E3\u673A\u8BF4\u660E\u4E66\u5DF2\u5B8C\u6210HTML+AI\u65B9\u6848\u7684\u5B8C\u6574\u9A8C\u8BC1\uFF1A"));
C.push(bp("\u4E2D\u82F1\u53CC\u8BED\u7248\u672C"));
C.push(bp("4\u79CD\u8BBE\u8BA1\u98CE\u683C\uFF08\u4E3B\u98CE\u683C/Swiss/\u5C0F\u7C73/Lifestyle\uFF09"));
C.push(bp("\u81EA\u52A8\u8D28\u68C0\u901A\u8FC7\uFF08\u56FE\u7247\u52A0\u8F7D\u3001\u5206\u9875\u3001\u54C1\u724C\u4E00\u81F4\u6027\uFF09"));
C.push(bp("\u9A91\u9A6C\u9489\u5C0F\u518C\u5B50\u81EA\u52A8\u751F\u6210"));
C.push(PB());

// 8. Summary decision matrix
C.push(h1("8. \u603B\u7ED3\uFF1A\u4E00\u9875\u7EB8\u51B3\u7B56\u77E9\u9635"));
const dw = [2400, 2400, 4838];
C.push(tbl(
  ["\u51B3\u7B56\u7EF4\u5EA6", "\u63A8\u8350\u9009\u62E9", "\u7406\u7531"],
  [
    ["\u8FFD\u6C42\u6700\u9AD8\u89C6\u89C9\u54C1\u8D28", "InDesign", "\u5370\u5237\u7EA7\u7CBE\u5EA6\uFF0C\u4F46\u9700\u4E13\u4E1A\u8BBE\u8BA1\u5E08"],
    ["\u8FFD\u6C42\u6700\u9AD8\u6027\u4EF7\u6BD4", "HTML+AI", "\u9996\u5E74\u6301\u5E73\uFF0C\u7B2C\u4E8C\u5E74\u8D77\u6210\u672C\u964D90%"],
    ["\u8FFD\u6C42\u6700\u4F4E\u95E8\u69DB", "Word\uFF08\u73B0\u72B6\uFF09", "\u4F46\u65E0\u6CD5\u89E3\u51B3\u7248\u672C\u7BA1\u7406\u548C\u4E00\u81F4\u6027\u95EE\u9898"],
    ["\u8FFD\u6C42\u6700\u5FEB\u4E0A\u624B", "SaaS", "\u4F46\u5B9A\u5236\u53D7\u9650\uFF0C\u4F9B\u5E94\u5546\u9501\u5B9A"],
    ["\u7EFC\u5408\u63A8\u8350\uFF08\u4E9A\u4FCA\u6C0F\uFF09", "Word + AI\u81EA\u52A8\u5316", "\u4FDD\u7559Word\u6613\u7528\u6027 + AI\u89E3\u51B3\u6548\u7387\u548C\u8D28\u91CF\u95EE\u9898"],
  ], dw));

C.push(pr(""));
C.push(pr([new TextRun({ text: "\u6700\u7EC8\u5EFA\u8BAE\uFF1A", size: 24, font: F, bold: true, color: ACCENT }),
  new TextRun({ text: "\u91C7\u7528\u201CWord + AI\u81EA\u52A8\u5316\u201D\u65B9\u6848\uFF0C\u9996\u671F\u6295\u5165\u7EA63-5\u4E07\u5143\uFF0C4-6\u5468\u53EF\u5B8C\u6210\u642D\u5EFA\uFF0C\u7B2C\u4E8C\u5E74\u8D77\u5E74\u8FD0\u8425\u6210\u672C\u4EC5\u7EA65,000-10,000\u5143\u3002V23\u8BF4\u660E\u4E66\u5DF2\u9A8C\u8BC1\u65B9\u6848\u53EF\u884C\u6027\u3002", size: 22, font: F })]));

// ── Build document ──
const ACCENT_CLR = "FF6900";
const doc = new Document({
  styles: {
    default: { document: { run: { font: F, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: F }, paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: F }, paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
    ],
  },
  numbering: {
    config: [{
      reference: "bl",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: PW, height: PH },
        margin: { top: MG, right: MG, bottom: MG, left: MG },
      },
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: "\u4E9A\u4FCA\u6C0F\u771F\u7A7A\u79D1\u6280 | \u8BF4\u660E\u4E66\u5236\u4F5C\u65B9\u6848\u5BF9\u6BD4", size: 18, font: F, color: "999999" })],
      })] }),
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "\u7B2C ", size: 18, font: F, color: "999999" }),
          new TextRun({ children: [PageNumber.CURRENT], size: 18, font: F, color: "999999" }),
          new TextRun({ text: " \u9875", size: 18, font: F, color: "999999" })],
      })] }),
    },
    children: C,
  }],
});

const path = require("path");
const OUT = path.join("D:", "work", "private", "yjsplan", "research", "yjs-manual-opt", "data", "\u8BF4\u660E\u4E66\u5236\u4F5C\u65B9\u6848\u5BF9\u6BD4\u5206\u6790.docx");
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  console.log("OK: " + OUT + " (" + buf.length + " bytes)");
}).catch(e => { console.error("FAIL:", e); process.exit(1); });
