from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

app = FastAPI(title="RAG Chatbot (FAISS + Local Docs)")

embedder = SentenceTransformer("all-MiniLM-L6-v2")
generator = pipeline("text2text-generation", model="google/flan-t5-small")

dimension = 384
index = faiss.IndexFlatL2(dimension)

documents = []


def load_docs(path="docs", chunk_size=400):
    global documents, index
    documents = []

    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created {path}/ - add .txt files and restart.")
        return

    texts = []
    filenames = [f for f in os.listdir(path) if f.endswith(".txt")]
    for file in filenames:
        with open(os.path.join(path, file), "r", encoding="utf-8") as fh:
            text = fh.read().strip()
            if not text:
                continue
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i+chunk_size].strip()
                if len(chunk) > 20:
                    texts.append(chunk)

    if not texts:
        print("No valid text found in docs/. Add files and restart.")
        return

    documents.extend(texts)
    embeddings = embedder.encode(texts, convert_to_numpy=True)
    index.reset()
    index.add(embeddings.astype(np.float32))

    print(f" Loaded {len(documents)} chunks from {len(filenames)} files.")


class Query(BaseModel):
    question: str


@app.post("/ask")
def ask_question(q: Query):
    if not documents:
        raise HTTPException(status_code=400, detail="No documents loaded. Put .txt files in docs/ and restart.")

    question = q.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    q_emb = embedder.encode([question], convert_to_numpy=True).astype(np.float32)
    distances, indices = index.search(q_emb, k=3)
    retrieved = [documents[i] for i in indices[0]]

    context = " ".join(retrieved)
    prompt = f"Answer the question using the context.\nContext: {context}\nQuestion: {question}"

    response = generator(prompt, max_length=120, do_sample=False)

    return {
        "question": question,
        "answer": response[0]['generated_text'],
        "retrieved_context": retrieved
    }


@app.post("/reload")
def reload_docs():
    load_docs("docs")
    return {"status": "reloaded", "chunks": len(documents)}


load_docs("docs")
