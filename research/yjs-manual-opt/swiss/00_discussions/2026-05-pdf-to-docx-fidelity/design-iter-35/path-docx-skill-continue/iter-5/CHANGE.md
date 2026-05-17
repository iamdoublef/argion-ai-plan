# iter-5: Per-paragraph autoSpaceDE/DN=0 on all 306 body pPr w/ spacing

W28 globally tried `autoSpaceDE/DN` in settings.xml and corrupted Word file.
This iter applies it ONLY at the paragraph level (proper OOXML position:
after overflowPunct/topLinePunct, before bidi/snapToGrid/spacing).

Should disable LO's auto-spacing between CJK and ASCII (e.g.
'87-105 号' → '87-105号'), which is the dominant pixel diff vs target.

Sites: 306 (every <w:spacing w:after=...> inside pPr).
