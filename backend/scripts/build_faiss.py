import faiss
import numpy as np
import json
import os

# --- Paths ---
EMBEDDINGS_PATH = "../output/embeddings.npy"
METADATA_PATH = "../output/metadata.json"
FAISS_INDEX_PATH = "../output/faiss_index.index"

# --- Load Data ---
embeddings = np.load(EMBEDDINGS_PATH).astype('float32')
with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# --- Create FAISS Index ---
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 = Euclidean distance; for cosine similarity, use inner product

index.add(embeddings)
print(f"Indexed {index.ntotal} vectors.")

# --- Save Index ---
faiss.write_index(index, FAISS_INDEX_PATH)
print(f"FAISS index saved to {FAISS_INDEX_PATH}")
