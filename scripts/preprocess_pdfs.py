import os
import pdfplumber
import nltk
import json

nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize

# --- Configuration ---
INPUT_DIR = "../data"
OUTPUT_PATH = "../output/chunks.json"
MAX_WORDS = 200  # max words per chunk

# --- Function: Extract text from a single PDF ---
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# --- Function: Chunk text into 200-word segments ---
def chunk_text(text, max_words=MAX_WORDS):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) <= max_words:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# --- Main Processing Function ---
def process_all_pdfs(input_dir, output_file):
    all_chunks = []
    file_list = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]

    for file_name in file_list:
        file_path = os.path.join(input_dir, file_name)
        print(f"Processing: {file_name}")
        text = extract_text_from_pdf(file_path)
        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks):
            all_chunks.append({
                "doc": file_name,
                "id": f"{file_name}_{idx}",
                "text": chunk
            })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"{len(all_chunks)} chunks saved to {output_file}")

# --- Run Script ---
if __name__ == "__main__":
    os.makedirs("../output", exist_ok=True)
    process_all_pdfs(INPUT_DIR, OUTPUT_PATH)
