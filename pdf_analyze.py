import os
import getpass
import pdfplumber
import pandas as pd

pdf_path = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\enc-09176061480_1750602194.pdf'
csv_path = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\output.csv'

all_tables = []
total_tables = 0
pdf_password = os.environ.get('GCASH_PDF_PASSWORD')
if not pdf_password:
    try:
        pdf_password = getpass.getpass("Enter PDF password: ")
    except Exception:
        pdf_password = None
if not pdf_password:
    raise RuntimeError("PDF password not provided. Set GCASH_PDF_PASSWORD environment variable or run interactively to enter password.")

with pdfplumber.open(pdf_path, password=pdf_password) as pdf:
    print(f"PDF has {len(pdf.pages)} pages.")
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        print(f"\n--- Page {i+1} ---")
        print(f"Found {len(tables)} tables on this page.")
        for t_idx, table in enumerate(tables):
            if table and len(table) > 1:
                headers = table[0]
                # Save all tables, even with non-unique headers
                df = pd.DataFrame(table[1:], columns=headers)
                all_tables.append(df)
                print(f"Table {t_idx+1} captured.")
                total_tables += 1
print(f"\nTotal tables in PDF: {total_tables}")
if all_tables:
    result = pd.concat(all_tables, ignore_index=True)
    result.to_csv(csv_path, index=False)
    print(f"CSV saved to {csv_path}")
else:
    print("No tables found in the PDF.")
