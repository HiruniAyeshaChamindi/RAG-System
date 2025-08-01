from sentence_transformers import SentenceTransformer
import json
import os
import numpy as np

# --- Paths ---
INPUT_JSON = "../output/chunks.json"
OUTPUT_EMBEDDINGS = "../output/embeddings.npy"
OUTPUT_METADATA = "../output/metadata.json"

# --- Load Chunks ---
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["text"] for item in data]

# --- Load Sentence Transformer Model ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Generate Embeddings ---
embeddings = model.encode(texts, show_progress_bar=True)

# --- Save Embeddings and Metadata ---
np.save(OUTPUT_EMBEDDINGS, embeddings)

metadata = [{"id": item["id"], "doc": item["doc"], "text": item["text"]} for item in data]
with open(OUTPUT_METADATA, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print(f"Saved embeddings to {OUTPUT_EMBEDDINGS}")
print(f"Saved metadata to {OUTPUT_METADATA}")
