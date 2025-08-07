# RetentionOS - Clean Frontend Layout Setup (Streamlit)

import streamlit as st
import pandas as pd
import plotly.express as px
from fuzzywuzzy import fuzz

# Page config
st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4149/4149643.png", width=60)
st.sidebar.title("RetentionOS")
section = st.sidebar.radio("Navigation", [
    "📉 Churn Analysis",
    "🧩 User Segments",
    "💬 Nudge Suggestions",
    "📊 RFM Analysis",
    "🚦 RAG Insights"
])

# File Upload (top area)
st.title("📊 RetentionOS – AI-powered Churn & Retention")
st.markdown("Upload a `.csv` or `.xlsx` user file to get started with churn prediction & retention insights.")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

# Data Loading
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        st.session_state.df = df
        st.success("✅ File uploaded successfully!")
        st.markdown(f"**Detected columns:** `{', '.join(df.columns[:6])}` ...")

    except Exception as e:
        st.error(f"Error reading file: {e}")

elif 'df' not in st.session_state:
    st.warning("⬆️ Please upload a user data file to begin.")

# Section placeholders (actual logic will be added after layout setup)
if 'df' in st.session_state:
    df = st.session_state.df

    if section == "📉 Churn Analysis":
        st.header("📉 Churn Analysis")
        st.info("This section will analyze churn risk based on user activity.")

    elif section == "🧩 User Segments":
        st.header("🧩 User Segments")
        st.info("This section will group users into high/medium/low risk cohorts.")

    elif section == "💬 Nudge Suggestions":
        st.header("💬 AI-powered Nudge Suggestions")
        st.info("Use GPT to generate personalized nudges for different segments.")

    elif section == "📊 RFM Analysis":
        st.header("📊 RFM Analysis")
        st.info("Recency, Frequency, and Monetary segmentation coming soon.")

    elif section == "🚦 RAG Insights":
        st.header("🚦 RAG Insights")
        st.info("GPT-based suggestions + insights powered by user segments.")
