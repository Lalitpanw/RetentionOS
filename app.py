import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RetentionOS", layout="wide")

# Sidebar Navigation

st.sidebar.markdown("<h3 style='margin-bottom: 10px;'>\ud83d\udcc2 Navigation</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<br>" \* 1, unsafe_allow_html=True)

# Radio navigation with About at the bottom

section = st.sidebar.radio("Go to", \["Home", "Summary", "Dashboard", "Segments", "About"])
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# File upload (common across pages)

if "df" not in st.session\_state:
st.session\_state.df = None

if section == "Home":
st.title("RetentionOS – A User Turning Point")
uploaded\_file = st.file\_uploader("Upload a CSV or Excel file", type=\["csv", "xlsx"])
if uploaded\_file:
if uploaded\_file.name.endswith(".csv"):
st.session\_state.df = pd.read\_csv(uploaded\_file)
elif uploaded\_file.name.endswith((".xls", ".xlsx")):
st.session\_state.df = pd.read\_excel(uploaded\_file)
st.success("✅ File uploaded successfully!")
st.dataframe(st.session\_state.df.head())

elif section == "Summary":
st.title("📈 User Summary Insights")
if st.session\_state.df is not None:
st.subheader("Key Columns Detected:")
st.write(", ".join(st.session\_state.df.columns))
st.subheader("📌 Sample Data")
st.dataframe(st.session\_state.df.head())
else:
st.warning("Please upload a file from the Home page.")

elif section == "Dashboard":
st.title("📊 Dashboard Metrics")
if st.session\_state.df is not None:
df = st.session\_state.df
st.metric("Total Users", len(df))
st.metric("High Risk Users", df\[df\["risk\_level"] == "High"].shape\[0])
st.metric("Average Churn Score", round(df\["churn\_score"].mean(), 2))
else:
st.warning("Please upload a file from the Home page.")

elif section == "Segments":
st.title("📌 Segmentation Insights")
if st.session\_state.df is not None:
df = st.session\_state.df
selected\_risk = st.selectbox("Select Risk Level", df\["risk\_level"].unique())
filtered = df\[df\["risk\_level"] == selected\_risk]
st.write(f"Filtered users in {selected\_risk} risk:", filtered.shape\[0])
st.dataframe(filtered)
else:
st.warning("Please upload a file from the Home page.")

elif section == "About":
st.title("About RetentionOS")
st.markdown("""
RetentionOS is a lightweight churn prediction and nudging assistant built for fast-moving product teams at early-stage startups.

```
**Benefits:**
- Detect churn risk across users (High, Medium, Low)
- Gain actionable insights using simple dashboards
- Get smart nudge recommendations
- Export ready-to-use campaign files

**Expected Outcomes:**
- Better retention strategies
- Data-backed nudge campaigns
- Faster user segmentation
- Clear churn trends and metrics
""")
```
