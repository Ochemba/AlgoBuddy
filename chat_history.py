# chat_history.py — Chat Session Persistence with Supabase
"""
Saves and loads full chat sessions using Supabase.
"""

from supabase_client import supabase
from datetime import datetime
import uuid


def new_session_id() -> str:
    """Generate a unique session ID."""
    return uuid.uuid4().hex[:12]


def _get_user_id() -> str | None:
    """Get current user ID from session state (set at login)."""
    try:
        import streamlit as st
        return st.session_state.get("user_id")
    except Exception:
        return None


def save_session(username: str, session_id: str, messages: list,
                 course_id=None, topic_id=None, persona="default") -> None:
    """
    Save or update a chat session.
    """
    user_id = _get_user_id()
    if not user_id or not messages:
        return

    # Build title from first user message
    first_user = next((m["content"] for m in messages if m["role"] == "user"), "Chat")
    title = first_user[:60] + ("…" if len(first_user) > 60 else "")

    # Strip audio bytes before saving — not serialisable and not needed in DB
    clean_messages = [
        {"role": m["role"], "content": m["content"], "time": m.get("time", "")}
        for m in messages
    ]

    try:
        # Check if session exists
        existing = supabase().table("chat_sessions").select("*").eq("user_id", user_id).eq("session_id", session_id).execute()

        if existing.data:
            # Update existing session
            session = existing.data[0]
            supabase().table("chat_sessions").update({
                "title": title,
                "course_id": course_id,
                "topic_id": topic_id,
                "persona": persona,
                "message_count": len(clean_messages),
                "updated_at": datetime.now().isoformat()
            }).eq("id", session["id"]).execute()

            # Delete old messages
            supabase().table("chat_messages").delete().eq("session_id", session["id"]).execute()

            # Insert new messages
            for msg in clean_messages:
                supabase().table("chat_messages").insert({
                    "session_id": session["id"],
                    "role": msg["role"],
                    "content": msg["content"],
                    "time": msg.get("time", "")
                }).execute()
        else:
            # Create new session
            result = supabase().table("chat_sessions").insert({
                "user_id": user_id,
                "session_id": session_id,
                "title": title,
                "course_id": course_id,
                "topic_id": topic_id,
                "persona": persona,
                "message_count": len(clean_messages)
            }).execute()

            if result.data:
                session = result.data[0]
                for msg in clean_messages:
                    supabase().table("chat_messages").insert({
                        "session_id": session["id"],
                        "role": msg["role"],
                        "content": msg["content"],
                        "time": msg.get("time", "")
                    }).execute()

        # Keep max 50 sessions per user
        all_sessions = supabase().table("chat_sessions").select("*").eq("user_id", user_id).order("updated_at", desc=True).execute()
        if len(all_sessions.data) > 50:
            to_delete = all_sessions.data[50:]
            for sess in to_delete:
                supabase().table("chat_messages").delete().eq("session_id", sess["id"]).execute()
                supabase().table("chat_sessions").delete().eq("id", sess["id"]).execute()

    except Exception as e:
        print(f"Error saving session: {e}")


def load_all_sessions(username: str) -> list:
    """Return all sessions for a user, newest first."""
    user_id = _get_user_id()
    if not user_id:
        return []

    try:
        result = supabase().table("chat_sessions").select("*").eq("user_id", user_id).order("updated_at", desc=True).execute()
        sessions = []
        for s in result.data:
            sessions.append({
                "session_id": s["session_id"],
                "created_at": s["created_at"],
                "updated_at": s["updated_at"],
                "title": s.get("title", "Chat"),
                "course_id": s.get("course_id"),
                "topic_id": s.get("topic_id"),
                "persona": s.get("persona", "default"),
                "message_count": s.get("message_count", 0),
            })
        return sessions
    except Exception as e:
        print(f"load_all_sessions error: {e}")
        return []


def load_session(username: str, session_id: str) -> dict | None:
    """Load a single full session (including messages)."""
    user_id = _get_user_id()
    if not user_id:
        return None

    try:
        result = supabase().table("chat_sessions").select("*").eq("user_id", user_id).eq("session_id", session_id).execute()
        if not result.data:
            return None

        session = result.data[0]

        # Load messages — order by id (insertion order), fallback to unordered
        try:
            messages_result = supabase().table("chat_messages").select("*").eq("session_id", session["id"]).order("id").execute()
        except Exception:
            messages_result = supabase().table("chat_messages").select("*").eq("session_id", session["id"]).execute()

        messages = []
        for msg in messages_result.data:
            messages.append({
                "role": msg["role"],
                "content": msg["content"],
                "time": msg.get("time", "")
            })

        return {
            "session_id": session["session_id"],
            "created_at": session["created_at"],
            "title": session.get("title", "Chat"),
            "course_id": session.get("course_id"),
            "topic_id": session.get("topic_id"),
            "persona": session.get("persona", "default"),
            "messages": messages
        }
    except Exception as e:
        print(f"load_session error: {e}")
        return None


def delete_session(username: str, session_id: str) -> bool:
    """Delete a session by ID."""
    user_id = _get_user_id()
    if not user_id:
        return False

    try:
        result = supabase().table("chat_sessions").select("*").eq("user_id", user_id).eq("session_id", session_id).execute()
        if result.data:
            supabase().table("chat_messages").delete().eq("session_id", result.data[0]["id"]).execute()
            supabase().table("chat_sessions").delete().eq("id", result.data[0]["id"]).execute()
            return True
        return False
    except Exception:
        return False


def format_session_date(iso_string: str) -> str:
    """Format an ISO datetime string into a friendly label."""
    try:
        dt = datetime.fromisoformat(iso_string)
        today = datetime.now().date()
        diff = (today - dt.date()).days
        time_str = dt.strftime("%H:%M")
        if diff == 0:
            return f"Today {time_str}"
        elif diff == 1:
            return f"Yesterday {time_str}"
        else:
            return dt.strftime("%d %b %Y")
    except Exception:
        return iso_string