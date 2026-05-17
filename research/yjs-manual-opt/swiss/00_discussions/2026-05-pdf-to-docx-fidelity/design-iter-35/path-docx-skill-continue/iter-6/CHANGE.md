# iter-6: Remove <w:useFELayout/> from settings.xml compat block

`<w:useFELayout/>` enables Far East (Japanese/Chinese) layout compatibility mode,
which controls many CJK-specific behaviors including the CJK-ASCII auto-spacing
that's causing '105号' to render as '105 号'.

Removing it lets the renderer use modern (post-Word 95) layout rules.
This is safe — it's an opt-in compat setting, not a required element.
