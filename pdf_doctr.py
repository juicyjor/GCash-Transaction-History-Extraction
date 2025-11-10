from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import pandas as pd
import re
import os
import getpass

pdf_path = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\enc-09176061480_1750602194.pdf'
csv_path = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\output_structured.csv'

pdf_password = os.environ.get('GCASH_PDF_PASSWORD')
if not pdf_password:
    try:
        pdf_password = getpass.getpass("Enter PDF password: ")
    except Exception:
        pdf_password = None
if not pdf_password:
    raise RuntimeError("PDF password not provided. Set GCASH_PDF_PASSWORD environment variable or run interactively to enter password.")

doc = DocumentFile.from_pdf(pdf_path, password=pdf_password)
model = ocr_predictor(pretrained=True)
result = model(doc)

header = ['Date and Time', 'Description', 'Reference No.', 'Debit', 'Credit', 'Balance']

REFNO_PATTERN = re.compile(r"\b\d{13}\b")
AMOUNT_PATTERN = re.compile(r"[\d,.]+")

def parse_transaction(row):
    if not row:
        return ['', '', '', '', '', '']
    joined = ' '.join(row)
    # Date and time (first match)
    date_time_match = re.match(r'(20\d{2}-\d{2}-\d{2}\s*\d{1,2}:?\d{2}\s*[AP]M?)', joined)
    if date_time_match:
        date_time = date_time_match.group(1).strip()
        rest = joined[date_time_match.end():].strip()
    else:
        # fallback: just take the first 16-20 chars as date/time
        date_time = joined[:19].strip()
        rest = joined[19:].strip()
    # Find 13-digit reference number
    ref_match = REFNO_PATTERN.search(rest)
    if ref_match:
        ref = ref_match.group(0)
        before_ref = rest[:ref_match.start()].strip()
        after_ref = rest[ref_match.end():].strip()
    else:
        ref = ''
        before_ref = rest
        after_ref = ''
    desc = before_ref
    # Find all amounts (debit, credit, balance) from after_ref
    amounts = AMOUNT_PATTERN.findall(after_ref)
    debit, credit, balance = '', '', ''
    if len(amounts) >= 3:
        debit, credit, balance = amounts[-3:]
    elif len(amounts) == 2:
        debit, credit = amounts
    elif len(amounts) == 1:
        debit = amounts[0]
    # Fix common OCR spelling errors
    desc = desc.replace('Paymentt', 'Payment').replace('Depositt', 'Deposit').replace('Referencel', 'Reference').replace('t0-', 'to ').replace('tol', 'to ').replace('t009', 'to 09').replace('t0', 'to ').replace('t ', 'to ').replace('withl', 'with').replace('witha', 'with').replace('accounte', 'account').replace('endingi', 'ending').replace('Sent GCasht', 'Sent GCash').replace('GLoan', 'GLoan').replace('GGives', 'GGives').replace('GCreditI', 'GCredit').replace('FIS VISAI', 'FIS VISA').replace('FISE BNF', 'FIS BNF').replace('Fucente', 'Fuentec').replace('Buy LoadT', 'Buy Load').replace('Globe Telecom One Click', 'Globe Telecom One Click')
    return [date_time, desc, ref, debit, credit, balance]

lines = []
for page in result.pages:
    for block in page.blocks:
        for line in block.lines:
            line_text = ' '.join([word.value for word in line.words])
            lines.append(line_text)

transactions = []
row = []
for line in lines:
    if any(x in line for x in ['ENDINGI BALANCE', 'Totall Debit', 'Total Credit', 'STARTINGI BALANCE']):
        continue
    if re.match(r'20\d{2}-\d{2}-\d{2}', line) or re.match(r'20\d{2}-\d{2}-\d{2}', line.replace(' ', '')):
        if row:
            transactions.append(parse_transaction(row))
        row = [line]
    else:
        row.append(line)
if row:
    transactions.append(parse_transaction(row))

final_df = pd.DataFrame(transactions, columns=header)
final_df.to_csv(csv_path, index=False)
print(f"Structured CSV saved to {csv_path}")
