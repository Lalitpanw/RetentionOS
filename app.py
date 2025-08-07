import streamlit as st
import pandas as pd

st.set_page_config(page_title="RetentionOS", layout="wide")

# --- Custom CSS for gradient sidebar and main UI ---
st.markdown("""
    <style>
    /* Sidebar gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f2c47, #0d1526);
        color: white;
    }

    /* Sidebar title */
    .sidebar .sidebar-content {
        padding-top: 2rem;
    }

    /* Sidebar text styling */
    .css-10trblm {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: white !important;
    }

    /* File upload box styling */
    .upload-container {
        border: 2px solid #e5e5e5;
        border-radius: 10px;
        padding: 3rem;
        text-align: center;
        background-color: #f9f9f9;
    }

    .upload-btn {
        background-color: white;
        padding: 10px 30px;
        border-radius: 5px;
        border: 1px solid #ccc;
        font-weight: 600;
        margin-top: 1rem;
        cursor: pointer;
    }

    .main-title {
        font-size: 30px;
        font-weight: 700;
    }

    .subtext {
        font-size: 16px;
        color: #666;
        margin-bottom: 2rem;
    }

    .coming-soon {
        font-size: 14px;
        color: gray;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("## 🌐 RetentionOS")
st.sidebar.markdown("### Navigation")
st.sidebar.radio("Go to", [
    "📉 Churn Analysis",
    "👥 User Segments",
    "💬 Nudge Suggestions",
    "📊 RFM",
    "📆 Cohort Analysis",
    "🧪 A/B Testing",
    "🚦 RAG Insights (Coming Soon)"
], label_visibility="collapsed")

# --- Main Header ---
st.markdown("<div class='main-title'>📊 RetentionOS – AI-powered Churn & Retention</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Upload your user file to get started with churn prediction & retention analysis.</div>", unsafe_allow_html=True)

# --- Upload Box ---
uploaded_file = st.file_uploader("", type=["csv", "xlsx"], label_visibility="collapsed")

if uploaded_file:
    st.success(f"✅ File uploaded: `{uploaded_file.name}`")
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    st.session_state.df = df
else:
    st.markdown("""
        <div class='upload-container'>
            <div style='font-size:50px;'>⬇️</div>
            <div class='upload-btn'>Upload CSV or Excel</div>
            <div style='margin-top:1rem;'>Upload your user file to get started with churn<br>prediction & retention analysis.</div>
        </div>
    """, unsafe_allow_html=True)
