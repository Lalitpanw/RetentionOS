import streamlit as st
import pandas as pd
import plotly.express as px
from fuzzywuzzy import fuzz

# --- App Config ---
st.set_page_config(page_title="RetentionOS", layout="wide")
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #0f172a;
        color: white;
    }
    .css-1aumxhk {
        background-color: #0f172a;
        color: white;
    }
    .css-1d391kg { color: white; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.markdown("## 🌐 RetentionOS")
section = st.sidebar.radio("Navigation", [
    "📉 Churn Analysis",
    "👥 User Segments",
    "💬 Nudge Suggestions",
    "📊 RFM",
    "📆 Cohort Analysis",
    "🧪 A/B Testing",
    "🚦 RAG Insights (Coming Soon)"
])

# --- Upload Section ---
st.markdown("# RetentionOS – AI-powered Churn & Retention")
st.markdown("Upload your user file to get started with churn prediction & retention analysis.")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
    st.session_state.df = df
    st.success("✅ Data uploaded successfully!")
else:
    st.warning("⚠️ Please upload a user data file to begin.")

if 'df' in st.session_state:
    df = st.session_state.df

    expected_fields = {
        'last_active_days': ['last_seen', 'last_active', 'inactive_days'],
        'total_sessions': ['sessions', 'login_count', 'visits'],
        'orders': ['orders', 'purchases', 'transactions'],
        'revenue': ['amount_spent', 'order_value', 'lifetime_value']
    }

    def auto_map_columns(df):
        mapping = {}
        for key, aliases in expected_fields.items():
            for col in df.columns:
                for alias in aliases:
                    if fuzz.partial_ratio(col.lower(), alias.lower()) > 80:
                        mapping[key] = col
                        break
        return mapping

    mapping = auto_map_columns(df)
    for key in expected_fields:
        if key not in mapping:
            mapping[key] = st.selectbox(f"Select column for {key}", df.columns)

    df = df.rename(columns={mapping[k]: k for k in mapping})

    def score_user(row):
        score = 0
        if row['last_active_days'] > 14: score += 1
        if row['orders'] < 1: score += 1
        if row['total_sessions'] < 3: score += 1
        return score

    df['churn_score'] = df.apply(score_user, axis=1)

    def label_risk(score):
        if score >= 2: return "🔴 High"
        elif score == 1: return "🟠 Medium"
        else: return "🟢 Low"

    df['churn_risk'] = df['churn_score'].apply(label_risk)

    if section == "📉 Churn Analysis":
        st.subheader("📊 Churn Analysis Dashboard")
        st.metric("Total Users", len(df))
        st.metric("High Risk Users", df[df['churn_risk'] == "🔴 High"].shape[0])
        st.metric("Average Churn Score", round(df['churn_score'].mean(), 2))

        st.plotly_chart(px.histogram(df, x='churn_score', nbins=10, title="Churn Score Distribution"), use_container_width=True)
        st.plotly_chart(px.pie(df, names='churn_risk', title="Risk Level Breakdown"), use_container_width=True)

    elif section == "👥 User Segments":
        st.subheader("User Segments by Risk Level")
        selected = st.selectbox("Select Risk Level", df['churn_risk'].unique())
        st.dataframe(df[df['churn_risk'] == selected])

    elif section == "💬 Nudge Suggestions":
        st.info("✨ Coming soon: AI-powered personalized nudges for each segment.")

    elif section == "📊 RFM":
        st.info("📊 RFM Segmentation module will allow you to identify user value.")

    elif section == "📆 Cohort Analysis":
        st.info("📆 Cohort Analysis module coming next.")

    elif section == "🧪 A/B Testing":
        st.info("🧪 A/B Testing toolkit under development.")

    elif section == "🚦 RAG Insights (Coming Soon)":
        st.info("🚦 GPT-powered RAG analysis launching soon.")
