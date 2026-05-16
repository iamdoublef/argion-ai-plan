# Cross Review

## Winner: B1 iter-03

## Why:
- Best visual score of the four reviewed candidates: 13.59 overall mean diff, 15/15 pages.
- Direct DOCX unpack confirms editable Word text: `<w:t>` present, zero `<wp:txbx>` / `<v:textbox>` / `<w:txbxContent>`.
- Most balanced customer choice: close enough to the PDF while staying a normal editable Word document.
- Better page rhythm than B2/A1/A2 on structure, operation, spec, and warranty pages; fewer obvious reflow penalties.
- Tables, bullets, images, and page breaks are usable for local Word edits without requiring a PDF-like fixed layout.

## Runner-up: B2 iter-03

B2 is also fully editable and has strong content coverage, but its larger typography/spacing creates more visible drift, especially safety and warranty pages. Max page diff is higher at 34.10.

## Suggested improvements:
- Remove the duplicate chapter reference line in headers and tighten header/footer sizing to match the PDF baseline.
- Restore stronger table styling and tune figure scale/placement, especially product structure, specs, and warranty pages.

## Risk / caveats:
- All four candidates unpacked with real `<w:t>` text and no Word/VML textboxes.
- A2 iter-02 has 16 pages versus the 15-page target, so it is weaker for customer delivery despite passing automated checks.
- A1 iter-02 and A2 iter-02 did not have complete prebuilt `side_by_side` folders available; missing pages were reviewed from reconstructed target/candidate PNG comparisons.
