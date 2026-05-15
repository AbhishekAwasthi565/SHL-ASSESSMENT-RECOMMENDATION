import requests
import json
import re

URL = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"


def extract_json_objects(text):
    """
    Extract JSON-like objects safely from broken JSON stream.
    """

    objects = []
    brace_count = 0
    start = None

    for i, ch in enumerate(text):

        if ch == "{":
            if brace_count == 0:
                start = i
            brace_count += 1

        elif ch == "}":
            brace_count -= 1

            if brace_count == 0 and start is not None:
                chunk = text[start:i+1]

                try:
                    obj = json.loads(chunk)
                    objects.append(obj)
                except:
                    pass

                start = None

    return objects


def download_catalog():

    try:
        res = requests.get(URL, timeout=30)
        raw = res.text

    except Exception as e:
        print("Network error:", e)
        return

    print("Downloaded raw text")

    data = extract_json_objects(raw)

    print(f"Recovered items: {len(data)}")

    with open("app/data/raw/catalog.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Saved catalog.json")


if __name__ == "__main__":
    download_catalog()