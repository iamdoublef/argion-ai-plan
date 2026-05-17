# iter-13 — Caution box styling fix (best so far)

## Changes from iter-11
- CAUTION box: removed icon (▲), white fill, thin black border (was: ▲ icon + black border)
- NOTICE box: confirmed gray fill + gray border (was already correct)
- WARNING box: keep ▲ red icon + thick red border + white fill (matches target)

## Result
- Visual diff: **13.77** (was 13.80) — slight improvement
- Page 4: 11.15 → 10.08 (caution box style now matches target)
- Page 11: 21.28 → 20.68

## Total improvement vs original winner (iter-05 of a2-custom)
- baseline: 16.65
- iter-13: 13.77
- **17.3% reduction in visual diff**

## Best iter so far
This is the recommended final. All structural fixes from DESIGN_BRIEF applied.
