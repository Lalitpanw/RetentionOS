from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load your trained model
model = joblib.load("churn_model.pkl")

REQUIRED_COLS = ['product_views', 'cart_items', 'total_sessions',
                 'last_active_days', 'orders', 'cart_value']

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    df = pd.read_csv(file)

    missing = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing:
        return jsonify({"error": f"Missing columns: {missing}"}), 400

    X = df[REQUIRED_COLS]
    preds = model.predict_proba(X)[:, 1]
    df["churn_probability"] = preds.round(2)
    df["churn_risk"] = df["churn_probability"].apply(
        lambda p: "🔴 High" if p >= 0.75 else ("🟠 Medium" if p >= 0.4 else "🟢 Low")
    )

    return df.to_json(orient="records")
