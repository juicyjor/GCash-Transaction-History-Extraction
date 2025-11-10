import re
import csv

INPUT_FILE = r"d:\\Downloads\\GCash-Transaction-History-Extraction-2.0.0\\text.txt"
OUTPUT_FILE = r"d:\\Downloads\\GCash-Transaction-History-Extraction-2.0.0\\final_output.csv"

# Regex to match a transaction line
# Date: YYYY-MM-DD, Time: HH:MM AM/PM, then description (multi-word), then reference (all digits or alphanum), then debit/credit/balance (float)
TRANSACTION_REGEX = re.compile(r"""
    ^(\d{4}-\d{2}-\d{2})\s+            # Date
    (\d{2}:\d{2}\s+[AP]M)\s+           # Time
    (.+?)\s+                             # Description (non-greedy)
    ([A-Z0-9-]+)\s+                      # Reference No. (alphanum, may have dash)
    ([\d,.]+)?\s*                       # Debit (optional, may be empty)
    ([\d,.]+)?\s*                       # Credit (optional, may be empty)
    ([\d,.]+)                            # Balance (always present)
    $""", re.VERBOSE)

# Lines to skip (summary/footer)
SKIP_PREFIXES = [
    "Date and Time", "STARTING BALANCE", "ENDING BALANCE", "Total Debit", "Total Credit"
]

def is_summary_line(line):
    return any(line.strip().startswith(prefix) for prefix in SKIP_PREFIXES)

def parse_line(line):
    match = TRANSACTION_REGEX.match(line)
    if not match:
        return None
    date, time, desc, ref, debit, credit, balance = match.groups()
    # If both debit and credit are present, assign accordingly
    # If only one is present, determine if it's debit or credit by position
    # (In your sample, usually only one of debit/credit is filled)
    if debit and credit:
        pass  # Both present
    elif debit and not credit:
        # If the next field is balance, then this is debit
        credit = ''
    elif credit and not debit:
        # If the next field is balance, then this is credit
        debit = ''
    else:
        debit = ''
        credit = ''
    return [date + ' ' + time, desc.strip(), ref, debit, credit, balance]

def main():
    with open(INPUT_FILE, 'r', encoding='utf-8') as infile, \
         open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Date and Time", "Description", "Reference No.", "Debit", "Credit", "Balance"])
        for line in infile:
            line = line.strip()
            if not line or is_summary_line(line):
                continue
            parsed = parse_line(line)
            if parsed:
                writer.writerow(parsed)

if __name__ == "__main__":
    main()
