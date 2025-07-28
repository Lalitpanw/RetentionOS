import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="RetentionOS", layout="wide")

# -------------------------------
# 🧠 Churn Scoring Logic with Column Validation
# -------------------------------
def process_churn_scores(df):
    df = df.copy()
    required_cols = ['last_active_days', 'orders', 'total_sessions']
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise KeyError(f"Missing required column(s): {', '.join(missing)}")

    def churn_score(row):
        score = 0
        if row['last_active_days'] > 14:
            score += 1
        if row['orders'] < 1:
            score += 1
        if row['total_sessions'] < 3:
            score += 1
        return score

    def risk_label(score):
        if score >= 2:
            return "🔴 High"
        elif score == 1:
            return "🟠 Medium"
        else:
            return "🟢 Low"

    df['churn_score'] = df.apply(churn_score, axis=1)
    df['churn_risk'] = df['churn_score'].apply(risk_label)

    return df

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("🔎 Navigation")
page = st.sidebar.radio("Go to", [
    "📁 Data Upload",
    "📊 Churn Overview",
    "👥 User Segments",
    "💬 Nudge Suggestions",
    "📈 Impact Snapshot"
])

if 'df' not in st.session_state:
    st.session_state.df = None

# -------------------------------
# 📁 Data Upload Page
# -------------------------------
if page == "📁 Data Upload":
    st.title("🚀 RetentionOS – Predict. Segment. Re-engage.")
    st.markdown("_Upload user data → Identify churn risk → Auto-nudge users_")

    st.header("📁 Data Upload")
    st.markdown("Upload your user data (CSV or Excel) to begin")

    st.markdown("📝 **Required Columns:** `last_active_days`, `orders`, `total_sessions`")

    uploaded_file = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            processed_df = process_churn_scores(df)
            st.session_state.df = processed_df
            st.success("✅ File uploaded and processed! Now move to 'Churn Overview' ➡")

        except KeyError as e:
            st.error(f"⚠️ Error: {e}")

    # Sample CSV download
    sample_data = {
        'user_id': [101, 102, 103],
        'last_active_days': [3, 18, 27],
        'total_sessions': [12, 4, 1],
        'orders': [3, 1, 0],
        'revenue': [499, 149, 0]
    }
    sample_df = pd.DataFrame(sample_data)
    csv_data = sample_df.to_csv(index=False).encode('utf-8')

    st.markdown("#### 📥 Don't have data? Download a sample to try it out:")
    st.download_button(
        label="⬇️ Download Sample CSV",
        data=csv_data,
        file_name="sample_retentionos.csv",
        mime="text/csv"
    )

# -------------------------------
# 📊 Churn Overview Page
# -------------------------------
elif page == "📊 Churn Overview":
    st.title("📊 Churn Overview")

    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        st.markdown("_Summary of churn scores and user distribution_")

        total_users = len(df)
        high_risk = (df['churn_risk'] == "🔴 High").sum()
        medium_risk = (df['churn_risk'] == "🟠 Medium").sum()
        low_risk = (df['churn_risk'] == "🟢 Low").sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👥 Total Users", total_users)
        col2.metric("🔴 High Risk", high_risk)
        col3.metric("🟠 Medium Risk", medium_risk)
        col4.metric("🟢 Low Risk", low_risk)

        st.markdown("### 📊 Churn Risk Distribution")
        st.bar_chart(df['churn_risk'].value_counts())

        st.markdown("### 👁 Preview with Scores")
        st.dataframe(df[['user_id', 'last_active_days', 'total_sessions', 'orders', 'churn_risk']])
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")

# -------------------------------
# 👥 User Segments Page
# -------------------------------
elif page == "👥 User Segments":
    st.title("👥 User Segments")

    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        st.markdown("_Segmented view by churn risk level_")

        st.subheader("🔴 High Risk Users")
        st.dataframe(df[df['churn_risk'] == "🔴 High"])

        st.subheader("🟠 Medium Risk Users")
        st.dataframe(df[df['churn_risk'] == "🟠 Medium"])

        st.subheader("🟢 Low Risk Users")
        st.dataframe(df[df['churn_risk'] == "🟢 Low"])
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")

# -------------------------------
# 💬 Nudge Suggestions Page
# -------------------------------
elif page == "💬 Nudge Suggestions":
    st.title("💬 Nudge Suggestions")

    if st.session_state.df is not None:
        st.markdown("_Auto-generated WhatsApp/Email nudges based on churn risk_")

        st.subheader("🔴 High Risk")
        st.code("👋 Hey there! We noticed you haven’t been active lately. Come back today and get 15% off your next purchase!")

        st.subheader("🟠 Medium Risk")
        st.code("👋 We miss you! Use code WELCOME10 for 10% off your next session.")

        st.subheader("🟢 Low Risk")
        st.code("Thanks for being an active user! Here's a sneak peek at what’s coming next…")
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")

# -------------------------------
# 📈 Impact Snapshot Page
# -------------------------------
elif page == "📈 Impact Snapshot":
    st.title("📈 Impact Snapshot")

    if st.session_state.df is not None:
        df = st.session_state.df.copy()

        high_risk = (df['churn_risk'] == "🔴 High").sum()
        est_saved = int(high_risk * 0.2)  # assume 20% response rate
        value_per_user = df['revenue'].mean() if 'revenue' in df.columns else 0
        est_revenue = int(est_saved * value_per_user)

        st.markdown("### 📌 Projected Retention Impact")
        st.metric("🧍 Users at Risk", high_risk)
        st.metric("✅ Est. Users Retained (20%)", est_saved)
        st.metric("💰 Est. Revenue Saved", f"₹ {est_revenue}")
    else:
        st.warning("⚠️ Please upload a file in 'Data Upload' first.")
