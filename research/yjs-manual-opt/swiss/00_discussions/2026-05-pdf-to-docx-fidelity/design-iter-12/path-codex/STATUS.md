# design-iter-12 path-codex status

## Result

- Best candidate: `output.docx` / `iter-3/output.docx`
- Change kept: list marker changed from `\u2022` round bullet to red bold ASCII `*`
- Bullet styling: `#E63946`, bold, `Arial Black` via existing bold font path
- Bullet size: `5.25pt` for tight lists, `5.8pt` for normal lists

## Scores

| Candidate | Overall diff | Max page diff | wt_count | image_hack | Notes |
| --- | ---: | ---: | ---: | --- | --- |
| iter-1 | 9.74 | 15.04 | 456 | false | Large ASCII `*`, regressed slightly |
| iter-2 | 10.08 | 16.13 | 456 | false | `✱` glyph, rejected due regression > 0.1 |
| iter-3 | 9.67 | 13.35 | 456 | false | Best kept variant |
| iter-4 | 9.67 | 13.44 | 456 | false | Smaller `*`, tied overall but worse max page |
| iter-5 | 9.69 | 13.49 | 456 | false | Arial bold instead of Arial Black, worse |
| output | 9.67 | 13.35 | 456 | false | Final rebuilt from kept code |

## Verification

Command used:

```powershell
$env:PYTHONUTF8='1'; python build_b2_docx.py output.docx; python ../../score_candidate.py output.docx --target "D:/work/private/yjsplan/research/yjs-manual-opt/swiss/output/imt050-wevac-eu-cn.pdf" --baseline-pngs ../../baseline/target_png
```

Final pass flags: pages true, text true, editable true, visual true, overall true.

DOCX XML marker check:

- `asterisk_count=72`
- `red_count=103`
- `bullet2022_count=0`

## Notes

- The final change addresses the customer-visible black round dot issue by making generated list markers red asterisks.
- It did not lower overall diff below W16's reported 9.67, but it preserved the 9.67 overall and lowered the max page diff to 13.35.
- Anti-cheat constraints passed: `wt_count=456` and `image_hack_detected=false`.
