import streamlit as st
import pandas as pd
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
st.write("✅ App loaded")

# ----------------------------
# Load the trained model
# ----------------------------
@st.cache_resource
def load_model():
    try:
        model = joblib.load("churn_model.pkl")
        return model
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        return None

model = load_model()

REQUIRED_COLS = ['product_views', 'cart_items', 'total_sessions', 'last_active_days', 'orders', 'cart_value']

# ----------------------------
# Column mapping logic
# ----------------------------
def smart_map_columns(df):
    rename_map = {}
    mapping = {
        'product_views': ['views', 'page_views'],
        'cart_items': ['items_in_cart', 'cart_count'],
        'total_sessions': ['sessions', 'session_count'],
        'last_active_days': ['inactive_days', 'last_seen_days'],
        'orders': ['purchases', 'number_of_orders'],
        'cart_value': ['basket_value', 'order_value']
    }

    for standard, aliases in mapping.items():
        for alias in aliases:
            match = [col for col in df.columns if alias.lower() in col.lower()]
            if match:
                rename_map[match[0]] = standard
                break

    df = df.rename(columns=rename_map)
    return df, rename_map

def assign_churn_risk(prob):
    if prob >= 0.75:
        return "🔴 High"
    elif prob >= 0.4:
        return "🟠 Medium"
    else:
        return "🟢 Low"

if "df" not in st.session_state:
    st.session_state.df = None

# ----------------------------
# 📂 Page: Upload
# ----------------------------
if page == "📂 Data Upload":
    st.subheader("📂 Upload CSV or Excel")
    uploaded_file = st.file_uploader("Upload file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            df, mapped = smart_map_columns(df)

            missing = [col for col in REQUIRED_COLS if col not in df.columns]
            if missing:
                st.error(f"❌ Missing required columns: {', '.join(missing)}")
            else:
                if mapped:
                    st.markdown("#### 🔍 Column Mapping Detected:")
                    for k, v in mapped.items():
                        st.write(f"`{k}` → `{v}`")

                X = df[REQUIRED_COLS]
                churn_probs = model.predict_proba(X)[:, 1]
                df['churn_probability'] = churn_probs.round(2)
                df['churn_risk'] = df['churn_probability'].apply(assign_churn_risk)

                st.session_state.df = df
                st.success("✅ Prediction complete!")
                st.dataframe(df.head())

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ----------------------------
# 📊 Page: Churn Overview
# ----------------------------
elif page == "📊 Churn Overview":
    st.title("📊 Churn Risk Overview")
    if st.session_state.df is not None:
        df = st.session_state.df
        st.metric("Total Users", len(df))
        st.metric("🔴 High Risk", sum(df['churn_risk'] == "🔴 High"))
        st.metric("🟠 Medium Risk", sum(df['churn_risk'] == "🟠 Medium"))
        st.metric("🟢 Low Risk", sum(df['churn_risk'] == "🟢 Low"))
        st.bar_chart(df['churn_risk'].value_counts())
    else:
        st.warning("⚠️ Please upload data first.")

# ----------------------------
# 👥 Page: User Segments
# ----------------------------
elif page == "👥 User Segments":
    st.title("👥 User Segments")
    if st.session_state.df is not None:
        df = st.session_state.df
        risk = st.selectbox("Select Segment", ["🔴 High", "🟠 Medium", "🟢 Low"])
        st.dataframe(df[df['churn_risk'] == risk])
    else:
        st.warning("⚠️ Please upload data first.")

# ----------------------------
# 💬 Page: Nudge Suggestions
# ----------------------------
elif page == "💬 Nudge Suggestions":
    st.title("💬 Suggested Nudges")
    if st.session_state.df is not None:
        st.markdown("- 📲 WhatsApp: “We miss you! Use code WELCOME10 for 10% off.”")
        st.markdown("- 📩 Email: “Your cart is waiting – come back!”")
        st.markdown("- 🎯 Focus on 🔴 High risk users.")
    else:
        st.warning("⚠️ Please upload data first.")

# ----------------------------
# 📈 Page: Impact Snapshot
# ----------------------------
elif page == "📈 Impact Snapshot":
    st.title("📈 Impact Projection")
    if st.session_state.df is not None:
        df = st.session_state.df
        high_risk = df[df['churn_risk'] == "🔴 High"]
        saved = int(len(high_risk) * 0.3)
        st.metric("High Risk Users", len(high_risk))
        st.metric("Projected Saved (via campaign)", saved)
    else:
        st.warning("⚠️ Please upload data first.")
