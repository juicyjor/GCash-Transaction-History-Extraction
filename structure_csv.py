import pandas as pd
import re

input_csv = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\output.csv'
output_csv = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\output_structured.csv'

df = pd.read_csv(input_csv)

# Find the header start
header_start_idx = df[df.iloc[:,0].str.strip().str.lower() == 'dates and time'].index
if len(header_start_idx) == 0:
    raise Exception("Header start row not found!")
header_start_idx = header_start_idx[0]

# Get header lines
header_lines = df.iloc[header_start_idx:header_start_idx+6, 0].tolist()
header = [h.replace('!', '').replace('l', 'l').replace('I', 'I').replace(' ', ' ').strip() for h in header_lines]

# Data starts after header
data_rows = df.iloc[header_start_idx+6:, 0]

# Prepare for parsing
structured = []
row = []
for line in data_rows:
    if any(x in line for x in ['ENDINGI BALANCE', 'Totall Debit', 'Total Credit', 'STARTINGI BALANCE']):
        continue
    # Heuristic: a new transaction starts with a date (2025-)
    if re.match(r'20\d{2}-\d{2}-\d{2}', line) or re.match(r'20\d{2}-\d{2}-\d{2}', line.replace(' ', '')):
        if row:
            structured.append(row)
        row = [line]
    else:
        row.append(line)
if row:
    structured.append(row)

# Flatten and align rows to 6 columns
final_rows = []
for r in structured:
    while len(r) < 6:
        r.append('')
    final_rows.append(r[:6])

final_df = pd.DataFrame(final_rows, columns=header)
final_df.to_csv(output_csv, index=False)
print(f"Structured CSV saved to {output_csv}")
