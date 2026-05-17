# iter-4: Change settings.xml themeFontLang eastAsia from ja-JP to zh-CN

Baseline has `<w:themeFontLang w:val="en-US" w:eastAsia="ja-JP"/>`. The eastAsia
is set to Japanese which causes LibreOffice (and possibly Word) to apply Japanese
typography rules (kinsoku, char-shaping) on Chinese text.

Change to `zh-CN` so renderers use Chinese rules, which is the actual content.
This is at settings.xml level — should not violate validate.py and Word will
read it fine.
