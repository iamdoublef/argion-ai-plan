# iter-02 notes

## Changes

- Restored normal bullet rhythm for standard pages; kept special compression only inside the p3 safety warning box.
- Increased compact troubleshooting table padding/row height enough to bring the disclaimer box back toward the target.
- Added compact-warranty-specific table row height/padding so p14 brand/manufacturer tables match PDF internal spacing better.
- Detected `Warranty separator` image and forced it to a narrow centered rule with target-like vertical spacing.

## Score

- Overall: `11.36 -> 10.74`
- Max page: `25.07 -> 17.74`
- Pages: `15`, editable: `100%`
- Stop condition met: overall `< 12.0` and max page `< 18.0`.

## Per-page changes

| Page | Previous best | iter-01 | iter-02 | Note |
| --- | ---: | ---: | ---: | --- |
| p3 | 17.99 | 15.80 | 17.38 | Safety box now matches height better than iter-01, but text extraction remains offset. |
| p5 | 14.49 | 13.45 | 13.72 | Subtitle position improved vs starting point; bullet rhythm still differs from PDF. |
| p6 | 14.70 | 7.39 | 7.39 | Product structure page remains strong. |
| p7 | 17.01 | 8.17 | 8.17 | Product function page remains strong. |
| p9 | 12.71 | 13.96 | 13.64 | Step/image page remains above target but within max-page cap. |
| p11 | 16.89 | 14.67 | 12.36 | Troubleshooting table/disclaimer now near target. |
| p13 | 15.02 | 14.35 | 13.79 | WEEE page slightly improved. |
| p14 | 19.59 | 25.07 | 17.74 | Separator and warranty table spacing fixed enough to pass max-page gate. |
