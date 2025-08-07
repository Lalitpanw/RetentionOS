import streamlit as st
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="RetentionOS", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.markdown("## 🌙 RetentionOS")
st.sidebar.markdown("### Navigation")
section = st.sidebar.radio("", [
    " Churn Analysis",
    " User Segments",
    " Nudge Suggestions",
    " RFM",
    " Cohort Analysis",
    " A/B Testing",
    " RAG Insights (Coming Soon)"
])

# --- Sidebar Upload ---
st.sidebar.markdown("### 📤 Upload Data")
uploaded_file = st.sidebar.file_uploader("📥 Upload CSV or Excel", type=["csv", "xlsx"])
st.sidebar.markdown("Limit 200MB per file • CSV, XLSX")

# --- Main Area ---
st.markdown(f"## {section}")
st.markdown("Upload your user file to get started with churn prediction & retention analysis.")

# --- Centered Upload Area ---
if uploaded_file is None:
    with st.container():
        st.write("### 📁 Upload CSV or Excel file")
        st.markdown("Please upload your user data to begin.")
else:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully.")
    st.dataframe(df.head())

# --- Placeholder for each section ---
if uploaded_file:
    if section == "📉 Churn Analysis":
        st.write("🚧 Churn analysis module coming soon.")
    elif section == "👥 User Segments":
        st.write("🚧 User segmentation coming soon.")
    elif section == "💬 Nudge Suggestions":
        st.write("🚧 Nudge engine coming soon.")
    elif section == "📊 RFM":
        st.write("🚧 RFM segmentation coming soon.")
    elif section == "📅 Cohort Analysis":
        st.write("🚧 Cohort Analysis module coming soon.")
    elif section == "🧪 A/B Testing":
        st.write("🚧 A/B test planning coming soon.")
    elif section == "🚦 RAG Insights (Coming Soon)":
        st.write("🚧 GPT-based RAG Insights will be added later.")
