import streamlit as st
import pandas as pd
import plotly.express as px
from fuzzywuzzy import fuzz
import openai

# --- Set OpenAI API Key ---
openai.api_key = "your-openai-api-key"

# --- Page setup ---
st.set_page_config(page_title="RetentionOS", layout="centered")
st.title("📊 RetentionOS – A User Turning Point")
st.markdown("_Upload your user data → Predict churn → Auto-nudge users._")

# --- Upload file ---
uploaded_file = st.file_uploader("📥 Upload your CSV file", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # --- Auto-map fields ---
    expected_fields = {
        'last_active_days': ['last_seen', 'last_active', 'inactive_days'],
        'total_sessions': ['sessions', 'login_count', 'visits'],
        'orders': ['orders', 'purchases', 'transactions'],
        'revenue': ['amount_spent', 'order_value', 'lifetime_value'],
        'cart_value': ['cart_value', 'cart_amount']
    }

    def auto_map_columns(df):
        mapping = {}
        for key, options in expected_fields.items():
            for col in df.columns:
                for option in options:
                    if fuzz.partial_ratio(col.lower(), option.lower()) > 80:
                        mapping[key] = col
                        break
        return mapping

    mapping = auto_map_columns(df)

    # --- Manual fallback ---
    st.subheader("🛠 Column Mapping")
    for key in expected_fields:
        if key not in mapping:
            mapping[key] = st.selectbox(f"Select column for **{key}**", df.columns)
        st.markdown(f"✅ `{key}` → `{mapping[key]}`")

    # --- Rename columns ---
    df = df.rename(columns={mapping[k]: k for k in mapping})

    # --- Churn scoring ---
    def score_user(row):
        score = 0
        if row['last_active_days'] > 14:
            score += 1
        if row['orders'] < 1:
            score += 1
        if row['total_sessions'] < 3:
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

    # --- Dashboard ---
    st.header("📈 Dashboard Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", len(df))
    col2.metric("High Risk Users", df[df["churn_risk"] == "🔴 High"].shape[0])
    col3.metric("Avg. Churn Score", round(df["churn_score"].mean(), 2))

    st.plotly_chart(px.pie(df, names="churn_risk", title="Risk Level Distribution"), use_container_width=True)
    if 'cart_value' in df.columns:
        st.plotly_chart(px.box(df, x="churn_risk", y="cart_value", title="Cart Value by Risk Level"), use_container_width=True)

    # --- Nudge Generator ---
    st.subheader("💬 Generate Personalized Nudges")
    if st.button("🧠 Generate GPT Nudges"):
        def generate_nudge(user_row):
            prompt = f"""
            The user is in the {user_row['churn_risk']} churn risk segment.
            Last active: {user_row['last_active_days']} days ago.
            Orders: {user_row['orders']}, Sessions: {user_row['total_sessions']}, Cart Value: ₹{user_row.get('cart_value', 'N/A')}.
            Write a short, friendly nudge message to re-engage them.
            """
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                    max_tokens=50
                )
                return response['choices'][0]['message']['content'].strip()
            except Exception as e:
                return f"Error: {e}"

        with st.spinner("Generating nudges with GPT..."):
            df['nudge'] = df.apply(generate_nudge, axis=1)
        st.success("Nudges generated!")
        st.dataframe(df[['churn_risk', 'nudge']])

    # --- Display Segments ---
    st.subheader("🔍 Explore Risk Segments")
    selected_risk = st.selectbox("Filter by Risk Level", df['churn_risk'].unique())
    filtered = df[df['churn_risk'] == selected_risk]
    st.write(f"Users in {selected_risk}: {filtered.shape[0]}")
    st.dataframe(filtered)

    # --- Optional: Download Results ---
    st.download_button("📤 Download Segment Data", filtered.to_csv(index=False), file_name="segment.csv", mime="text/csv")

else:
    st.info("👆 Please upload a CSV or Excel file to get started.")
