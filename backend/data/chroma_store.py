import os
import chromadb

from data.knowledge_base import KNOWLEDGE_BASE


CHROMA_DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "chroma_db"
)

COLLECTION_NAME = "helpsync_knowledge_base"


def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)


def get_knowledge_collection():
    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": "HelpSync AI service desk knowledge base"
        }
    )

    return collection


def build_document(article: dict) -> str:
    keywords = ", ".join(article.get("keywords", []))

    return (
        f"Category: {article.get('category')}\n"
        f"Title: {article.get('title')}\n"
        f"Keywords: {keywords}\n"
        f"Solution: {article.get('solution')}"
    )


def seed_knowledge_base() -> dict:
    collection = get_knowledge_collection()

    existing_count = collection.count()

    if existing_count > 0:
        return {
            "seeded": False,
            "message": "ChromaDB knowledge base already seeded.",
            "document_count": existing_count
        }

    ids = []
    documents = []
    metadatas = []

    for article in KNOWLEDGE_BASE:
        ids.append(article["id"])
        documents.append(build_document(article))
        metadatas.append({
            "kb_id": article["id"],
            "category": article["category"],
            "title": article["title"],
            "keywords": ", ".join(article.get("keywords", [])),
            "solution": article["solution"]
        })

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    return {
        "seeded": True,
        "message": "ChromaDB knowledge base seeded successfully.",
        "document_count": len(ids)
    }


def reset_knowledge_base() -> dict:
    client = get_chroma_client()

    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    return seed_knowledge_base()


def calculate_confidence(distance) -> float:
    if distance is None:
        return 0.0

    confidence = 1 / (1 + float(distance))
    return round(confidence, 3)


def search_knowledge_base(user_query: str, issue_type: str, n_results: int = 3) -> dict:
    seed_knowledge_base()

    collection = get_knowledge_collection()

    results = collection.query(
        query_texts=[user_query],
        n_results=n_results
    )

    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    matches = []

    for index, metadata in enumerate(metadatas):
        distance = distances[index] if index < len(distances) else None
        confidence = calculate_confidence(distance)

        match = {
            "kb_id": metadata.get("kb_id"),
            "title": metadata.get("title"),
            "category": metadata.get("category"),
            "solution": metadata.get("solution"),
            "keywords": metadata.get("keywords"),
            "distance": distance,
            "confidence_score": confidence,
            "document": documents[index] if index < len(documents) else "",
            "id": ids[index] if index < len(ids) else None
        }

        matches.append(match)

    if not matches:
        return {
            "found": False,
            "message": "No vector matches found in ChromaDB.",
            "matches": [],
            "agent": "Vector Retrieval Agent"
        }

    best_match = matches[0]
    same_category = best_match.get("category", "").lower() == issue_type.lower()
    confidence = best_match.get("confidence_score", 0)

    if same_category or confidence >= 0.45:
        return {
            "found": True,
            "kb_id": best_match.get("kb_id"),
            "title": best_match.get("title"),
            "category": best_match.get("category"),
            "solution": best_match.get("solution"),
            "confidence_score": confidence,
            "distance": best_match.get("distance"),
            "top_matches": matches,
            "retrieval_type": "ChromaDB Vector Search",
            "agent": "Vector Retrieval Agent"
        }

    return {
        "found": False,
        "message": "No strong semantic match found in ChromaDB.",
        "top_matches": matches,
        "retrieval_type": "ChromaDB Vector Search",
        "agent": "Vector Retrieval Agent"
    }