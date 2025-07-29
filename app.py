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

# ✅ DEBUG: Confirm app loaded
st.write("✅ App started")

# ----------------------------
# Load ML model
# ----------------------------
@st.cache_resource
def load_model():
    try:
        model = joblib.load("churn_model.pkl")
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None

model = load_model()

REQUIRED_COLS = ['product_views', 'cart_items', 'total_sessions', 'last_active_days', 'orders', 'cart_value']

# ----------------------------
# Smart column mapper
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

    for target, aliases in mapping.items():
        for alias in aliases:
            match = [col for col in df.columns if alias.lower() in col.lower()]
            if match:
                rename_map[match[0]] = target
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
# Page: Upload
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
            st.error(f"❌ Error processing file: {e}")

