import streamlit as st
import pandas as pd
import plotly.express as px
from fuzzywuzzy import fuzz

# Page configuration
st.set_page_config(page_title="RetentionOS", layout="wide")
@@ -68,59 +69,25 @@
elif section == "Dashboard":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a file from the Home page first.")
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
        st.title("📊 Dashboard Metrics")
        df = st.session_state.df
        df = pd.read_csv(uploaded_file)

        st.metric("Total Users", len(df))
        st.metric("High Risk Users", df[df["risk_level"] == "High"].shape[0])
        st.metric("Average Churn Score", round(df["churn_score"].mean(), 2))
    st.success(f"File uploaded: {uploaded_file.name}")
    st.markdown(f"📄 **Columns detected**: `{', '.join(df.columns)}`")

        st.subheader("Churn Score Distribution")
        fig1 = px.histogram(df, x="churn_score", nbins=20, title="Churn Score Histogram")
        st.plotly_chart(fig1, use_container_width=True)
    # --- Step 3: Auto-map columns ---
    expected_fields = {
        'last_active_days': ['last_seen', 'last_active', 'inactive_days'],
        'total_sessions': ['sessions', 'login_count', 'visits'],
        'orders': ['orders', 'purchases', 'transactions'],
        'revenue': ['amount_spent', 'order_value', 'lifetime_value'],
    }

        st.subheader("Risk Level Distribution")
        fig2 = px.pie(df, names="risk_level", title="Risk Level Breakdown")
        st.plotly_chart(fig2, use_container_width=True)
    def auto_map_columns(df):
        mapping = {}
        for key, possible_names in expected_fields.items():
            for col in df.columns:
                for option in possible_names:
                    if fuzz.partial_ratio(col.lower(), option.lower()) > 80:
                        mapping[key] = col
                        break
        return mapping

        st.subheader("Cart Value by Risk Level")
        fig3 = px.box(df, x="risk_level", y="cart_value", title="Cart Value vs Risk Level")
        st.plotly_chart(fig3, use_container_width=True)
    mapping = auto_map_columns(df)

# --- SEGMENT PAGE ---
elif section == "Segments":
@@ -129,50 +96,65 @@ def auto_map_columns(df):
    else:
        st.title("📌 Segmentation Insights")
        df = st.session_state.df

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

        # --- Manual fallback mapping ---
        st.markdown("### 🔍 Column Mapping")
        for key in expected_fields:
            if key not in mapping:
                mapping[key] = st.selectbox(f"Select column for **{key}**", df.columns)
            st.markdown(f"✅ `{key}` → `{mapping[key]}`")

        # --- Standardize ---
        df = df.rename(columns={mapping[k]: k for k in mapping})

        # --- Scoring logic ---
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

        df['risk_level'] = df['churn_score'].apply(label_risk)

        # --- Display Results ---
        st.markdown("### 📊 Churn Risk Segments")
        selected_risk = st.selectbox("Select Risk Level", df["risk_level"].unique())
        filtered = df[df["risk_level"] == selected_risk]
        st.write(f"Filtered users in {selected_risk} risk: {filtered.shape[0]}")
        st.dataframe(filtered)
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
