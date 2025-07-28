import streamlit as st
import pandas as pd

st.title("🚀 RetentionOS – Predict. Segment. Re-engage.")
st.markdown("_Upload user data → Identify churn risk → Auto-nudge users_")

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

# --- Sample CSV download button ---
import io

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
