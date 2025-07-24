import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar Navigation with About at bottom
st.sidebar.markdown("### 📂 Navigation")
menu = ["Home", "Summary", "Dashboard", "Segments"]
section = st.sidebar.radio("Go to", menu)

# Add space and About button at bottom
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
about_clicked = st.sidebar.button("🔍 About RetentionOS")

# File upload shared state
if "df" not in st.session_state:
    st.session_state.df = None

# --- ABOUT PAGE (Triggered separately) ---
if about_clicked:
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
    st.stop()

# --- HOME PAGE ---
if section == "Home":
    st.title("RetentionOS – A User Turning Point")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                st.session_state.df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                import openpyxl
                st.session_state.df = pd.read_excel(uploaded_file, engine="openpyxl")
            st.success("✅ File uploaded successfully!")
            st.dataframe(st.session_state.df.head())
        except Exception as e:
            st.error("❌ Could not read the uploaded file.")
            st.exception(e)

# --- SUMMARY PAGE ---
elif section == "Summary":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a file from the Home page first.")
    else:
        st.title("📈 User Summary Insights")
        st.subheader("📌 Sample Data")
        st.dataframe(st.session_state.df.head())

# --- DASHBOARD PAGE ---
elif section == "Dashboard":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a file from the Home page first.")
    else:
        st.title("📊 Dashboard Metrics")
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

# --- SEGMENT PAGE ---
elif section == "Segments":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a file from the Home page first.")
    else:
        st.title("📌 Segmentation Insights")
        df = st.session_state.df
        selected_risk = st.selectbox("Select Risk Level", df["risk_level"].unique())
        filtered = df[df["risk_level"] == selected_risk]
        st.write(f"Filtered users in {selected_risk} risk: {filtered.shape[0]}")
        st.dataframe(filtered)
