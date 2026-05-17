# design-iter-30 status

## Result

Accepted at `iter-4/output.docx`.

Validation and score:

- Official docx validation: `All validations PASSED!`
- Pages: 15 target / 15 candidate
- Text ratio: 1.00
- Editability: 100.0%, `wt_count` 457
- Drawings: 16, image bytes 530887, image hack false
- Visual diff: mean 8.67, max 12.35

This matches the W27 plateau threshold exactly while adding a text-parameter workflow.

## Iterations

- `iter-1`: direct OOXML rebuild from Swiss base template. Validation passed, editable passed, visual 11.44 mean / 25.35 max.
- `iter-2`: fixed footer placeholders, alert icon, warranty contact wrap. Validation passed, visual 10.82 / 22.98.
- `iter-3`: added percentage table widths. Validation passed, visual 10.64 / 22.66.
- `iter-4`: official docx-skill unpack/edit/pack of W27 structural reference, extracted params, normalized OOXML order. Validation passed, visual 8.67 / 12.35.

## Artifacts

- `build_template.py`: generator.
- `iter-4/output.docx`: accepted DOCX.
- `iter-4/params.json`: editable text values for SKU substitution.
- `iter-4/text_params.json`: extracted default text values.
- `iter-4/template_parts/`: placeholder XML templates.
- `TEMPLATE.md`: text-replacement workflow.

## Notes

The installed Claude docx skill did not include a `reference/` directory. The closest available structural reference was the W27 DOCX generated from the requested source-of-truth builder, then normalized through the official docx unpack/edit/pack flow.
