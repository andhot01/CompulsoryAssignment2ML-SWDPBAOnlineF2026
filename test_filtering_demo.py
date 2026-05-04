from tools.semantic_scholar_tool import search_semantic_scholar
from logic.filtering import SearchConstraints, filter_papers


def main():
    papers = search_semantic_scholar("retrieval augmented generation", limit=3)

    constraints = SearchConstraints(
        year_operator="<",
        year_value=2021,
        citation_operator=">",
        citation_value=500,
    )

    filtered = filter_papers(papers, constraints)

    print(f"Total retrieved: {len(papers)}")
    print(f"Total after filtering: {len(filtered)}\n")

    for i, paper in enumerate(filtered, start=1):
        print(f"Result #{i}")
        print("Title:", paper.get("title"))
        print("Authors:", ", ".join(paper.get("authors", [])))
        print("Year:", paper.get("year"))
        print("Citations:", paper.get("citation_count"))
        print("URL:", paper.get("paper_url"))
        print("-" * 60)


if __name__ == "__main__":
    main()