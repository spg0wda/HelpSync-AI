import os
from typing import Any

from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


def is_groq_enabled() -> bool:
    return bool(os.getenv("GROQ_API_KEY"))


def polish_final_response(
    user_query: str,
    classification: dict[str, Any] | None,
    retrieval_result: dict[str, Any] | None,
    ticket: dict[str, Any] | None,
    escalation: dict[str, Any] | None,
    base_response: str
) -> dict:
    if not is_groq_enabled():
        return {
            "used_llm": False,
            "provider": "None",
            "message": "GROQ_API_KEY not found. Used fallback response.",
            "response": base_response
        }

    try:
        from groq import Groq

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

        prompt = f"""
You are HelpSync AI, an enterprise service desk assistant.

Rewrite the final response in a professional, helpful, and concise way.

Do not invent ticket IDs, escalation IDs, teams, or solutions.
Use only the provided details.

User Issue:
{user_query}

Classification:
{classification}

Knowledge Base Retrieval:
{retrieval_result}

Ticket:
{ticket}

Escalation:
{escalation}

Base Response:
{base_response}

Return only the final polished response.
"""

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional enterprise IT service desk assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=350
        )

        polished_response = completion.choices[0].message.content.strip()

        return {
            "used_llm": True,
            "provider": "Groq",
            "model": model,
            "message": "Groq polished the final response successfully.",
            "response": polished_response
        }

    except Exception as error:
        return {
            "used_llm": False,
            "provider": "Groq",
            "message": f"Groq failed. Used fallback response. Error: {str(error)}",
            "response": base_response
        }