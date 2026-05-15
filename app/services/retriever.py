

# import json
# import re
# import numpy as np
# import faiss

# from sentence_transformers import SentenceTransformer
# from rank_bm25 import BM25Okapi


# class SHLRetriever:

#     def __init__(self, path="app/data/processed/catalog_clean.json"):

#         self.model = SentenceTransformer("all-MiniLM-L6-v2")

#         with open(path, "r", encoding="utf-8") as f:
#             self.data = json.load(f)

#         self.texts = []
#         self.tokenized = []

#         for item in self.data:
#             normalized = self.normalize(item)
#             text = self.build_text(normalized)

#             self.texts.append(text)
#             self.tokenized.append(text.split())

#         self.bm25 = BM25Okapi(self.tokenized)

#         embeddings = self.model.encode(
#             self.texts,
#             convert_to_numpy=True,
#             show_progress_bar=False
#         ).astype("float32")

#         self.index = faiss.IndexFlatL2(embeddings.shape[1])
#         self.index.add(embeddings)

#         print(f"Hybrid index built: {len(self.data)}")

#     # ---------------- CLEAN ----------------
#     def clean(self, text):
#         if not text:
#             return ""
#         return re.sub(r"\s+", " ", str(text).lower()).strip()

#     # ---------------- NORMALIZE ----------------
#     def normalize(self, item):

#         name = item.get("name", "").strip()
#         description = item.get("description") or item.get("summary") or ""

#         skills = item.get("skills", [])
#         tags = item.get("tags", [])

#         if not isinstance(skills, list):
#             skills = []
#         if not isinstance(tags, list):
#             tags = []

#         test_type = item.get("test_type") or item.get("type") or ""

#         # improved fallback
#         if not test_type:
#             n = name.lower()
#             d = description.lower()

#             if "personality" in d or "opq" in n:
#                 test_type = "Personality"
#             elif "cognitive" in d or "reasoning" in d:
#                 test_type = "Cognitive"
#             elif any(k in n for k in ["java", "python", "sql", "javascript"]):
#                 test_type = "Technical"
#             else:
#                 test_type = "Assessment"

#         url = item.get("url") or item.get("href") or item.get("link")
#         if not url:
#             url = "https://www.shl.com/en/assessments/"

#         return {
#             "name": name,
#             "description": description,
#             "skills": skills,
#             "tags": tags,
#             "test_type": test_type,
#             "url": url
#         }

#     # ---------------- BUILD TEXT ----------------
#     def build_text(self, item):
#         return self.clean(
#             f"{item.get('name','')} "
#             f"{item.get('description','')} "
#             f"{' '.join(item.get('skills', []))} "
#             f"{' '.join(item.get('tags', []))} "
#             f"{item.get('test_type','')}"
#         )

#     # ---------------- SEARCH ----------------
#     def bm25_search(self, query, top_k=25):
#         scores = self.bm25.get_scores(self.clean(query).split())
#         return np.argsort(scores)[::-1][:top_k]

#     def vector_search(self, query, top_k=25):
#         q = self.model.encode(
#             [self.clean(query)],
#             convert_to_numpy=True,
#             show_progress_bar=False
#         ).astype("float32")

#         _, idx = self.index.search(q, top_k)
#         return idx[0]

#     # ---------------- BOOST (FIXED HEAVY VERSION) ----------------
#     def boost_score(self, query, item):

#         q = query.lower()
#         name = item["name"].lower()
#         desc = item["description"].lower()

#         boost = 0.0

#         # TECH PRIORITY (VERY IMPORTANT FIX)
#         tech_keywords = ["java", "python", "sql", "javascript", "backend", "engineer"]

#         if any(k in q for k in tech_keywords):
#             if any(k in name for k in ["java", "python", "sql", "javascript"]):
#                 boost += 1.5

#         # SOFT SKILLS
#         if "communication" in q or "stakeholder" in q:
#             if "communication" in desc or "communication" in name:
#                 boost += 0.8

#         # PERSONALITY
#         if "personality" in q or "opq" in q:
#             if "personality" in desc or "opq" in name:
#                 boost += 1.2

#         # PENALIZE GENERIC HR REPORTS (CRITICAL FIX)
#         bad_items = ["hipo", "360", "report", "smart interview"]

#         if any(b in name for b in bad_items):
#             boost -= 1.2

#         return boost

#     # ---------------- SEARCH MAIN ----------------
#     def search(self, query, top_k=5):

#         bm25_idx = self.bm25_search(query)
#         vec_idx = self.vector_search(query)

#         score_map = {}

#         for r, i in enumerate(bm25_idx):
#             score_map[i] = score_map.get(i, 0) + 0.35 / (r + 1)

#         for r, i in enumerate(vec_idx):
#             score_map[i] = score_map.get(i, 0) + 0.65 / (r + 1)

#         for idx in list(score_map.keys()):
#             item = self.normalize(self.data[idx])
#             score_map[idx] += self.boost_score(query, item)

#         ranked = sorted(score_map.items(), key=lambda x: x[1], reverse=True)

#         results = []
#         used = set()

#         for idx, score in ranked:
#             item = self.normalize(self.data[idx])

