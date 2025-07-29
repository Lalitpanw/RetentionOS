import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ------------------------------------------
# ✅ STEP 1: Create or load training dataset
# ------------------------------------------
data = {
    'product_views':     [10, 1, 15, 2, 7, 12, 0, 5, 3, 8, 6, 0, 4, 11, 9],
    'cart_items':        [2, 0, 1, 0, 1, 3, 0, 1, 0, 2, 1, 0, 1, 2, 3],
    'total_sessions':    [8, 1, 10, 2, 4, 7, 1, 5, 3, 6, 3, 2, 4, 7, 8],
    'last_active_days':  [2, 30, 3, 27, 6, 1, 35, 9, 22, 5, 11, 28, 13, 4, 3],
    'orders':            [1, 0, 1, 0, 1, 2, 0, 1, 0, 1, 1, 0, 1, 2, 2],
    'cart_value':        [150, 0, 200, 0, 100, 300, 0, 120, 0, 180, 90, 0, 110, 220, 250],
    'churned':           [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0]
}

df = pd.DataFrame(data)

# ------------------------------------------
# ✅ STEP 2: Train/test split
# ------------------------------------------
X = df[['product_views', 'cart_items', 'total_sessions', 'last_active_days', 'orders', 'cart_value']]
y = df['churned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ------------------------------------------
# ✅ STEP 3: Train Logistic Regression model
# ------------------------------------------
model = LogisticRegression()
model.fit(X_train, y_train)

# ------------------------------------------
# ✅ STEP 4: Evaluate the model
# ------------------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("🎯 Accuracy:", round(accuracy, 2))
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

# ------------------------------------------
# ✅ STEP 5: Save the model
# ------------------------------------------
joblib.dump(model, "churn_model.pkl")
print("✅ churn_model.pkl saved successfully.")
