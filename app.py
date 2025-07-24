import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar navigation (About included in main radio list)
menu = ["Home", "Summary", "Dashboard", "Segments", "About"]
section = st.sidebar.radio("📂 Navigation", menu)

# File uploader common
if "df" not in st.session_state:
    st.session_state.df = None

# --- HOME ---
if section == "Home":
    st.title("RetentionOS – A User Turning Point")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                st.session_state.df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                import openpyxl  # Required for Excel
                st.session_state.df = pd.read_excel(uploaded_file, engine="openpyxl")
            st.success("✅ File uploaded successfully!")
            st.dataframe(st.session_state.df.head())
        except Exception as e:
            st.error("❌ Could not read the uploaded file.")
            st.exception(e)

# --- SUMMARY ---
elif section == "Summary":
    st.title("📈 User Summary Insights")
    if st.session_state.df is not None:
        st.subheader("📌 Sample Data")
        st.dataframe(st.session_state.df.head())
    else:
        st.warning("⚠️ Please upload a file from the Home page.")

# --- DASHBOARD ---
elif section == "Dashboard":
    st.title("📊 Dashboard Metrics")
    if st.session_state.df is not None:
        df = st.session_state.df

        st.metric("Total Users", len(df))
        st.metric("High Risk Users", df[df["risk_level"] == "High"].shape[0])
        st.metric("Average Churn Score", round(df["churn_score"].mean(), 2))

        st.subheader("Churn Score Distribution")
        fig1 = px.histogram(df, x="churn_score", nbins=20, title="Churn Score Histogram")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Risk Level Distribution")
        fig2 = px.pie(df, names="risk_level", title="Risk Level Breakdown")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Cart Value by Risk Level")
        fig3 = px.box(df, x="risk_level", y="cart_value", title="Cart Value vs Risk Level")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("⚠️ Please upload a file from the Home page.")

# --- SEGMENTS ---
elif section == "Segments":
    st.title("📌 Segmentation Insights")
    if st.session_state.df is not None:
        df = st.session_state.df
        selected_risk = st.selectbox("Select Risk Level", df["risk_level"].unique())
        filtered = df[df["risk_level"] == selected_risk]
        st.write(f"Filtered users in {selected_risk} risk: {filtered.shape[0]}")
        st.dataframe(filtered)
    else:
        st.warning("⚠️ Please upload a file from the Home page.")

# --- ABOUT ---
elif section == "About":
    st.title("About RetentionOS")
    st.markdown("""
    **RetentionOS** is a lightweight churn prediction and nudging assistant built for fast-moving product teams at early-stage startups.

    ### ✅ Benefits:
    - Detect churn risk across users (High, Medium, Low)
    - Gain actionable insights using interactive dashboards
    - Get smart nudge recommendations
    - Export ready-to-use campaign files

    ### 🚀 Expected Outcomes:
    - Better retention strategies
    - Data-backed nudge campaigns
    - Faster user segmentation
    - Clear churn trends and risk metrics
    """)
