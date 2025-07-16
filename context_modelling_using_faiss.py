from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

def query_vani(question, top_k=3):
    # Load the pre-trained model and index
    model = SentenceTransformer('BAAI/bge-small-en-v1.5')  # light, fast, great performance
    index = faiss.read_index("vani_index.faiss")

    with open("vani_metadata.json", "r", encoding="utf-8") as f:
        letters = json.load(f)

    question_vector = model.encode([question])
    D, I = index.search(np.array(question_vector).astype("float32"), top_k)

    results = []
    for i in I[0]:
        results.append(letters[i])
    return results