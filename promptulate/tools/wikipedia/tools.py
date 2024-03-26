from typing import Any, Optional


def wikipedia_search(
    query: str,
    top_k_results: int = 3,
    lang: str = "en",
    doc_content_chars_max: int = 4000,
) -> str:
    """
    Function to search Wikipedia for a given query and return page summaries.

    Args:
        query (str): The search query for Wikipedia.
        top_k_results (int): The number of top results to retrieve. Default is 3.
        lang (str): The language for the Wikipedia search. Default is "en".
        doc_content_chars_max (int): Maximum number of characters
                                    for the document content. Default is 4000.

    Returns:
        str: A string containing the concatenated page summaries
            of the top search results,limited by doc_content_chars_max.
    """
    WIKIPEDIA_MAX_QUERY_LENGTH = 300

    try:
        import wikipedia

        wikipedia.set_lang(lang)
    except ImportError:
        raise ImportError(
            "Could not import wikipedia python package. "
            "Please install it with `pip install wikipedia`."
        )

    wiki_client = wikipedia
    page_titles = wiki_client.search(
        query[:WIKIPEDIA_MAX_QUERY_LENGTH], results=top_k_results
    )
    summaries = []

    for page_title in page_titles[:top_k_results]:
        wiki_page = _fetch_page(wiki_client, page_title)
        if wiki_page:
            summary = _formatted_page_summary(page_title, wiki_page)
            if summary:
                summaries.append(summary)

    if not summaries:
        return "No good Wikipedia Search Result was found"

    return "\n\n".join(summaries)[:doc_content_chars_max]


def _formatted_page_summary(page_title: str, wiki_page: Any) -> Optional[str]:
    return f"Page: {page_title}\nSummary: {wiki_page.summary}"


def _fetch_page(wiki_client: Any, page: str) -> Optional[str]:
    try:
        return wiki_client.page(title=page, auto_suggest=False)
    except (
        wiki_client.exceptions.PageError,
        wiki_client.exceptions.DisambiguationError,
    ):
        return None