#             if item["name"] in used:
#                 continue

#             used.add(item["name"])
#             item["score"] = round(float(score), 4)

#             results.append(item)

#             if len(results) >= top_k:
#                 break

#         return results



# import json
# import re
# import numpy as np
# import faiss
# from sentence_transformers import SentenceTransformer
# from rank_bm25 import BM25Okapi


# class SHLRetriever:

#     def __init__(self, path="app/data/processed/catalog_clean.json"):

#         self.model = SentenceTransformer("all-MiniLM-L6-v2")

#         with open(path, "r", encoding="utf-8") as f:
#             self.data = json.load(f)

#         self.texts = []
#         self.tokenized = []

#         for item in self.data:
#             normalized = self.normalize(item)
#             text = self.build_text(normalized)

#             self.texts.append(text)
#             self.tokenized.append(text.split())

#         self.bm25 = BM25Okapi(self.tokenized)

#         embeddings = self.model.encode(
#             self.texts,
#             convert_to_numpy=True,
#             show_progress_bar=False
#         ).astype("float32")

#         self.index = faiss.IndexFlatL2(embeddings.shape[1])
#         self.index.add(embeddings)

#         print(f"Hybrid index built: {len(self.data)}")

#     # ---------------- CLEAN ----------------
#     def clean(self, text):
#         if not text:
#             return ""
#         return re.sub(r"\s+", " ", str(text).lower()).strip()

#     # ---------------- NORMALIZE ----------------
#     def normalize(self, item):

#         name = item.get("name", "").strip()
#         description = item.get("description") or item.get("summary") or ""

#         skills = item.get("skills", [])
#         tags = item.get("tags", [])

#         if not isinstance(skills, list):
#             skills = []
#         if not isinstance(tags, list):
#             tags = []

#         test_type = item.get("test_type") or item.get("type") or ""

#         if not test_type:
#             n = name.lower()
#             d = description.lower()

#             if "personality" in d or "opq" in n:
#                 test_type = "Personality"
#             elif "cognitive" in d or "reasoning" in d:
#                 test_type = "Cognitive"
#             elif any(k in n for k in ["java", "python", "sql", "javascript"]):
#                 test_type = "Technical"
#             else:
#                 test_type = "Assessment"

#         url = item.get("url") or item.get("href") or item.get("link") or ""

#         return {
#             "name": name,
#             "description": description,
#             "skills": skills,
#             "tags": tags,
#             "test_type": test_type,
#             "url": url
#         }

#     # ---------------- BUILD TEXT ----------------
#     def build_text(self, item):
#         return self.clean(
#             f"{item.get('name','')} "
#             f"{item.get('description','')} "
#             f"{' '.join(item.get('skills', []))} "
#             f"{' '.join(item.get('tags', []))} "
#             f"{item.get('test_type','')}"
#         )

#     # ---------------- SEARCH ----------------
#     def bm25_search(self, query, top_k=25):
#         scores = self.bm25.get_scores(self.clean(query).split())
#         return np.argsort(scores)[::-1][:top_k]

#     def vector_search(self, query, top_k=25):
#         q = self.model.encode(
#             [self.clean(query)],
#             convert_to_numpy=True
#         ).astype("float32")

#         _, idx = self.index.search(q, top_k)
#         return idx[0]

#     # ---------------- BOOST ----------------
#     def boost_score(self, query, item):

#         q = query.lower()
#         name = item["name"].lower()
#         desc = item["description"].lower()

#         boost = 0.0

#         tech_keywords = ["java", "python", "sql", "javascript", "backend", "engineer"]

#         if any(k in q for k in tech_keywords):
#             if any(k in name for k in tech_keywords):
#                 boost += 1.5

#         if "communication" in q or "stakeholder" in q:
#             if "communication" in desc or "communication" in name:
#                 boost += 0.8

#         if "personality" in q or "opq" in q:
#             if "personality" in desc or "opq" in name:
#                 boost += 1.2

#         bad_items = ["hipo", "360", "report", "smart interview"]
#         if any(b in name for b in bad_items):
#             boost -= 1.2

#         return boost

#     # ---------------- SEARCH MAIN ----------------
#     def search(self, query, top_k=5):

#         bm25_idx = self.bm25_search(query)
#         vec_idx = self.vector_search(query)

#         score_map = {}

#         for r, i in enumerate(bm25_idx):
#             score_map[i] = score_map.get(i, 0) + 0.35 / (r + 1)

#         for r, i in enumerate(vec_idx):
#             score_map[i] = score_map.get(i, 0) + 0.65 / (r + 1)

#         for idx in list(score_map.keys()):
#             item = self.normalize(self.data[idx])
#             score_map[idx] += self.boost_score(query, item)

#         ranked = sorted(score_map.items(), key=lambda x: x[1], reverse=True)

#         results = []
#         used = set()

#         for idx, score in ranked:
#             item = self.normalize(self.data[idx])

#             if item["name"] in used:
#                 continue

#             used.add(item["name"])

#             results.append({
#                 "name": item["name"],
#                 "url": item["url"],
#                 "test_type": item["test_type"],
#                 "description": item["description"],
#                 "score": float(round(score, 4))
#             })

