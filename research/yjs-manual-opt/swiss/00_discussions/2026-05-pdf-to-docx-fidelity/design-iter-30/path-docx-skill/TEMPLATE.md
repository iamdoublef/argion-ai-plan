# IMT050 DOCX Text-Template Workflow

## Build command

```powershell
$env:PYTHONUTF8='1'
python build_template.py iter-4/output.docx --params iter-4/params.json
python C:/Users/iamdo/.claude/skills/docx/scripts/office/validate.py iter-4/output.docx
python ../../score_candidate.py iter-4/output.docx --target ../../../../output/imt050-wevac-eu-cn.pdf --baseline-pngs ../../baseline/target_png
```

## Template source

- `build_template.py` uses the official Claude docx workflow:
  - `unpack.py` unpacks the W27 structural reference DOCX.
  - XML text nodes in `word/document.xml`, `word/header*.xml`, and `word/footer*.xml` are extracted into params.
  - OOXML is normalized for validator-clean element order.
  - `pack.py` repacks the DOCX.
- Placeholder XML is written to `iter-4/template_parts/`.
- Final DOCX XML contains real text only; no `{{key}}` placeholders remain in `iter-4/output.docx`.

## Parameter files

- `iter-4/params.json`: values used to build the DOCX.
- `iter-4/text_params.json`: extracted default values from the reference.
- Keys are stable for this template source and are named by XML part plus sequence.

Important SKU keys:

| Key | Current value | Use |
| --- | --- | --- |
| `word_document_xml_003` | `MODEL IMT050` | Cover model |
| `word_document_xml_009` | IMT050 manual title | Cover/footer-adjacent manual title |
| `word_footer2_xml_001` ... `word_footer15_xml_001` | IMT050 footer label | Per-page footer label |
| `word_document_xml_418` | `WEVAC TECHNOLOGY CO., LIMITED` | Brand company name |
| `word_document_xml_413` | `support@wevactech.com \| www.wevactech.com` | Cover/contact line |
| `word_document_xml_424` | `support@wevactech.com` | Brand support email |
| `word_document_xml_443` | Warranty service email sentence | Warranty service email |

## Variant delivery

For IMT060/IMT070 variants, start from `iter-4/params.json`, replace only the needed values, then run:

```powershell
$env:PYTHONUTF8='1'
python build_template.py iter-imt060/output.docx --params iter-imt060/params.json
python C:/Users/iamdo/.claude/skills/docx/scripts/office/validate.py iter-imt060/output.docx
```

Use plain text substitution in `params.json`; do not edit XML by hand unless layout structure changes.
