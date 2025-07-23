import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="RetentionOS", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("🧭 Navigation")
section = st.sidebar.radio("Go to", ["Home", "Summary", "Dashboard", "Segmentation Insights"])

# --- Session State for Data ---
if 'df' not in st.session_state:
    st.session_state['df'] = None

# --- HOME SECTION ---
if section == "Home":
    st.title("📊 RetentionOS – Upload User Data")
    uploaded_file = st.file_uploader("Upload your user Excel/CSV file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.session_state['df'] = df
            st.success("✅ File uploaded successfully!")
            st.dataframe(df.head())

        except Exception as e:
            st.error(f"Error: {e}")

# --- SUMMARY SECTION ---
elif section == "Summary":
    st.title("📈 User Summary Insights")

    df = st.session_state['df']
    if df is None:
        st.warning("Please upload a file first in the Home section.")
    else:
        st.subheader("📊 Key Columns Detected:")
        st.write(list(df.columns))

        st.subheader("📌 Sample Data")
        st.dataframe(df.head())

        st.subheader("🔍 Null Values")
        st.write(df.isnull().sum())

# --- DASHBOARD SECTION ---
elif section == "Dashboard":
    st.title("📊 Dashboard Metrics")
    df = st.session_state['df']
    if df is None:
        st.warning("Please upload a file first in the Home section.")
    else:
        total_users = df.shape[0]
        high_risk = df[df['risk_level'] == 'High'].shape[0]
        avg_churn = round(df['churn_score'].mean(), 2)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", total_users)
        col2.metric("High Risk Users", high_risk)
        col3.metric("Avg. Churn Score", avg_churn)

        st.subheader("📉 Churn Score Distribution")
        fig = px.histogram(df, x="churn_score", nbins=20, title="Churn Score Distribution")
        st.plotly_chart(fig, use_container_width=True)

# --- SEGMENTATION INSIGHTS ---
elif section == "Segmentation Insights":
    st.title("🔍 Segmentation Insights")
    df = st.session_state['df']
    if df is None:
        st.warning("Please upload a file first in the Home section.")
    else:
        seg_col = st.selectbox("Select column to segment", ["gender", "price_range", "risk_level"])

        st.subheader(f"📊 Churn Score by {seg_col}")
        fig = px.box(df, x=seg_col, y="churn_score", title=f"Churn Score Distribution by {seg_col}")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(f"📊 User Count by {seg_col}")
        fig2 = px.histogram(df, x=seg_col, title=f"User Count by {seg_col}")
        st.plotly_chart(fig2, use_container_width=True)
