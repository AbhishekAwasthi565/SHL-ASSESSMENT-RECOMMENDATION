import json
import re


def extract_skills(text):
    """Simple skill extractor (starter version)"""

    if not text:
        return []

    skills = []

    keywords = [
        "java", "python", "sql", "c++", "c#", "javascript",
        "communication", "leadership", "logical", "aptitude",
        "personality", "problem solving", "excel"
    ]

    lower = text.lower()

    for k in keywords:
        if k in lower:
            skills.append(k)

    return list(set(skills))


def normalize_item(item):

    name = item.get("name", "")
    description = item.get("description", "")

    return {
        "name": name,
        "url": item.get("url", ""),
        "description": description,
        "skills": extract_skills(name + " " + description),
        "test_type": item.get("test_type", "unknown"),
        "level": item.get("level", ""),
        "duration": item.get("duration", ""),
        "tags": item.get("tags", [])
    }


def run():

    with open("app/data/raw/catalog.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = []

    for item in data:
        cleaned.append(normalize_item(item))

    with open("app/data/processed/catalog_clean.json", "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

    print("Cleaned items:", len(cleaned))


if __name__ == "__main__":
    run()