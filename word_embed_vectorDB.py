from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

# Load model (you can replace with a local one if needed)
model = SentenceTransformer('BAAI/bge-small-en-v1.5')  # light, fast, great performance

# Load your letters
with open("data/letters_no_date.json", "r", encoding="utf-8") as f:
    letters = json.load(f)

texts = [letter["body"] for letter in letters]
titles = [letter["title"] for letter in letters]

# Create embeddings
embeddings = model.encode(texts, show_progress_bar=True)

# Save vector index
dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))
faiss.write_index(index, "vani_index.faiss")

# Save metadata
with open("vani_metadata.json", "w", encoding="utf-8") as f:
    json.dump(letters, f, ensure_ascii=False, indent=2)

print(f"✅ Indexed {len(letters)} letters.")