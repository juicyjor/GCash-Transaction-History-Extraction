import os
import getpass
import tabula
import pandas as pd

pdf_path = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\enc-09176061480_1750602194.pdf'
csv_path = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\output.csv'

# Extract all tables from PDF into a list of DataFrames
pdf_password = os.environ.get('GCASH_PDF_PASSWORD')
if not pdf_password:
    try:
        pdf_password = getpass.getpass("Enter PDF password: ")
    except Exception:
        pdf_password = None
if not pdf_password:
    raise RuntimeError("PDF password not provided. Set GCASH_PDF_PASSWORD environment variable or run interactively to enter password.")

dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True, password=pdf_password)

if dfs:
    result = pd.concat(dfs, ignore_index=True)
    result.to_csv(csv_path, index=False)
    print(f"CSV saved to {csv_path}")
else:
    print("No tables found in the PDF.")
