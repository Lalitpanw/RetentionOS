import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="RetentionOS", layout="wide")
st.title("📊 RetentionOS – Upload User Data")

uploaded_file = st.file_uploader("Upload your user Excel/CSV file")
if uploaded_file.name.endswith('.csv'):
    df = pd.read_csv(uploaded_file)
elif uploaded_file.name.endswith(('.xls', '.xlsx')):
    df = pd.read_excel(uploaded_file)
else:
    st.error("Unsupported file format. Please upload a CSV or Excel file.")
    st.stop()

