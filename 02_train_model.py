"""
Day 1 - Step 2: Train an XGBoost churn model and evaluate it properly.
"""
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, roc_auc_score, precision_score,
    recall_score, f1_score, accuracy_score
)
from xgboost import XGBClassifier

df = pd.read_csv("telco_churn_clean.csv")

X = df.drop(columns=["Churn"])
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# scale_pos_weight helps XGBoost pay more attention to the minority
# class (churners), since only ~27% of customers actually churn.
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

model = XGBClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    scale_pos_weight=scale_pos_weight,
    eval_metric="logloss",
    random_state=42,
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("=== Evaluation on test set ===")
print("Accuracy: {:.3f}".format(accuracy_score(y_test, y_pred)))
print("Precision: {:.3f}".format(precision_score(y_test, y_pred)))
print("Recall: {:.3f}".format(recall_score(y_test, y_pred)))
print("F1 score: {:.3f}".format(f1_score(y_test, y_pred)))
print("ROC-AUC: {:.3f}".format(roc_auc_score(y_test, y_proba)))
print()
print(classification_report(y_test, y_pred, target_names=["Stayed", "Churned"]))

# Save everything needed for the dashboard later
joblib.dump(model, "churn_model.pkl")
X_test.to_csv("X_test.csv", index=False)
y_test.to_csv("y_test.csv", index=False)
print("Saved model to churn_model.pkl")
