import streamlit as st
import pandas as pd
import json
import re
from datetime import datetime
import plotly.express as px
import os
import openai
import pdfplumber

st.set_page_config(page_title="Business Expense Dashboard", layout="wide")

YEAR = 2025
RULES_PATH = "rules/interactive_rules.json"
SETTINGS_PATH = "rules/settings.json"
CATEGORY_LIST = sorted([
    "Advertising", "Equipment", "Fuel", "Home Office Equipment", "Insurance",
    "N/A", "Office Supplies", "Phone", "Power", "Rent", "Software",
    "Sub-contractors", "Subscription", "Transport", "Uncategorized", "Water"
])

# Ensure rules folder exists
os.makedirs("rules", exist_ok=True)

# Load saved business settings
if os.path.exists(SETTINGS_PATH):
    with open(SETTINGS_PATH) as f:
        settings = json.load(f)
        default_biz_type = settings.get("business_type", "")
        additional_context = settings.get("additional_context", "")
else:
    default_biz_type = ""
    additional_context = ""

# Business profile form
with st.expander("💼 Business Profile"):
    with st.form(key="biz_profile_form"):
        business_type = st.text_input(
            "What kind of business do you run?",
            value=default_biz_type,
            help="e.g., consulting, freelancing, ecommerce"
        )
        additional_context = st.text_area(
            "Anything else that might help categorize your expenses?",
            value=additional_context,
            help="e.g., I work from home. I often buy tools and materials for sub-contractors."
        )
        submitted = st.form_submit_button("💾 Save Business Profile")
        if submitted:
            with open(SETTINGS_PATH, "w") as f:
                json.dump({"business_type": business_type, "additional_context": additional_context}, f)
            st.success("✅ Business profile information saved.")

# Utility functions
def convert_date(text_date: str) -> str:
    return datetime.strptime(f"{text_date} {YEAR}", "%d %b %Y").strftime("%Y-%m-%d")

def extract_from_pdf(uploaded_pdf):
    all_lines = []
    with pdfplumber.open(uploaded_pdf) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            all_lines.extend(lines)

    pattern = re.compile(r"^(\d{1,2} \w{3})\s+(.+?)\s+((?:[\d,]+\.\d{2})?)\s+((?:[\d,]+\.\d{2})?)$")
    transactions = []
    for line in all_lines:
        match = pattern.match(line)
        if match:
            raw_date, description, withdrawal, deposit = match.groups()
            date = convert_date(raw_date)
            description = description.strip()
            if withdrawal:
                amount = -float(withdrawal.replace(",", ""))
            elif deposit:
                amount = float(deposit.replace(",", ""))
            else:
                continue
            transactions.append([date, description, amount])

    df = pd.DataFrame(transactions, columns=["date", "description", "amount"])
    return df

def load_saved_rules():
    if os.path.exists(RULES_PATH):
        with open(RULES_PATH, "r") as f:
            try:
                rules = json.load(f)
                return [r for r in rules if isinstance(r, dict) and "vendor" in r]
            except Exception:
                return []
    return []

def get_rule_for_vendor(vendor, rules):
    for rule in rules:
        if rule.get("vendor", "").lower()[:8] == vendor.lower()[:8]:
            return rule
    return None

def suggest_category_ai(vendor):
    prompt = f"The user runs a {business_type} business. {additional_context}\n\n"
    prompt += f"Suggest the most likely expense category for the vendor: '{vendor}'. "
    prompt += f"Choose from: {', '.join(CATEGORY_LIST)}. Reply with only the category."
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        suggestion = response.choices[0].message.content.strip()
        return suggestion if suggestion in CATEGORY_LIST else "Uncategorized"
    except:
        return "Uncategorized"

# App starts
st.title("💼 Business Expense Dashboard")
uploaded = st.file_uploader("📤 Upload your bank statement (CSV or PDF)", type=["csv", "pdf"])

saved_rules = load_saved_rules()
df = pd.DataFrame()

if uploaded:
    if uploaded.name.endswith(".pdf"):
        with open("temp_uploaded.pdf", "wb") as f:
            f.write(uploaded.read())
        df = extract_from_pdf("temp_uploaded.pdf")
    else:
        df = pd.read_csv(uploaded)

if "rules_applied" not in st.session_state:
    st.session_state["rules_applied"] = False

