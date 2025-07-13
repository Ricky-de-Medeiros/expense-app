import argparse
import json
from transaction_parser import load_transactions, tag_business_expenses
from report_generator import calculate_business_percentages, export_report

def main():
    parser = argparse.ArgumentParser(description="Extract business expenses from bank statement CSV")
    parser.add_argument("--input", required=True, help="Path to bank statement CSV file")
    parser.add_argument("--output", required=True, help="Path to output report CSV file")
    parser.add_argument("--category-rules", help="Optional JSON file with tagging rules")
    args = parser.parse_args()

    rules = {}
    if args.category_rules:
        with open(args.category_rules, "r") as f:
            rules = json.load(f)

    df = load_transactions(args.input)
    df = tag_business_expenses(df, rules)
    df = calculate_business_percentages(df)
    export_report(df, args.output)
    print(f"✅ Report saved to {args.output}")

if __name__ == "__main__":
    main()
