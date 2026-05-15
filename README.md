# SHL Assessment Recommender API

A hybrid AI-powered recommendation system using BM25 + SentenceTransformers + FAISS.

---

## 🚀 Features

- Hybrid search (BM25 + semantic embeddings)
- FastAPI backend
- SHL assessment recommendations
- Compare assessments
- Rule-based scoring boost system

---

## 🧠 Tech Stack

- FastAPI
- SentenceTransformers
- FAISS
- NumPy
- Pandas
- rank-bm25
- PyTorch (CPU)

---

## 📁 Project Structure
  app/
  ├── main.py
  ├── services/
  │ ├── retriever.py
  │ └── agent.py


  
---

## ⚙️ Installation

```bash
pip install -r requirements.txt


🌐 API Endpoints
🔹 Root
GET /

Response:

{
  "message": "SHL Assessment Recommender API"
}
🔹 Health Check
GET /health

Response:

{
  "status": "ok"
}
🔹 Chat Endpoint
POST /chat

Request:

{
  "messages": [
    {
      "role": "user",
      "content": "python developer test"
    }
  ]
}

Response:

{
  "reply": "Here are matching SHL assessments",
  "recommendations": [],
  "end_of_conversation": false
}

If you want, I can next:
- :contentReference[oaicite:0]{index=0}
- or :contentReference[oaicite:1]{index=1}
    
   
  {
    "reply": "Here are matching SHL assessments",
    "recommendations": [],
    "end_of_conversation": false
  }
