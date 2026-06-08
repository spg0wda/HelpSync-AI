import json
import os
from datetime import datetime
from uuid import uuid4


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FEEDBACK_FILE = os.path.join(BASE_DIR, "data", "feedback.json")


def ensure_feedback_file():
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)

    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def load_feedback():
    ensure_feedback_file()

    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except Exception:
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)

        return []


def save_feedback(feedback_records):
    ensure_feedback_file()

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as file:
        json.dump(feedback_records, file, indent=4)


def create_feedback(
    conversation_id=None,
    helpful=True,
    rating=5,
    comment="",
    improvement_suggestion=""
):
    feedback_records = load_feedback()

    feedback = {
        "feedback_id": f"FB-{str(uuid4())[:8].upper()}",
        "conversation_id": conversation_id,
        "helpful": helpful,
        "rating": rating,
        "comment": comment,
        "improvement_suggestion": improvement_suggestion,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    feedback_records.append(feedback)
    save_feedback(feedback_records)

    return feedback


def get_all_feedback():
    return load_feedback()


def get_feedback_summary():
    feedback_records = load_feedback()

    total_feedback = len(feedback_records)

    if total_feedback == 0:
        return {
            "total_feedback": 0,
            "helpful_count": 0,
            "not_helpful_count": 0,
            "average_rating": 0,
            "positive_percentage": 0,
            "negative_percentage": 0
        }

    helpful_count = len([item for item in feedback_records if item.get("helpful") is True])
    not_helpful_count = total_feedback - helpful_count

    ratings = [
        int(item.get("rating", 0))
        for item in feedback_records
        if str(item.get("rating", "")).isdigit()
    ]

    average_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

    positive_percentage = round((helpful_count / total_feedback) * 100, 2)
    negative_percentage = round((not_helpful_count / total_feedback) * 100, 2)

    return {
        "total_feedback": total_feedback,
        "helpful_count": helpful_count,
        "not_helpful_count": not_helpful_count,
        "average_rating": average_rating,
        "positive_percentage": positive_percentage,
        "negative_percentage": negative_percentage
    }


def get_rating_distribution():
    feedback_records = load_feedback()

    distribution = {
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0
    }

    for item in feedback_records:
        rating = str(item.get("rating", ""))

        if rating in distribution:
            distribution[rating] += 1

    return distribution


def get_recent_feedback(limit=5):
    feedback_records = load_feedback()

    return list(reversed(feedback_records))[:limit]


def get_improvement_suggestions():
    feedback_records = load_feedback()

    suggestions = []

    for item in feedback_records:
        suggestion = item.get("improvement_suggestion", "")
        comment = item.get("comment", "")

        if suggestion.strip():
            suggestions.append(
                {
                    "feedback_id": item.get("feedback_id"),
                    "conversation_id": item.get("conversation_id"),
                    "suggestion": suggestion,
                    "rating": item.get("rating"),
                    "created_at": item.get("created_at")
                }
            )

        elif comment.strip() and item.get("helpful") is False:
            suggestions.append(
                {
                    "feedback_id": item.get("feedback_id"),
                    "conversation_id": item.get("conversation_id"),
                    "suggestion": comment,
                    "rating": item.get("rating"),
                    "created_at": item.get("created_at")
                }
            )

    return suggestions


def get_learning_insights():
    feedback_records = load_feedback()
    summary = get_feedback_summary()
    suggestions = get_improvement_suggestions()
    rating_distribution = get_rating_distribution()

    low_rated_feedback = [
        item for item in feedback_records
        if int(item.get("rating", 5)) <= 2
    ]

    medium_rated_feedback = [
        item for item in feedback_records
        if int(item.get("rating", 5)) == 3
    ]

    high_rated_feedback = [
        item for item in feedback_records
        if int(item.get("rating", 5)) >= 4
    ]

    learning_actions = []

    if summary.get("average_rating", 0) < 3:
        learning_actions.append("Improve response quality because average rating is below 3.")

    if summary.get("negative_percentage", 0) > 40:
        learning_actions.append("Review failed responses because not-helpful percentage is high.")

    if len(suggestions) > 0:
        learning_actions.append("Use improvement suggestions to update knowledge base and prompts.")

    if len(low_rated_feedback) > 0:
        learning_actions.append("Analyze low-rated conversations and add better troubleshooting steps.")

    if not learning_actions:
        learning_actions.append("Feedback quality is healthy. Continue monitoring user responses.")

    return {
        "summary": summary,
        "rating_distribution": rating_distribution,
        "recent_feedback": get_recent_feedback(limit=5),
        "improvement_suggestions": suggestions,
        "learning_actions": learning_actions,
        "low_rated_count": len(low_rated_feedback),
        "medium_rated_count": len(medium_rated_feedback),
        "high_rated_count": len(high_rated_feedback)
    }