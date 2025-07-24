import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="RetentionOS", layout="wide")

# Custom title using HTML with color and shadow
st.markdown("""
    <h1 style='text-align: center; color: #ff4b4b; text-shadow: 1px 1px 2px gray;'>
        RetentionOS – The Retention Operating System
    </h1>
""", unsafe_allow_html=True)

# Sidebar navigation
section = st.sidebar.radio("📂 Navigate", ["Home", "Summary", "Dashboard", "Segments", "About"])

# Initialize session
if "df" not in st.session_state:
    st.session_state.df = None

# ---- Home ----
if section == "Home":
    st.header("📊 Upload User Data")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file")

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Please upload a CSV or Excel file only.")
            st.stop()

        st.session_state.df = df
        st.success("✅ File uploaded successfully!")

        with st.expander("Preview Uploaded Data"):
            st.dataframe(df)

        st.download_button("📥 Download Clean File", df.to_csv(index=False), file_name="retention_clean_data.csv")

# ---- Summary ----
elif section == "Summary":
    st.header("📈 Retention Summary")
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

# ---- Dashboard ----
elif section == "Dashboard":
    st.header("📊 Dashboard")
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

# ---- Segments ----
elif section == "Segments":
    st.header("📦 User Segments")
    df = st.session_state.df

    if df is None:
        st.warning("Please upload a file first in the Home tab.")
    else:
        risk = st.selectbox("Select Risk Level", df["risk_level"].unique())
        filtered = df[df["risk_level"] == risk]
        st.write(f"{len(filtered)} users in {risk} risk segment")
        st.dataframe(filtered)

        st.download_button("📥 Download Segment", filtered.to_csv(index=False),
                           file_name=f"{risk.lower()}_risk_users.csv")

# ---- About ----
elif section == "About":
    st.header("🔍 About RetentionOS")

    st.markdown("""
    ### 🧠 What is RetentionOS?

    **RetentionOS** is a lightweight churn prediction and nudging assistant designed for fast-moving product teams at early-stage startups.

    It empowers you to:
    - 📥 Upload raw user data
    - 🚨 Detect churn risk (High, Medium, Low)
    - 🎯 Get smart nudge recommendations
    - 📊 Explore insights via dashboard & segments
    - 📤 Export data for campaigns or CRM

    ---
    ### 👨‍💻 Built by
    Created with a product-first mindset by **Lalit Panwar**  
    _For makers who prefer action over waiting._
    """, unsafe_allow_html=True)
