from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime

# =========================================================
# Import ML predictor
# =========================================================

from ML.predictor import predict_risk


# =========================================================
# Import RAG + Gemini
# =========================================================

from RAG.rag import ask_prosperos


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="ProsperOS API",
    version="2.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# Household Model
# =========================================================

class Household(BaseModel):

    name: str = Field(
        ...,
        min_length=3
    )

    age: int = Field(
        ...,
        ge=18,
        le=100
    )

    gender: str

    mobile: str = Field(
        ...,
        min_length=10,
        max_length=10
    )

    family_members: int = Field(
        ...,
        ge=1
    )

    occupation: str

    education: str

    location: str

    income: float = Field(
        ...,
        ge=0
    )

    expenses: float = Field(
        ...,
        ge=0
    )

    savings: float = Field(
        ...,
        ge=0
    )

    loan_emi: float = Field(
        ...,
        ge=0
    )

    skill: str


# =========================================================
# Chat Request Model
# =========================================================

class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1
    )


# =========================================================
# Home API
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to ProsperOS API",
        "status": "running"
    }


# =========================================================
# Health Check
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "ProsperOS",
        "ml": "enabled",
        "rag": "enabled",
        "gemini": "enabled"
    }


# =========================================================
# Financial Analysis
# =========================================================

def calculate_financial_health(
    data: Household
):

    # -----------------------------------------------------
    # Monthly Remaining Money
    # -----------------------------------------------------

    remaining_money = (
        data.income
        - data.expenses
        - data.loan_emi
    )


    # -----------------------------------------------------
    # ML Risk Prediction
    # -----------------------------------------------------

    risk = predict_risk(

        income=data.income,

        expenses=data.expenses,

        savings=data.savings,

        loan_emi=data.loan_emi,

        family_members=data.family_members

    )


    # -----------------------------------------------------
    # Financial Health Score
    # -----------------------------------------------------

    if risk == "Low":

        score = 85

    elif risk == "Medium":

        score = 60

    else:

        score = 30


    # -----------------------------------------------------
    # Saving Rate
    # -----------------------------------------------------

    if data.income > 0:

        saving_rate = round(

            (
                data.savings
                / data.income
            ) * 100,

            2

        )

    else:

        saving_rate = 0


    # -----------------------------------------------------
    # Expense Ratio
    # -----------------------------------------------------

    if data.income > 0:

        expense_ratio = round(

            (
                data.expenses
                / data.income
            ) * 100,

            2

        )

    else:

        expense_ratio = 0


    # -----------------------------------------------------
    # EMI Ratio
    # -----------------------------------------------------

    if data.income > 0:

        emi_ratio = round(

            (
                data.loan_emi
                / data.income
            ) * 100,

            2

        )

    else:

        emi_ratio = 0


    # -----------------------------------------------------
    # Future Financial Prediction
    # -----------------------------------------------------

    future_income = round(

        data.income * 1.08,

        2

    )

    future_expense = round(

        data.expenses * 1.12,

        2

    )


    # -----------------------------------------------------
    # Recommendation
    # -----------------------------------------------------

    if risk == "Low":

        recommendation = (

            "Your household has a low financial risk. "
            "Continue saving regularly and maintain "
            "your current financial discipline."

        )

    elif risk == "Medium":

        recommendation = (

            "Your household has a medium financial risk. "
            "Try to reduce unnecessary expenses, "
            "manage your EMI carefully, and increase "
            "your monthly savings."

        )

    else:

        recommendation = (

            "Your household has a high financial risk. "
            "Your expenses and EMI may place pressure "
            "on your income. Prioritize essential "
            "expenses, manage EMI payments, and build "
            "an emergency fund."

        )


    # -----------------------------------------------------
    # Analysis Result
    # -----------------------------------------------------

    return {

        "financial_health_score": score,

        "risk_level": risk,

        "monthly_savings": (

            data.income
            - data.expenses

        ),

        "saving_rate": saving_rate,

        "expense_ratio": expense_ratio,

        "emi_ratio": emi_ratio,

        "remaining_money": remaining_money,

        "future_income": future_income,

        "future_expense": future_expense,

        "recommendation": recommendation,

        "analysis_date": datetime.now().strftime(
            "%d-%m-%Y"
        ),

        "model_version": (
            "ProsperOS Random Forest ML v2.0"
        )

    }


# =========================================================
# Register API
# =========================================================

@app.post("/register")
def register_household(
    household: Household
):

    analysis = calculate_financial_health(
        household
    )


    return {

        "success": True,

        "message": (
            "Household Registered Successfully"
        ),

        "household": household,

        "analysis": analysis

    }


# =========================================================
# RAG + GEMINI CHAT API
# =========================================================

@app.post("/chat")
def chat(
    request: ChatRequest
):

    # -----------------------------------------------------
    # Clean user question
    # -----------------------------------------------------

    question = request.question.strip()


    # -----------------------------------------------------
    # Check empty question
    # -----------------------------------------------------

    if not question:

        return {

            "success": False,

            "message": (
                "Question cannot be empty."
            )

        }


    # -----------------------------------------------------
    # Run RAG pipeline
    # -----------------------------------------------------

    result = ask_prosperos(

        question,

        top_k=5

    )


    # -----------------------------------------------------
    # Return chatbot response
    # -----------------------------------------------------

    return {

        "success": True,

        "question": result["question"],

        "answer": result["answer"],

        "sources": result["sources"]

    }