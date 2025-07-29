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

# -------------------------
# 🔌 Load Model
# -------------------------
@st.cache_resource
def load_model():
    try:
        model = joblib.load("churn_model.pkl")
        return model
    except Exception as e:
        st.error(f"❌ Failed to load ML model: {e}")
        return None

model = load_model()

# -------------------------
# 🧠 Universal Column Mapping
# -------------------------
REQUIRED_COLS = ['product_views', 'cart_items', 'total_sessions', 'last_active_days', 'orders', 'cart_value']

COLUMN_ALIASES = {
    'product_views': ['views', 'page_views', 'browses'],
    'cart_items': ['items_in_cart', 'cart_count'],
    'total_sessions': ['sessions', 'session_count', 'visits'],
    'last_active_days': ['inactive_days', 'days_since_last_visit'],
    'orders': ['purchases', 'number_of_orders'],
    'cart_value': ['basket_value', 'total_cart_value']
}

def smart_map_columns(df):
    rename_map = {}
    for target_col, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            matches = [col for col in df.columns if alias.lower() in col.lower()]
            if matches:
                rename_map[matches[0]] = target_col
                break
    return df.rename(columns=rename_map), rename_map

def assign_churn_risk(prob):
    if prob >= 0.75:
        return "🔴 High"
    elif prob >= 0.4:
        return "🟠 Medium"
    else:
        return "🟢 Low"

if "df" not in st.session_state:
    st.session_state.df = None

# -------------------------
# 📂 Page: Upload
# -------------------------
if page == "📂 Data Upload":
    st.subheader("📂 Upload User CSV or Excel")
    uploaded_file = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            # Read file
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)

            # Map unknown columns
            df, mapped = smart_map_columns(df)

            # Check required columns
            missing = [col for col in REQUIRED_COLS if col not in df.columns]
            if missing:
                st.error(f"❌ Missing required column(s): {', '.join(missing)}")
            else:
                st.success("✅ All required columns detected. Processing...")

                # Show detected mappings
                if mapped:
                    st.markdown("#### 🔍 Column Mapping Detected:")
                    for original, new_col in mapped.items():
                        st.write(f"`{original}` → `{new_col}`")

                # Run prediction
                X = df[REQUIRED_COLS]
                churn_probs = model.predict_proba(X)[:, 1]
                df['churn_probability'] = churn_probs.round(2)
                df['churn_risk'] = df['churn_probability'].apply(assign_churn_risk)

                st.session_state.df = df
                st.success("✅ Prediction complete!")
                st.dataframe(df.head())

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

    st.markdown("📥 Don’t have data? [Download sample file](https://raw.githubusercontent.com/lalitpanw/RetentionOS/main/sample.csv)")

# -------------------------
# 📊 Page: Churn Overview
# -------------------------
elif page == "📊 Churn Overview":
    st.title("📊 Churn Risk Breakdown")
    if st.session_state.df is not None:
        df = st.session_state.df
        st.metric("Total Users", len(df))
        st.metric("🔴 High Risk", sum(df['churn_risk'] == "🔴 High"))
        st.metric("🟠 Medium Risk", sum(df['churn_risk'] == "🟠 Medium"))
        st.metric("🟢 Low Risk", sum(df['churn_risk'] == "🟢 Low"))
        st.bar_chart(df['churn_risk'].value_counts())
    else:
        st.warning("⚠️ Please upload data first.")

# -------------------------
# 👥 Page: Segments
# -------------------------
elif page == "👥 User Segments":
    st.title("👥 User Segments")
    if st.session_state.df is not None:
        df = st.session_state.df
        risk = st.selectbox("Select Risk Segment", ["🔴 High", "🟠 Medium", "🟢 Low"])
        st.dataframe(df[df['churn_risk'] == risk])
    else:
        st.warning("⚠️ Please upload data first.")

# -------------------------
# 💬 Page: Nudge Suggestions
# -------------------------
elif page == "💬 Nudge Suggestions":
    st.title("💬 Suggested Nudges")
    if st.session_state.df is not None:
        st.markdown("- 📲 WhatsApp: “We miss you! Use code WELCOME10 for 10% off.”")
        st.markdown("- 📩 Email: “Get back to shopping – your cart is waiting!”")
        st.markdown("- 🎯 Segment: Target 🔴 High risk users with special offers.")
    else:
        st.warning("⚠️ Please upload data first.")

# -------------------------
# 📈 Page: Impact Snapshot
# -------------------------
elif page == "📈 Impact Snapshot":
    st.title("📈 Impact Simulation")
    if st.session_state.df is not None:
        df = st.session_state.df
        high = df[df['churn_risk'] == "🔴 High"]
        improved = int(len(high) * 0.3)  # Assume 30% saved
        st.metric("High Risk Users", len(high))
        st.metric("Saved by Campaign", improved)
    else:
        st.warning("⚠️ Please upload data first.")
