import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

# --- Config ---
FAISS_INDEX_PATH = "../output/faiss_index.index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
METADATA_PATH = "../output/metadata.json"
TOP_K = 1  # Only return the best one

# --- Load FAISS index ---
index = faiss.read_index(FAISS_INDEX_PATH)

# --- Load metadata ---
with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# --- Load sentence transformer model ---
model = SentenceTransformer(EMBEDDING_MODEL)

def query_faiss(user_query):
    # Step 1: Embed the user query
    query_embedding = model.encode([user_query]).astype('float32')

    # Step 2: Search the FAISS index
    distances, indices = index.search(query_embedding, TOP_K)

    # Step 3: Return the best matched chunk
    best_index = indices[0][0]
    best_chunk = metadata[best_index]
    best_score = distances[0][0]

    print(f"\n {best_chunk['text']}")

# --- Interactive Loop ---
if __name__ == "__main__":
    while True:
        user_input = input("\nEnter your question (or 'exit'): ")
        if user_input.lower() == "exit":
            break
        query_faiss(user_input)
