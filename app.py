import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="RetentionOS", layout="wide")

# -------------------------------
# 🧠 Auto-map close column names
# -------------------------------
def auto_map_columns(df):
    expected = {
        'last_active_days': ['last_active', 'inactive_days', 'last_seen', 'days_since_active'],
        'orders': ['orders', 'purchases', 'transactions', 'total_orders'],
        'total_sessions': ['sessions', 'visits', 'login_count']
    }
    mapping = {}
    for standard_col, options in expected.items():
        for col in df.columns:
            if col.lower() == standard_col:
                mapping[standard_col] = col
                break
            for alt in options:
                if alt.lower() in col.lower():
                    mapping[standard_col] = col
                    break
    return mapping

# -------------------------------
# 🧠 Churn Scoring Logic
# -------------------------------
def process_churn_scores(df):
    df = df.copy()

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
    uploaded_file = st.file_uploader("Upload CSV or XLSX", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # 🧠 Auto-map columns
            mapping = auto_map_columns(df)
            required = ['last_active_days', 'orders', 'total_sessions']
            if not all(col in mapping for col in required):
                missing = [col for col in required if col not in mapping]
                raise KeyError(f"Missing required data fields: {', '.join(missing)}")

            df = df.rename(columns={v: k for k, v in mapping.items()})
            processed_df = process_churn_scores(df)
            st.session_state.df = processed_df
            st.success("✅ File uploaded and auto-mapped successfully!")

            # Show mapping
            st.markdown("#### 🔍 Column Mapping Detected:")
            for k, v in mapping.items():
                st.markdown(f"`{k}` → **{v}**")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

    # Sample CSV download
    sample_data = {
        'user_id': [101, 102, 103],
        'last_seen': [3, 18, 27],
        'login_count': [12, 4, 1],
        'transactions': [3, 1, 0],
        'revenue': [499, 149, 0]
    }
    sample_df = pd.DataFrame(sample_data)
    csv_data = sample_df.to_csv(index=False).encode('utf-8')

    st.markdown("#### 📥 Try Sample File:")
    st.download_button(
        label="⬇️ Download Sample CSV",
        data=csv_data,
        file_name="sample_retentionos.csv",
        mime="text/csv"
    )

# -------------------------------
# 📊 Churn Overview
# -------------------------------
elif page == "📊 Churn Overview":
    st.title("📊 Churn Overview")
    if st.session_state.df is not None:
        df = st.session_state.df.copy()

        total_users = len(df)
        high_risk = (df['churn_risk'] == "🔴 High").sum()
        medium_risk = (df['churn_risk'] == "🟠 Medium").sum()
        low_risk = (df['churn_risk'] == "🟢 Low").sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👥 Total Users", total_users)
        col2.metric("🔴 High Risk", high_risk)
        col3.metric("🟠 Medium Risk", medium_risk)
        col4.metric("🟢 Low Risk", low_risk)

        st.markdown("### 📊 Risk Breakdown")
        st.bar_chart(df['churn_risk'].value_counts())

        st.markdown("### 🔍 Preview Table")
        st.dataframe(df[['user_id', 'last_active_days', 'total_sessions', 'orders', 'churn_risk']])
    else:
        st.warning("⚠️ Please upload data first.")

# -------------------------------
# 👥 User Segments
# -------------------------------
elif page == "👥 User Segments":
    st.title("👥 User Segments")
    if st.session_state.df is not None:
        df = st.session_state.df.copy()
        st.subheader("🔴 High Risk Users")
        st.dataframe(df[df['churn_risk'] == "🔴 High"])

        st.subheader("🟠 Medium Risk Users")
        st.dataframe(df[df['churn_risk'] == "🟠 Medium"])

        st.subheader("🟢 Low Risk Users")
        st.dataframe(df[df['churn_risk'] == "🟢 Low"])
    else:
        st.warning("⚠️ Please upload data first.")

# -------------------------------
# 💬 Nudge Suggestions
# -------------------------------
elif page == "💬 Nudge Suggestions":
    st.title("💬 Nudge Suggestions")
    if st.session_state.df is not None:
        st.markdown("_Auto-generated WhatsApp/Email messages based on user segment_")

        st.subheader("🔴 High Risk")
        st.code("👋 We noticed you haven’t visited lately. Come back today and get 20% off!")

        st.subheader("🟠 Medium Risk")
        st.code("👋 Quick reminder! Use code 'STAY10' for 10% off your next session.")

        st.subheader("🟢 Low Risk")
        st.code("Thanks for being with us! Here's what’s coming next…")
    else:
        st.warning("⚠️ Please upload data first.")

# -------------------------------
# 📈 Impact Snapshot
# -------------------------------
elif page == "📈 Impact Snapshot":
    st.title("📈 Impact Snapshot")
    if st.session_state.df is not None:
        df = st.session_state.df.copy()

        high_risk = (df['churn_risk'] == "🔴 High").sum()
        est_saved = int(high_risk * 0.2)
        value_per_user = df['revenue'].mean() if 'revenue' in df.columns else 0
        est_revenue = int(est_saved * value_per_user)

        st.metric("🧍 At-Risk Users", high_risk)
        st.metric("✅ Projected Saved (20%)", est_saved)
        st.metric("💰 Potential Revenue Recovered", f"₹ {est_revenue}")
    else:
        st.warning("⚠️ Please upload data first.")