if not df.empty:
    with st.expander("🧠 Help us categorize your expenses", expanded=not st.session_state["rules_applied"]):

        df["category"] = ""
        df["is_business"] = False
        df["business_usage_pct"] = 0

        user_rules = []
        seen_prefixes = set()
        unique_vendors = df["description"].dropna().unique()

        accept_all_ai = st.checkbox("🔮 Accept all AI suggestions for uncategorized vendors")

        for vendor in unique_vendors:
            prefix = vendor[:8].lower()
            if prefix in seen_prefixes:
                continue
            seen_prefixes.add(prefix)

            existing_rule = get_rule_for_vendor(vendor, saved_rules)
            ai_suggestion = suggest_category_ai(vendor) if not existing_rule else None
            ai_note = f"💡 AI Suggestion: {ai_suggestion}" if ai_suggestion else ""

            # Updated color logic
            bg_color = (
                "#009900" if existing_rule else
                "#999900" if ai_suggestion else
                "#CC0000"
            )

            with st.container():
                st.markdown(f"""
                    <div style='background-color:{bg_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <strong>Vendor:</strong> {vendor}
                    </div>
                """, unsafe_allow_html=True)

                is_business = st.radio(
                    f"Is '{vendor}' a business expense?",
                    ["No", "Yes"],
                    index=1 if existing_rule and existing_rule["is_business"] else 0,
                    key=f"biz-{vendor}"
                )

                category_disabled = is_business == "No"
                default_cat = (
                    existing_rule["category"] if existing_rule else
                    (ai_suggestion if accept_all_ai else "Uncategorized")
                )

                category = st.selectbox(
                    f"Category for '{vendor}' ({ai_note})" if ai_note else f"Category for '{vendor}'",
                    CATEGORY_LIST,
                    index=CATEGORY_LIST.index(default_cat) if default_cat in CATEGORY_LIST else 0,
                    key=f"cat-{vendor}",
                    disabled=category_disabled
                )

                usage_pct = st.slider(
                    f"Business usage % for '{vendor}'",
                    0, 100,
                    existing_rule["usage_pct"] if existing_rule else 100,
                    key=f"pct-{vendor}"
                ) if is_business == "Yes" else 0

                user_rules.append({
                    "vendor": vendor,
                    "category": category if is_business == "Yes" else "N/A",
                    "is_business": is_business == "Yes",
                    "usage_pct": usage_pct
                })

    if st.button("✅ Apply Rules and Show Dashboard"):
        st.session_state["rules_applied"] = True

        for rule in user_rules:
            prefix = rule["vendor"][:8].lower()
            mask = df["description"].str.lower().str.startswith(prefix)
            df.loc[mask, "category"] = rule["category"]
            df.loc[mask, "is_business"] = rule["is_business"]
            df.loc[mask, "business_usage_pct"] = rule["usage_pct"]

        with open(RULES_PATH, "w") as f:
            json.dump(user_rules, f, indent=2)

        st.success("✔ Categorization complete! View your dashboard below.")

        df = df[df["is_business"] == True]

        tab1, tab2, tab3 = st.tabs(["📄 Table", "📊 Chart", "📈 Summary"])

        with tab1:
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Business Transactions CSV",
                data=csv,
                file_name="business_expenses.csv",
                mime="text/csv"
            )

        with tab2:
            st.subheader("Expense Breakdown by Category")
            pie_data = df.groupby("category")["amount"].apply(lambda x: -x.sum()).reset_index()
            fig = px.pie(pie_data, values="amount", names="category", title="Category Breakdown")
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.subheader("Summary")
            total = df["amount"].sum()
            business_count = df.shape[0]
            business_pct = df["business_usage_pct"].mean() if not df.empty else 0
            st.markdown(f"**Total Business Transactions:** {business_count}")
            st.markdown(f"**Average Business Usage:** {business_pct:.2f}%")
            st.markdown(f"**Total Business Amount:** ${total:.2f}")

with st.expander("🛠 Rule Manager"):
    st.markdown("Review, edit, or delete your saved rules below:")

    rules_df = pd.DataFrame(saved_rules)
    edited_rules = []

    if not rules_df.empty:
        for i, rule in rules_df.iterrows():
            with st.container():
                cols = st.columns([2, 2, 2, 1, 1])

                vendor = cols[0].text_input("Vendor", value=rule["vendor"], key=f"edit-vendor-{i}")
                category = cols[1].selectbox("Category", CATEGORY_LIST, index=CATEGORY_LIST.index(rule["category"]), key=f"edit-cat-{i}")
                is_business = cols[2].selectbox("Business?", ["Yes", "No"], index=0 if rule["is_business"] else 1, key=f"edit-biz-{i}")
                usage_pct = cols[3].slider("% Usage", 0, 100, rule["usage_pct"], key=f"edit-pct-{i}")
                delete = cols[4].checkbox("🗑 Delete", key=f"del-{i}")

                if not delete:
                    edited_rules.append({
                        "vendor": vendor,
                        "category": category,
                        "is_business": is_business == "Yes",
                        "usage_pct": usage_pct
                    })

        if st.button("💾 Save Rule Changes"):
            with open(RULES_PATH, "w") as f:
                json.dump(edited_rules, f, indent=2)
            st.success("✅ Rules updated. Refresh to load changes.")
    else:
        st.info("No rules saved yet.")
