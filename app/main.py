

# from fastapi import FastAPI
# from pydantic import BaseModel

# from app.services.retriever import SHLRetriever
# from app.services.agent import SHLAgent


# app = FastAPI(
#     title="SHL Assessment Recommender",
#     version="1.0"
# )

# # =========================================================
# # LOAD SERVICES
# # =========================================================
# retriever = SHLRetriever()
# agent = SHLAgent(retriever)


# # =========================================================
# # REQUEST SCHEMA
# # =========================================================
# class ChatRequest(BaseModel):
#     messages: list


# # =========================================================
# # ROOT
# # =========================================================
# @app.get("/")
# def root():

#     return {
#         "message": "SHL Assessment Recommender API",
#         "endpoints": [
#             "/health",
#             "/chat"
#         ]
#     }


# # =========================================================
# # HEALTH
# # =========================================================
# @app.get("/health")
# def health():

#     return {
#         "status": "ok"
#     }


# # =========================================================
# # CHAT
# # =========================================================
# @app.post("/chat")
# def chat(req: ChatRequest):

#     return agent.chat(req.dict())



from fastapi import FastAPI
from pydantic import BaseModel

from app.services.retriever import SHLRetriever
from app.services.agent import SHLAgent


app = FastAPI(
    title="SHL Assessment Recommender",
    version="1.0"
)

retriever = SHLRetriever()
agent = SHLAgent(retriever)


class ChatRequest(BaseModel):
    messages: list


@app.get("/")
def root():
    return {
        "message": "SHL Assessment Recommender API"
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    return agent.chat(req.dict())