from data.chroma_store import search_knowledge_base
from agents.learning_agent import search_approved_learning_notes


def retrieve_solution(user_query: str, issue_type: str) -> dict:
    vector_result = search_knowledge_base(
        user_query=user_query,
        issue_type=issue_type,
        n_results=3
    )

    learning_result = search_approved_learning_notes(
        user_query=user_query,
        issue_type=issue_type
    )

    if vector_result.get("found") is True:
        if learning_result.get("found") is True:
            vector_result["learning_note_support"] = learning_result

        return vector_result

    if learning_result.get("found") is True:
        return learning_result

    return vector_result