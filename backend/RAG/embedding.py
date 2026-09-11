from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).parent

DOCUMENT_PATH = BASE_DIR / "documents" / "schemes.txt"

INDEX_PATH = BASE_DIR / "schemes.index"

TEXT_PATH = BASE_DIR / "scheme_chunks.txt"


# =========================================================
# LOAD DOCUMENT
# =========================================================

print("Loading government scheme document...")

text = DOCUMENT_PATH.read_text(
    encoding="utf-8"
)


# =========================================================
# SPLIT INTO SCHEMES
# =========================================================

separator = "=================================================="


schemes = [

    scheme.strip()

    for scheme in text.split(separator)

    if scheme.strip()

]


print(
    f"Loaded {len(schemes)} scheme documents."
)


# =========================================================
# DISPLAY SCHEMES
# =========================================================

print("\nSchemes found:")

for i, scheme in enumerate(
    schemes,
    start=1
):

    lines = scheme.splitlines()

    name = lines[0].strip()

    print(
        f"{i}. {name}"
    )


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

print("\nLoading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# =========================================================
# CREATE EMBEDDINGS
# =========================================================

print("\nCreating embeddings...")


embeddings = model.encode(

    schemes,

    convert_to_numpy=True,

    normalize_embeddings=True

).astype("float32")


# =========================================================
# CREATE FAISS INDEX
# =========================================================

dimension = embeddings.shape[1]


index = faiss.IndexFlatIP(
    dimension
)


index.add(
    embeddings
)


# =========================================================
# SAVE FAISS INDEX
# =========================================================

faiss.write_index(

    index,

    str(INDEX_PATH)

)


# =========================================================
# SAVE SCHEMES
# =========================================================

TEXT_PATH.write_text(

    separator.join(

        f"\n\n{scheme}\n\n"

        for scheme in schemes

    ),

    encoding="utf-8"

)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n===================================")
print("RAG Embedding Creation Completed!")
print("===================================")

print(
    f"FAISS index: {INDEX_PATH}"
)

print(
    f"Scheme text: {TEXT_PATH}"
)

print(
    f"Total schemes: {len(schemes)}"
)