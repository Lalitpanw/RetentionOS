import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="RetentionOS", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.title("🧭 Navigation")
section = st.sidebar.radio("Go to", ["Home", "Summary", "Dashboard", "Segmentation Insights"])

# --- Session State for Data ---
if 'df' not in st.session_state:
    st.session_state['df'] = None

# --- HOME SECTION ---
if section == "Home":
    st.title("📊 RetentionOS – Upload User Data")
    uploaded_file = st.file_uploader("Upload your user Excel/CSV file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.session_state['df'] = df
            st.success("✅ File uploaded successfully!")
            st.dataframe(df.head())

            # --- Download button ---
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download This Data as CSV",
                data=csv,
                file_name='retention_data.csv',
                mime='text/csv'
            )

        except Exception as e:
            st.error(f"Error: {e}")

# --- SUMMARY SECTION ---
elif section == "Summary":
    st.title("📈 User Summary Insights")

    if st.session_state['df'] is None:
        st.warning("⚠️ Please upload a file in the Home section.")
    else:
        df = st.session_state['df']

        # --- Metrics ---
        st.markdown("### 📊 Overview Metrics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("👥 Total Users", len(df))

        with col2:
            avg_churn = round(df['churn_score'].mean(), 2)
            st.metric("📉 Avg. Churn Score", avg_churn)

        with col3:
            high_risk_count = df[df['risk_level'] == 'High'].shape[0]
            st.metric("🚨 High Risk Users", high_risk_count)

        # --- Charts ---
        st.markdown("### 📊 Visual Insights")
        col4, col5 = st.columns(2)

        with col4:
            st.write("#### Gender Distribution")
            gender_dist = df['gender'].value_counts().reset_index()
            gender_dist.columns = ['Gender', 'Count']
            fig_gender = px.bar(gender_dist, x='Gender', y='Count', color='Gender', title="Users by Gender")
            st.plotly_chart(fig_gender, use_container_width=True)

        with col5:
            st.write("#### Risk Level Distribution")
            risk_dist = df['risk_level'].value_counts().reset_index()
            risk_dist.columns = ['Risk Level', 'Users']
            fig_risk = px.pie(risk_dist, values='Users', names='Risk Level', title="Risk Level Share", hole=0.3)
            st.plotly_chart(fig_risk, use_container_width=True)

        # --- Top Risk Users ---
        st.markdown("### 🔥 Top 5 Users at Churn Risk")
        top_risk_users = df.sort_values(by='churn_score', ascending=False).head(5)
        st.dataframe(top_risk_users[['user_id', 'churn_score', 'risk_level', 'nudge_recommendation']])

        # --- Nudge Recommendation Summary ---
        st.markdown("### 📬 Nudge Recommendation Breakdown")
        nudge_summary = df['nudge_recommendation'].value_counts().reset_index()
        nudge_summary.columns = ['Nudge Recommendation', 'User Count']
        st.dataframe(nudge_summary)

        # --- Sample Data ---
        st.markdown("### 🔍 Sample Data Preview")
        st.dataframe(df.head())


# --- DASHBOARD SECTION ---
elif section == "Dashboard":
    st.title("📊 Dashboard Metrics")
    df = st.session_state['df']
    if df is None:
        st.warning("Please upload a file first in the Home section.")
    else:
        total_users = df.shape[0]
        high_risk = df[df['risk_level'] == 'High'].shape[0]
        avg_churn = round(df['churn_score'].mean(), 2)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Users", total_users)
        col2.metric("High Risk Users", high_risk)
        col3.metric("Avg. Churn Score", avg_churn)

        st.subheader("📉 Churn Score Distribution")
        fig = px.histogram(df, x="churn_score", nbins=20, title="Churn Score Distribution")
        st.plotly_chart(fig, use_container_width=True)

# --- SEGMENTATION INSIGHTS ---
elif section == "Segmentation Insights":
    st.title("🔍 Segmentation Insights")
    df = st.session_state['df']
    if df is None:
        st.warning("Please upload a file first in the Home section.")
    else:
        seg_col = st.selectbox("Select column to segment", ["gender", "price_range", "risk_level"])

        st.subheader(f"📊 Churn Score by {seg_col}")
        fig = px.box(df, x=seg_col, y="churn_score", title=f"Churn Score Distribution by {seg_col}")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(f"📊 User Count by {seg_col}")
        fig2 = px.histogram(df, x=seg_col, title=f"User Count by {seg_col}")
        st.plotly_chart(fig2, use_container_width=True)
