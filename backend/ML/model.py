import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "ProsperOS_loan_emi_dataset_500.xlsx"

MODEL_PATH = BASE_DIR / "financial_risk_model.pkl"


# =========================================================
# LOAD DATASET
# =========================================================

data = pd.read_excel(DATASET_PATH)

print("Columns in dataset:")
print(data.columns.tolist())

print("\nDataset loaded successfully!")
print(data.head())


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [
    "income",
    "expenses",
    "savings",
    "loan_emi",
    "family_members",
    "risk_level"
]

for column in required_columns:

    if column not in data.columns:

        raise ValueError(
            f"Missing required column: {column}"
        )


# =========================================================
# CLEAN DATA
# =========================================================

data = data.dropna(
    subset=required_columns
)

# Make sure numeric columns are numeric

numeric_columns = [
    "income",
    "expenses",
    "savings",
    "loan_emi",
    "family_members"
]

for column in numeric_columns:

    data[column] = pd.to_numeric(
        data[column],
        errors="coerce"
    )

data = data.dropna(
    subset=numeric_columns
)


# =========================================================
# CREATE FINANCIAL FEATURES
# =========================================================

# Prevent division by zero

income_safe = data["income"].replace(
    0,
    1
)


# ---------------------------------------------------------
# Expense Ratio
# ---------------------------------------------------------

data["expense_ratio"] = (
    data["expenses"] / income_safe
)


# ---------------------------------------------------------
# EMI Ratio
# ---------------------------------------------------------

data["emi_ratio"] = (
    data["loan_emi"] / income_safe
)


# ---------------------------------------------------------
# Savings Ratio
# ---------------------------------------------------------

data["savings_ratio"] = (
    data["savings"] / income_safe
)


# ---------------------------------------------------------
# Remaining Money
# ---------------------------------------------------------

data["remaining_money"] = (
    data["income"]
    - data["expenses"]
    - data["loan_emi"]
)


# =========================================================
# DISPLAY FEATURES
# =========================================================

print("\nFinancial features created:")

print(
    data[
        [
            "income",
            "expenses",
            "savings",
            "loan_emi",
            "expense_ratio",
            "emi_ratio",
            "savings_ratio",
            "remaining_money",
            "risk_level"
        ]
    ].head()
)


# =========================================================
# RISK DISTRIBUTION
# =========================================================

print("\nRisk Level Distribution:")

print(
    data["risk_level"].value_counts()
)


# =========================================================
# ML FEATURES
# =========================================================

features = [

    "income",

    "expenses",

    "savings",

    "loan_emi",

    "family_members",

    "expense_ratio",

    "emi_ratio",

    "savings_ratio",

    "remaining_money"

]


X = data[features]

y = data["risk_level"]


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)


# =========================================================
# RANDOM FOREST
# =========================================================

model = RandomForestClassifier(

    n_estimators=500,

    max_depth=12,

    min_samples_split=4,

    min_samples_leaf=2,

    class_weight="balanced",

    random_state=42,

    n_jobs=-1

)


# =========================================================
# TRAIN
# =========================================================

model.fit(

    X_train,

    y_train

)

print("\nModel Training Completed!")


# =========================================================
# TEST PREDICTION
# =========================================================

y_pred = model.predict(
    X_test
)


# =========================================================
# ACCURACY
# =========================================================

accuracy = accuracy_score(

    y_test,

    y_pred

)

print("\nModel Accuracy:")

print(
    round(accuracy, 2)
)


# =========================================================
# CLASSIFICATION REPORT
# =========================================================

print("\nClassification Report:")

print(

    classification_report(

        y_test,

        y_pred,

        zero_division=0

    )

)


# =========================================================
# FEATURE IMPORTANCE
# =========================================================

print("\nFeature Importance:")

importance = pd.DataFrame({

    "Feature": features,

    "Importance":
        model.feature_importances_

}).sort_values(

    by="Importance",

    ascending=False

)


print(
    importance.to_string(
        index=False
    )
)


# =========================================================
# SAVE MODEL
# =========================================================

joblib.dump(

    model,

    MODEL_PATH

)


print("\nModel saved successfully!")

print(
    f"File: {MODEL_PATH}"
)