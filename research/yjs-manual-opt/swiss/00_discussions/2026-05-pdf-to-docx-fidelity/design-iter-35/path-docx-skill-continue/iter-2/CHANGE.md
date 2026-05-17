# iter-2: Set w:docGrid type="default" on all 15 sections

Default OOXML docGrid w/o `type` attr can be interpreted as snap-to-chars by some
renderers (causing CJK chars to align to a grid), but Word treats omitted type
as "default" (no grid). Adding `w:type="default"` explicitly to all 15 sections
should give LibreOffice the same behavior as Word — no character snap.

This may reduce horizontal/vertical drift in CJK-dense pages (3/9/11/14).
