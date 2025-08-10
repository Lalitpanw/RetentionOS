import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="RetentionOS", page_icon="📊", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("📊 RetentionOS")
section = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📉 Churn Analysis",
        "👥 User Segments",
        "💬 Nudge Suggestions",
        "📆 Cohort Analysis",
        "🔍 RAG Insights",
        "📤 Export Data"
    ]
)

# --- HOME SECTION ---
if section == "🏠 Home":
    st.markdown("<h2 style='text-align: center;'>📥 Upload Your User Data File</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"], key="file_uploader_home")

    if uploaded_file:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        st.session_state.df = df
        st.success("✅ File uploaded and loaded successfully!")
        st.dataframe(df.head())
    else:
        st.warning("⚠️ Please upload a file to proceed.")

    st.stop()  # Stop execution so other sections don't run

# --- DATA CHECK ---
if "df" not in st.session_state:
    st.error("🚫 No data found. Please upload a file in the Home section first.")
    st.stop()

df = st.session_state.df.copy()

# --- CHURN ANALYSIS ---
if section == "📉 Churn Analysis":
    st.header("Churn Analysis")
    if "risk_level" not in df.columns:
        st.warning("⚠️ No 'risk_level' column found. Please add churn prediction logic.")
    else:
        churn_counts = df["risk_level"].value_counts().reset_index()
        churn_counts.columns = ["Risk Level", "Count"]
        fig = px.bar(churn_counts, x="Risk Level", y="Count", color="Risk Level", title="Churn Risk Levels")
        st.plotly_chart(fig, use_container_width=True)

# --- USER SEGMENTS ---
elif section == "👥 User Segments":
    st.header("User Segments")
    if "risk_level" not in df.columns:
        st.warning("⚠️ No 'risk_level' column found.")
    else:
        risk_choice = st.selectbox("Select Risk Level", df["risk_level"].unique())
        segment_df = df[df["risk_level"] == risk_choice]
        st.write(f"Total Users: {len(segment_df)}")
        st.dataframe(segment_df)

# --- NUDGE SUGGESTIONS ---
elif section == "💬 Nudge Suggestions":
    st.header("Nudge Suggestions")
    if "risk_level" not in df.columns:
        st.warning("⚠️ No 'risk_level' column found.")
    else:
        nudges = {
            "High": "Offer discount or personalized outreach.",
            "Medium": "Send engagement email with feature highlights.",
            "Low": "Promote referral program."
        }
        for risk, message in nudges.items():
            st.subheader(f"{risk} Risk Users")
            st.write(message)

# --- COHORT ANALYSIS ---
elif section == "📆 Cohort Analysis":
    st.header("Cohort Analysis")
    if "signup_date" not in df.columns:
        st.warning("⚠️ No 'signup_date' column found.")
    else:
        df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
        df["signup_month"] = df["signup_date"].dt.to_period("M")
        cohort = df.groupby("signup_month")["user_id"].nunique().reset_index()
        cohort.columns = ["Signup Month", "Unique Users"]
        fig = px.line(cohort, x="Signup Month", y="Unique Users", title="Monthly Cohorts")
        st.plotly_chart(fig, use_container_width=True)

# --- RAG INSIGHTS ---
elif section == "🔍 RAG Insights":
    st.header("RAG Insights (Placeholder)")
    st.info("Integrate GPT/LangChain here for insights.")

# --- EXPORT DATA ---
elif section == "📤 Export Data":
    st.header("Export Data")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="retention_data.csv",
        mime="text/csv"
    )
