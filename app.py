import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar
menu = ["Home", "Summary", "Dashboard", "Segments", "About"]
page = st.sidebar.radio("Navigate", menu)

# Store uploaded data
if "df" not in st.session_state:
    st.session_state.df = None

# Home
if page == "Home":
    st.title("RetentionOS – A User Turning Point")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file")

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            st.success("File uploaded successfully!")

            with st.expander("Preview Uploaded Data"):
                st.dataframe(df)

            st.download_button("Download Clean File", df.to_csv(index=False), file_name="retention_clean_data.csv")

        except Exception as e:
            st.error(f"Error reading file: {e}")

# Summary
elif page == "Summary":
    st.title("Retention Summary")
    df = st.session_state.df

    if df is None:
        st.warning("Please upload a file first in the Home tab.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", len(df))
        col2.metric("High Risk Users", (df["risk_level"] == "High").sum())
        col3.metric("Average Churn Score", round(df["churn_score"].mean(), 2))

        st.subheader("Churn Risk Breakdown")
        st.bar_chart(df["risk_level"].value_counts())

        if "gender" in df.columns:
            st.subheader("Gender Distribution")
            st.plotly_chart(px.pie(df, names="gender", title="User Gender Split"))

        if "churn_score" in df.columns:
            st.subheader("Top 5 High-Risk Users")
            top_risky = df.sort_values(by="churn_score", ascending=False).head(5)
            st.dataframe(top_risky[["user_id", "churn_score", "nudge_recommendation"]])

        if "nudge_recommendation" in df.columns:
            st.subheader("Nudge Recommendation Distribution")
            chart_data = df["nudge_recommendation"].value_counts().reset_index()
            st.plotly_chart(px.bar(chart_data, x="index", y="nudge_recommendation",
                                   labels={"index": "Nudge Type", "nudge_recommendation": "Count"}))

# Dashboard
elif page == "Dashboard":
    st.title("Dashboard")
    df = st.session_state.df

    if df is None:
        st.warning("Please upload a file first in the Home tab.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", len(df))
        col2.metric("High Risk Users", (df["risk_level"] == "High").sum())
        col3.metric("Average Churn Score", round(df["churn_score"].mean(), 2))

        st.subheader("Churn Score Histogram")
        st.plotly_chart(px.histogram(df, x="churn_score", nbins=20))

# Segments
elif page == "Segments":
    st.title("User Segments")
    df = st.session_state.df

    if df is None:
        st.warning("Please upload a file first in the Home tab.")
    else:
        risk = st.selectbox("Select Risk Level", df["risk_level"].unique())
        filtered = df[df["risk_level"] == risk]
        st.write(f"{len(filtered)} users in {risk} risk segment")
        st.dataframe(filtered)

        st.download_button("Download Segment", filtered.to_csv(index=False),
                           file_name=f"{risk.lower()}_risk_users.csv")

# About
elif page == "About":
    st.title("About RetentionOS")
    st.write("""
    RetentionOS is a lightweight churn prediction and nudging assistant
    built for fast-moving product teams at early-stage startups.

    Features:
    - Upload raw user data
    - Detect churn risk (High, Medium, Low)
    - Get smart nudge recommendations
    - Explore insights via dashboard and segments
    - Export data for campaigns or CRM

    Built by Lalit Panwar – a product-first thinker focused on solving real user problems.
    """)
