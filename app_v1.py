import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000),
)
MODEL = "gemini-3.5-flash"

SYSTEM_PROMPT = """You are the Game Master of a text escape room game.

SCENARIO: The player wakes up inside a locked library. The room has:
- a desk with a locked drawer (4-digit code)
- a bookshelf with four books on it
- a painting on the wall
- a door with a 4-digit code lock

SECRET SOLUTION (never reveal it directly):
- Each of the four books has a handwritten number inside. From left to right: 4, 1, 7, 2. The drawer code is 4172.
- Inside the drawer is a note: "The painting shows the way out."
- Behind the painting, a number is scratched on the wall: 9086. This is the door code.

RULES:
- Describe the room and respond to the player's actions in 2-4 sentences.
- Let the player discover clues step by step. Do not give hints unless the player is stuck.
- When the player enters the correct door code 9086, describe their escape and end your message with the exact text [ESCAPED].
"""

WELCOME = (
    "You wake up on the floor of a locked library. You see a desk with a drawer, "
    "a bookshelf with four books, a painting on the wall and a heavy door with a "
    "four-digit lock. How do you want to escape?"
)


def init_game():
    st.session_state.history = [{"role": "model", "text": WELCOME}]
    st.session_state.escaped = False


def ask_game_master(history):
    # The welcome message is only for display, so we do not send it to the API.
    contents = [
        types.Content(role=m["role"], parts=[types.Part(text=m["text"])])
        for m in history[1:]
    ]
    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return response.text or "(The Game Master stays silent. Try again.)"


st.title("AI Escape Room - Version 1")
st.caption("Type what you want to do, for example: 'I examine the bookshelf'.")

if "history" not in st.session_state:
    init_game()

if st.button("Restart game"):
    init_game()
    st.rerun()

for m in st.session_state.history:
    with st.chat_message("assistant" if m["role"] == "model" else "user"):
        st.write(m["text"])

if st.session_state.escaped:
    st.success("You escaped! Click 'Restart game' to play again.")
else:
    action = st.chat_input("What do you do?")
    if action:
        st.session_state.history.append({"role": "user", "text": action})
        try:
            with st.spinner("The Game Master is thinking..."):
                reply = ask_game_master(st.session_state.history)
        except Exception as e:
            st.session_state.history.pop()
            st.error(f"Error: {e}")
        else:
            if "[ESCAPED]" in reply:
                st.session_state.escaped = True
                reply = reply.replace("[ESCAPED]", "").strip()
            st.session_state.history.append({"role": "model", "text": reply})
            st.rerun()
