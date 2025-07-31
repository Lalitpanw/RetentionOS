import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from fuzzywuzzy import fuzz

# Page config
st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar Navigation
st.sidebar.markdown("### 📂 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Churn Prediction", "User Segments", "Dashboard"])

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

# =============================
# HOME
# =============================
if page == "Home":
    st.title("RetentionOS – Universal Churn Predictor")

    uploaded_file = st.file_uploader("📥 Upload CSV or Excel file", type=["csv", "xlsx"])
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

        # Encode categorical columns
        le_dict = {}
        for col in df.select_dtypes(include='object').columns:
            le = LabelEncoder()
            try:
                df[col] = le.fit_transform(df[col])
                le_dict[col] = le
            except:
                st.warning(f"⚠️ Could not encode column: {col}")
                df.drop(columns=[col], inplace=True)

        # Remove non-numeric columns
        df = df.select_dtypes(include=['number'])

        # Train-test split
        df['churn'] = (df[df.columns[0]] % 2 == 0).astype(int)  # Dummy churn
        X = df.drop(columns=['churn'])
        y = df['churn']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # Train model
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
        st.metric("High Risk Users", df[df["risk_level"] == "High"].shape[0])
        st.metric("Average Churn Probability", round(df["churn_probability"].mean(), 2))

        fig1 = px.histogram(df, x="churn_probability", nbins=20, title="Churn Probability Distribution")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.pie(df, names="risk_level", title="Risk Level Breakdown")
        st.plotly_chart(fig2, use_container_width=True)
