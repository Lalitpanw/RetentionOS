import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# Page Config
st.set_page_config(page_title="RetentionOS – Cohort Analysis", layout="wide")

# Sidebar Styling
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #1e293b;
        color: white;
    }
    .css-1v3fvcr {background-color: #1e293b;}
    .css-1d391kg {color: white;}
    </style>
""", unsafe_allow_html=True)

# Sidebar Content
st.sidebar.markdown("### 🌙 RetentionOS")
section = st.sidebar.radio("Navigation", ["📈 Cohort Analysis", "📥 Upload Data"])

# View toggle
st.sidebar.markdown("### View By:")
cohort_view = st.sidebar.selectbox("", ["Monthly", "Weekly"])

# Main Content
st.markdown("## RetentionOS – Cohort Analysis")
uploaded_file = st.file_uploader("📥 Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    if "user_id" not in df.columns or "last_purchase_date" not in df.columns:
        st.error("❌ Please ensure the file contains 'user_id' and 'last_purchase_date' columns.")
    else:
        df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'])
        df['signup_date'] = df.groupby('user_id')['last_purchase_date'].transform('min')

        if cohort_view == "Monthly":
            df['signup_month'] = df['signup_date'].dt.to_period('M')
            df['cohort_month'] = df['last_purchase_date'].dt.to_period('M')
            cohort_index = (df['cohort_month'].dt.to_timestamp() - df['signup_month'].dt.to_timestamp()) // pd.Timedelta('30D')
        else:
            df['signup_week'] = df['signup_date'].dt.to_period('W')
            df['cohort_week'] = df['last_purchase_date'].dt.to_period('W')
            cohort_index = (df['cohort_week'].dt.start_time - df['signup_week'].dt.start_time).dt.days // 7

        cohort_col = 'signup_month' if cohort_view == "Monthly" else 'signup_week'
        df['cohort_index'] = cohort_index

        cohort_data = df.groupby([cohort_col, 'cohort_index'])['user_id'].nunique().unstack(fill_value=0)
        cohort_sizes = cohort_data.iloc[:, 0]
        retention = cohort_data.divide(cohort_sizes, axis=0).round(3) * 100

        # Display Heatmap
        st.markdown("### 📉 Retention Heatmap")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(retention, annot=True, fmt=".0f", cmap="Blues", ax=ax)
        plt.title(f"{cohort_view} Retention (%)")
        st.pyplot(fig)

        # Download
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        st.download_button("⬇️ Download Heatmap", buffer.getvalue(), file_name="retention_heatmap.png")

else:
    st.info("📤 Please upload your CSV or Excel file to begin analysis.")
