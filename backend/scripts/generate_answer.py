import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# --- Paths ---
FAISS_INDEX_PATH = "../output/faiss_index.index"
METADATA_PATH = "../output/metadata.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GENERATION_MODEL = "google/flan-t5-base"

# --- Load FAISS and metadata ---
index = faiss.read_index(FAISS_INDEX_PATH)
with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# --- Load models ---
retriever = SentenceTransformer(EMBEDDING_MODEL)
tokenizer = AutoTokenizer.from_pretrained(GENERATION_MODEL)
generator = AutoModelForSeq2SeqLM.from_pretrained(GENERATION_MODEL)

# --- Function to find the best chunk ---
def retrieve_best_chunk(query):
    query_embedding = retriever.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, 1)
    best_idx = indices[0][0]
    return metadata[best_idx]["text"]

# --- Function to generate an answer using HF model ---
def generate_answer(query):
    context = retrieve_best_chunk(query)
    
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    with torch.no_grad():
        outputs = generator.generate(
            inputs.input_ids,
            max_length=200,
            num_beams=5,
            early_stopping=True
        )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

# --- Run it interactively ---
if __name__ == "__main__":
    print("🎓 Ask your university registration questions below:")
    while True:
        user_input = input("\nEnter your question (or 'exit'): ")
        if user_input.lower() == "exit":
            break
        answer = generate_answer(user_input)
        print(f"\n🤖 Answer:\n{answer}")
