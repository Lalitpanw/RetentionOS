import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar sections
top_sections = ["Home", "Summary", "Dashboard", "Segments"]
bottom_section = "About RetentionOS"

# Sidebar layout
selected_top = st.sidebar.radio("📂 Navigation", top_sections)
st.sidebar.markdown("---")
go_about = st.sidebar.button("🔍 About RetentionOS")

# File Upload Setup
if "df" not in st.session_state:
    st.session_state.df = None

# Upload logic
if selected_top == "Home":
    st.title("RetentionOS – A User Turning Point")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                st.session_state.df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                st.session_state.df = pd.read_excel(uploaded_file)
            st.success("✅ File uploaded successfully!")
            st.dataframe(st.session_state.df.head())
        except Exception as e:
            st.error("❌ Error reading file. Please check format or required libraries.")
            st.exception(e)

# Summary
elif selected_top == "Summary":
    st.title("📈 User Summary Insights")
    if st.session_state.df is not None:
        st.subheader("📌 Key Columns Detected")
        st.write(", ".join(st.session_state.df.columns))
        st.subheader("📌 Sample Data")
        st.dataframe(st.session_state.df.head())
    else:
        st.warning("Please upload a file from the Home page.")

# Dashboard
elif selected_top == "Dashboard":
    st.title("📊 Dashboard Metrics")
    if st.session_state.df is not None:
        df = st.session_state.df
        st.metric("Total Users", len(df))
        st.metric("High Risk Users", df[df["risk_level"] == "High"].shape[0])
        st.metric("Average Churn Score", round(df["churn_score"].mean(), 2))
    else:
        st.warning("Please upload a file from the Home page.")

# Segments
elif selected_top == "Segments":
    st.title("📌 Segmentation Insights")
    if st.session_state.df is not None:
        df = st.session_state.df
        selected_risk = st.selectbox("Select Risk Level", df["risk_level"].unique())
        filtered = df[df["risk_level"] == selected_risk]
        st.write(f"Filtered users in {selected_risk} risk:", filtered.shape[0])
        st.dataframe(filtered)
    else:
        st.warning("Please upload a file from the Home page.")

# About section triggered by button
if go_about:
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
