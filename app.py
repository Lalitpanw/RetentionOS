import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RetentionOS", layout="wide")
st.title("📊 RetentionOS – Upload User Data")

uploaded_file = st.file_uploader("Upload your user Excel/CSV file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("✅ File uploaded successfully!")
    st.dataframe(df.head())
