import streamlit as st
import pandas as pd
import plotly.express as px
from fuzzywuzzy import fuzz
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# Page configuration
st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar Navigation with About at bottom
st.sidebar.markdown("### 📂 Navigation")
menu = ["Home", "Summary", "Dashboard", "Segments"]
section = st.sidebar.radio("Go to", menu)

st.sidebar.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
about_clicked = st.sidebar.button("🔍 About RetentionOS")

if "df" not in st.session_state:
    st.session_state.df = None

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

elif section == "Summary":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a file from the Home page first.")
    else:
        st.title("📈 User Summary Insights")
        st.subheader("📌 Sample Data")
        st.dataframe(st.session_state.df.head())

elif section == "Dashboard":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a file from the Home page first.")
    else:
        st.title("📊 Dashboard Metrics")
        df = st.session_state.df

        if "churn_score" in df.columns and "risk_level" in df.columns:
            st.metric("Total Users", len(df))
            st.metric("High Risk Users", df[df["risk_level"] == "🔴 High"].shape[0])
            st.metric("Average Churn Score", round(df["churn_score"].mean(), 2))

            st.subheader("Churn Score Distribution")
            fig1 = px.histogram(df, x="churn_score", nbins=20, title="Churn Score Histogram")
            st.plotly_chart(fig1, use_container_width=True)

            st.subheader("Risk Level Distribution")
            fig2 = px.pie(df, names="risk_level", title="Risk Level Breakdown")
            st.plotly_chart(fig2, use_container_width=True)

            if "cart_value" in df.columns:
                st.subheader("Cart Value by Risk Level")
                fig3 = px.box(df, x="risk_level", y="cart_value", title="Cart Value vs Risk Level")
                st.plotly_chart(fig3, use_container_width=True)

elif section == "Segments":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a file from the Home page first.")
    else:
        st.title("📌 Segmentation Insights")
        df = st.session_state.df

        expected_fields = {
            'last_active_days': ['last_seen', 'last_active', 'inactive_days'],
            'total_sessions': ['sessions', 'login_count', 'visits'],
            'orders': ['orders', 'purchases', 'transactions'],
            'revenue': ['amount_spent', 'order_value', 'lifetime_value'],
        }

        def auto_map_columns(df):
            mapping = {}
            for key, possible_names in expected_fields.items():
                for col in df.columns:
                    for option in possible_names:
                        if fuzz.partial_ratio(col.lower(), option.lower()) > 80:
                            mapping[key] = col
                            break
            return mapping

        mapping = auto_map_columns(df)

        st.markdown("### 🔍 Column Mapping")
        for key in expected_fields:
            if key not in mapping:
                mapping[key] = st.selectbox(f"Select column for **{key}**", df.columns)
            st.markdown(f"✅ `{key}` → `{mapping[key]}`")

        df = df.rename(columns={mapping[k]: k for k in mapping})

        # --- Machine Learning Prediction ---
        st.markdown("### 🧠 ML-Based Churn Prediction")
        df_clean = df.dropna(subset=["last_active_days", "orders", "total_sessions"])
        X = df_clean[["last_active_days", "orders", "total_sessions"]]
        y = (df_clean["orders"] == 0).astype(int)  # Simulated churn label: 1 if no orders

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = LogisticRegression()
        model.fit(X_scaled, y)

        df_clean["churn_probability"] = model.predict_proba(X_scaled)[:, 1]

        def label_risk(score):
            if score >= 0.7:
                return "🔴 High"
            elif score >= 0.4:
                return "🟠 Medium"
            else:
                return "🟢 Low"

        df_clean['risk_level'] = df_clean['churn_probability'].apply(label_risk)

        df_clean['churn_score'] = (df_clean['churn_probability'] * 3).round().astype(int)
        st.session_state.df = df_clean

        st.markdown("### 📊 Churn Risk Segments")
        selected_risk = st.selectbox("Select Risk Level", df_clean["risk_level"].unique())
        filtered = df_clean[df_clean["risk_level"] == selected_risk]
        st.write(f"Filtered users in {selected_risk} risk: {filtered.shape[0]}")
        st.dataframe(filtered)

else:
    st.info("👆 Upload a CSV or Excel file to begin.")
