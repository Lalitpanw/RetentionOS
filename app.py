import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup

st.set\_page\_config(page\_title="RetentionOS", layout="wide")

# App Title

st.markdown(""" <h1 style='text-align: center; color: #f63366; text-shadow: 1px 1px 2px gray;'>
RetentionOS – A User Turning Point </h1>
""", unsafe\_allow\_html=True)

# Sidebar navigation

menu = \["Home", "Summary", "Dashboard", "Segments", "About"]
page = st.sidebar.radio("📂 Navigate", menu)

# Session state setup

if "df" not in st.session\_state:
st.session\_state.df = None

# Home Page

if page == "Home":
st.header("📊 Upload User Data")
uploaded\_file = st.file\_uploader("Upload a CSV or Excel file")

```
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.session_state.df = df
        st.success("✅ File uploaded successfully!")

        with st.expander("🔍 Preview Uploaded Data"):
            st.dataframe(df)

        st.download_button("📥 Download Clean File", df.to_csv(index=False), file_name="retention_clean_data.csv")
    except Exception as e:
        st.error(f"Error reading file: {e}")
```

# Summary Page

elif page == "Summary":
st.header("📈 Retention Summary")
df = st.session\_state.df

```
if df is None:
    st.warning("Please upload a file first in the Home tab.")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", len(df))
    col2.metric("High Risk Users", (df["risk_level"] == "High").sum())
    col3.metric("Average Churn Score", round(df["churn_score"].mean(), 2))

    st.subheader("Churn Risk Breakdown")
    st.bar_chart(df["risk_level"].value_counts())

    if "gender" in df.columns:
        st.subheader("Gender Distribution")
        st.plotly_chart(px.pie(df, names="gender", title="User Gender Split"))

    if "churn_score" in df.columns:
        st.subheader("Top 5 High-Risk Users")
        top_risky = df.sort_values(by="churn_score", ascending=False).head(5)
        st.dataframe(top_risky[["user_id", "churn_score", "nudge_recommendation"]])

    if "nudge_recommendation" in df.columns:
        st.subheader("Nudge Recommendation Distribution")
        chart_data = df["nudge_recommendation"].value_counts().reset_index()
        st.plotly_chart(px.bar(chart_data, x="index", y="nudge_recommendation",
                               labels={"index": "Nudge Type", "nudge_recommendation": "Count"}))
```

# Dashboard Page

elif page == "Dashboard":
st.header("📊 Dashboard")
df = st.session\_state.df

```
if df is None:
    st.warning("Please upload a file first in the Home tab.")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", len(df))
    col2.metric("High Risk Users", (df["risk_level"] == "High").sum())
    col3.metric("Average Churn Score", round(df["churn_score"].mean(), 2))

    st.subheader("Churn Score Histogram")
    st.plotly_chart(px.histogram(df, x="churn_score", nbins=20))
```

# Segments Page

elif page == "Segments":
st.header("📦 User Segments")
df = st.session\_state.df

```
if df is None:
    st.warning("Please upload a file first in the Home tab.")
else:
    risk = st.selectbox("Select Risk Level", df["risk_level"].unique())
    filtered = df[df["risk_level"] == risk]
    st.write(f"{len(filtered)} users in {risk} risk segment")
    st.dataframe(filtered)

    st.download_button("📥 Download Segment", filtered.to_csv(index=False),
                       file_name=f"{risk.lower()}_risk_users.csv")
```

# About Page

elif page == "About":
st.header("🔍 About RetentionOS")
st.markdown("""
\### 🧠 What is RetentionOS?

```
**RetentionOS** is a lightweight churn prediction and nudging assistant designed for fast-moving product teams at early-stage startups.

It empowers you to:
- 📥 Upload raw user data
- 🚨 Detect churn risk (High, Medium, Low)
- 🎯 Get smart nudge recommendations
- 📊 Explore insights via dashboard & segments
- 📤 Export data for campaigns or CRM

---
### 👨‍💻 Built by
**Lalit Panwar**  
_A product-first thinker focused on solving real user problems and building tools that drive action, not just analysis._
""", unsafe_allow_html=True)
```
