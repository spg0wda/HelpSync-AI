from data.chroma_store import search_knowledge_base


def retrieve_solution(user_query: str, issue_type: str) -> dict:
    """
    Retrieval Agent:
    Uses ChromaDB vector search to find the most relevant knowledge base solution.
    """

    result = search_knowledge_base(
        user_query=user_query,
        issue_type=issue_type,
        n_results=3
    )

    return result