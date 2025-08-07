import streamlit as st
import pandas as pd
import plotly.express as px
from fuzzywuzzy import fuzz

# Page config
st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar Navigation
st.markdown("""
<style>
/* Sidebar background */
section[data-testid="stSidebar"] {
    background-color: #0f1c2e;
}

/* Sidebar text color */
section[data-testid="stSidebar"] .css-1v3fvcr {
    color: #e1e6f0 !important;
    font-weight: 500;
}

/* Active item */
section[data-testid="stSidebar"] .css-1v3fvcr > div[aria-checked="true"] {
    background-color: transparent;
    font-weight: 700;
    color: #ffffff !important;
}

/* Section titles */
section[data-testid="stSidebar"] h2 {
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #ffffff;
    margin-bottom: 1rem;
}

/* Label fixes */
section[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🌐 RetentionOS")
st.sidebar.markdown("## Navigation")
section = st.sidebar.radio("", [
    " Churn Analysis",
    " User Segments",
    " Nudge Suggestions",
    " RFM",
    " Cohort Analysis",
    " A/B Testing",
    " RAG Insights (Coming Soon)"
])

# Main Area UI
st.markdown("""
### <span style='font-size:32px;'>📊 RetentionOS – AI-powered Churn & Retention</span>
<p style='font-size:16px;'>Upload your user file to get started with churn prediction & retention analysis.</p>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    st.session_state.df = df
    st.success("✅ File uploaded successfully!")
else:
    st.warning("⚠️ Please upload a user data file to begin.")

# Load and view placeholder section
if 'df' in st.session_state:
    st.subheader(f"You selected: {section}")
    st.write("We'll display the relevant features here soon...")
