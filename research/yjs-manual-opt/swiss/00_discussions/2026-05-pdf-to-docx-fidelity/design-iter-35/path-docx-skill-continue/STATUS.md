# design-iter-35 path-docx-skill-continue — STATUS

## Outcome: BREAKTHROUGH at iter-10

**Final accepted**: `final/imt050-wevac-eu-cn.docx`

Scores vs baseline (W27 / design-iter-30/iter-4):
- LibreOffice visual diff mean: **8.67 → 8.64** (-0.03)
- LibreOffice visual diff max: **12.35 → 12.29** (-0.06)
- Per-page improvements: p5 -0.23, p9 -0.10, p13 -0.11, p14 -0.06
- Per-page slight regressions (all <0.05): p3 +0.03, p11 +0.01, p10 +0.03
- All gates passed: validate.py PASS, Word COM open PASS, editable 100%, wt_count 445

## Iterations summary

| iter | change | mean | max | verdict |
|------|--------|------|-----|---------|
| 0 (base) | baseline.docx (iter-4 W27) | 8.67 | 12.35 | baseline |
| 1 | Fix line=24→240 typo on 2 spacer paragraphs | 8.73 | 12.65 | regression (typo was load-bearing) |
| 2 | Add w:docGrid w:type="default" to 15 sections | 8.67 | 12.35 | neutral (LO ignores) |
| 3 | Add scissor-cut decoration line to p14 | 8.67 | 12.36 | neutral |
| 4 | Change themeFontLang eastAsia ja-JP → zh-CN | 8.69 | 12.88 | regression (p3 +0.84) |
| 5 | Add w:autoSpaceDE/DN=0 to every pPr (306 sites) | 8.67 | 12.35 | neutral (LO ignores at pPr level) |
| 6 | Remove w:useFELayout from settings.xml | 8.67 | 12.35 | neutral |
| 7 | Add w:autoSpaceLikeWord95 + doNotUseHTMLParagraphAutoSpacing | 9.26 | 15.57 | major regression |
| 8 | Add w:noPunctuationKerning + strictFirstAndLastChars to settings | 8.67 | 12.35 | neutral |
| 9 | Body run w:spacing 5 → 2 on 75 sz=14 body rPr | 8.70 | 12.47 | regression (LO already tight) |
| **10** | **Body run w:spacing 5 → 8 on 75 sz=14 body rPr** | **8.64** | **12.29** | **WIN** |

## Key finding

The dominant pixel-diff vs target was driven by **line-wrap mismatch** on CJK
body paragraphs. LibreOffice was rendering body text *slightly narrower* than
target PDF, causing lines to wrap at different points. Compat-block tweaks
(autoSpaceDE/DN, useFELayout, themeFontLang, kerning) were all silently ignored
by LibreOffice. The lever that worked was **character spacing in rPr**.

iter-9 (5 → 2) made it worse, confirming candidate was already narrower than
target. iter-10 (5 → 8) widened body text by ~3 twips per char (≈0.15 pt),
forcing earlier line-wraps and matching target's wrap points more closely.

## Word safety

iter-10 changes only `<w:spacing w:val="5"/>` → `<w:spacing w:val="8"/>` inside
75 specific rPr blocks. No settings.xml changes, no scheme changes, no
margin/page edits, no font edits. Validates via official validate.py. Opens
in MS Word via docx2pdf COM (verified in 3.4s, no corruption).

## Files

- `baseline.docx`: input baseline (W27)
- `_baseline_unpacked/`: unpacked baseline reference
- `iter-1/` ... `iter-10/`: per-iter unpacked + output + CHANGE.md + score.json
- `final/imt050-wevac-eu-cn.docx`: accepted output
- `final/word_render.pdf`: Word COM rendering proof
- `run_iter.py`: pack+score helper
- `diff_view.py`: side-by-side target/candidate PNG diff generator

## Next angles (if further iteration needed)

1. Try body spacing val=6 or 7 (between 5 and 8) — fine-tune
2. Apply same +3 spacing bump to OTHER colors (title/red/etc) on hard pages
3. Differential spacing per hard page (e.g. spacing=10 on p14 only)
4. Reduce body line-spacing (currently 278) to gain vertical real estate
