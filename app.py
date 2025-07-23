import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="RetentionOS", layout="wide")
st.title("📊 RetentionOS – Upload User Data")

# File uploader
uploaded_file = st.file_uploader("Upload your user Excel/CSV file")

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        st.stop()
    
    st.success("✅ File uploaded successfully!")
    st.dataframe(df.head())

    # Optional: Save to session for later use in dashboard
    st.session_state['df'] = df
else:
    st.info("📂 Please upload a file to proceed.")


