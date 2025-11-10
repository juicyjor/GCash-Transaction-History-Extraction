import pdftables_api

pdf_path = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\xenc-09176061480_1750602194.pdf'
csv_path = r'd:\Downloads\GCash-Transaction-History-Extraction-2.0.0\output.csv'

# Replace 'your-api-key' with your actual PDFTables API key
tables_client = pdftables_api.Client('xuod9unawxh4')
tables_client.csv(pdf_path, csv_path)
print(f"CSV saved to {csv_path}")
