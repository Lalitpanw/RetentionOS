import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar navigation
st.sidebar.title("📂 Navigation")
section = st.sidebar.radio("Go to", ["Home", "Summary", "Dashboard", "Segments", "About RetentionOS"])
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# File upload
if "df" not in st.session_state:
    st.session_state.df = None

if section == "Home":
    st.title("RetentionOS – A User Turning Point")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            st.session_state.df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xls", ".xlsx")):
            st.session_state.df = pd.read_excel(uploaded_file)
        st.success("✅ File uploaded successfully!")
        st.dataframe(st.session_state.df.head())

elif section == "Summary":
    st.title("📈 User Summary Insights")
    if st.session_state.df is not None:
        st.subheader("📌 Key Columns Detected")
        st.write(", ".join(st.session_state.df.columns))
        st.subheader("📌 Sample Data")
        st.dataframe(st.session_state.df.head())
    else:
        st.warning("Please upload a file from the Home page.")

elif section == "Dashboard":
    st.title("📊 Dashboard Metrics")
    if st.session_state.df is not None:
        df = st.session_state.df
        st.metric("Total Users", len(df))
        st.metric("High Risk Users", df[df["risk_level"] == "High"].shape[0])
        st.metric("Average Churn Score", round(df["churn_score"].mean(), 2))
    else:
        st.warning("Please upload a file from the Home page.")

elif section == "Segments":
    st.title("📌 Segmentation Insights")
    if st.session_state.df is not None:
        df = st.session_state.df
        selected_risk = st.selectbox("Select Risk Level", df["risk_level"].unique())
        filtered = df[df["risk_level"] == selected_risk]
        st.write(f"Filtered users in {selected_risk} risk:", filtered.shape[0])
        st.dataframe(filtered)
    else:
        st.warning("Please upload a file from the Home page.")

elif section == "About RetentionOS":
    st.title("About RetentionOS")
    st.markdown("""
    RetentionOS is a lightweight churn prediction and nudging assistant built for fast-moving product teams at early-stage startups.

    **Benefits:**
    - Detect churn risk across users (High, Medium, Low)
    - Gain actionable insights using simple dashboards
    - Get smart nudge recommendations
    - Export ready-to-use campaign files

    **Expected Outcomes:**
    - Better retention strategies
    - Data-backed nudge campaigns
    - Faster user segmentation
    - Clear churn trends and metrics
    """)
