import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

# -----------------------
# Step 1: Create sample churn dataset
# -----------------------
data = {
    "user_id": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    "last_active_days": [2, 25, 5, 18, 3, 30, 6, 22, 8, 15],
    "orders": [4, 0, 2, 1, 3, 0, 3, 0, 2, 1],
    "total_sessions": [10, 1, 7, 2, 5, 1, 6, 2, 8, 3],
    "churned": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

# -----------------------
# Step 2: Prepare features and label
# -----------------------
X = df[["last_active_days", "orders", "total_sessions"]]
y = df["churned"]

# -----------------------
# Step 3: Train/test split
# -----------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# -----------------------
# Step 4: Train model
# -----------------------
model = LogisticRegression()
model.fit(X_train, y_train)

# -----------------------
# Step 5: Evaluate
# -----------------------
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("✅ Model Trained")
print(f"🎯 Accuracy: {acc:.2f}")
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))
print("🔍 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# -----------------------
# Step 6: Save model
# -----------------------
joblib.dump(model, "churn_model.pkl")
print("💾 Model saved to churn_model.pkl")
