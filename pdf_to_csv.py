import os
import getpass
import pdfplumber
import pandas as pd

# Update these paths if needed
pdf_path = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\enc-09176061480_1750602194.pdf'
csv_path = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\output.csv'

pdf_password = os.environ.get('GCASH_PDF_PASSWORD')
if not pdf_password:
    try:
        pdf_password = getpass.getpass("Enter PDF password: ")
    except Exception:
        pdf_password = None
if not pdf_password:
    raise RuntimeError("PDF password not provided. Set GCASH_PDF_PASSWORD environment variable or run interactively to enter password.")

with pdfplumber.open(pdf_path, password=pdf_password) as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            all_tables.append(df)
    if all_tables:
        result = pd.concat(all_tables, ignore_index=True)
        result.to_csv(csv_path, index=False)
        print(f"CSV saved to {csv_path}")
    else:
        print("No tables found in the PDF.")
