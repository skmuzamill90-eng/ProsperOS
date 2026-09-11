// ==========================================
// ProsperOS - Main JavaScript
// ==========================================

console.log("ProsperOS Loaded Successfully");

// ===============================
// Register Button
// ===============================

const registerButton = document.querySelector(".primary-btn");

if (registerButton) {

    registerButton.addEventListener("click", () => {

        window.location.href = "registration.html";

    });

}

// ===============================
// Learn More Button
// ===============================

const learnMoreButton = document.querySelector(".secondary-btn");

if (learnMoreButton) {

    learnMoreButton.addEventListener("click", () => {

        document.getElementById("about").scrollIntoView({

            behavior: "smooth"

        });

    });

}

// ===============================
// Smooth Navigation
// ===============================

const navLinks = document.querySelectorAll('a[href^="#"]');

navLinks.forEach(link => {

    link.addEventListener("click", function(e){

        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if(target){

            target.scrollIntoView({

                behavior: "smooth"

            });

        }

    });

});

// ===============================
// Navbar Shadow on Scroll
// ===============================

window.addEventListener("scroll", () => {

    const header = document.querySelector("header");

    if(window.scrollY > 50){

        header.style.boxShadow = "0 2px 10px rgba(0,0,0,0.2)";

    }

    else{

        header.style.boxShadow = "none";

    }

});

// ===============================
// Feature Card Animation
// ===============================

const cards = document.querySelectorAll(".feature-card");

cards.forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-8px)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "translateY(0px)";

    });

});

// ===============================
// Welcome Message
// ===============================

window.onload = () => {

    console.log("Welcome to ProsperOS");

};