import pdfplumber
import csv
import re
import sys

def extract_transactions_from_text(pdf_path, output_csv):
    all_lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            all_lines.extend(lines)

    # ANZ transactions start after "Statement period" and look like:
    # 27 Mar  THE WAREHOUSE     35.98                          3,272.52
    pattern = re.compile(r"(\d{1,2} \w{3})\s+(.+?)\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})?$")
    transactions = []

    for line in all_lines:
        match = pattern.search(line)
        if match:
            date, description, amount, _ = match.groups()
            amount = amount.replace(",", "")
            # Guess if it's withdrawal or deposit based on nearby labels
            is_withdrawal = "Withdrawals" in line or float(amount) < 1000
            amount = -float(amount) if is_withdrawal else float(amount)
            transactions.append([date, description.strip(), amount])

    if not transactions:
        print("❌ No matching transaction lines found.")
        return

    with open(output_csv, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["date", "description", "amount"])
        writer.writerows(transactions)

    print(f"✅ CSV saved to {output_csv} with {len(transactions)} transactions.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_csv.py <input.pdf> <output.csv>")
        sys.exit(1)

    extract_transactions_from_text(sys.argv[1], sys.argv[2])
