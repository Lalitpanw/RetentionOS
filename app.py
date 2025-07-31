import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from fuzzywuzzy import fuzz
from datetime import datetime

# Page config
st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar Navigation
st.sidebar.markdown("### 📂 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Churn Prediction", "User Segments", "Dashboard", "RFM Analysis"])

# About section at bottom
st.sidebar.markdown("<br><br><br><hr>", unsafe_allow_html=True)
if st.sidebar.button("ℹ️ About RetentionOS"):
    st.info("""
    **RetentionOS** is a lightweight churn prediction tool.
    - Upload data → Train model → Predict churn → Export results.
    - Designed for early-stage teams and product managers.
    """)

# Shared session state
if "df" not in st.session_state:
    st.session_state.df = None
if "predicted_df" not in st.session_state:
    st.session_state.predicted_df = None

# Smart Column Mapper for RFM
RFM_TARGETS = {
    'user_id': ['user_id', 'customer_id', 'id'],
    'last_seen': ['last_seen', 'last_active', 'last_activity_date'],
    'orders': ['orders', 'purchases', 'transactions'],
    'revenue': ['revenue', 'total_spent', 'amount_spent']
}

def smart_rfm_mapper(df):
    mapping = {}
    for target, options in RFM_TARGETS.items():
        for col in df.columns:
            for option in options:
                if fuzz.partial_ratio(col.lower(), option.lower()) > 80:
                    mapping[target] = col
                    break
        if target not in mapping:
            mapping[target] = st.selectbox(f"Select column for **{target}**", df.columns)
    return mapping

# RFM Calculation Function
def calculate_rfm(df, mapping):
    df[mapping['last_seen']] = pd.to_datetime(df[mapping['last_seen']], errors='coerce')
    snapshot_date = df[mapping['last_seen']].max()
    rfm = df.groupby(mapping['user_id']).agg({
        mapping['last_seen']: lambda x: (snapshot_date - x.max()).days,
        mapping['orders']: 'count',
        mapping['revenue']: 'sum'
    }).reset_index()
    rfm.columns = ["user_id", 'recency', 'frequency', 'monetary']

    # RFM Segmentation
    rfm['R_score'] = pd.qcut(rfm['recency'], 4, labels=[4, 3, 2, 1])
    rfm['F_score'] = pd.qcut(rfm['frequency'].rank(method="first"), 4, labels=[1, 2, 3, 4])
    rfm['M_score'] = pd.qcut(rfm['monetary'], 4, labels=[1, 2, 3, 4])
    rfm['RFM_Segment'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

    def classify_rfm(row):
        if row['RFM_Segment'] == '444': return 'Champion'
        elif row['R_score'] == 4: return 'Loyal'
        elif row['F_score'] == 4: return 'Frequent'
        elif row['M_score'] == 4: return 'High Value'
        elif row['R_score'] == 1: return 'At Risk'
        else: return 'Others'

    rfm['Segment'] = rfm.apply(classify_rfm, axis=1)
    return rfm

# =============================
# HOME
# =============================
if page == "Home":
    st.title("RetentionOS – A User Turning Point")
    uploaded_file = st.file_uploader("📅 Upload CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            st.success("✅ File uploaded successfully!")
            st.dataframe(df.head())
        except Exception as e:
            st.error("❌ Failed to read file.")
            st.exception(e)

# =============================
# RFM Analysis
# =============================
elif page == "RFM Analysis":
    st.title("🧮 RFM Analysis")
    if st.session_state.df is None:
        st.warning("⚠️ Please upload your dataset from the Home page.")
    else:
        df = st.session_state.df.copy()
        mapping = smart_rfm_mapper(df)
        rfm = calculate_rfm(df, mapping)
        st.dataframe(rfm.head())

        st.subheader("📊 RFM Distributions")
        st.plotly_chart(px.histogram(rfm, x='recency', nbins=20, title="Recency Distribution"))
        st.plotly_chart(px.histogram(rfm, x='frequency', nbins=20, title="Frequency Distribution"))
        st.plotly_chart(px.histogram(rfm, x='monetary', nbins=20, title="Monetary Distribution"))

        st.subheader("🌎 Segment Breakdown")
        fig3 = px.pie(rfm, names='Segment', title="RFM Segment Share")
        st.plotly_chart(fig3, use_container_width=True)

        csv = rfm.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download RFM Data", data=csv, file_name="rfm_analysis.csv", mime="text/csv")
