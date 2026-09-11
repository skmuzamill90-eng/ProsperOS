// =========================================================
// ProsperOS Dashboard
// Displays real data returned by FastAPI + ML Model
// =========================================================


// =========================================================
// LOAD DATA
// =========================================================

const household =
    JSON.parse(
        localStorage.getItem("household")
    );

const analysis =
    JSON.parse(
        localStorage.getItem("analysis")
    );


// =========================================================
// CHECK DATA
// =========================================================

if (!household || !analysis) {

    alert(
        "No household analysis found. Please register first."
    );

    window.location.href =
        "registration.html";

}


// =========================================================
// HELPER FUNCTION
// =========================================================

function formatCurrency(value) {

    return "₹ " +
        Number(value || 0).toLocaleString("en-IN");

}


// =========================================================
// WELCOME
// =========================================================

document.getElementById(
    "welcomeName"
).textContent =
    `Welcome, ${household.name}`;


// =========================================================
// HOUSEHOLD INFORMATION
// =========================================================

document.getElementById(
    "name"
).textContent =
    household.name;

document.getElementById(
    "age"
).textContent =
    household.age;

document.getElementById(
    "gender"
).textContent =
    household.gender;

document.getElementById(
    "mobile"
).textContent =
    household.mobile;

document.getElementById(
    "members"
).textContent =
    household.family_members;

document.getElementById(
    "occupation"
).textContent =
    household.occupation;

document.getElementById(
    "education"
).textContent =
    household.education;

document.getElementById(
    "location"
).textContent =
    household.location;


// =========================================================
// FINANCIAL INFORMATION
// =========================================================

document.getElementById(
    "income"
).textContent =
    formatCurrency(
        household.income
    );

document.getElementById(
    "expenses"
).textContent =
    formatCurrency(
        household.expenses
    );

document.getElementById(
    "savings"
).textContent =
    formatCurrency(
        household.savings
    );

document.getElementById(
    "loanEmi"
).textContent =
    formatCurrency(
        household.loan_emi
    );

document.getElementById(
    "skill"
).textContent =
    household.skill;


// =========================================================
// ML RESULT
// =========================================================

document.getElementById(
    "healthScore"
).textContent =
    analysis.financial_health_score;

document.getElementById(
    "riskLevel"
).textContent =
    analysis.risk_level;

document.getElementById(
    "monthlySavings"
).textContent =
    formatCurrency(
        analysis.monthly_savings
    );


// =========================================================
// FINANCIAL ANALYSIS
// =========================================================

document.getElementById(
    "savingRate"
).textContent =
    analysis.saving_rate + "%";


document.getElementById(
    "expenseRatio"
).textContent =
    analysis.expense_ratio + "%";


document.getElementById(
    "emiRatio"
).textContent =
    analysis.emi_ratio + "%";


document.getElementById(
    "remainingMoney"
).textContent =
    formatCurrency(
        analysis.remaining_money
    );


document.getElementById(
    "futureIncome"
).textContent =
    formatCurrency(
        analysis.future_income
    );


document.getElementById(
    "futureExpense"
).textContent =
    formatCurrency(
        analysis.future_expense
    );


// =========================================================
// AI RECOMMENDATION
// =========================================================

document.getElementById(
    "recommendation"
).textContent =
    analysis.recommendation;


// =========================================================
// ANALYSIS INFORMATION
// =========================================================

document.getElementById(
    "analysisDate"
).textContent =
    analysis.analysis_date;

document.getElementById(
    "modelVersion"
).textContent =
    analysis.model_version;


// =========================================================
// RISK COLOR
// =========================================================

const riskElement =
    document.getElementById(
        "riskLevel"
    );


if (
    analysis.risk_level === "Low"
) {

    riskElement.style.color =
        "green";

}

else if (
    analysis.risk_level === "Medium"
) {

    riskElement.style.color =
        "orange";

}

else {

    riskElement.style.color =
        "red";

}


// =========================================================
// HEALTH SCORE COLOR
// =========================================================

const scoreElement =
    document.getElementById(
        "healthScore"
    );


if (
    analysis.financial_health_score >= 80
) {

    scoreElement.style.color =
        "green";

}

else if (
    analysis.financial_health_score >= 50
) {

    scoreElement.style.color =
        "orange";

}

else {

    scoreElement.style.color =
        "red";

}




// =========================================================
// GOVERNMENT SCHEME BUTTON
// =========================================================

const schemeButton = document.getElementById("schemeButton");
const schemeResults = document.getElementById("schemeResults");

console.log("Scheme button:", schemeButton);


if (schemeButton) {

    schemeButton.addEventListener("click", async function () {

        console.log("Find Government Schemes button clicked");


        // Show loading
        schemeButton.disabled = true;

        schemeButton.textContent =
            "🔄 Finding Schemes...";


        schemeResults.innerHTML = `
            <p>
                🔎 Searching relevant government schemes...
            </p>
        `;


        try {

            const question = `
                Find government schemes relevant to this household.

                Occupation: ${household.occupation}
                Education: ${household.education}
                Location: ${household.location}
                Monthly Income: ${household.income}
                Monthly Expenses: ${household.expenses}
                Savings: ${household.savings}
                Loan EMI: ${household.loan_emi}
                Family Members: ${household.family_members}
                Skill: ${household.skill}

                Risk Level: ${analysis.risk_level}
                Financial Health Score:
                ${analysis.financial_health_score}
            `;


            console.log("Sending scheme request...");


            const response = await fetch(
                "http://127.0.0.1:8000/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        question: question
                    })
                }
            );


            console.log(
                "Server response:",
                response.status
            );


            if (!response.ok) {

                throw new Error(
                    `Server returned ${response.status}`
                );

            }


            const data = await response.json();


            console.log(
                "RAG response:",
                data
            );


            // Display result
            schemeResults.innerHTML = `

                <div class="scheme-answer">

                    <h3>
                        🤖 Recommended Government Schemes
                    </h3>

                    ${marked.parse(
                        data.answer || 
                        "No scheme information found."
                    )}

                </div>

            `;


        }

        catch (error) {

            console.error(
                "Scheme search error:",
                error
            );


            schemeResults.innerHTML = `

                <div class="scheme-error">

                    <h3>
                        ⚠️ Unable to find schemes
                    </h3>

                    <p>
                        ${error.message}
                    </p>

                    <p>
                        Please make sure FastAPI is running.
                    </p>

                </div>

            `;

        }


        finally {

            schemeButton.disabled = false;

            schemeButton.textContent =
                "🔎 Find Government Schemes";

        }

    });

}