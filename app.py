import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Streamlit UI config
st.set_page_config(page_title="RetentionOS", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🌙 RetentionOS")
    section = st.radio("Navigation", ["📈 Cohort Analysis", "📥 Upload Data"])
    cohort_view = st.selectbox("View By:", ["Monthly", "Weekly"])

# --- File Upload ---
st.title("RetentionOS – Cohort Analysis")
uploaded_file = st.file_uploader("📁 Upload your CSV or Excel file", type=["csv", "xlsx"])

# --- Data Handling ---
if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    st.success(f"✅ Uploaded: {uploaded_file.name}")
    st.write("### 🔍 Data Preview", df.head())

    # --- Preprocessing ---
    df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'])
    df['cohort_date'] = df.groupby('user_id')['last_purchase_date'].transform('min')

    if cohort_view == "Monthly":
        df['cohort_group'] = df['cohort_date'].dt.to_period('M')
        df['purchase_period'] = df['last_purchase_date'].dt.to_period('M')
    else:
        df['cohort_group'] = df['cohort_date'].dt.to_period('W')
        df['purchase_period'] = df['last_purchase_date'].dt.to_period('W')

    cohort_data = df.groupby(['cohort_group', 'purchase_period'])['user_id'].nunique().unstack(0)
    cohort_sizes = cohort_data.iloc[0]
    retention = cohort_data.divide(cohort_sizes, axis=1)

    # --- Heatmap ---
    st.markdown("### 📊 Retention Heatmap")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(retention.T, annot=True, fmt=".0%", cmap="Blues", cbar=False, ax=ax)
    ax.set_title(f"{cohort_view} Retention")
    st.pyplot(fig)

    # --- Download CSV ---
    csv = retention.fillna(0).to_csv(index=True).encode("utf-8")
    st.download_button("⬇️ Download CSV", data=csv, file_name="retention_data.csv", mime="text/csv")

    # --- Download PNG ---
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="retention_heatmap.png">⬇️ Download Heatmap PNG</a>'
    st.markdown(href, unsafe_allow_html=True)

else:
    st.info("📂 Please upload your CSV or Excel file to begin analysis.")
