import streamlit as st
import pandas as pd
import plotly.express as px
from fuzzywuzzy import fuzz
import openai

# --- Setup ---
openai.api_key = "your-openai-api-key"
st.set_page_config(page_title="RetentionOS", layout="wide")

# --- Sidebar ---
st.sidebar.title("🔎 RetentionOS")
section = st.sidebar.radio("Navigation", [
    "Churn Analysis",
    "User Segments",
    "Nudge Suggestions",
    "RFM",
    "RAG Insights"
])

# --- Upload Handler (Always Visible) ---
st.markdown("### 📥 Upload Your User File")
st.markdown("Upload a `.csv` or `.xlsx` file with basic user data to begin analyzing churn risk and generating AI-powered insights.")

uploaded_file = st.file_uploader("", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    st.session_state.df = df
    st.success("✅ Data loaded successfully.")

elif 'df' not in st.session_state:
    st.warning("⬆️ Please upload a valid CSV or Excel file to proceed.")

# --- Continue only if data is present ---
if 'df' in st.session_state:
    df = st.session_state.df

    # --- Section: Churn Analysis ---
    if section == "Churn Analysis":
        st.markdown("## 📉 Churn Analysis")
        # Mapping, scoring, and plots go here...

    # --- Section: User Segments ---
    elif section == "User Segments":
        st.markdown("## 📌 Segment View")
        # Filter and display logic...

    # --- Section: Nudges ---
    elif section == "Nudge Suggestions":
        st.markdown("## 💬 Personalized Nudge Suggestions")
        # GPT prompt logic...

    # --- Section: RFM (Placeholder) ---
    elif section == "RFM":
        st.markdown("## 🧩 RFM Segmentation (Coming Soon)")
        st.info("RFM scoring will allow more granular churn and monetization predictions.")

   elif section == "RAG Insights":
    st.markdown("## 🤖 Ask GPT Your Retention Questions")

    # Basic stats to provide as context
    context = ""

    for risk in df['churn_risk'].unique():
        segment = df[df['churn_risk'] == risk]
        avg_inactive = segment['last_active_days'].mean()
        avg_orders = segment['orders'].mean()
        count = len(segment)
        context += f"\nSegment {risk}: {count} users, avg inactive days: {avg_inactive:.1f}, avg orders: {avg_orders:.1f}"

    st.text_area("🧠 Context to GPT (auto-filled)", value=context, height=150)

    user_question = st.text_input("💬 Ask something about user segments")

    if user_question:
        with st.spinner("Thinking..."):
            prompt = f"""You are a retention strategy assistant. Here's the data:\n{context}\n\nUser question: {user_question}"""
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=200
                )
                answer = response.choices[0].message.content.strip()
                st.markdown("### 🧠 GPT Suggests:")
                st.write(answer)
            except Exception as e:
                st.error(f"Error from GPT: {e}")
