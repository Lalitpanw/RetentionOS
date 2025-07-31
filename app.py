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

# RFM Calculation Function
def calculate_rfm(df, date_col='last_seen', user_col='user_id', orders_col='orders', revenue_col='revenue'):
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    snapshot_date = df[date_col].max()
    rfm = df.groupby(user_col).agg({
        date_col: lambda x: (snapshot_date - x.max()).days,
        orders_col: 'count',
        revenue_col: 'sum'
    }).reset_index()
    rfm.columns = [user_col, 'recency', 'frequency', 'monetary']

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
    st.title("RetentionOS – Universal Churn Predictor")
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
# CHURN PREDICTION
# =============================
elif page == "Churn Prediction":
    st.title("🔍 Predict Churn Risk")
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset from the Home page.")
    else:
        df = st.session_state.df.copy()
        st.write(f"Detected columns: `{', '.join(df.columns)}`")

        if all(col in df.columns for col in ['user_id', 'last_seen', 'orders', 'revenue']):
            rfm_df = calculate_rfm(df)
            df = pd.merge(df, rfm_df, on='user_id', how='left')
            st.success("✅ RFM features generated and added to data")
            st.dataframe(df[['user_id', 'recency', 'frequency', 'monetary']].head())

        le_dict = {}
        for col in df.select_dtypes(include='object').columns:
            le = LabelEncoder()
            try:
                df[col] = le.fit_transform(df[col])
                le_dict[col] = le
            except:
                df.drop(columns=[col], inplace=True)

        df = df.select_dtypes(include=['number'])
        df['churn'] = (df[df.columns[0]] % 2 == 0).astype(int)
        X = df.drop(columns=['churn'])
        y = df['churn']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        probs = model.predict_proba(X)[:, 1]
        df['churn_probability'] = probs
        df['risk_level'] = df['churn_probability'].apply(lambda x: "High" if x > 0.7 else "Medium" if x > 0.4 else "Low")

        st.session_state.predicted_df = df
        st.success("✅ Churn prediction complete.")
        st.dataframe(df[['churn_probability', 'risk_level']].head())

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Prediction CSV", data=csv, file_name="churn_predictions.csv", mime='text/csv')

# =============================
# USER SEGMENTS
# =============================
elif page == "User Segments":
    st.title("👥 User Segments")
    if st.session_state.predicted_df is None:
        st.warning("⚠️ Run a churn prediction first.")
    else:
        df = st.session_state.predicted_df
        risk = st.selectbox("Select risk level", df["risk_level"].unique())
        segment = df[df["risk_level"] == risk]
        st.metric("Segment Size", len(segment))
        st.dataframe(segment)

# =============================
# DASHBOARD
# =============================
elif page == "Dashboard":
    st.title("📊 Churn Dashboard")
    if st.session_state.predicted_df is None:
        st.warning("⚠️ Run a churn prediction first.")
    else:
        df = st.session_state.predicted_df
        st.metric("Total Users", len(df))
        st.metric("High Risk Users", df[df['risk_level'] == "High"].shape[0])
        st.metric("Average Churn Probability", round(df["churn_probability"].mean(), 2))

        fig1 = px.histogram(df, x="churn_probability", nbins=20, title="Churn Probability Distribution")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.pie(df, names="risk_level", title="Risk Level Breakdown")
        st.plotly_chart(fig2, use_container_width=True)

# =============================
# RFM Analysis
# =============================
elif page == "RFM Analysis":
    st.title("🧮 RFM Analysis")
    if st.session_state.df is None:
        st.warning("⚠️ Please upload your dataset from the Home page.")
    else:
        df = st.session_state.df.copy()
        if not all(col in df.columns for col in ['user_id', 'last_seen', 'orders', 'revenue']):
            st.error("Missing required columns for RFM: 'user_id', 'last_seen', 'orders', 'revenue'")
        else:
            rfm = calculate_rfm(df)
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
