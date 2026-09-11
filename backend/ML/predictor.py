import joblib
import pandas as pd
from pathlib import Path


# =========================================================
# LOAD MODEL
# =========================================================

BASE_DIR = Path(__file__).parent

MODEL_PATH = BASE_DIR / "financial_risk_model.pkl"

model = joblib.load(MODEL_PATH)


# =========================================================
# PREDICT RISK
# =========================================================

def predict_risk(
    income,
    expenses,
    savings,
    loan_emi,
    family_members
):

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    if income <= 0:
        raise ValueError("Income must be greater than zero.")

    if expenses < 0:
        raise ValueError("Expenses cannot be negative.")

    if savings < 0:
        raise ValueError("Savings cannot be negative.")

    if loan_emi < 0:
        raise ValueError("Loan EMI cannot be negative.")

    if family_members < 1:
        raise ValueError("Family members must be at least 1.")


    # -----------------------------------------------------
    # Financial Features
    # -----------------------------------------------------

    expense_ratio = expenses / income

    emi_ratio = loan_emi / income

    savings_ratio = savings / income

    remaining_money = (
        income
        - expenses
        - loan_emi
    )


    # -----------------------------------------------------
    # Create DataFrame
    # IMPORTANT:
    # The columns must match model.py
    # -----------------------------------------------------

    input_data = pd.DataFrame([{

        "income": income,

        "expenses": expenses,

        "savings": savings,

        "loan_emi": loan_emi,

        "family_members": family_members,

        "expense_ratio": expense_ratio,

        "emi_ratio": emi_ratio,

        "savings_ratio": savings_ratio,

        "remaining_money": remaining_money

    }])


    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    prediction = model.predict(input_data)

    risk = prediction[0]

    return risk


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("\n===================================")
    print("ProsperOS ML Prediction Test")
    print("===================================")


    # Test household

    income = 10000

    expenses = 7000

    savings = 3000

    loan_emi = 2000

    family_members = 4


    print(f"\nIncome: ₹{income}")
    print(f"Expenses: ₹{expenses}")
    print(f"Savings: ₹{savings}")
    print(f"Loan EMI: ₹{loan_emi}")
    print(f"Family Members: {family_members}")


    # -----------------------------------------------------
    # Calculate financial metrics
    # -----------------------------------------------------

    expense_ratio = expenses / income

    emi_ratio = loan_emi / income

    savings_ratio = savings / income

    remaining_money = (
        income
        - expenses
        - loan_emi
    )


    print("\nFinancial Metrics:")

    print(
        f"Expense Ratio: {expense_ratio:.2%}"
    )

    print(
        f"EMI Ratio: {emi_ratio:.2%}"
    )

    print(
        f"Savings Ratio: {savings_ratio:.2%}"
    )

    print(
        f"Remaining Money: ₹{remaining_money}"
    )


    # -----------------------------------------------------
    # Predict
    # -----------------------------------------------------

    risk = predict_risk(

        income=income,

        expenses=expenses,

        savings=savings,

        loan_emi=loan_emi,

        family_members=family_members

    )


    print("\nPredicted Risk:")

    print(risk)