import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class RAGEngine:
    def __init__(self,
                 faiss_index_path="../output/faiss_index.index",
                 metadata_path="../output/metadata.json",
                 embedding_model="all-MiniLM-L6-v2",
                 generation_model="google/flan-t5-base"):
        
        self.index = faiss.read_index(faiss_index_path)
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        
        self.retriever = SentenceTransformer(embedding_model)
        self.tokenizer = AutoTokenizer.from_pretrained(generation_model)
        self.generator = AutoModelForSeq2SeqLM.from_pretrained(generation_model)

    def ask(self, query):
        # Embed the query
        query_embedding = self.retriever.encode([query]).astype('float32')
        _, indices = self.index.search(query_embedding, 1)
        best_chunk = self.metadata[indices[0][0]]["text"]

        # Prompt construction
        prompt = f"Context: {best_chunk}\n\nQuestion: {query}\n\nAnswer:"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True)

        with torch.no_grad():
            outputs = self.generator.generate(
                inputs.input_ids,
                max_length=200,
                num_beams=5,
                early_stopping=True
            )

        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer
