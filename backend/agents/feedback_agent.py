import json
import os
from datetime import datetime


FEEDBACK_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "feedback.json"
)


def load_feedback() -> list:
    """
    Loads user feedback records.
    """

    if not os.path.exists(FEEDBACK_FILE):
        return []

    with open(FEEDBACK_FILE, "r") as file:
        return json.load(file)


def save_feedback_records(feedback_records: list) -> None:
    """
    Saves user feedback records.
    """

    with open(FEEDBACK_FILE, "w") as file:
        json.dump(feedback_records, file, indent=4)


def create_feedback(
    conversation_id: str | None,
    helpful: bool,
    rating: int,
    comment: str,
    improvement_suggestion: str
) -> dict:
    """
    Feedback Agent:
    Stores human feedback and creates a simple learning note.
    """

    feedback_records = load_feedback()

    feedback_id = f"FDB-{5001 + len(feedback_records)}"

    feedback = {
        "feedback_id": feedback_id,
        "conversation_id": conversation_id,
        "helpful": helpful,
        "rating": rating,
        "comment": comment,
        "improvement_suggestion": improvement_suggestion,
        "learning_note": generate_learning_note(
            helpful=helpful,
            rating=rating,
            comment=comment,
            improvement_suggestion=improvement_suggestion
        ),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": "Feedback Agent"
    }

    feedback_records.append(feedback)
    save_feedback_records(feedback_records)

    return feedback


def generate_learning_note(
    helpful: bool,
    rating: int,
    comment: str,
    improvement_suggestion: str
) -> str:
    """
    Creates a basic learning note from feedback.
    """

    if helpful and rating >= 4:
        return "Response was useful. Similar workflow can be reused for future similar issues."

    if not helpful or rating <= 2:
        return (
            "Response needs improvement. Review classification, knowledge base coverage, "
            "routing decision, and final response quality."
        )

    if improvement_suggestion.strip():
        return f"User suggested improvement: {improvement_suggestion}"

    if comment.strip():
        return f"User comment should be reviewed: {comment}"

    return "Feedback received. Use this record for future workflow improvement."


def get_all_feedback() -> list:
    """
    Returns all feedback records.
    """

    return load_feedback()[::-1]


def get_feedback_summary() -> dict:
    """
    Returns feedback analytics.
    """

    feedback_records = load_feedback()

    if not feedback_records:
        return {
            "total_feedback": 0,
            "helpful_count": 0,
            "not_helpful_count": 0,
            "average_rating": 0,
            "recent_feedback": []
        }

    helpful_count = len([
        feedback for feedback in feedback_records
        if feedback.get("helpful") is True
    ])

    not_helpful_count = len(feedback_records) - helpful_count

    total_rating = sum(
        feedback.get("rating", 0)
        for feedback in feedback_records
    )

    average_rating = round(total_rating / len(feedback_records), 2)

    return {
        "total_feedback": len(feedback_records),
        "helpful_count": helpful_count,
        "not_helpful_count": not_helpful_count,
        "average_rating": average_rating,
        "recent_feedback": feedback_records[-5:][::-1]
    }