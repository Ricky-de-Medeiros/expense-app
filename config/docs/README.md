# 💼 Business Expense Extractor

A local Python application that parses bank statement CSV files, identifies business-related transactions, calculates business usage percentages, and generates a clean report for use in tax declarations — ready for Google Sheets.

---

## 🚀 Features

- Parse bank statements in CSV format  
- Identify and tag business expenses  
- Calculate % of business usage  
- Export results as a formatted CSV for Google Sheets  
- Lightweight CLI for local use

---

## 📦 Installation

Clone the repo:

```bash
git clone https://bitbucket.org/yourworkspace/business-expense-extractor.git
cd business-expense-extractor
```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🛠 Usage

```bash
python main.py --input your_bank_statement.csv --output report.csv
```

Optional flags:

- `--category-rules rules.json` – Define business logic per merchant or keyword  
- `--interactive` – Review and tag expenses manually before export

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📁 Project Structure

```
business-expense-extractor/
├── main.py
├── report_generator.py
├── transaction_parser.py
├── rules/
│   └── sample_rules.json
├── data/
│   └── sample_statement.csv
├── tests/
│   └── test_parser.py
├── README.md
└── requirements.txt
```

---

## 📌 Notes

- Compatible with NZ/AU bank CSV exports  
- Extendable for multiple bank formats  
- Runs entirely offline

---

## 📃 License

MIT – see `LICENSE` file.

---

# 📊 Project Overview

## Objective

To simplify tax reporting for sole traders and small business owners by providing a lightweight, local Python tool to extract business-related expenses from bank statement CSVs and produce structured reports.

---

## Use Case

As a self-employed individual, you may find it tedious to manually identify business-related transactions from personal bank statements. This tool automates that process with optional manual review and tagging.

---

## Key Modules

- `transaction_parser.py`: Reads and structures raw CSV data.  
- `report_generator.py`: Applies logic for business usage, categorizes expenses, and generates a final CSV.  
- `rules/`: Directory containing JSON-based rules for common expense categories.  
- `tests/`: Pytest-based unit tests.

---

## Development Plan

### Phase 1: Foundation  
✅ CLI app  
✅ CSV parsing  
✅ Simple tagging logic  
✅ Google Sheets-ready export

### Phase 2: Enrichment  
🔜 Category rule system via JSON  
🔜 Business usage percentage calculation  
🔜 Interactive mode for manual tagging

### Phase 3: Automation & UI  
🔜 Dashboard / web frontend  
🔜 AI-assisted tagging  
🔜 Auto sync with bank APIs (future)

---

## Tech Stack

- Python 3.10+  
- Pandas  
- CLI (argparse / typer)  
- Pytest  
- Bitbucket for repo & version control

---

## Contributing

1. Fork it  
2. Create your feature branch (`git checkout -b feature/foo`)  
3. Commit your changes (`git commit -am 'Add new feature'`)  
4. Push to the branch (`git push origin feature/foo`)  
5. Create a new Pull Request
