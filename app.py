import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="RetentionOS", layout="wide")

st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", [
    "📂 Data Upload",
    "📊 Churn Overview",
    "👥 User Segments",
    "💬 Nudge Suggestions",
    "📈 Impact Snapshot"
])

st.markdown("# 🚀 RetentionOS – Predict. Segment. Re-engage.")
st.markdown("Upload user data → Predict churn → Auto-nudge users.")

# Load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load("churn_model.pkl")
        st.write("✅ ML model loaded.")
        return model
    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")
        return None

model = load_model()

# Required features for prediction
REQUIRED_COLS = ['product_views', 'cart_items', 'total_sessions', 'last_active_days', 'orders', 'cart_value']

# Map uploaded column names to required
COLUMN_ALIASES = {
    'number_of_purchases': 'orders',
    'sessions_last_7_days': 'total_sessions',
    'last_seen_days': 'last_active_days',
    'purchases': 'orders',
    'value': 'cart_value'
}

def map_columns(df):
    for col in df.columns:
        if col in COLUMN_ALIASES:
            df.rename(columns={col: COLUMN_ALIASES[col]}, inplace=True)
    return df

def assign_churn_risk(prob):
    if prob >= 0.75:
        return "🔴 High"
    elif prob >= 0.4:
        return "🟠 Medium"
    else:
        return "🟢 Low"

if "df" not in st.session_state:
    st.session_state.df = None

# 📂 PAGE: Upload
if page == "📂 Data Upload":
    st.subheader("📂 Data Upload")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            df = map_columns(df)

            missing = [col for col in REQUIRED_COLS if col not in df.columns]
            if missing:
                st.error(f"Missing required column(s): {', '.join(missing)}")
            else:
                df_model = df.copy()
                X = df_model[REQUIRED_COLS]

                # Predict
                churn_probs = model.predict_proba(X)[:, 1]
                df['churn_probability'] = churn_probs
                df['churn_risk'] = df['churn_probability'].apply(assign_churn_risk)

                st.session_state.df = df
                st.success("✅ File uploaded and processed!")
                st.dataframe(df.head())

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

    st.markdown("📥 Don’t have a dataset? [Download sample](https://raw.githubusercontent.com/lalitpanw/RetentionOS/main/sample.csv)")

# 📊 PAGE: Churn Overview
elif page == "📊 Churn Overview":
    st.title("📊 Churn Overview")
    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        st.metric("Total Users", len(df))
        st.metric("High Risk Users", sum(df['churn_risk'] == "🔴 High"))
        st.metric("Medium Risk", sum(df['churn_risk'] == "🟠 Medium"))
        st.metric("Low Risk", sum(df['churn_risk'] == "🟢 Low"))
        st.bar_chart(df['churn_risk'].value_counts())
    else:
        st.warning("⚠️ Please upload data first.")

# 👥 PAGE: Segments
elif page == "👥 User Segments":
    st.title("👥 User Segments")
    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        segment = st.selectbox("Select Churn Segment", ["🔴 High", "🟠 Medium", "🟢 Low"])
        st.dataframe(df[df['churn_risk'] == segment])
    else:
        st.warning("⚠️ Please upload data first.")

# 💬 PAGE: Nudges
elif page == "💬 Nudge Suggestions":
    st.title("💬 Nudge Suggestions")
    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        st.write("🚨 For High Risk Users, suggest offers like:")
        st.markdown("- 💸 10% Discount on next purchase\n- 🔁 Win-back Email\n- 📲 WhatsApp reminder")
    else:
        st.warning("⚠️ Please upload data first.")

# 📈 PAGE: Snapshot
elif page == "📈 Impact Snapshot":
    st.title("📈 Impact Snapshot")
    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        st.write("📍 Assume campaign applied on High Risk users")
        before = len(df[df['churn_risk'] == "🔴 High"])
        after = int(before * 0.7)  # Dummy assumption
        st.metric("Churn Before", before)
        st.metric("Churn After (Projected)", after)
    else:
        st.warning("⚠️ Please upload data first.")
