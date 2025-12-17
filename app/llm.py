import asyncio

# Ye function AI ke response ko word-by-word stream karta hai
async def stream_llm_response(user_input: str):
    response = f"AI response for: {user_input}"

    for word in response.split():
        await asyncio.sleep(0.3)  # thoda delay = realtime feel
        yield word + " "

# Ye ek fake internal tool hai (complex interaction dikhane ke liye)
async def fake_tool_call(query: str):
    await asyncio.sleep(1)
    return f"[Tool Result] fetched data for '{query}'"
