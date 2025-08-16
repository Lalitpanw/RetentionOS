import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup ---
st.set_page_config(page_title="RetentionOS", page_icon="📊", layout="wide")

# --- Sidebar Navigation ---
st.sidebar.markdown("<h2 style='text-align:center; color:#4B8BBE;'>RetentionOS</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

sections = [
    "Home",
    "Churn Analysis",
    "User Segments",
    "Nudge Suggestions",
    "Cohort Analysis",
    "RAG Insights",
    "Export Data"
]

# Initialize selected section
if "section_index" not in st.session_state:
    st.session_state.section_index = 0

# Sidebar buttons
for i, title in enumerate(sections):
    if st.sidebar.button(title, key=f"nav_{i}"):
        st.session_state.section_index = i

# Get selected section
section = sections[st.session_state.section_index]

# --- HOME SECTION ---
if section == "Home":
    st.markdown("<h2 style='text-align: center;'>Upload Your User Data File</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"], key="file_uploader_home")

    if uploaded_file:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        st.session_state.df = df
        st.success("File uploaded successfully!")
        st.dataframe(df.head())
    else:
        st.warning("Please upload a file to proceed.")

    st.stop()

# --- DATA CHECK ---
if "df" not in st.session_state:
    st.error("No data found. Please upload a file in the Home section first.")
    st.stop()

df = st.session_state.df.copy()

# --- CHURN ANALYSIS ---
if section == "Churn Analysis":
    st.header("Churn Analysis")
    if "risk_level" not in df.columns:
        st.warning("No 'risk_level' column found. Please add churn prediction logic.")
    else:
        churn_counts = df["risk_level"].value_counts().reset_index()
        churn_counts.columns = ["Risk Level", "Count"]
        fig = px.bar(churn_counts, x="Risk Level", y="Count", color="Risk Level", title="Churn Risk Levels")
        st.plotly_chart(fig, use_container_width=True)

# --- USER SEGMENTS ---
elif section == "User Segments":
    st.header("User Segments by Risk & Gender")
    if "risk_level" not in df.columns or "gender" not in df.columns:
        st.warning("Ensure 'risk_level' and 'gender' columns exist.")
    else:
        risk_choice = st.selectbox("Select Risk Level", df["risk_level"].unique())
        segment_df = df[df["risk_level"] == risk_choice]
        st.write(f"Total Users: {len(segment_df)}")
        st.dataframe(segment_df)

        # Gender Breakdown
        gender_counts = segment_df["gender"].value_counts().reset_index()
        gender_counts.columns = ["Gender", "Count"]
        fig = px.pie(gender_counts, names="Gender", values="Count", title=f"Gender Distribution - {risk_choice} Risk")
        st.plotly_chart(fig, use_container_width=True)

# --- NUDGE SUGGESTIONS ---
elif section == "Nudge Suggestions":
    st.header("Nudge Templates for User Retention")
    if "risk_level" not in df.columns:
        st.warning("No 'risk_level' column found.")
    else:
        nudges = {
            "High": "Send an exclusive discount email + personalized support message.",
            "Medium": "Send engagement tips with feature highlights and benefits.",
            "Low": "Encourage referrals & loyalty program participation."
        }
        for risk, message in nudges.items():
            st.subheader(f"{risk} Risk Users")
            st.write(message)

        # Show sample users for selected risk
        risk_choice = st.selectbox("Show Users for Risk Level", df["risk_level"].unique(), key="nudge_user_select")
        st.dataframe(df[df["risk_level"] == risk_choice])

# --- COHORT ANALYSIS ---
elif section == "Cohort Analysis":
    st.header("Cohort Analysis & Insights")
    if "signup_date" not in df.columns or "user_id" not in df.columns:
        st.warning("'signup_date' or 'user_id' missing.")
    else:
        df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
        df["signup_month"] = df["signup_date"].dt.to_period("M")
        cohort = df.groupby("signup_month")["user_id"].nunique().reset_index()
        cohort.columns = ["Signup Month", "Unique Users"]

        # Line Chart
        fig = px.line(cohort, x="Signup Month", y="Unique Users", title="Monthly Cohorts")
        st.plotly_chart(fig, use_container_width=True)

        # Actionable Insight
        if len(cohort) > 1:
            last_month = cohort.iloc[-1]["Unique Users"]
            prev_month = cohort.iloc[-2]["Unique Users"]
            growth = ((last_month - prev_month) / prev_month * 100) if prev_month != 0 else 0
            st.info(f"Last Month Signup: {last_month} users ({growth:.2f}% change vs previous month)")

# --- RAG INSIGHTS ---
elif section == "RAG Insights":
    st.header("RAG Insights via GPT/LangChain")

    if "risk_level" not in df.columns:
        st.warning("⚠️ 'risk_level' column not found. Please add churn prediction results first.")
    else:
        # Count users by risk level
        high_risk_count = len(df[df["risk_level"]=="High"])
        medium_risk_count = len(df[df["risk_level"]=="Medium"])
        low_risk_count = len(df[df["risk_level"]=="Low"])

        st.write(f"High Risk Users Count: {high_risk_count}")
        st.write(f"Medium Risk Users Count: {medium_risk_count}")
        st.write(f"Low Risk Users Count: {low_risk_count}")

        # Display placeholder while GPT generates insights
        st.info("Generating actionable retention strategies using GPT...")

        # --- GPT/LangChain Integration ---
        try:
            from langchain.llms import OpenAI
            from langchain.prompts import PromptTemplate
            from langchain.chains import LLMChain

            # Initialize GPT
            llm = OpenAI(temperature=0, model_name="gpt-4")  # Change to "gpt-3.5-turbo" if needed

            # Prompt template
            prompt_template = """
            You are a product analyst. You have the following user data summary:

            High Risk Users Count: {high_risk_count}
            Medium Risk Users Count: {medium_risk_count}
            Low Risk Users Count: {low_risk_count}

            Generate actionable retention strategies for each category. Be specific and practical.
            """

            prompt = PromptTemplate(
                input_variables=["high_risk_count", "medium_risk_count", "low_risk_count"],
                template=prompt_template
            )

            # LLM Chain
            chain = LLMChain(llm=llm, prompt=prompt)

            # Run the chain
            insight = chain.run(
                high_risk_count=high_risk_count,
                medium_risk_count=medium_risk_count,
                low_risk_count=low_risk_count
            )

            st.subheader("Actionable GPT Insights")
            st.write(insight)

        except Exception as e:
            st.error(f"Error generating GPT insights: {e}")
            st.info("Ensure you have set your OpenAI API key and installed langchain.")

# --- EXPORT DATA ---
elif section == "Export Data":
    st.header("Export Data")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="retention_data.csv",
        mime="text/csv"
    )
