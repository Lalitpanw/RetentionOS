import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import openai
from fuzzywuzzy import fuzz
from io import BytesIO

# --- OpenAI Key ---
openai.api_key = "your-openai-api-key"  # Replace this with your actual key

# --- Page Setup ---
st.set_page_config(page_title="RetentionOS", layout="wide")

# --- Better Sidebar Styling ---
st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background-color: #1f2937;
        color: white;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    /* Highlight selected */
    div[role="radiogroup"] > label[data-baseweb="radio"] {
        border-radius: 5px;
        padding: 4px 6px;
    }
    div[role="radiogroup"] > label[data-selected="true"] {
        background-color: #374151;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("📊 RetentionOS")
section = st.sidebar.radio("Navigation", [
    "🏠 Home",
    "Churn Analysis",
    "User Segments",
    "Nudge Suggestions",
    "Cohort Analysis",
    "RAG Insights",
    "Export Data"
])

# --- File Upload (Center UI) ---
st.markdown("<h2 style='text-align: center;'>📥 Upload Your User Data File</h2>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    st.session_state.df = df
    st.success("✅ File uploaded and loaded successfully!")

elif 'df' not in st.session_state:
    st.warning("⚠️ Please upload a valid file to proceed.")

# --- Home Page ---
if section == "🏠 Home":
    st.markdown("<h2 style='text-align: center;'>📥 Upload Your User Data File</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.success("✅ File uploaded and loaded successfully!")

    elif 'df' not in st.session_state:
        st.warning("⚠️ Please upload a valid file to proceed.")

    st.stop()  # Stop here so no extra content is shown

# Continue only if data exists
if 'df' in st.session_state:
    df = st.session_state.df.copy()

    # Auto column mapping
    expected_fields = {
        'last_active_days': ['last_seen', 'last_active', 'inactive_days'],
        'total_sessions': ['sessions', 'login_count', 'visits', 'sessions_last_7_days'],
        'orders': ['orders', 'transactions', 'purchases', 'number_of_purchases'],
        'revenue': ['order_value', 'lifetime_value', 'cart_value'],
    }

    def auto_map_columns(df):
        mapping = {}
        for key, candidates in expected_fields.items():
            for col in df.columns:
                for option in candidates:
                    if fuzz.partial_ratio(col.lower(), option.lower()) > 80:
                        mapping[key] = col
                        break
        return mapping

    mapping = auto_map_columns(df)
    df = df.rename(columns={v: k for k, v in mapping.items()})

    # Churn Risk Scoring
    def score_user(row):
        score = 0
        if row.get('last_active_days', 0) > 14:
            score += 1
        if row.get('orders', 1) < 1:
            score += 1
        if row.get('total_sessions', 3) < 3:
            score += 1
        return score

    df['churn_score'] = df.apply(score_user, axis=1)

    def label_risk(score):
        if score >= 2:
            return "🔴 High"
        elif score == 1:
            return "🟠 Medium"
        else:
            return "🟢 Low"

    df['churn_risk'] = df['churn_score'].apply(label_risk)

    # --- Churn Analysis ---
    if section == "Churn Analysis":
        st.header("📉 Churn Analysis")
        st.metric("Total Users", len(df))
        st.metric("High Risk Users", df[df["churn_risk"] == "🔴 High"].shape[0])
        st.metric("Avg. Churn Score", round(df["churn_score"].mean(), 2))

        st.subheader("Churn Score Distribution")
        fig1 = px.histogram(df, x="churn_score", nbins=10)
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Risk Level Breakdown")
        fig2 = px.pie(df, names="churn_risk")
        st.plotly_chart(fig2, use_container_width=True)

    # --- User Segments ---
    elif section == "User Segments":
        st.header("📌 Segment Explorer")
        selected_risk = st.selectbox("Filter by Risk Level", df["churn_risk"].unique())
        filtered_df = df[df["churn_risk"] == selected_risk]
        st.dataframe(filtered_df)
        st.download_button("📤 Download Segment", filtered_df.to_csv(index=False), file_name="segment.csv")

    # --- Nudge Suggestions ---
    elif section == "Nudge Suggestions":
        st.header("💬 GPT-based Nudge Generator")
        sample_user = df.sample(1).to_dict(orient="records")[0]
        st.json(sample_user)
        prompt = st.text_area("🧠 Custom Prompt", value=f"Suggest a reactivation message for this user:\n{sample_user}")
        if st.button("Ask GPT"):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                suggestion = response.choices[0].message.content
                st.success("✅ GPT Suggestion:")
                st.write(suggestion)
            except Exception as e:
                st.error(f"Error: {e}")

    # --- Cohort Analysis ---
    elif section == "Cohort Analysis":
        st.header("📈 Cohort Retention Analysis")
        df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'], errors='coerce')
        df['cohort'] = df['last_purchase_date'].dt.to_period("M")
        df['week'] = df['last_purchase_date'].dt.to_period("W")
        mode = st.radio("Time Granularity", ["Monthly", "Weekly"], horizontal=True)

        cohort_col = 'cohort' if mode == "Monthly" else 'week'
        cohort_data = df.groupby([cohort_col])['user_id'].nunique().reset_index()
        pivot = cohort_data.pivot_table(index=cohort_col, values='user_id', aggfunc='sum')

        fig, ax = plt.subplots(figsize=(10, 4))
        sns.heatmap(pivot, annot=True, fmt="g", cmap="Blues", ax=ax)
        st.pyplot(fig)

    # --- RAG Insights (GPT) ---
    elif section == "RAG Insights":
        st.header("🧠 Ask GPT Anything about Retention")
        segment_summary = df.groupby('churn_risk').agg({
            'last_active_days': 'mean',
            'orders': 'mean',
            'user_id': 'count'
        }).reset_index()
        context = segment_summary.to_markdown()
        st.text_area("📄 Auto-generated context", value=context, height=150)

        question = st.text_input("💬 Ask a Question")
        if question:
            with st.spinner("Thinking..."):
                try:
                    prompt = f"Data:\n{context}\n\nQ: {question}"
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7
                    )
                    st.success("✅ GPT's Answer")
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")

    # --- Export Data ---
    elif section == "Export Data":
        st.header("📤 Download All Processed Data")
        st.dataframe(df)
        st.download_button("⬇️ Download CSV", data=df.to_csv(index=False), file_name="retention_data.csv")
