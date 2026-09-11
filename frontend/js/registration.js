// =========================================================
// ProsperOS Registration
// Registration UI → FastAPI → ML Model → Dashboard
// =========================================================


// =========================================================
// FORM
// =========================================================

const form = document.getElementById("registrationForm");


// =========================================================
// SUBMIT FORM
// =========================================================

form.addEventListener("submit", async function (event) {

    // Prevent normal form submission
    event.preventDefault();


    // =====================================================
    // GET FORM VALUES
    // =====================================================

    const householdData = {

        // -----------------------------
        // Personal Information
        // -----------------------------

        name: document
            .getElementById("name")
            .value
            .trim(),

        age: Number(
            document.getElementById("age").value
        ),

        gender: document
            .getElementById("gender")
            .value,

        mobile: document
            .getElementById("mobile")
            .value
            .trim(),


        // -----------------------------
        // Household Information
        // -----------------------------

        family_members: Number(
            document.getElementById("members").value
        ),

        occupation: document
            .getElementById("occupation")
            .value
            .trim(),

        education: document
            .getElementById("education")
            .value,

        location: document
            .getElementById("location")
            .value
            .trim(),


        // -----------------------------
        // Financial Information
        // -----------------------------

        income: Number(
            document.getElementById("income").value
        ),

        expenses: Number(
            document.getElementById("expenses").value
        ),

        savings: Number(
            document.getElementById("savings").value
        ),

        loan_emi: Number(
            document.getElementById("loan_emi").value
        ),


        // -----------------------------
        // Skill
        // -----------------------------

        skill: document
            .getElementById("skill")
            .value
            .trim()

    };


    // =====================================================
    // VALIDATION
    // =====================================================

    // Name
    if (householdData.name.length < 3) {

        alert(
            "Please enter a valid name."
        );

        return;
    }


    // Age
    if (
        householdData.age < 18 ||
        householdData.age > 100
    ) {

        alert(
            "Age must be between 18 and 100."
        );

        return;
    }


    // Mobile
    if (
        !/^[0-9]{10}$/.test(
            householdData.mobile
        )
    ) {

        alert(
            "Please enter a valid 10-digit mobile number."
        );

        return;
    }


    // Family members
    if (
        householdData.family_members < 1
    ) {

        alert(
            "Family members must be at least 1."
        );

        return;
    }


    // Income
    if (
        householdData.income <= 0
    ) {

        alert(
            "Monthly income must be greater than ₹0."
        );

        return;
    }


    // Expenses
    if (
        householdData.expenses < 0
    ) {

        alert(
            "Monthly expenses cannot be negative."
        );

        return;
    }


    // Savings
    if (
        householdData.savings < 0
    ) {

        alert(
            "Savings cannot be negative."
        );

        return;
    }


    // Loan EMI
    if (
        householdData.loan_emi < 0
    ) {

        alert(
            "Loan EMI cannot be negative."
        );

        return;
    }


    // =====================================================
    // SUBMIT BUTTON
    // =====================================================

    const submitButton =
        form.querySelector(
            'button[type="submit"]'
        );


    submitButton.disabled = true;

    submitButton.textContent =
        "🤖 Analyzing Financial Risk...";


    // =====================================================
    // SEND DATA TO FASTAPI
    // =====================================================

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/register",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(
                    householdData
                )

            }
        );


        // =================================================
        // CHECK API RESPONSE
        // =================================================

        if (!response.ok) {

            let errorMessage =
                "Registration failed.";

            try {

                const errorData =
                    await response.json();

                console.error(
                    "FastAPI Error:",
                    errorData
                );

                if (
                    errorData.detail
                ) {

                    errorMessage =
                        "Registration failed: " +
                        JSON.stringify(
                            errorData.detail
                        );

                }

            }

            catch (error) {

                console.error(
                    "Unable to read API error:",
                    error
                );

            }


            alert(errorMessage);

            return;
        }


        // =================================================
        // GET API JSON RESPONSE
        // =================================================

        const result =
            await response.json();


        console.log(
            "ProsperOS API Response:",
            result
        );


        // =================================================
        // CHECK SUCCESS
        // =================================================

        if (!result.success) {

            alert(
                "Household registration failed."
            );

            return;
        }


        // =================================================
        // SAVE HOUSEHOLD DATA
        // =================================================

        localStorage.setItem(
            "household",
            JSON.stringify(
                result.household
            )
        );


        // =================================================
        // SAVE ML ANALYSIS
        // =================================================

        localStorage.setItem(
            "analysis",
            JSON.stringify(
                result.analysis
            )
        );


        // =================================================
        // OPTIONAL: SAVE COMPLETE RESPONSE
        // =================================================

        localStorage.setItem(
            "prosperosResult",
            JSON.stringify(
                result
            )
        );


        // =================================================
        // REDIRECT TO DASHBOARD
        // =================================================

        window.location.href =
            "dashboard.html";


    }


    // =====================================================
    // CONNECTION ERROR
    // =====================================================

    catch (error) {

        console.error(
            "Connection Error:",
            error
        );


        alert(
            "Unable to connect to ProsperOS backend.\n\n" +
            "Please make sure FastAPI is running on:\n" +
            "http://127.0.0.1:8000"
        );

    }


    // =====================================================
    // RESTORE BUTTON
    // =====================================================

    finally {

        submitButton.disabled = false;

        submitButton.textContent =
            "🤖 Analyze My Financial Risk";

    }

});