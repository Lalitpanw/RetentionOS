import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

st.set_page_config(page_title="RetentionOS", layout="centered")

st.title("📊 RetentionOS – A User Turning Point")
st.markdown("_Upload your user data → Predict churn → Auto-nudge users._")

# --- Step 1: Upload file ---
uploaded_file = st.file_uploader("📥 Upload your CSV file", type=["csv", "xlsx"])

if uploaded_file:
    # --- Step 2: Load data ---
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    st.success(f"File uploaded: {uploaded_file.name}")
    st.markdown(f"📄 **Columns detected**: `{', '.join(df.columns)}`")

    # --- Step 3: Auto-map columns ---
    expected_fields = {
        'last_active_days': ['last_seen', 'last_active', 'inactive_days'],
        'total_sessions': ['sessions', 'login_count', 'visits'],
        'orders': ['orders', 'purchases', 'transactions'],
        'revenue': ['amount_spent', 'order_value', 'lifetime_value'],
    }

    def auto_map_columns(df):
        mapping = {}
        for key, possible_names in expected_fields.items():
            for col in df.columns:
                for option in possible_names:
                    if fuzz.partial_ratio(col.lower(), option.lower()) > 80:
                        mapping[key] = col
                        break
        return mapping

    mapping = auto_map_columns(df)

    # --- Step 4: Manual fallback ---
    st.markdown("### 🔍 Column Mapping")
    for key in expected_fields:
        if key not in mapping:
            mapping[key] = st.selectbox(f"Select column for **{key}**", df.columns)
        st.markdown(f"✅ `{key}` → `{mapping[key]}`")

    # --- Step 5: Standardize ---
    df = df.rename(columns={mapping[k]: k for k in mapping})

    # --- Step 6: Scoring logic (simple rules) ---
    def score_user(row):
        score = 0
        if row['last_active_days'] > 14:
            score += 1
        if row['orders'] < 1:
            score += 1
        if row['total_sessions'] < 3:
            score += 1
        return score

    df['churn_score'] = df.apply(score_user, axis=1)

    def label_risk(score):
        if score >= 2:
            return "🔴 High"
        elif score == 1:
            return "🟠 Medium"
        else:
            return "🟢 Low"

    df['churn_risk'] = df['churn_score'].apply(label_risk)

    # --- Step 7: Display Results ---
    st.markdown("### 📊 Churn Risk Segments")
    st.dataframe(df[['churn_risk', 'last_active_days', 'orders', 'total_sessions']])

    # --- Optional: Future Add-ons ---
    # - Nudge message generator
    # - Export filtered segments
    # - Twilio API integration
else:
    st.info("👆 Upload a CSV or Excel file to begin.")
