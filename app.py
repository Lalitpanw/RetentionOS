import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="RetentionOS", layout="wide")

st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio(
    " ",
    [
        "📂 Data Upload",
        "📊 Churn Overview",
        "👥 User Segments",
        "💬 Nudge Suggestions",
        "📈 Impact Snapshot",
        "📉 Impact Tracker"
    ],
    label_visibility="collapsed"
)

st.markdown(
    """
    <h2 style='font-family: Inter, sans-serif; font-weight: 600; margin-bottom: 0.5rem;'>
    🚀 RetentionOS
    </h2>
    <p style='font-size: 16px; margin-top: -10px; color: #444;'>Predict. Segment. Re-engage.</p>
    """,
    unsafe_allow_html=True
)

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
# 📂 Upload Page
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

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Processed File (CSV)",
                    data=csv,
                    file_name='churn_prediction_output.csv',
                    mime='text/csv'
                )

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ----------------------------
# 📊 Churn Overview
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
# 👥 Segments
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
# 💬 Nudge Suggestions
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
# 📈 Impact Snapshot
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

# ----------------------------
# 📉 Impact Tracker – New Feature!
# ----------------------------
elif page == "📉 Impact Tracker":
    st.title("📉 Nudge Impact Tracker")

    st.markdown("#### Step 1: Upload your PREVIOUS scored file (with churn_risk)")
    prev_file = st.file_uploader("Upload previous scored CSV", key="prev_file", type=["csv"])

    st.markdown("#### Step 2: Upload NEW behavior data (post-nudge)")
    new_file = st.file_uploader("Upload new user behavior file", key="new_file", type=["csv", "xlsx"])

    if prev_file and new_file and model:
        try:
            prev_df = pd.read_csv(prev_file)
            prev_df = prev_df[['user_id', 'churn_risk']]
            prev_df.rename(columns={'churn_risk': 'churn_risk_before'}, inplace=True)

            new_df = pd.read_csv(new_file) if new_file.name.endswith(".csv") else pd.read_excel(new_file)
            new_df, _ = smart_map_columns(new_df)

            if 'user_id' not in new_df.columns:
                st.error("❌ 'user_id' column is required in new behavior data.")
            else:
                X = new_df[REQUIRED_COLS]
                churn_probs = model.predict_proba(X)[:, 1]
                new_df['churn_probability'] = churn_probs.round(2)
                new_df['churn_risk_after'] = new_df['churn_probability'].apply(assign_churn_risk)

                merged = pd.merge(prev_df, new_df[['user_id', 'churn_risk_after']], on='user_id', how='inner')

                total_users = len(merged)
                improved = len(merged[(merged['churn_risk_before'] == "🔴 High") & (merged['churn_risk_after'] != "🔴 High")])
                no_change = len(merged[merged['churn_risk_before'] == merged['churn_risk_after']])
                worsened = len(merged[(merged['churn_risk_before'] != "🔴 High") & (merged['churn_risk_after'] == "🔴 High")])

                st.success(f"✅ Compared {total_users} users.")
                st.metric("🙌 Improved Users", improved)
                st.metric("⚠️ Unchanged Risk", no_change)
                st.metric("🔻 Risk Worsened", worsened)

                st.subheader("📄 Risk Comparison Table")
                st.dataframe(merged)

        except Exception as e:
            st.error(f"❌ Error comparing files: {e}")
