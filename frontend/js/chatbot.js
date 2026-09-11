// =========================================================
// ProsperOS AI Chatbot
// RAG + FAISS + Gemini
// =========================================================


// =========================================================
// CHATBOT ELEMENTS
// =========================================================

const chatbotWindow =
    document.getElementById("chatbot-window");

const chatMessage =
    document.getElementById("chat-message");

const chatMessages =
    document.getElementById("chat-messages");


// =========================================================
// OPEN / CLOSE CHATBOT
// =========================================================

function toggleChatbot() {

    chatbotWindow.classList.toggle("show");

}


// =========================================================
// ENTER KEY
// =========================================================

chatMessage.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            sendChatMessage();

        }

    }
);


// =========================================================
// SEND MESSAGE
// =========================================================

async function sendChatMessage() {

    const message =
        chatMessage.value.trim();


    // -----------------------------------------------------
    // Empty message
    // -----------------------------------------------------

    if (message === "") {

        return;

    }


    // -----------------------------------------------------
    // Display user message
    // -----------------------------------------------------

    chatMessages.innerHTML += `

        <div class="chat-user">

            <strong>You</strong>

            <p>
                ${escapeHTML(message)}
            </p>

        </div>

    `;


    // Clear input

    chatMessage.value = "";


    // Scroll

    scrollChat();


    // -----------------------------------------------------
    // Loading message
    // -----------------------------------------------------

    const loadingId =
        "loading-" + Date.now();


    chatMessages.innerHTML += `

        <div
            class="chat-ai"
            id="${loadingId}"
        >

            <strong>🤖 ProsperOS AI</strong>

            <p>
                Thinking...
            </p>

        </div>

    `;


    scrollChat();


    try {

        // =================================================
        // CALL FASTAPI
        // =================================================

        const response =
            await fetch(
                "http://127.0.0.1:8000/chat",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        question: message

                    })

                }
            );


        // -------------------------------------------------
        // HTTP ERROR
        // -------------------------------------------------

        if (!response.ok) {

            throw new Error(
                `HTTP error: ${response.status}`
            );

        }


        // -------------------------------------------------
        // JSON RESPONSE
        // -------------------------------------------------

        const data =
            await response.json();


        // -------------------------------------------------
        // Remove loading
        // -------------------------------------------------

        const loading =
            document.getElementById(
                loadingId
            );


        if (loading) {

            loading.remove();

        }


        // =================================================
        // DISPLAY AI ANSWER
        // =================================================

        chatMessages.innerHTML += `

            <div class="chat-ai">

                <strong>
                    🤖 ProsperOS AI
                </strong>

                <div class="ai-answer">

                    ${marked.parse(
                        data.answer || 
                        "Sorry, I could not generate an answer."
                    )}

                </div>

            </div>

        `;


        scrollChat();


    }

    catch (error) {

        console.error(
            "Chatbot error:",
            error
        );


        // -------------------------------------------------
        // Remove loading
        // -------------------------------------------------

        const loading =
            document.getElementById(
                loadingId
            );


        if (loading) {

            loading.remove();

        }


        // -------------------------------------------------
        // Error message
        // -------------------------------------------------

        chatMessages.innerHTML += `

            <div class="chat-ai">

                <strong>
                    ⚠️ ProsperOS AI
                </strong>

                <p>
                    Unable to connect to the AI server.
                </p>

                <small>
                    Please make sure FastAPI is running.
                </small>

            </div>

        `;


        scrollChat();

    }

}


// =========================================================
// SCROLL CHAT
// =========================================================

function scrollChat() {

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


// =========================================================
// ESCAPE HTML
// =========================================================

function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}