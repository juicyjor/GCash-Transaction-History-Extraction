import os
import getpass
import pytesseract
from pdf2image import convert_from_path
import pandas as pd

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

# Pass the password to convert_from_path
images = convert_from_path(pdf_path, userpw=pdf_password)
all_text = []
for img in images:
    text = pytesseract.image_to_string(img)
    all_text.append(text)

# Parse all_text as in the PyMuPDF example above
lines = []
for page_text in all_text:
    for line in page_text.split('\n'):
        if line.strip():
            lines.append(line.split())  # Adjust split logic as needed

df = pd.DataFrame(lines)
df.to_csv(csv_path, index=False, header=False)
print(f"CSV saved to {csv_path}")
