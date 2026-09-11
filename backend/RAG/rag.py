from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer
from google import genai


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).parent

INDEX_PATH = BASE_DIR / "schemes.index"
TEXT_PATH = BASE_DIR / "scheme_chunks.txt"


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

GEMINI_API_KEY = "YOUR API KEY"

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# LOAD FAISS INDEX
# =========================================================

print("Loading FAISS index...")

index = faiss.read_index(
    str(INDEX_PATH)
)

print(
    f"FAISS vectors: {index.ntotal}"
)


# =========================================================
# LOAD SCHEME DOCUMENTS
# =========================================================

print("Loading scheme documents...")

text = TEXT_PATH.read_text(
    encoding="utf-8"
)


# =========================================================
# SPLIT DOCUMENTS
# =========================================================

separator = "=================================================="

schemes = [
    part.strip()
    for part in text.split(separator)
    if part.strip()
]


print(
    f"Loaded {len(schemes)} scheme documents."
)


# =========================================================
# CHECK INDEX / DOCUMENT COUNT
# =========================================================

if index.ntotal != len(schemes):

    raise ValueError(
        f"Mismatch detected!\n"
        f"FAISS vectors: {index.ntotal}\n"
        f"Scheme documents: {len(schemes)}\n\n"
        f"Run embedding.py again."
    )


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

print("\nLoading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print(
    "Embedding model loaded."
)


# =========================================================
# SEARCH SCHEMES USING FAISS
# =========================================================

def search_schemes(
    query,
    top_k=5
):

    # -----------------------------------------------------
    # Create query embedding
    # -----------------------------------------------------

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")


    # -----------------------------------------------------
    # Search FAISS
    # -----------------------------------------------------

    distances, indices = index.search(
        query_embedding,
        top_k
    )


    results = []


    # -----------------------------------------------------
    # Collect matching schemes
    # -----------------------------------------------------

    for distance, scheme_index in zip(
        distances[0],
        indices[0]
    ):

        if scheme_index < 0:
            continue


        if scheme_index >= len(schemes):
            continue


        results.append({

            "scheme": schemes[scheme_index],

            "distance": float(distance)

        })


    return results


# =========================================================
# BUILD CONTEXT FOR GEMINI
# =========================================================

def build_context(results):

    context_parts = []


    for i, result in enumerate(
        results,
        start=1
    ):

        context_parts.append(

            f"""
SOURCE {i}

{result["scheme"]}

Similarity Score:
{result["distance"]:.4f}
"""

        )


    return "\n\n".join(
        context_parts
    )


# =========================================================
# GENERATE ANSWER USING GEMINI
# =========================================================

def generate_answer(
    question,
    results
):

    # -----------------------------------------------------
    # No results
    # -----------------------------------------------------

    if not results:

        return (
            "I could not find relevant government "
            "scheme information for your question."
        )


    # -----------------------------------------------------
    # Build context
    # -----------------------------------------------------

    context = build_context(
        results
    )


    # -----------------------------------------------------
    # RAG Prompt
    # -----------------------------------------------------

    prompt = f"""
You are the AI assistant for ProsperOS.

ProsperOS helps households understand their financial
situation and discover potentially relevant government
schemes.

Your task is to answer the user's question using ONLY
the information provided in the CONTEXT.

IMPORTANT RULES:

1. Do not invent government schemes.

2. Do not invent eligibility requirements.

3. Do not invent benefits or financial amounts.

4. Do not invent loan amounts or subsidy amounts.

5. Do not invent application procedures.

6. Do not invent deadlines.

7. Do not assume that a person is eligible for a scheme.

8. Low income alone does not automatically make someone
   eligible for a particular scheme.

9. If the context does not contain enough information,
   clearly say that the available information is not
   sufficient.

10. Give the answer in simple and easy-to-understand
    language.

11. Mention the relevant scheme name clearly.

12. If multiple schemes are relevant, explain them
    separately.

CONTEXT:
==================================================
{context}
==================================================

USER QUESTION:
{question}

ANSWER:
"""


    # -----------------------------------------------------
    # Call Gemini
    # -----------------------------------------------------

    response = client.models.generate_content(

        model="gemini-3.6-flash",

        contents=prompt

    )


    return response.text


# =========================================================
# COMPLETE RAG PIPELINE
# =========================================================

def ask_prosperos(
    question,
    top_k=5
):

    # -----------------------------------------------------
    # STEP 1
    # Convert question into embedding and search FAISS
    # -----------------------------------------------------

    results = search_schemes(
        question,
        top_k=top_k
    )


    # -----------------------------------------------------
    # STEP 2
    # Send retrieved schemes to Gemini
    # -----------------------------------------------------

    answer = generate_answer(
        question,
        results
    )


    # -----------------------------------------------------
    # Return complete result
    # -----------------------------------------------------

    return {

        "question": question,

        "answer": answer,

        "sources": results

    }


# =========================================================
# TEST PROGRAM
# =========================================================

if __name__ == "__main__":

    print("\n===================================")
    print("ProsperOS RAG + Gemini")
    print("===================================")


    # -----------------------------------------------------
    # Get question from user
    # -----------------------------------------------------

    question = input(
        "\nAsk about government schemes: "
    )


    # -----------------------------------------------------
    # Run RAG pipeline
    # -----------------------------------------------------

    response = ask_prosperos(
        question,
        top_k=5
    )


    # =====================================================
    # DISPLAY FINAL GEMINI ANSWER
    # =====================================================

    print("\n===================================")
    print("Gemini Answer")
    print("===================================")

    print(
        response["answer"]
    )


    # =====================================================
    # DISPLAY RETRIEVED SOURCES
    # =====================================================

    print("\n===================================")
    print("Retrieved Sources")
    print("===================================")


    for i, source in enumerate(
        response["sources"],
        start=1
    ):

        print(
            f"\n---------- Source {i} ----------"
        )


        print(
            source["scheme"]
        )


        print(
            f"\nSimilarity Score: "
            f"{source['distance']:.4f}"
        )


    print("\n===================================")
    print("RAG Pipeline Completed")
    print("===================================")