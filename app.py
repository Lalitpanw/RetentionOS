import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar navigation
section = st.sidebar.radio("📂 Navigate", ["Home", "Summary", "Dashboard", "Segments", "About"])

# Global variable to store data
if "df" not in st.session_state:
    st.session_state.df = None

# -------------------------------------
# 📥 HOME – Upload Data
# -------------------------------------
if section == "Home":
    st.title("📊 RetentionOS – Upload User Data")
    uploaded_file = st.file_uploader("Upload your user Excel/CSV file")

    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            st.stop()

        st.session_state.df = df
        st.success("✅ File uploaded successfully!")

        with st.expander("🔍 Preview Uploaded Data"):
            st.dataframe(df)

        st.download_button("📥 Download Clean File", df.to_csv(index=False), file_name="retention_clean_data.csv")

# -------------------------------------
# 📈 SUMMARY – Key Insights
# -------------------------------------
elif section == "Summary":
    st.title("📈 Retention Summary Dashboard")
    df = st.session_state.df

    if df is None:
        st.warning("Please upload a file in the Home section first.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", len(df))
        col2.metric("High Risk Users", (df["risk_level"] == "High").sum())
        col3.metric("Average Churn Score", round(df["churn_score"].mean(), 2))

        st.markdown("### 🎯 Churn Risk Breakdown")
        st.bar_chart(df["risk_level"].value_counts())

        st.markdown("### 👥 Gender Split")
        if "gender" in df.columns:
            st.plotly_chart(px.pie(df, names="gender", title="Users by Gender"))

        st.markdown("### 🔝 Top 5 High-Risk Users")
        if "churn_score" in df.columns:
            top_risky = df.sort_values(by="churn_score", ascending=False).head(5)
            st.dataframe(top_risky[["user_id", "churn_score", "nudge_recommendation"]])

        st.markdown("### 💡 Nudge Recommendations")
        if "nudge_recommendation" in df.columns:
            st.plotly_chart(px.bar(
                df["nudge_recommendation"].value_counts().reset_index(),
                x="index", y="nudge_recommendation",
                labels={"index": "Nudge Type", "nudge_recommendation": "Count"},
                title="Nudge Recommendation Distribution"
            ))

# -------------------------------------
# 📊 DASHBOARD – Metrics View
# -------------------------------------
elif section == "Dashboard":
    st.title("📊 Dashboard Metrics")
    df = st.session_state.df

    if df is None:
        st.warning("Please upload a file in the Home section first.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", len(df))
        col2.metric("High Risk Users", (df["risk_level"] == "High").sum())
        col3.metric("Average Churn Score", round(df["churn_score"].mean(), 2))

        st.markdown("### 📉 Churn Score Distribution")
        fig = px.histogram(df, x="churn_score", nbins=20, title="Churn Score Histogram")
        st.plotly_chart(fig)

# -------------------------------------
# 🧠 SEGMENTS – Filtered Insights
# -------------------------------------
elif section == "Segments":
    st.title("📦 User Segments")
    df = st.session_state.df

    if df is None:
        st.warning("Please upload a file in the Home section first.")
    else:
        risk = st.selectbox("Select Risk Level", options=df["risk_level"].unique())
        filtered = df[df["risk_level"] == risk]
        st.write(f"Showing {len(filtered)} users in **{risk}** risk segment.")
        st.dataframe(filtered)

        st.download_button(
            "📥 Download Segment",
            filtered.to_csv(index=False),
            file_name=f"{risk.lower()}_risk_users.csv"
        )

# -------------------------------------
# 📖 ABOUT – Tool Info
# -------------------------------------
elif section == "About":
    st.title("ℹ️ About RetentionOS")

    st.markdown("""
    ### 🧠 What is RetentionOS?
    **RetentionOS** is a lightweight churn prediction and nudging assistant built for fast-moving Product teams in early-stage startups.

    It empowers teams to:
    - 🚨 Detect at-risk users before they churn
    - 🎯 Get smart nudging recommendations
    - 📤 Export segments for real reactivation
    - 🧠 Make data-backed growth decisions without needing data scientists

    ---

    ### 💡 Why It Exists
    Built with the belief that **Product Managers shouldn't wait on data teams** to get insights — RetentionOS gives PMs a plug-and-play dashboard to take action, fast.

    Whether you're at a D2C brand, a mobility startup, or a healthcare app — if retention matters, this is for you.

    ---

    ### 🔧 Built By
    Created with curiosity, grit, and a product-first mindset by **Lalit Panwar** — a Product Manager passionate about growth, retention, and building tools that actually solve problems.

    _“I built RetentionOS because I saw how much time teams waste figuring out what to do with raw user data. This tool does the thinking for you — so you can focus on execution.”_

    ---

    ### 🧪 Who Can Use It
    - Product Managers 🎯
    - Growth Teams 📈
    - Startup Founders 🚀
    - Aspiring PMs & Analysts 🛠️

    ---

    ### 📦 Supported Industries
    - 🛍️ D2C / E-Commerce (e.g., skincare, fashion)
    - 🚗 Mobility / Vehicle Services
    - 🏥 Health & Wellness

    ---
    """, unsafe_allow_html=True)

