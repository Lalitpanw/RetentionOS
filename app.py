import streamlit as st
import pandas as pd

st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar navigation
st.sidebar.title("🔎 Navigation")
page = st.sidebar.radio("Go to", [
    "📁 Data Upload",
    "📊 Churn Overview",
    "👥 User Segments",
    "💬 Nudge Suggestions",
    "📈 Impact Snapshot"
])

# Global session state to store uploaded data
if 'df' not in st.session_state:
    st.session_state.df = None

# 1. Data Upload Page
if page == "📁 Data Upload":
    st.title("📁 Data Upload")
    st.markdown("_Upload your user data (CSV or Excel) to begin_")
    
    uploaded_file = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx"])
    
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.session_state.df = df
        st.success("✅ File uploaded successfully! Now move to 'Churn Overview' ➡")

# 2. Churn Overview Page
elif page == "📊 Churn Overview":
    st.title("📊 Churn Overview")
    
    if st.session_state.df is not None:
        st.markdown("_Summary of churn scores and user distribution_")
        # You’ll add churn scoring + chart here in next step
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")

# 3. User Segments Page
elif page == "👥 User Segments":
    st.title("👥 User Segments")
    
    if st.session_state.df is not None:
        st.markdown("_See users segmented by churn risk (High / Medium / Low)_")
        # You’ll add filtered table logic here next
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")

# 4. Nudge Suggestions Page
elif page == "💬 Nudge Suggestions":
    st.title("💬 Nudge Suggestions")
    
    if st.session_state.df is not None:
        st.markdown("_Auto-generated WhatsApp/Email nudges based on risk level_")
        # You’ll add message previews per risk group
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")

# 5. Impact Snapshot Page
elif page == "📈 Impact Snapshot":
    st.title("📈 Impact Snapshot")
    
    if st.session_state.df is not None:
        st.markdown("_Estimated uplift from nudges, retention impact, and more_")
        # Later: Add a basic ROI calculator or uplift projection
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")
