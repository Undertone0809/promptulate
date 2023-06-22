import arxiv


def main():
    search = arxiv.Search(
        query="Tree of Thoughts",
        max_results=10,
        sort_by=arxiv.SortCriterion.Relevance
    )
    for result in search.results():
        print(result.__dict__)


if __name__ == '__main__':
    main()
