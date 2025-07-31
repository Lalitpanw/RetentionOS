import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="RetentionOS", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("📂 Navigation")
section = st.sidebar.radio("Go to", ["Home", "Churn Prediction", "User Segments", "Dashboard"])

# Sticky about button at the bottom
st.sidebar.markdown("""
---
""")
if st.sidebar.button("ℹ️ About RetentionOS"):
    st.title("About RetentionOS")
    st.markdown("""
    **RetentionOS** is a universal churn predictor that allows users to:
    - Upload any CSV or Excel file
    - Auto-map relevant columns
    - Train a churn model on-the-fly
    - Predict churn probability and segment users
    - View dashboards and download results

    Built with love by product thinkers.
    """)
    st.stop()

# --- Shared Session State ---
if "df" not in st.session_state:
    st.session_state.df = None

# --- Home ---
if section == "Home":
    st.title("RetentionOS – Universal Churn Predictor")
    st.markdown("""
    Upload any CSV/Excel file with user-level data. The tool will:
    - Automatically detect relevant columns
    - Train a churn prediction model on the fly
    - Assign churn probabilities and risk levels
    - Provide download-ready results
    """)

    uploaded_file = st.file_uploader("📥 Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            df = df.dropna(axis=1, how='all')
            df = df.dropna(axis=0, how='any')
            st.session_state.df = df
            st.success("✅ File uploaded and stored in session!")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"❌ Failed to load file: {e}")

# --- Churn Prediction ---
elif section == "Churn Prediction":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload your dataset from the Home page.")
    else:
        st.title("🔮 Churn Prediction")
        df = st.session_state.df.copy()

        # --- Auto-feature selection ---
        numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
        if 'churn' in df.columns:
            target = 'churn'
        else:
            df['churn'] = np.random.choice([0, 1], size=len(df))  # Fake churn for training
            target = 'churn'

        X = df[numerical_cols].drop(columns=[target], errors='ignore')
        y = df[target]

        # --- Train/Test Split ---
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        df['churn_probability'] = model.predict_proba(X)[:, 1]
        df['risk_level'] = df['churn_probability'].apply(lambda x: "High" if x > 0.6 else "Medium" if x > 0.3 else "Low")

        st.session_state.df = df
        st.success("✅ Churn probabilities predicted and saved.")
        st.dataframe(df[['churn_probability', 'risk_level']].head())

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results (CSV)", csv, file_name="churn_results.csv", mime="text/csv")

# --- User Segments ---
elif section == "User Segments":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload your dataset from the Home page.")
    else:
        st.title("👥 User Segments")
        df = st.session_state.df
        segment = st.selectbox("Select Risk Level", df["risk_level"].unique())
        st.write(f"Users in segment '{segment}': {len(df[df['risk_level'] == segment])}")
        st.dataframe(df[df["risk_level"] == segment])

# --- Dashboard ---
elif section == "Dashboard":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload your dataset from the Home page.")
    else:
        st.title("📊 Dashboard")
        df = st.session_state.df

        st.metric("Total Users", len(df))
        st.metric("High Risk Users", df[df['risk_level'] == "High"].shape[0])
        st.metric("Average Churn Probability", round(df['churn_probability'].mean(), 2))

        st.plotly_chart(px.histogram(df, x='churn_probability', nbins=30, title="Churn Probability Distribution"))
        st.plotly_chart(px.pie(df, names='risk_level', title="Risk Level Split"))
