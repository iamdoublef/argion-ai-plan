"""
Use MS Word COM (via docx2pdf) to convert DOCX → PDF.
This should give higher fidelity than LibreOffice headless on Windows.
"""
import sys
from pathlib import Path
from docx2pdf import convert

def main(docx_in: str, pdf_out: str):
    docx_p = Path(docx_in).resolve()
    pdf_p = Path(pdf_out).resolve()
    pdf_p.parent.mkdir(parents=True, exist_ok=True)
    convert(str(docx_p), str(pdf_p))
    print(f"OK: {docx_p} -> {pdf_p}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
