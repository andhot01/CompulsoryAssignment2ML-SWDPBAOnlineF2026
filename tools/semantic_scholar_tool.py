import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def search_semantic_scholar(topic: str, limit: int = 10, offset: int = 0):
    """
    Search Semantic Scholar for papers matching a topic.
    Returns a normalized list of candidate papers.
    """
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    params = {
        "query": topic,
        "limit": limit,
        "offset": offset,
        "fields": "title,authors,year,abstract,citationCount,url"
    }

    response = requests.get(BASE_URL, params=params, headers=headers, timeout=30)

    if response.status_code != 200:
        raise Exception(
            f"Semantic Scholar request failed: {response.status_code} - {response.text}"
        )

    payload = response.json()

    normalized_results = []
    for paper in payload.get("data", []):
        normalized_results.append({
            "title": paper.get("title"),
            "authors": [author.get("name") for author in paper.get("authors", []) if author.get("name")],
            "year": paper.get("year"),
            "citation_count": paper.get("citationCount"),
            "citation_count_source": "Semantic Scholar API",
            "paper_url": paper.get("url"),
            "abstract": paper.get("abstract"),
        })

    return normalized_results


if __name__ == "__main__":
    query = "artificial intelligence agents"
    results = search_semantic_scholar(query, limit=5)

    print(f"Found {len(results)} results for: {query}\n")
    for i, paper in enumerate(results, start=1):
        print(f"Result #{i}")
        print(json.dumps(paper, indent=2, ensure_ascii=False))
        print("-" * 60)