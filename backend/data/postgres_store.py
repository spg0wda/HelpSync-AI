import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

engine = None
SessionLocal = None


class ConversationRecord(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(100), unique=True, index=True)
    user_query = Column(Text)
    classification = Column(JSON)
    route_to = Column(String(100))
    retrieval_result = Column(JSON)
    ticket = Column(JSON)
    escalation = Column(JSON)
    final_response = Column(Text)
    raw_record = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)


def is_postgres_enabled() -> bool:
    return bool(DATABASE_URL)


def get_engine():
    global engine

    if not is_postgres_enabled():
        return None

    if engine is None:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    return engine


def get_session_factory():
    global SessionLocal

    db_engine = get_engine()

    if db_engine is None:
        return None

    if SessionLocal is None:
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=db_engine
        )

    return SessionLocal


def init_postgres_tables() -> dict:
    if not is_postgres_enabled():
        return {
            "enabled": False,
            "message": "DATABASE_URL not found. PostgreSQL is disabled."
        }

    db_engine = get_engine()
    Base.metadata.create_all(bind=db_engine)

    return {
        "enabled": True,
        "message": "PostgreSQL tables initialized successfully."
    }


def save_conversation_to_postgres(record: dict[str, Any]) -> dict:
    if not is_postgres_enabled():
        return {
            "saved": False,
            "message": "DATABASE_URL not found. Skipped PostgreSQL save."
        }

    init_postgres_tables()

    session_factory = get_session_factory()
    db = session_factory()

    try:
        existing = (
            db.query(ConversationRecord)
            .filter(ConversationRecord.conversation_id == record.get("conversation_id"))
            .first()
        )

        if existing:
            return {
                "saved": False,
                "message": "Conversation already exists in PostgreSQL.",
                "conversation_id": record.get("conversation_id")
            }

        conversation = ConversationRecord(
            conversation_id=record.get("conversation_id"),
            user_query=record.get("user_query"),
            classification=record.get("classification"),
            route_to=record.get("route_to"),
            retrieval_result=record.get("retrieval_result"),
            ticket=record.get("ticket"),
            escalation=record.get("escalation"),
            final_response=record.get("final_response"),
            raw_record=record
        )

        db.add(conversation)
        db.commit()

        return {
            "saved": True,
            "message": "Conversation saved to PostgreSQL.",
            "conversation_id": record.get("conversation_id")
        }

    except Exception as error:
        db.rollback()

        return {
            "saved": False,
            "message": f"PostgreSQL save failed: {str(error)}"
        }

    finally:
        db.close()


def get_recent_postgres_conversations(limit: int = 10) -> list:
    if not is_postgres_enabled():
        return []

    init_postgres_tables()

    session_factory = get_session_factory()
    db = session_factory()

    try:
        rows = (
            db.query(ConversationRecord)
            .order_by(ConversationRecord.id.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "conversation_id": row.conversation_id,
                "user_query": row.user_query,
                "classification": row.classification,
                "route_to": row.route_to,
                "retrieval_result": row.retrieval_result,
                "ticket": row.ticket,
                "escalation": row.escalation,
                "final_response": row.final_response,
                "created_at": row.created_at.strftime("%Y-%m-%d %H:%M:%S") if row.created_at else None
            }
            for row in rows
        ]

    finally:
        db.close()


def get_postgres_status() -> dict:
    if not is_postgres_enabled():
        return {
            "enabled": False,
            "connected": False,
            "message": "DATABASE_URL not found."
        }

    try:
        init_postgres_tables()

        session_factory = get_session_factory()
        db = session_factory()

        try:
            total_conversations = db.query(ConversationRecord).count()

            return {
                "enabled": True,
                "connected": True,
                "message": "PostgreSQL connected successfully.",
                "total_conversations": total_conversations
            }

        finally:
            db.close()

    except Exception as error:
        return {
            "enabled": True,
            "connected": False,
            "message": f"PostgreSQL connection failed: {str(error)}"
        }