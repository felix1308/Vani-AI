
# 📜 Vāṇī – Devotional AI Assistant (RAG over Śrīla Prabhupāda’s Letters)

Vāṇī is a local AI assistant that answers spiritual questions *only* using the original personal letters of **Śrīla A.C. Bhaktivedanta Swami Prabhupāda** (Founder of ISKCON, 1947–1977).

This project uses **Retrieval-Augmented Generation (RAG)** to pull relevant excerpts from 6500+ letters and generate spiritually rooted responses — no hallucinations, no opinions, just the mood of the spiritual master.

---

## ✨ Features

- 🔍 **RAG pipeline with FAISS** for fast semantic retrieval
- 🧠 **Multi-Context Prompting (MCP)** to merge diverse letter insights
- 📜 **Modes**: Letters Only | Paraphrased | Hybrid
- 🦙 Uses **Zephyr or Mistral** via **Ollama** for local inference
- 🧱 Built with **LangChain**, **FAISS**, **transformers**, and **Tkinter GUI** or CLI

---

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/vani.git
cd vani
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Load Model using Ollama (Recommended for Local Inference)

Instead of using Hugging Face Transformers, use **[Ollama](https://ollama.com/)** — a simple CLI tool that runs LLMs locally.

#### Step 1: Install Ollama  
https://ollama.com/download

#### Step 2: Pull the model (e.g., Zephyr or Mistral)

```bash
ollama pull mistral
# or
ollama pull zephyr
```

#### Step 3: Run the model server

```bash
ollama run mistral
```

> The model will now listen at `http://localhost:11434`

---

### 🧩 5. Update your Python code to use Ollama

Install the Python client:

```bash
pip install ollama
```

Example usage:

```python
def ask_zephyr(prompt):
    result = subprocess.run(
        [r"C:\Program Files\Ollama\ollama.exe", "run", "zephyr"],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode()

def rag_response(user_question):
    # 1. Retrieve top relevant letters
    relevant_letters = query_vani(user_question, top_k=3)

    # 2. Combine letter bodies
    context = "\n\n---\n\n".join([l["body"] for l in relevant_letters])

    # 3. Bhakti-Style Prompt
    prompt = f"""You are speaking only through the actual letters of His Divine Grace A. C. Bhaktivedanta Swami Prabhupāda.

Below are excerpts from Śrīla Prabhupāda’s original letters to his disciples. Your only job is to answer the following question **strictly using these letters alone**, either by quoting directly or paraphrasing in the same tone — without adding your own opinions or explanations and bro, i just need answers from the letters only not your hallucinations.

If unsure, humbly say: "Kindly study more of Śrīla Prabhupāda’s letters for further guidance."

--------------------------
{context}
--------------------------

🙏 Question from a sincere devotee:
"{user_question}"

Now respond with humility and clarity, as Śrīla Prabhupāda would through his letters:
"""

    # 4. Ask Zephyr LLM
    return ask_zephyr(prompt)


response = rag_response("How to increase Book distribution?")
print(response)
```

---

## 🧘 How It Works

1. User enters a spiritual question
2. The query is embedded using a SentenceTransformer
3. FAISS finds top-k most relevant letters
4. MCP combines distinct letters into a single context block
5. Prompt + context fed to the LLM (via Ollama)
6. Output is returned as:
   - 📜 Letters Only
   - ✍️ Paraphrased Response
   - 🪷 Hybrid Mode

---

## 💻 Running the App

### Option 1: Run via CLI

```bash
python Vani_RAG.py
```

### Option 2: Run GUI (Tkinter)

```bash
python gradio_interface_with_LLM.py
```

---

## 🔧 Customization

You can customize:
- `top_k`: Number of letters retrieved
- Prompt templates in `prompts/prompt_templates.py`
- Model choice (Zephyr, Mistral via Ollama)

---

## 🧪 Planned Improvements

- ✅ LoRA / QLoRA fine-tuning on letter tone
- 🕊️ Web frontend (React/Streamlit)
- 🔖 Citation-aware responses
- 🌐 Language support for Hindi/Bengali/others

---

## 🙏 Credits

- Letters from [Vedabase.io](https://vedabase.io) (scraped with respect)
- LLM: [Zephyr via Ollama](https://ollama.com/library)
- FAISS + LangChain + Transformers stack

---

## 📬 Want to Contribute?

If you're a bhakta, engineer, or AI enthusiast and want to help extend Vāṇī — you're welcome!  
Feel free to open an issue or PR.

---

## 📘 License

Open-source under Apache 2.0 (with attribution to Śrīla Prabhupāda’s legacy)

---

🪷 *"The letters of the spiritual master are non-different from his direct instructions."*  
— Inspired by Śrīla Prabhupāda’s mercy
