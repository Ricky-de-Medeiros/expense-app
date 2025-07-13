import pandas as pd
import matplotlib.pyplot as plt

def generate_pie_chart(csv_file, output_image="chart.png"):
    df = pd.read_csv(csv_file)
    cat_summary = df[df["is_business"] == True].groupby("category")["amount"].sum().abs()

    if cat_summary.empty:
        print("❌ No business expenses to plot.")
        return

    plt.figure(figsize=(8, 8))
    cat_summary.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title("Business Expenses by Category")
    plt.ylabel("")  # hide y-label
    plt.tight_layout()
    plt.savefig(output_image)
    print(f"✅ Pie chart saved as {output_image}")
