# design-iter-29 path-codex status

## Goal

Optimize for MS Word rendering while still tracking the LibreOffice baseline.

Acceptance rule from prompt: keep an iteration if either LibreOffice or Word score improves and the other score does not regress by more than `0.5`.

## Baseline

- Final retained candidate from this workspace: `output.docx`
- LibreOffice baseline reproduced locally: `8.67 / 12.35`
- Existing W27 Word render copied from design-iter-28 and rescored locally: `9.16 / 15.27`
- Word COM gate is blocked in this session before opening the DOCX:
  - `compare_word.py output.docx word_render.pdf`
  - fails with `pywintypes.com_error: (-2147023584, '指定的登录会话不存在。可能已被终止。', None, None)`
  - direct `Start-Process WINWORD.EXE` fails with the same logon-session error

## Iterations

| Candidate | Focused change | LO overall / max | Word overall / max | Decision |
| --- | --- | ---: | ---: | --- |
| iter-1 | `w:rFonts/@w:hint="eastAsia"` + `w:szCs` equal to `w:sz` + `w:kern=2` | `10.62 / 22.31` | blocked by host Word session | rejected: LO regression `+1.95 / +9.96` |
| iter-2 | iter-1 + body paragraph `w:adjustRightInd=0`, `w:autoSpaceDE=0`, `w:autoSpaceDN=0` | `10.62 / 22.31` | blocked by host Word session | rejected: LO regression `+1.95 / +9.96` |
| iter-3 | iter-1 + `w:szCs` reduced by 1 half-point | `10.62 / 22.31` | blocked by host Word session | rejected: LO regression `+1.95 / +9.96` |
| iter-4 | iter-1 + `w:szCs` increased by 1 half-point | `10.62 / 22.31` | blocked by host Word session | rejected: LO regression `+1.95 / +9.96` |
| iter-5 | iter-1 + tighter `tcMar` on troubleshooting/warranty tables | `10.46 / 19.55` | blocked by host Word session | rejected: LO regression `+1.79 / +7.20` |
| iter-6 | iter-2 + tighter `tcMar` on troubleshooting/warranty tables | `10.46 / 19.55` | blocked by host Word session | rejected: LO regression `+1.79 / +7.20` |

## Notes

- Starter builder copied from `design-iter-22/path-codex/build_b2_docx.py`.
- Each candidate must pass `compare_word.py` and produce `word_render.pdf`.
- In this host session, the required Word gate cannot launch Word at all, so no candidate can satisfy the compatibility gate here.
- The Word-directed run properties are not harmless for the LibreOffice score. Adding `w:szCs`/`w:kern` caused large LO regressions on p3, p11, and p14, so no experimental branch was retained.
- `build_b2_docx.py` keeps the probes behind `WORD_TUNE`; default/no-env output is the W27-equivalent path.
