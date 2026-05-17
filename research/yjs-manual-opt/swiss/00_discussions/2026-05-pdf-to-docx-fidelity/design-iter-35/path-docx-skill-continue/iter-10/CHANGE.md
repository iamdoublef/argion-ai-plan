# iter-10: INCREASE body char spacing 5→8 on sz=14 body color runs

iter-9 tightened to 2 and got worse (target is *wider* than candidate).
Reverse direction: increase spacing 5→8 to add ~0.15pt per char (+3 twips).
For 30-char line: +90 twips (~4.5mm). Should force lines to wrap earlier,
hopefully matching target's actual wrap points.

Targeted: same 75 body rPr blocks as iter-9.
