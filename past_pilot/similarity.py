import os
import PyPDF2
from sentence_transformers import SentenceTransformer, util
from pathlib import Path
from directory_modifier import get_data_dir
model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')

# directory parameter refers to the folder containing all pdfs for a key
def get_chunks(directory):
    chunks = []
    files = Path(directory).glob('*')
    for pdf_file in files:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            chunks.append((pdf_file.resolve(), page_num, text))
        return chunks

def calculate_similarity(user_input, data):
    embeddings = model.encode([user_input, data], convert_to_tensor=True)
    sim = util.cos_sim(embeddings[0], embeddings[1]).item()
    return sim

def chunks_similarity(user_input, chunks):
    similarity_scores = []
    for chunk in chunks:
        sim = calculate_similarity(user_input, chunk[1])
        similarity_scores.append((chunk, sim))
    return similarity_scores

def get_similar(user_input, keys):
    directory = get_data_dir()
    sim_scores = []
    for key in keys:
        key_dir = os.path.join(directory, key)
        chunks = get_chunks(key_dir)
        sim_scores.extend(chunks_similarity(user_input, chunks))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    return sim_scores
