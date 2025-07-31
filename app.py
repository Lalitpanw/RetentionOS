mport streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar Navigation with About at bottom
st.sidebar.markdown("### 📂 Navigation")
menu = ["Home", "Summary", "Dashboard", "Segments"]
section = st.sidebar.radio("Go to", menu)

# Add space and About button at bottom
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
about_clicked = st.sidebar.button("🔍 About RetentionOS")

# File upload shared state
if "df" not in st.session_state:
    st.session_state.df = None

# --- ABOUT PAGE (Triggered separately) ---
if about_clicked:
    st.title("About RetentionOS")
    st.markdown("""
    **RetentionOS** is a lightweight churn prediction and nudging assistant built for fast-moving product teams at early-stage startups.

    ### ✅ Benefits:
    - Detect churn risk across users (High, Medium, Low)
    - Gain actionable insights using interactive dashboards
    - Get smart nudge recommendations
    - Export ready-to-use campaign files

    ### 🚀 Expected Outcomes:
    - Better retention strategies  
    - Data-backed nudge campaigns  
    - Faster user segmentation  
    - Clear churn trends and risk metrics  
    """)
    st.stop()

# --- HOME PAGE ---
if section == "Home":
    st.title("RetentionOS – A User Turning Point")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                st.session_state.df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                import openpyxl
                st.session_state.df = pd.read_excel(uploaded_file, engine="openpyxl")
            st.success("✅ File uploaded successfully!")
            st.dataframe(st.session_state.df.head())
        except Exception as e:
            st.error("❌ Could not read the uploaded file.")
            st.exception(e)

# --- SUMMARY PAGE ---
elif section == "Summary":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a file from the Home page first.")
    else:
        st.title("📈 User Summary Insights")
        st.subheader("📌 Sample Data")
        st.dataframe(st.session_state.df.head())

# --- DASHBOARD PAGE ---
elif section == "Dashboard":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a file from the Home page first.")
from fuzzywuzzy import fuzz

st.set_page_config(page_title="RetentionOS", layout="centered")

st.title("📊 RetentionOS – A User Turning Point")
st.markdown("_Upload your user data → Predict churn → Auto-nudge users._")

# --- Step 1: Upload file ---
uploaded_file = st.file_uploader("📥 Upload your CSV file", type=["csv", "xlsx"])

if uploaded_file:
    # --- Step 2: Load data ---
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        st.title("📊 Dashboard Metrics")
        df = st.session_state.df
        df = pd.read_csv(uploaded_file)

        st.metric("Total Users", len(df))
        st.metric("High Risk Users", df[df["risk_level"] == "High"].shape[0])
        st.metric("Average Churn Score", round(df["churn_score"].mean(), 2))
    st.success(f"File uploaded: {uploaded_file.name}")
    st.markdown(f"📄 **Columns detected**: `{', '.join(df.columns)}`")

        st.subheader("Churn Score Distribution")
        fig1 = px.histogram(df, x="churn_score", nbins=20, title="Churn Score Histogram")
        st.plotly_chart(fig1, use_container_width=True)
    # --- Step 3: Auto-map columns ---
    expected_fields = {
        'last_active_days': ['last_seen', 'last_active', 'inactive_days'],
        'total_sessions': ['sessions', 'login_count', 'visits'],
        'orders': ['orders', 'purchases', 'transactions'],
        'revenue': ['amount_spent', 'order_value', 'lifetime_value'],
    }

        st.subheader("Risk Level Distribution")
        fig2 = px.pie(df, names="risk_level", title="Risk Level Breakdown")
        st.plotly_chart(fig2, use_container_width=True)
    def auto_map_columns(df):
        mapping = {}
        for key, possible_names in expected_fields.items():
            for col in df.columns:
                for option in possible_names:
                    if fuzz.partial_ratio(col.lower(), option.lower()) > 80:
                        mapping[key] = col
                        break
        return mapping

        st.subheader("Cart Value by Risk Level")
        fig3 = px.box(df, x="risk_level", y="cart_value", title="Cart Value vs Risk Level")
        st.plotly_chart(fig3, use_container_width=True)
    mapping = auto_map_columns(df)

# --- SEGMENT PAGE ---
elif section == "Segments":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a file from the Home page first.")
    else:
        st.title("📌 Segmentation Insights")
        df = st.session_state.df
        selected_risk = st.selectbox("Select Risk Level", df["risk_level"].unique())
        filtered = df[df["risk_level"] == selected_risk]
        st.write(f"Filtered users in {selected_risk} risk: {filtered.shape[0]}")
        st.dataframe(filtered)
    # --- Step 4: Manual fallback ---
    st.markdown("### 🔍 Column Mapping")
    for key in expected_fields:
        if key not in mapping:
            mapping[key] = st.selectbox(f"Select column for **{key}**", df.columns)
        st.markdown(f"✅ `{key}` → `{mapping[key]}`")

    # --- Step 5: Standardize ---
    df = df.rename(columns={mapping[k]: k for k in mapping})

    # --- Step 6: Scoring logic (simple rules) ---
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

    # --- Step 7: Display Results ---
    st.markdown("### 📊 Churn Risk Segments")
    st.dataframe(df[['churn_risk', 'last_active_days', 'orders', 'total_sessions']])

    # --- Optional: Future Add-ons ---
    # - Nudge message generator
    # - Export filtered segments
    # - Twilio API integration
else:
    st.info("👆 Upload a CSV or Excel file to begin.")
