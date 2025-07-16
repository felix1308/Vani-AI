import gradio as gr
import subprocess
from context_modelling_using_faiss import query_vani
import sys

# 1. Zephyr call via Ollama
def ask_zephyr(prompt):
    result = subprocess.run(
        [r"C:\Program Files\Ollama\ollama.exe", "run", "zephyr"],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode()

# 2. Full RAG response using your prompt and retrieval
def rag_response(user_question):
    relevant_letters = query_vani(user_question, top_k=3)
    context = "\n\n---\n\n".join([l["body"] for l in relevant_letters])

    prompt = f"""You are speaking only through the actual letters of His Divine Grace A. C. Bhaktivedanta Swami Prabhupāda.

Below are excerpts from Śrīla Prabhupāda’s original letters to his disciples. Your only job is to answer the following question **strictly using these letters alone**, either by quoting directly or paraphrasing in the same tone — without adding your own opinions or explanations.

If unsure, humbly say: "Kindly study more of Śrīla Prabhupāda’s letters for further guidance."

--------------------------
{context}
--------------------------

🙏 Question from a sincere devotee:
"{user_question}"

Now respond with humility and clarity, as Śrīla Prabhupāda would through his letters:
"""
    return ask_zephyr(prompt), relevant_letters

# 3. Gradio interaction handler
def chat(user_input, history, output_mode):
    history = history or []

    ai_reply, sources = rag_response(user_input)
    letters_text = "\n\n---\n\n".join([f"📜 {l['title']}\n{l['body']}" for l in sources])

    if output_mode == "Letters Only":
        answer = letters_text
    elif output_mode == "Paraphrased Answer":
        answer = ai_reply
    else:
        answer = f"{ai_reply}\n\n---\n📚 Letters Used:\n{letters_text}"

    history.append((user_input, answer))
    return history, history

# 4. Exit button handler
def exit_app():
    print("Exiting Vāṇī chat...")
    sys.exit(0)

# 5. Build Gradio UI
with gr.Blocks() as VaniChat:
    gr.Markdown("## 🙏 Vāṇī — Chat with Śrīla Prabhupāda's Letters")

    radio = gr.Radio(
        choices=["Letters Only", "Paraphrased Answer", "Both"],
        value="Both",
        label="Choose Output Mode"
    )

    chatbot = gr.Chatbot(label="Vāṇī's Response")
    msg = gr.Textbox(label="Your Question to Śrīla Prabhupāda")
    state = gr.State([])

    ask_btn = gr.Button("Ask")
    ask_btn.click(fn=chat, inputs=[msg, state, radio], outputs=[chatbot, state])

    gr.Button("Exit").click(fn=exit_app)

# 6. Launch
VaniChat.launch()
