from context_modelling_using_faiss import query_vani
import subprocess

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