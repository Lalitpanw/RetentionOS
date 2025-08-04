import streamlit as st
import pandas as pd
import plotly.express as px
from fuzzywuzzy import fuzz
import openai

# --- Set your OpenAI API key ---
openai.api_key = "your-openai-api-key"

# --- Page Config ---
st.set_page_config(page_title="RetentionOS", layout="wide")
st.title("📊 RetentionOS – AI-powered Churn & Retention Toolkit")

# --- Sidebar Navigation ---
st.sidebar.title("📁 Navigation")
section = st.sidebar.radio("Go to", [
    "Home",
    "Churn Analysis",
    "User Segments",
    "Nudge Suggestions",
    "RFM",
    "RAG Insights"
])

# --- Global Upload ---
if 'df' not in st.session_state:
    st.session_state.df = None

if section == "Home":
    st.header("🏠 Home")
    st.markdown("_Upload your user file to get started with churn prediction & retention analysis._")
    uploaded_file = st.file_uploader("📥 Upload CSV or Excel", type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.success("✅ File uploaded successfully.")

elif section == "Churn Analysis":
    st.header("📉 Churn Analysis")

    if st.session_state.df is not None:
        df = st.session_state.df

        # Auto-map
        expected_fields = {
            'last_active_days': ['last_seen', 'last_active'],
            'total_sessions': ['sessions', 'login_count'],
            'orders': ['orders', 'transactions'],
        }

        def auto_map_columns(df):
            mapping = {}
            for key, options in expected_fields.items():
                for col in df.columns:
                    for option in options:
                        if fuzz.partial_ratio(col.lower(), option.lower()) > 80:
                            mapping[key] = col
            return mapping

        mapping = auto_map_columns(df)

        # Manual fallback
        for key in expected_fields:
            if key not in mapping:
                mapping[key] = st.selectbox(f"Select column for `{key}`", df.columns)
        df = df.rename(columns={mapping[k]: k for k in mapping})

        # Scoring
        def score_user(row):
            score = 0
            if row['last_active_days'] > 14: score += 1
            if row['orders'] < 1: score += 1
            if row['total_sessions'] < 3: score += 1
            return score

        df['churn_score'] = df.apply(score_user, axis=1)
        df['churn_risk'] = df['churn_score'].apply(lambda s: "🔴 High" if s >= 2 else ("🟠 Medium" if s == 1 else "🟢 Low"))
        st.session_state.df = df

        # Metrics + Charts
        st.metric("Total Users", len(df))
        st.metric("Avg. Churn Score", round(df["churn_score"].mean(), 2))
        st.plotly_chart(px.pie(df, names="churn_risk", title="Churn Risk Distribution"), use_container_width=True)

    else:
        st.warning("⚠️ Please upload a file on the Home page first.")

elif section == "User Segments":
    st.header("📌 User Segments")
    if st.session_state.df is not None:
        df = st.session_state.df
        selected_risk = st.selectbox("Select Risk Level", df["churn_risk"].unique())
        st.write(f"Users in {selected_risk}: {df[df['churn_risk'] == selected_risk].shape[0]}")
        st.dataframe(df[df["churn_risk"] == selected_risk])
    else:
        st.warning("⚠️ No data loaded.")

elif section == "Nudge Suggestions":
    st.header("💬 GPT-Powered Nudge Suggestions")

    if st.session_state.df is not None:
        df = st.session_state.df

        if st.button("🧠 Generate Nudges"):
            def generate_nudge(row):
                prompt = f"""
                The user is in {row['churn_risk']} churn risk.
                Last seen {row['last_active_days']} days ago. Orders: {row['orders']}, Sessions: {row['total_sessions']}.
                Suggest a short friendly re-engagement message.
                """
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=60
                    )
                    return response.choices[0].message.content.strip()
                except:
                    return "Error"

            with st.spinner("Generating..."):
                df['nudge'] = df.apply(generate_nudge, axis=1)
            st.success("✅ Nudges ready!")
            st.dataframe(df[['churn_risk', 'nudge']])
        else:
            st.info("Click the button to generate AI-powered nudges.")

    else:
        st.warning("⚠️ Please upload user data first.")

elif section == "RFM":
    st.header("📊 RFM Segmentation")
    st.info("🚧 Coming soon: RFM-based segmentation with Recency, Frequency, Monetary scoring.")

elif section == "RAG Insights":
    st.header("🧠 GPT Assistant (RAG-style)")
    st.info("🚧 Coming soon: Ask GPT questions like 'Why are high-risk users churning this week?'")
