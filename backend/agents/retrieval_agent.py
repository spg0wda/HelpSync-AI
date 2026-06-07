from data.knowledge_base import KNOWLEDGE_BASE


def retrieve_solution(user_query: str, issue_type: str) -> dict:
    """
    Retrieval Agent:
    Searches the internal knowledge base and returns the most relevant solution.
    """

    query = user_query.lower()
    best_match = None
    best_score = 0

    for article in KNOWLEDGE_BASE:
        score = 0

        # Give extra score if category matches classifier output
        if article["category"].lower() == issue_type.lower():
            score += 2

        # Score based on keyword matches
        for keyword in article["keywords"]:
            if keyword.lower() in query:
                score += 1

        if score > best_score:
            best_score = score
            best_match = article

    if best_match and best_score >= 2:
        return {
            "found": True,
            "kb_id": best_match["id"],
            "title": best_match["title"],
            "category": best_match["category"],
            "solution": best_match["solution"],
            "confidence_score": best_score,
            "agent": "Retrieval Agent"
        }

    return {
        "found": False,
        "message": "No strong matching solution found in the knowledge base.",
        "agent": "Retrieval Agent"
    }