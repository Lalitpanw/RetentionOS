


import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="RetentionOS", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("🧭 Navigation")
section = st.sidebar.radio("Go to", ["Home", "Summary", "Dashboard", "Segmentation Insights"])

# --- Session State for file ---
if 'df' not in st.session_state:
    st.session_state['df'] = None

# --- HOME ---
if section == "Home":
    st.title("📊 RetentionOS – Upload User Data")
    uploaded_file = st.file_uploader("Upload your user Excel/CSV file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.session_state['df'] = df
            st.success("✅ File uploaded successfully!")

            # Show first few rows
            st.dataframe(df.head())

            # --- Download Button ---
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Uploaded Data as CSV",
                data=csv,
                file_name='uploaded_data.csv',
                mime='text/csv'
            )

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
    else:
        st.info("📂 Please upload a CSV or Excel file to begin.")

# --- SUMMARY ---
elif section == "Summary":
    st.title("📈 User Summary")
    df = st.session_state['df']
    if df is not None:
        st.subheader("🔍 Basic Description")
        st.dataframe(df.describe(include='all'))

        st.subheader("📊 Industry Detection (Beta)")
        if 'price_range' in df.columns and 'product_views' in df.columns:
            st.info("🛍️ Looks like a D2C/eCommerce dataset.")
        elif 'last_purchase_date' in df.columns and 'risk_level' in df.columns:
            st.info("🚗 This could be a mobility or service retention dataset.")
        elif 'sessions_last_7_days' in df.columns and 'cart_value' in df.columns:
            st.info("💊 Possibly healthcare or wellness related.")
        else:
            st.warning("❓ Industry could not be detected from columns.")

    else:
        st.warning("⚠️ No data uploaded yet.")

# --- DASHBOARD ---
elif section == "Dashboard":
    st.title("📊 Dashboard Metrics")
    df = st.session_state['df']
    if df is not None:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", len(df))
        col2.metric("High Risk Users", (df["risk_level"] == "High").sum() if 'risk_level' in df.columns else "N/A")
        col3.metric("Average Churn Score", round(df["churn_score"].mean(), 2) if 'churn_score' in df.columns else "N/A")

        if 'churn_score' in df.columns:
            fig = px.histogram(df, x="churn_score", nbins=20, title="Churn Score Distribution")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No data uploaded yet.")

# --- SEGMENTATION ---
elif section == "Segmentation Insights":
    st.title("🧠 Segmentation Insights")
    df = st.session_state['df']
    if df is not None:
        if "gender" in df.columns and "risk_level" in df.columns:
            seg = df.groupby(["gender", "risk_level"]).size().reset_index(name='Count')
            fig = px.bar(seg, x="gender", y="Count", color="risk_level", barmode="group")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("❗ Required columns ('gender', 'risk_level') not found.")
    else:
        st.warning("⚠️ No data uploaded yet.")
