# design-iter-07 notes

Starting point:
- `design-iter-05/path-codex/build_b2_docx.py`
- Local baseline `iter-00/output.docx`: overall `10.31`, max `17.67`
- Anti-cheat gates passed: `editable_pct=100.0`, `wt_count=457`, `image_hack_detected=false`, `text_ratio=1.00`

Best valid result:
- `selected/output.docx`
- Same score as retained `iter-03/output.docx`
- Overall visual diff: `10.09`
- Max page diff: `15.35`
- Pages: `15 / 15`
- Text ratio: `1.00`
- `wt_count`: `457`
- Image bytes: `533482`
- Image hack detected: `false`
- Editable percent: `100.0`

Iteration log:

| Iter | Change | Overall | Max | Decision |
| --- | --- | ---: | ---: | --- |
| iter-00 | Rebuilt copied iter-05 builder unchanged | 10.31 | 17.67 | Baseline |
| iter-01 | Reduced p10 status labels and tightened note-box bullets | 10.24 | 17.67 | Kept |
| iter-02 | Added extra after-list spacing on plain text pages | 10.25 | 17.67 | Reverted, p13 regressed |
| iter-03 | Tightened compact-warranty table padding/row height to `48/238` | 10.09 | 15.35 | Kept, best |
| iter-04 | More aggressive warranty table compaction to `42/228` | 10.40 | 20.12 | Reverted |
| iter-05 | Midpoint warranty table compaction to `45/234` | 10.26 | 17.92 | Reverted |
| iter-06 | Increased compact safety warning title spacing | 10.14 | 15.35 | Reverted, p3 regressed |
| iter-07 | Increased step-flow paragraph spacing | 10.21 | 15.35 | Reverted |
| iter-08 | Reduced compact troubleshooting table padding/row height | 10.21 | 15.35 | Reverted |

Best per-page diffs:
- `[3.62, 3.55, 13.81, 7.87, 13.72, 7.39, 8.17, 8.13, 13.05, 9.99, 12.36, 10.30, 13.57, 15.35, 10.41]`

Result against requested goal:
- Overall `< 9.0`: not met
- Max `< 14.0`: not met
- Max improved from `17.67` to `15.35`
- p10 improved from `11.06` to `9.99`
- p14 improved from `17.67` to `15.35`

Legal/anti-cheat verification:
- No full-page screenshots embedded.
- All text remains normal editable Word text.
- Final selected score: `editable_pct=100.0`, `wt_count=457`, `image_hack_detected=false`, `text_ratio=1.00`.

Retained builder changes:
- p10 status indicator labels are rendered lighter/smaller.
- Note-box bullet lists use tight spacing.
- Compact warranty tables use `pad_v=48` and `row_height=238`.
