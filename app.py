import streamlit as st
import pandas as pd
import plotly.express as px

st.set\_page\_config(page\_title="RetentionOS", layout="wide")

# ---- Sidebar Navigation ----

st.sidebar.image("[https://your-image-host.com/retentionos-logo.png](https://your-image-host.com/retentionos-logo.png)", width=120)  # Replace with your real logo URL
section = st.sidebar.radio("📂 Navigate", \["Home", "Summary", "Dashboard", "Segments", "About"])

st.sidebar.markdown("---")
st.sidebar.markdown("#### ℹ️ About RetentionOS")
st.sidebar.markdown("""
**RetentionOS** is a churn prediction tool for fast-moving product teams.

* Upload data
* Predict churn
* Nudge smartly
* Export easily

Built by **Lalit Panwar**
""")

# Store data

if "df" not in st.session\_state:
st.session\_state.df = None

# ---- Home Page ----

if section == "Home":
st.title("📊 RetentionOS – Upload User Data")
uploaded\_file = st.file\_uploader("Upload your user Excel/CSV file")

```
if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        st.stop()

    st.session_state.df = df
    st.success("✅ File uploaded successfully!")

    with st.expander("🔍 Preview Uploaded Data"):
        st.dataframe(df)

    st.download_button("📥 Download Clean File", df.to_csv(index=False), file_name="retention_clean_data.csv")
```

# ---- Summary ----

elif section == "Summary":
st.title("📈 Retention Summary Dashboard")
df = st.session\_state.df

```
if df is None:
    st.warning("Please upload a file in the Home section first.")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", len(df))
    col2.metric("High Risk Users", (df["risk_level"] == "High").sum())
    col3.metric("Average Churn Score", round(df["churn_score"].mean(), 2))

    st.markdown("### 🎯 Churn Risk Breakdown")
    st.bar_chart(df["risk_level"].value_counts())

    st.markdown("### 👥 Gender Split")
    if "gender" in df.columns:
        st.plotly_chart(px.pie(df, names="gender", title="Users by Gender"))

    st.markdown("### 🔝 Top 5 High-Risk Users")
    if "churn_score" in df.columns:
        top_risky = df.sort_values(by="churn_score", ascending=False).head(5)
        st.dataframe(top_risky[["user_id", "churn_score", "nudge_recommendation"]])

    st.markdown("### 💡 Nudge Recommendations")
    if "nudge_recommendation" in df.columns:
        st.plotly_chart(px.bar(
            df["nudge_recommendation"].value_counts().reset_index(),
            x="index", y="nudge_recommendation",
            labels={"index": "Nudge Type", "nudge_recommendation": "Count"},
            title="Nudge Recommendation Distribution"
        ))
```

# ---- Dashboard ----

elif section == "Dashboard":
st.title("📊 Dashboard Metrics")
df = st.session\_state.df

```
if df is None:
    st.warning("Please upload a file in the Home section first.")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", len(df))
    col2.metric("High Risk Users", (df["risk_level"] == "High").sum())
    col3.metric("Average Churn Score", round(df["churn_score"].mean(), 2))

    st.markdown("### 📉 Churn Score Distribution")
    fig = px.histogram(df, x="churn_score", nbins=20, title="Churn Score Histogram")
    st.plotly_chart(fig)
```

# ---- Segments ----

elif section == "Segments":
st.title("📦 User Segments")
df = st.session\_state.df

```
if df is None:
    st.warning("Please upload a file in the Home section first.")
else:
    risk = st.selectbox("Select Risk Level", options=df["risk_level"].unique())
    filtered = df[df["risk_level"] == risk]
    st.write(f"Showing {len(filtered)} users in **{risk}** risk segment.")
    st.dataframe(filtered)

    st.download_button(
        "📥 Download Segment",
        filtered.to_csv(index=False),
        file_name=f"{risk.lower()}_risk_users.csv"
    )
```

# ---- About ----

elif section == "About":
st.title("🔍 About RetentionOS")

```
st.image("https://your-image-host.com/retentionos-logo.png", width=200)  # Replace with real logo URL

st.markdown("""
### 🧠 What is RetentionOS?

**RetentionOS** is a lightweight churn prediction and nudging assistant designed for fast-moving product teams at early-stage startups.

It empowers you to:  
- 📥 Upload raw user data  
- 🚨 Detect churn risk (High, Medium, Low)  
- 🎯 Get smart nudge recommendations  
- 📊 Explore insights via dashboard & segments  
- 📤 Export data for campaigns or CRM

---

### 👨‍💻 Built by
Created with a product-first mindset by **Lalit Panwar**  
_For makers who prefer action over waiting._
""", unsafe_allow_html=True)
```
