import os
import getpass
import fitz  # PyMuPDF
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

doc = fitz.open(pdf_path)
if doc.needs_pass:
    if not doc.authenticate(pdf_password):
        raise RuntimeError("Incorrect PDF password!")

all_text = []
for page in doc:
    text = page.get_text()
    all_text.append(text)

# Now, you need to parse all_text to extract rows and columns.
# This step is highly dependent on your PDF's formatting.
# Example: Split by lines, then by whitespace or delimiter.
lines = []
for page_text in all_text:
    for line in page_text.split('\n'):
        if line.strip():
            lines.append(line.split())  # Adjust split logic as needed

# Save to CSV
df = pd.DataFrame(lines)
df.to_csv(csv_path, index=False, header=False)
print(f"CSV saved to {csv_path}")
