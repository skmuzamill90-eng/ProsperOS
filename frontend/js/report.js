// ==========================================
// ProsperOS Report JavaScript
// ==========================================

// Load data from Local Storage
const household = JSON.parse(localStorage.getItem("household"));
const analysis = JSON.parse(localStorage.getItem("analysis"));

// If no data, go back to registration
if (!household || !analysis) {

    alert("No household data found.");

    window.location.href = "registration.html";

}

// ==========================================
// Household Information
// ==========================================

document.getElementById("name").textContent = household.name;
document.getElementById("age").textContent = household.age;
document.getElementById("gender").textContent = household.gender;
document.getElementById("mobile").textContent = household.mobile;
document.getElementById("members").textContent = household.family_members;
document.getElementById("occupation").textContent = household.occupation;
document.getElementById("education").textContent = household.education;
document.getElementById("location").textContent = household.location;

// ==========================================
// Financial Information
// ==========================================

document.getElementById("income").textContent =
    "₹ " + household.income.toLocaleString();

document.getElementById("expenses").textContent =
    "₹ " + household.expenses.toLocaleString();

document.getElementById("savings").textContent =
    "₹ " + household.savings.toLocaleString();

document.getElementById("loans").textContent =
    "₹ " + household.loans.toLocaleString();

document.getElementById("assets").textContent =
    "₹ " + household.assets.toLocaleString();

document.getElementById("skill").textContent =
    household.skill;

// ==========================================
// AI Analysis
// ==========================================

document.getElementById("healthScore").textContent =
    analysis.financial_health_score;

document.getElementById("riskLevel").textContent =
    analysis.risk_level;

document.getElementById("monthlySavings").textContent =
    "₹ " + analysis.monthly_savings.toLocaleString();

document.getElementById("recommendation").textContent =
    analysis.recommendation;

// ==========================================
// Health Score Color
// ==========================================

const score = document.getElementById("healthScore");

if (analysis.financial_health_score >= 80) {

    score.style.color = "green";

}
else if (analysis.financial_health_score >= 50) {

    score.style.color = "orange";

}
else {

    score.style.color = "red";

}

// ==========================================
// Risk Level Color
// ==========================================

const risk = document.getElementById("riskLevel");

if (analysis.risk_level === "Low") {

    risk.style.color = "green";

}
else if (analysis.risk_level === "Medium") {

    risk.style.color = "orange";

}
else {

    risk.style.color = "red";

}

// ==========================================
// Console
// ==========================================

console.log("ProsperOS Report Loaded Successfully");