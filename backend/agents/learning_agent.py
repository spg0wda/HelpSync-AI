import json
import os
import re
from datetime import datetime
from uuid import uuid4

from agents.feedback_agent import get_all_feedback


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

LEARNING_NOTES_FILE = os.path.join(DATA_DIR, "learning_notes.json")
APPROVED_LEARNING_FILE = os.path.join(DATA_DIR, "approved_learning_notes.json")


def ensure_learning_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    for file_path in [LEARNING_NOTES_FILE, APPROVED_LEARNING_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)


def load_json_file(file_path):
    ensure_learning_files()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except Exception:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)

        return []


def save_json_file(file_path, data):
    ensure_learning_files()

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def safe_rating(feedback):
    try:
        return int(feedback.get("rating", 5))
    except Exception:
        return 5


def should_create_learning_note(feedback):
    rating = safe_rating(feedback)
    helpful = feedback.get("helpful", True)
    suggestion = feedback.get("improvement_suggestion", "")
    comment = feedback.get("comment", "")

    if rating <= 3:
        return True

    if helpful is False:
        return True

    if suggestion.strip():
        return True

    if comment.strip() and rating <= 4:
        return True

    return False


def note_exists_for_feedback(notes, feedback_id):
    for note in notes:
        if note.get("source_feedback_id") == feedback_id:
            return True

    return False


def build_learning_note(feedback):
    rating = safe_rating(feedback)
    helpful = feedback.get("helpful", True)
    suggestion = feedback.get("improvement_suggestion", "")
    comment = feedback.get("comment", "")

    issue_text = suggestion.strip() or comment.strip() or "User was not fully satisfied with the service desk response."

    if rating <= 2 or helpful is False:
        priority = "High"
    elif rating == 3:
        priority = "Medium"
    else:
        priority = "Low"

    confidence_score = 90 if priority == "High" else 70 if priority == "Medium" else 50

    suggested_update = (
        "For similar future issues, improve the response by addressing this feedback: "
        f"{issue_text}. Provide clearer troubleshooting steps, ask one confirmation question if required, "
        "and create or escalate a ticket when the issue cannot be resolved directly."
    )

    return {
        "note_id": f"LN-{str(uuid4())[:8].upper()}",
        "source_feedback_id": feedback.get("feedback_id"),
        "conversation_id": feedback.get("conversation_id"),
        "priority": priority,
        "confidence_score": confidence_score,
        "status": "pending",
        "rating": rating,
        "helpful": helpful,
        "user_comment": comment,
        "improvement_suggestion": suggestion,
        "suggested_update": suggested_update,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "applied_at": None
    }


def get_all_learning_notes():
    return load_json_file(LEARNING_NOTES_FILE)


def get_pending_learning_notes():
    notes = get_all_learning_notes()

    return [
        note for note in notes
        if note.get("status") == "pending"
    ]


def get_applied_learning_notes():
    return load_json_file(APPROVED_LEARNING_FILE)


def generate_learning_notes_from_feedback():
    feedback_records = get_all_feedback()
    learning_notes = get_all_learning_notes()

    generated_notes = []

    for feedback in feedback_records:
        feedback_id = feedback.get("feedback_id")

        if not feedback_id:
            continue

        if not should_create_learning_note(feedback):
            continue

        if note_exists_for_feedback(learning_notes, feedback_id):
            continue

        note = build_learning_note(feedback)
        learning_notes.append(note)
        generated_notes.append(note)

    save_json_file(LEARNING_NOTES_FILE, learning_notes)

    return {
        "generated_count": len(generated_notes),
        "total_learning_notes": len(learning_notes),
        "generated_notes": generated_notes
    }


def apply_learning_note(note_id):
    learning_notes = get_all_learning_notes()
    approved_notes = get_applied_learning_notes()

    selected_note = None

    for note in learning_notes:
        if note.get("note_id") == note_id:
            selected_note = note
            break

    if not selected_note:
        return {
            "applied": False,
            "message": "Learning note not found."
        }

    if selected_note.get("status") == "applied":
        return {
            "applied": False,
            "message": "Learning note is already applied."
        }

    selected_note["status"] = "applied"
    selected_note["applied_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    approved_note = selected_note.copy()
    approved_note["approved_id"] = f"AL-{str(uuid4())[:8].upper()}"

    approved_notes.append(approved_note)

    save_json_file(LEARNING_NOTES_FILE, learning_notes)
    save_json_file(APPROVED_LEARNING_FILE, approved_notes)

    return {
        "applied": True,
        "message": "Learning note applied successfully.",
        "learning_note": selected_note
    }


def run_autonomous_learning_loop():
    generation_result = generate_learning_notes_from_feedback()
    summary = get_learning_summary()

    return {
        "message": "Autonomous learning loop completed.",
        "generation_result": generation_result,
        "summary": summary
    }


def get_learning_summary():
    notes = get_all_learning_notes()
    approved_notes = get_applied_learning_notes()

    pending_notes = [
        note for note in notes
        if note.get("status") == "pending"
    ]

    high_priority = [
        note for note in notes
        if note.get("priority") == "High"
    ]

    medium_priority = [
        note for note in notes
        if note.get("priority") == "Medium"
    ]

    low_priority = [
        note for note in notes
        if note.get("priority") == "Low"
    ]

    return {
        "total_learning_notes": len(notes),
        "pending_notes": len(pending_notes),
        "applied_notes": len(approved_notes),
        "high_priority_notes": len(high_priority),
        "medium_priority_notes": len(medium_priority),
        "low_priority_notes": len(low_priority),
        "latest_pending_notes": list(reversed(pending_notes))[:5],
        "latest_applied_notes": list(reversed(approved_notes))[:5]
    }


def tokenize(text):
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())

    return [
        word for word in words
        if len(word) > 2
    ]


def search_approved_learning_notes(user_query, issue_type=""):
    approved_notes = get_applied_learning_notes()

    if not approved_notes:
        return {
            "found": False,
            "retrieval_type": "Approved Learning Notes",
            "agent": "Autonomous Learning Retrieval Agent",
            "message": "No approved learning notes found."
        }

    query_tokens = set(tokenize(f"{user_query} {issue_type}"))
    matches = []

    for note in approved_notes:
        note_text = " ".join(
            [
                str(note.get("user_comment", "")),
                str(note.get("improvement_suggestion", "")),
                str(note.get("suggested_update", "")),
                str(note.get("priority", ""))
            ]
        )

        note_tokens = set(tokenize(note_text))
        score = len(query_tokens.intersection(note_tokens))

        if score > 0:
            matches.append(
                {
                    "score": score,
                    "note": note
                }
            )

    matches = sorted(matches, key=lambda item: item["score"], reverse=True)

    if not matches:
        return {
            "found": False,
            "retrieval_type": "Approved Learning Notes",
            "agent": "Autonomous Learning Retrieval Agent",
            "message": "No matching approved learning note found."
        }

    best_match = matches[0]["note"]

    return {
        "found": True,
        "retrieval_type": "Approved Learning Notes",
        "agent": "Autonomous Learning Retrieval Agent",
        "issue_type": issue_type,
        "solution": best_match.get("suggested_update"),
        "confidence_score": matches[0]["score"],
        "matched_learning_note": best_match,
        "top_matches": matches[:3]
    }