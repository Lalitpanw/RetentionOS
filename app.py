import streamlit as st
import pandas as pd
import io

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

# Session state for storing uploaded data
if 'df' not in st.session_state:
    st.session_state.df = None

# 📁 Data Upload Page
if page == "📁 Data Upload":
    st.title("🚀 RetentionOS – Predict. Segment. Re-engage.")
    st.markdown("_Upload user data → Identify churn risk → Auto-nudge users_")

    st.header("📁 Data Upload")
    st.markdown("Upload your user data (CSV or Excel) to begin")
    uploaded_file = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.session_state.df = df
        st.success("✅ File uploaded successfully! Now move to 'Churn Overview' ➡")

    # Sample CSV download
    sample_data = {
        'user_id': [101, 102, 103],
        'last_active_days': [3, 18, 27],
        'total_sessions': [12, 4, 1],
        'orders': [3, 1, 0],
        'revenue': [499, 149, 0]
    }
    sample_df = pd.DataFrame(sample_data)
    csv_data = sample_df.to_csv(index=False).encode('utf-8')

    st.markdown("#### 📥 Don't have data? Download a sample to try it out:")
    st.download_button(
        label="⬇️ Download Sample CSV",
        data=csv_data,
        file_name="sample_retentionos.csv",
        mime="text/csv"
    )

# ✅ Syntax fixed here (colon added)
elif page == "📊 Churn Overview":
    st.title("📊 Churn Overview")

    if st.session_state.df is not None:
        st.markdown("_Summary of churn scores and user distribution_")
        # You'll add churn scoring logic here later
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")

elif page == "👥 User Segments":
    st.title("👥 User Segments")

    if st.session_state.df is not None:
        st.markdown("_See users segmented by churn risk (High / Medium / Low)_")
        # You'll add segmentation display here
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")

elif page == "💬 Nudge Suggestions":
    st.title("💬 Nudge Suggestions")

    if st.session_state.df is not None:
        st.markdown("_Auto-generated WhatsApp/Email nudges based on risk level_")
        # You'll add nudge previews here
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")

elif page == "📈 Impact Snapshot":
    st.title("📈 Impact Snapshot")

    if st.session_state.df is not None:
        st.markdown("_Estimated uplift from nudges, retention impact, and more_")
        # You'll add ROI/impact logic here
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")
