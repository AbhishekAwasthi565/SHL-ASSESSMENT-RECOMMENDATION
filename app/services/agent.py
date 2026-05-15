

# import re


# class SHLAgent:

#     def __init__(self, retriever):
#         self.retriever = retriever

#     def detect_intent(self, text):
#         t = text.lower()

#         if any(x in t for x in ["compare", "vs", "difference"]):
#             return "compare"

#         if any(x in t for x in ["add", "include", "refine"]):
#             return "refine"

#         return "recommend"

#     def is_blocked(self, text):
#         blocked = ["salary", "visa", "legal", "firing", "system prompt"]
#         return any(b in text.lower() for b in blocked)

#     # FIXED: less aggressive
#     def needs_clarification(self, text):
#         t = text.lower()
#         return not any(k in t for k in ["developer", "engineer", "java", "python", "sql", "manager", "analyst"])

#     def validate_results(self, results):
#         return [r for r in results if isinstance(r, dict) and r.get("name")]

#     def format_results(self, results):
#         return [
#             {
#                 "name": r["name"],
#                 "url": r.get("url", ""),
#                 "test_type": r.get("test_type", "")
#             }
#             for r in results
#         ]

#     def compare(self, query):

#         results = self.validate_results(self.retriever.search(query, 2))

#         if len(results) < 2:
#             return {
#                 "reply": "Not enough assessments to compare.",
#                 "recommendations": [],
#                 "end_of_conversation": False
#             }

#         a, b = results[:2]

#         return {
#             "reply": f"{a['name']} focuses on {a['test_type']} while {b['name']} focuses on {b['test_type']}.",
#             "recommendations": self.format_results(results),
#             "end_of_conversation": False
#         }

#     def chat(self, req):

#         user_msg = req["messages"][-1]["content"]

#         if self.is_blocked(user_msg):
#             return {
#                 "reply": "I can only help with SHL assessments.",
#                 "recommendations": [],
#                 "end_of_conversation": False
#             }

#         intent = self.detect_intent(user_msg)

#         if intent == "compare":
#             return self.compare(user_msg)

#         results = self.validate_results(
#             self.retriever.search(user_msg, 5)
#         )

#         if not results:
#             return {
#                 "reply": "No matching assessments found.",
#                 "recommendations": [],
#                 "end_of_conversation": False
#             }

#         return {
#             "reply": f"Here are {len(results)} SHL assessments matching your needs.",
#             "recommendations": self.format_results(results),
#             "end_of_conversation": False,
#             "explanation": "Hybrid BM25 + FAISS with role-aware boosting"
#         }




class SHLAgent:

    def __init__(self, retriever):
        self.retriever = retriever
        self.memory = {}   # simple session memory

    # ---------------- INTENT ----------------
    def detect_intent(self, text):
        t = text.lower()

        if any(x in t for x in ["compare", "vs", "difference"]):
            return "compare"

        if any(x in t for x in ["add", "include", "refine"]):
            return "refine"

        return "recommend"

    # ---------------- BLOCKING ----------------
    def is_blocked(self, text):
        blocked = ["salary", "visa", "legal", "firing", "system prompt"]
        return any(b in text.lower() for b in blocked)

    # ---------------- CLARIFICATION ----------------
    def needs_clarification(self, text):
        t = text.lower()
        return not any(k in t for k in [
            "developer", "engineer", "java", "python",
            "sql", "manager", "analyst"
        ])

    # ---------------- VALIDATION ----------------
    def validate_results(self, results):
        return [r for r in results if r.get("name")]

    # ---------------- FORMAT ----------------
    def format_results(self, results):
        return [
            {
                "name": r["name"],
                "url": r["url"],
                "test_type": r["test_type"]
            }
            for r in results
        ]

    # ---------------- COMPARE ----------------
    def compare(self, query):

        results = self.validate_results(self.retriever.search(query, 2))

        if len(results) < 2:
            return {
                "reply": "I need more context to compare assessments.",
                "recommendations": [],
                "end_of_conversation": False
            }

        a, b = results[:2]

        return {
            "reply": f"{a['name']} is a {a['test_type']} assessment, while {b['name']} is a {b['test_type']} assessment focusing on different skill areas.",
            "recommendations": self.format_results([a, b]),
            "end_of_conversation": False
        }

    # ---------------- CHAT ----------------
    def chat(self, req):

        user_msg = req["messages"][-1]["content"]
        user_id = "default"

        if self.is_blocked(user_msg):
            return {
                "reply": "I can only help with SHL assessments.",
                "recommendations": [],
                "end_of_conversation": False
            }

        intent = self.detect_intent(user_msg)

        # ---------------- CLARIFY ----------------
        if self.needs_clarification(user_msg):
            return {
                "reply": "Could you please specify role (e.g., developer, analyst) and required skills?",
                "recommendations": [],
                "end_of_conversation": False
            }

        # ---------------- COMPARE ----------------
        if intent == "compare":
            return self.compare(user_msg)

        # ---------------- RETRIEVE ----------------
        results = self.validate_results(
            self.retriever.search(user_msg, 5)
        )

        if not results:
            return {
                "reply": "No matching assessments found in SHL catalog.",
                "recommendations": [],
                "end_of_conversation": False
            }

        # ---------------- STORE FOR REFINE ----------------
        self.memory[user_id] = results

        return {
            "reply": f"Here are {len(results)} SHL assessments matching your requirements.",
            "recommendations": self.format_results(results),
            "end_of_conversation": False
        }