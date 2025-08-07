import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import io

# Page config
st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #1E2B3A;
            color: white;
        }
        .css-1aumxhk, .css-qcqlej {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🌙 RetentionOS")
st.sidebar.markdown("#### Navigation")
section = st.sidebar.radio("", [
    " Churn Analysis",
    " User Segments",
    " Nudge Suggestions",
    " RFM",
    " Cohort Analysis",
    " A/B Testing",
    " RAG Insights (Coming Soon)"
])

# --- Upload Section (Always visible in sidebar) ---
st.sidebar.markdown("#### Upload Data")
uploaded_file = st.sidebar.file_uploader("📤 Upload CSV or Excel", type=["csv", "xlsx"])

# View Switch (Only for Cohort for now)
if section == "📅 Cohort Analysis":
    view_option = st.sidebar.selectbox("View By:", ["Monthly", "Weekly"])

# --- Load file ---
df = None
if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    if 'last_purchase_date' in df.columns:
        df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'], errors='coerce')

# --- Section: Churn Analysis ---
if section == "📉 Churn Analysis":
    st.title("RetentionOS – Churn Analysis")
    if df is not None:
        st.write("### Coming Soon: Churn metrics, scoring, and analysis!")
    else:
        st.info("Please upload a user data file to begin.")

# --- Section: User Segments ---
elif section == "👥 User Segments":
    st.title("RetentionOS – User Segmentation")
    if df is not None:
        st.write("### Coming Soon: Segment users by behavior and usage patterns!")
    else:
        st.info("Please upload a user data file to begin.")

# --- Section: Nudge Suggestions ---
elif section == "💬 Nudge Suggestions":
    st.title("RetentionOS – Nudge Suggestions")
    if df is not None:
        st.write("### Coming Soon: GPT-powered personalized nudges!")
    else:
        st.info("Please upload a user data file to begin.")

# --- Section: RFM Analysis ---
elif section == "📊 RFM":
    st.title("RetentionOS – RFM Analysis")
    if df is not None:
        st.write("### Coming Soon: Recency, Frequency, Monetary analysis!")
    else:
        st.info("Please upload a user data file to begin.")

# --- Section: Cohort Analysis ---
elif section == "📅 Cohort Analysis":
    st.title("RetentionOS – Cohort Analysis")

    if df is not None and 'user_id' in df.columns and 'last_purchase_date' in df.columns:

        df['order_period'] = df['last_purchase_date'].dt.to_period('M' if view_option == 'Monthly' else 'W').dt.to_timestamp()
        df['cohort'] = df.groupby('user_id')['last_purchase_date'].transform('min')
        df['cohort'] = df['cohort'].dt.to_period('M' if view_option == 'Monthly' else 'W').dt.to_timestamp()
        cohort_data = df.groupby(['cohort', 'order_period']).agg(n_customers=('user_id', 'nunique')).reset_index()

        cohort_pivot = cohort_data.pivot(index='cohort', columns='order_period', values='n_customers')
        cohort_size = cohort_pivot.iloc[:, 0]
        retention = cohort_pivot.divide(cohort_size, axis=0)

        st.write("### Retention Heatmap")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(retention, annot=True, fmt=".0%", cmap="Blues", cbar=False, ax=ax)
        st.pyplot(fig)

        # Export CSV
        st.download_button("Download Retention Table as CSV", retention.to_csv().encode(), file_name="retention_matrix.csv", mime="text/csv")
    else:
        st.info("Please upload your CSV or Excel file with `user_id` and `last_purchase_date` columns to begin analysis.")

# --- Section: A/B Testing ---
elif section == "🧪 A/B Testing":
    st.title("RetentionOS – A/B Testing")
    if df is not None:
        st.write("### Coming Soon: A/B test analyzer and experiment dashboards!")
    else:
        st.info("Please upload a user data file to begin.")

# --- Section: RAG Insights ---
elif section == "🚦 RAG Insights (Coming Soon)":
    st.title("RetentionOS – RAG Insights")
    st.info("🚧 This feature is under development. Stay tuned!")
