import streamlit as st
from App.business_profile import BusinessProfile
from App.rule_manager import RuleManager
from App.statement_processor import StatementProcessor
from App.dashboard_renderer import DashboardRenderer
from App.rule_ui import render_rule_ui
from dotenv import load_dotenv

# Load environment variables (e.g., OpenAI API key)
load_dotenv()

st.set_page_config(page_title="Business Expense Dashboard", layout="wide")

# Initialize components
biz_profile = BusinessProfile()
rule_manager = RuleManager()
processor = StatementProcessor()
renderer = DashboardRenderer()

# Load settings
business_type = biz_profile.business_type
additional_context = biz_profile.additional_context
rules = rule_manager.load_rules()

# Initialize session state
if "rules_applied" not in st.session_state:
    st.session_state["rules_applied"] = False

# File upload
uploaded_file = st.file_uploader("📤 Upload your bank statement (CSV or PDF)", type=["csv", "pdf"])
df = processor.load_file(uploaded_file)

# Store dataframe in session
if df is not None:
    st.session_state['df'] = df
elif 'df' in st.session_state:
    df = st.session_state['df']

# Categorization step
if df is not None and not st.session_state["rules_applied"]:
    user_rules = render_rule_ui(df, rules, business_type, additional_context)
    if user_rules is not None:
        rule_manager.save_rules(user_rules)
        processor.apply_rules(df, user_rules)
        st.session_state["rules_applied"] = True
        st.rerun()

# Render dashboard
if df is not None and st.session_state["rules_applied"]:
    df = df[df["is_business"] == True]
    renderer.render(df)
