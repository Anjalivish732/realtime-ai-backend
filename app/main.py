from fastapi import FastAPI, WebSocket
import time, asyncio

from app.database import supabase
from app.llm import stream_llm_response, fake_tool_call
from app.tasks import process_session_summary

app = FastAPI()   # 👈 ye line bahut important hai

@app.websocket("/ws/session/{session_id}")
async def websocket_chat(ws: WebSocket, session_id: str):
    await ws.accept()
    start_time = time.time()

    # session start save karo
    supabase.table("sessions").insert({
        "session_id": session_id
    }).execute()

    try:
        while True:
            # user message receive
            user_msg = await ws.receive_text()

            # user message log
            supabase.table("session_events").insert({
                "session_id": session_id,
                "event_type": "user_message",
                "content": user_msg
            }).execute()

            # tool calling condition
            if "fetch" in user_msg.lower():
                tool_result = await fake_tool_call(user_msg)

                supabase.table("session_events").insert({
                    "session_id": session_id,
                    "event_type": "tool_call",
                    "content": tool_result
                }).execute()

            # AI response streaming
            async for token in stream_llm_response(user_msg):
                await ws.send_text(token)

                supabase.table("session_events").insert({
                    "session_id": session_id,
                    "event_type": "ai_message",
                    "content": token
                }).execute()

    except:
        # client disconnect
        duration = int(time.time() - start_time)

        asyncio.create_task(
            process_session_summary(session_id, duration)
        )
