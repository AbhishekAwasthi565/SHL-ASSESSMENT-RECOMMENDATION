from app.services.retriever import SHLRetriever


retriever = SHLRetriever()

query = "Java developer who works with stakeholders"

results = retriever.search(query, top_k=5)

for r in results:
    print(r["name"], "->", r["url"])