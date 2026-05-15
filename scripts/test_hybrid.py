from app.services.retriever import SHLRetriever


retriever = SHLRetriever()

query = "Java developer who works with stakeholders and SQL"

results = retriever.search(query, top_k=5)

for r in results:
    print(r["name"], "->", r.get("score"), "->", r["url"])