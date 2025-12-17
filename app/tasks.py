from app.database import supabase

# WebSocket close hone ke baad ye function chalega
async def process_session_summary(session_id: str, duration: int):
    # Puri conversation nikaalo
    events = supabase.table("session_events") \
        .select("content") \
        .eq("session_id", session_id) \
        .execute()

    conversation_text = " ".join(e["content"] for e in events.data)

    # Simple summary (real LLM later add ho sakta hai)
    summary = conversation_text[:200]

    # Session table update karo
    supabase.table("sessions").update({
        "end_time": "now()",
        "duration_seconds": duration,
        "summary": summary
    }).eq("session_id", session_id).execute()
