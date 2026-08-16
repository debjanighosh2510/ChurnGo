"""
Day 2 - Step 1: Compute SHAP values so we can explain WHY the model
makes each prediction, not just WHAT it predicts.
"""
import pandas as pd
import joblib
import shap

# Load the trained model and the held-out test data from Day 1
model = joblib.load("churn_model.pkl")
X_test = pd.read_csv("X_test.csv")

print("Loaded model and test data:", X_test.shape)

# TreeExplainer is the fast, exact SHAP method for tree-based models
# like XGBoost (as opposed to KernelExplainer, which is slower and
# approximate - good to know for interview questions).
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

print("SHAP values shape:", shap_values.shape)  # (n_customers, n_features)

# Save everything the dashboard will need:
# - shap_values as a DataFrame (same shape/columns as X_test)
# - the base_value (average prediction before any features are applied)
shap_df = pd.DataFrame(shap_values, columns=X_test.columns)
shap_df.to_csv("shap_values.csv", index=False)

with open("shap_base_value.txt", "w") as f:
    f.write(str(explainer.expected_value))

print("Saved shap_values.csv and shap_base_value.txt")
print("Base value (average model output before features applied):",
      explainer.expected_value)
