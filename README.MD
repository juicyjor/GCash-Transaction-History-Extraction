# GCash Transaction History — PDF → CSV

This repository contains scripts to extract and convert GCash Transaction History PDF exports into structured CSV files. The project originally contains an R extractor (using tabulizer) and several Python helper scripts for alternate extraction/analysis paths.

This README documents both the original R workflow and the Python-side utilities included in this repository so you can pick the approach that fits your environment.

## Contents

- `GCash_Transaction-History_Extraction_Public.R` — original R script that uses `tabulizer`/`rJava` to extract tables and produce CSVs.
- `pdf_*.py` (several) — Python utilities for analyzing PDFs, running OCR, and converting to CSV (`pdf_analyze.py`, `pdf_doctr.py`, `pdf_ocr.py`, `pdf_pdftables.py`, `pdf_pymupdf.py`, `pdf_tabula.py`, `pdf_to_csv.py`).
- `space_delimited_to_structured_csv.py`, `structure_csv.py` — scripts to clean/structure space-delimited outputs.
- `text.txt` — example or scratch text used during development.

## Approaches

Two main approaches are supported in this repo:

1. R-based extraction (tabulizer + rJava) — works well when the PDF has clear table regions and you can run R with a working Java/JDK installation.
2. Python utilities (OCR + PDF parsing) — helpful when tabular extraction fails and you need to use OCR (Tesseract) or alternative PDF parsers.

Choose the approach that matches your environment and the PDF quality.

## Prerequisites

Common requirements across approaches:

- Java JDK (required if you plan to use `tabulizer` in R or `tabula`/`tabula-py` in Python).
- A reasonably recent Python 3 (3.8+) if you use the Python scripts.

Additional (R):

- R (>= 3.5) and the following packages: `rJava`, `tabulizer`, `tidyverse`, `data.table`, `lubridate`.

Install in R (example):

```r
install.packages('rJava')
install.packages('tabulizer')
install.packages('tidyverse')
install.packages('data.table')
install.packages('lubridate')
```

Additional (Python, optional depending on script):

- Common useful packages: `pandas`, `pdfplumber`, `tabula-py`, `camelot`, `pytesseract`, `python-mupdf` (PyMuPDF / fitz), `doctr` (if used). Install only what you need.
- Tesseract OCR (system binary) if you plan to use OCR (`pytesseract` wraps it).

Example pip installs (adjust to needs):

```powershell
# Use your Python venv or global python as appropriate
python -m pip install pandas pdfplumber tabula-py camelot-py[cv] pytesseract PyMuPDF
```

Note: `tabula-py` requires Java and the `tabula` jar; `camelot` may require a system Ghostscript and OpenCV. Adjust installs per your OS.

## Quick start — R (original script)

1. Open `GCash_Transaction-History_Extraction_Public.R` in R/RStudio.
2. Set your working directory and update the call near the end of the file with the input file, password, and page count. Example (as in the original script):

```r
setwd("/path/to/pdf-and-output")
ExtractTxnHistory2CSV("transaction_history.pdf", "surname_last-4-digits-of-mobtel", 2)
```

3. Run the script in RStudio or via `Rscript` and it will attempt to extract table data using `tabulizer` and save CSV(s).

## Quick start — Python utilities

The Python scripts are small helpers; usage will vary by script. A recommended quick workflow:

1. Inspect the PDF layout with `pdf_analyze.py` (helps identify pages/regions).
2. Try `pdf_to_csv.py` or `pdf_pdftables.py` to convert obvious tables to CSV.
3. If table extraction fails or text is rasterized, run OCR with `pdf_ocr.py` (requires system Tesseract) and then use `space_delimited_to_structured_csv.py` / `structure_csv.py` to clean up output.

Most scripts accept a PDF path and an output path or are easy to adapt by editing the top of the script — check the top-level comments in each `pdf_*.py` file for usage examples or `-h`/`--help` flags if implemented.

Example (generic):

```powershell
# inspect
python .\pdf_analyze.py .\transaction_history.pdf

# attempt a direct conversion
python .\pdf_to_csv.py .\transaction_history.pdf .\transaction_history.csv

# if needed, run OCR (creates text/pdf with OCR layer)
python .\pdf_ocr.py .\transaction_history.pdf .\transaction_history_ocr.pdf
```

If a script does not expose a CLI, open the file and adjust the input/output variables near the top — the Python utilities are intentionally small and script-like.

## Files of interest (short summary)

- `GCash_Transaction-History_Extraction_Public.R` — R extractor using `tabulizer` (main original tool).
- `pdf_to_csv.py` — entry-point-style script to attempt PDF-to-CSV conversion (see script header for exact usage).
- `pdf_ocr.py` — OCR helper using Tesseract (if present).
- `space_delimited_to_structured_csv.py`, `structure_csv.py` — helpers to parse/normalize space-delimited table output into structured CSV columns.

## Notes & assumptions

- This README expands the original R-focused instructions to include the Python scripts present in the repository. I did not modify any code; the Python scripts may have different CLI expectations — open the script header or run `python script.py -h` to confirm exact flags.
- If you want, I can add a `requirements.txt` or minimal usage examples for each Python script after inspecting their headers.

## Contributing

If you add a script or enhance extraction, please include a short usage example in the script header and consider adding the dependency list to `requirements.txt`.

## License

This project is licensed under the MIT License — see `LICENSE.txt` for details.

---

If you'd like, I can:

- Add a `requirements.txt` with the minimal Python dependencies used here and small per-script usage examples.
- Create a short example run that demonstrates converting one of the shipped PDFs to CSV.

Tell me which of those you'd like next and I'll proceed.
