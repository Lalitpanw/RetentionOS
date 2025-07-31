import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
from fuzzywuzzy import fuzz

st.set_page_config(page_title="RetentionOS", layout="wide")

st.title("RetentionOS – Universal Churn Predictor")

st.markdown("""
Upload any CSV/Excel file with user-level data. The tool will:
- Automatically detect relevant columns
- Train a churn prediction model on the fly
- Assign churn probabilities and risk levels
- Provide download-ready results
""")

uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head())

        # Step 1: Try auto-mapping
        expected_fields = {
            'last_active_days': ['last_seen', 'last_active', 'inactive_days'],
            'total_sessions': ['sessions', 'login_count', 'visits'],
            'orders': ['orders', 'purchases', 'transactions'],
        }

        def auto_map_columns(df):
            mapping = {}
            for key, options in expected_fields.items():
                for col in df.columns:
                    for opt in options:
                        if fuzz.partial_ratio(col.lower(), opt.lower()) > 80:
                            mapping[key] = col
                            break
            return mapping

        mapping = auto_map_columns(df)

        st.markdown("### 🧠 Column Mapping")
        for key in expected_fields:
            if key in mapping:
                st.markdown(f"✅ `{key}` → `{mapping[key]}`")
            else:
                mapping[key] = st.selectbox(f"Select column for **{key}**", df.columns)

        # Step 2: Rename and prepare features
        df = df.rename(columns={mapping[k]: k for k in mapping})

        # Step 3: Use required columns if available, else fallback to numeric
        required = ['last_active_days', 'orders', 'total_sessions']
        if all(col in df.columns for col in required):
            X = df[required].fillna(0)
        else:
            st.warning("Standard fields missing. Using all numeric columns.")
            X = df.select_dtypes(include='number').fillna(0)

        # Step 4: Simulated label
        y = (df['orders'] == 0).astype(int) if 'orders' in df.columns else np.random.randint(0, 2, size=len(df))

        # Step 5: Train model
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = LogisticRegression()
        model.fit(X_scaled, y)

        df['churn_probability'] = model.predict_proba(X_scaled)[:, 1]

        def label_risk(p):
            if p >= 0.7:
                return "🔴 High"
            elif p >= 0.4:
                return "🟠 Medium"
            else:
                return "🟢 Low"

        df['risk_level'] = df['churn_probability'].apply(label_risk)

        st.markdown("### 📊 Churn Prediction Results")
        st.dataframe(df[['churn_probability', 'risk_level']].join(df.drop(columns=['churn_probability', 'risk_level'])))

        st.markdown("### 📈 Insights")
        fig1 = px.histogram(df, x="churn_probability", nbins=20, title="Churn Probability Distribution")
        st.plotly_chart(fig1, use_container_width=True)

        fig2 = px.pie(df, names="risk_level", title="Risk Level Breakdown")
        st.plotly_chart(fig2, use_container_width=True)

        # Step 6: Downloadable output
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results (CSV)", csv, file_name="retentionos_output.csv", mime="text/csv")

    except Exception as e:
        st.error("❌ Error while processing file:")
        st.exception(e)
else:
    st.info("👆 Upload your user-level data to begin.")
