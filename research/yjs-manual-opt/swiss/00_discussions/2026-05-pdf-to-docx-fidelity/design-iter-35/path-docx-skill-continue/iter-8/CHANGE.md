# iter-8: Add noPunctuationKerning + strictFirstAndLastChars to settings.xml

`<w:noPunctuationKerning/>` disables Word's auto-kerning around CJK punctuation.
`<w:strictFirstAndLastChars/>` uses strict (vs custom) CJK line-break first/last
char rules — these are the standard CJK punctuation forbidden at line start/end.

Both elements appear in OOXML CT_Settings spec. Properly placed between
defaultTabStop and characterSpacingControl. Should be Word-safe.
