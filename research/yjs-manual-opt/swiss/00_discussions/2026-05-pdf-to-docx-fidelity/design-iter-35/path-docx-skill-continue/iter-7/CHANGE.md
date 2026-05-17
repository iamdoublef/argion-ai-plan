# iter-7: Add autoSpaceLikeWord95 + doNotUseHTMLParagraphAutoSpacing to compat

Word 95 didn't auto-space between CJK and ASCII chars. `<w:autoSpaceLikeWord95/>`
tells renderers to disable this behavior. Also added `doNotUseHTMLParagraphAutoSpacing`
which is a related compat that should reduce extra spacing.

Both are valid children of <w:compat>. Should be Word-safe.