#             if len(results) >= top_k:
#                 break

#         return results



import json
import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi


class SHLRetriever:

    def __init__(self, path="app/data/processed/catalog_clean.json"):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        with open(path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        # ✅ STORE CLEAN PROCESSED DATA (IMPORTANT FIX)
        self.processed_data = []

        self.texts = []
        self.tokenized = []

        for item in self.data:
            normalized = self.normalize(item)

            # store once (DO NOT RE-NORMALIZE LATER)
            self.processed_data.append(normalized)

            text = self.build_text(normalized)

            self.texts.append(text)
            self.tokenized.append(text.split())

        self.bm25 = BM25Okapi(self.tokenized)

        embeddings = self.model.encode(
            self.texts,
            convert_to_numpy=True,
            show_progress_bar=False
        ).astype("float32")

        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

        print(f"Hybrid index built: {len(self.data)}")

    # ---------------- CLEAN ----------------
    def clean(self, text):
        if not text:
            return ""
        return re.sub(r"\s+", " ", str(text).lower()).strip()

    # ---------------- NORMALIZE ----------------
    def normalize(self, item):

        name = item.get("name", "").strip()
        description = item.get("description") or item.get("summary") or ""

        skills = item.get("skills", [])
        tags = item.get("tags", [])

        if not isinstance(skills, list):
            skills = []
        if not isinstance(tags, list):
            tags = []

        # ---------------- FIX TEST TYPE ----------------
        test_type = item.get("test_type") or item.get("type") or ""

        if not test_type or test_type.strip() == "":
            n = name.lower()
            d = description.lower()

            if "personality" in d or "opq" in n:
                test_type = "Personality"
            elif "cognitive" in d or "reasoning" in d:
                test_type = "Cognitive"
            elif any(k in n for k in ["java", "python", "sql", "javascript"]):
                test_type = "Technical"
            else:
                test_type = "Technical"  # safer default for SHL ranking

        # ---------------- FIX URL HANDLING ----------------
        url = (
            item.get("url")
            or item.get("href")
            or item.get("link")
            or item.get("assessment_url")
        )

        if not url or url.strip() == "":
            url = "https://www.shl.com/en/assessments/"

        return {
            "name": name,
            "description": description,
            "skills": skills,
            "tags": tags,
            "test_type": test_type,
            "url": url
        }

    # ---------------- BUILD TEXT ----------------
    def build_text(self, item):
        return self.clean(
            f"{item.get('name','')} "
            f"{item.get('description','')} "
            f"{' '.join(item.get('skills', []))} "
            f"{' '.join(item.get('tags', []))} "
            f"{item.get('test_type','')}"
        )

    # ---------------- BM25 ----------------
    def bm25_search(self, query, top_k=25):
        scores = self.bm25.get_scores(self.clean(query).split())
        return np.argsort(scores)[::-1][:top_k]

    # ---------------- VECTOR SEARCH ----------------
    def vector_search(self, query, top_k=25):
        q = self.model.encode(
            [self.clean(query)],
            convert_to_numpy=True
        ).astype("float32")

        _, idx = self.index.search(q, top_k)
        return idx[0]

    # ---------------- BOOST ----------------
    def boost_score(self, query, item):

        q = query.lower()
        name = item["name"].lower()
        desc = item["description"].lower()

        boost = 0.0

        tech_keywords = ["java", "python", "sql", "javascript", "backend", "engineer"]

        if any(k in q for k in tech_keywords):
            if any(k in name for k in tech_keywords):
                boost += 1.5

        if "communication" in q or "stakeholder" in q:
            if "communication" in desc or "communication" in name:
                boost += 0.8

        if "personality" in q or "opq" in q:
            if "personality" in desc or "opq" in name:
                boost += 1.2

        bad_items = ["hipo", "360", "report", "smart interview"]
        if any(b in name for b in bad_items):
            boost -= 1.2

        return boost

    # ---------------- SEARCH MAIN ----------------
    def search(self, query, top_k=5):

        bm25_idx = self.bm25_search(query)
        vec_idx = self.vector_search(query)

        score_map = {}

        for r, i in enumerate(bm25_idx):
            score_map[i] = score_map.get(i, 0) + 0.35 / (r + 1)

        for r, i in enumerate(vec_idx):
            score_map[i] = score_map.get(i, 0) + 0.65 / (r + 1)

        # ---------------- IMPORTANT FIX ----------------
        for idx in list(score_map.keys()):
            item = self.processed_data[idx]   # FIXED (no re-normalization)
            score_map[idx] += self.boost_score(query, item)

        ranked = sorted(score_map.items(), key=lambda x: x[1], reverse=True)

        results = []
        used = set()

        for idx, score in ranked:
            item = self.processed_data[idx]   # FIXED

            if item["name"] in used:
                continue

            used.add(item["name"])

            results.append({
                "name": item["name"],
                "url": item["url"],
                "test_type": item["test_type"],
                "description": item["description"],
                "score": float(round(score, 4))
            })

            if len(results) >= top_k:
                break

        return results