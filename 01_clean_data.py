import pandas as pd

# Load raw data
df = pd.read_csv("churn-dataset.csv")
print("Raw shape:", df.shape)

# 1. Drop customerID - it's just an identifier, not useful for prediction
df = df.drop(columns=["customerID"])

# 2. TotalCharges is stored as text and has some blank strings for brand-new
#    customers (tenure = 0). Convert to numeric, then fill blanks with 0.
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# 3. Convert target column to 0/1
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# 4. Convert SeniorCitizen (already 0/1) to keep consistent, no change needed

# 5. One-hot encode all remaining text/categorical columns
categorical_cols = df.select_dtypes(include="object").columns.tolist()
print("Categorical columns to encode:", categorical_cols)

df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

print("Cleaned shape:", df_encoded.shape)
print("Churn rate: {:.1f}%".format(df_encoded["Churn"].mean() * 100))

df_encoded.to_csv("telco_churn_clean.csv", index=False)
print("Saved cleaned data to telco_churn_clean.csv")
