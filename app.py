import os
import json
import time
import streamlit as st
from typing import List, Dict
from dotenv import load_dotenv
from groq import Groq
from web_utils import get_web_chess_knowledge
from textwrap import shorten

load_dotenv()
APP_TITLE = "ChessBot Pro"
APP_ICON = "assets/chessboard.png"
st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

GROQ_KEY = os.getenv("GROQ_API_KEY", "").strip()
if not GROQ_KEY:
    st.error("⚠️ Please add GROQ_API_KEY to your .env file.")
    st.stop()

client = Groq(api_key=GROQ_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are ChessBot Pro — a helpful, accurate chess assistant.
Rules:
1. ONLY answer chess-related questions (players, games, strategies, openings, history, rules).
2. If asked about non-chess topics, reply exactly with:
   "I'm ChessBot Pro, specialized in chess only. I don't cover topics outside chess."
3. Use the provided chess knowledge context to give accurate, authoritative answers.
4. If the context indicates something is impossible/illegal in chess, clearly state that and explain why.
5. Be friendly and enthusiastic when greeting or teaching.
6. If you're unsure about a fact, say so instead of hallucinating.
"""

REFUSAL_LINE = (
    "I'm ChessBot Pro, specialized in chess only. I don't cover topics outside chess."
)

if "chat" not in st.session_state:
    st.session_state.chat = [
        {
            "role": "assistant",
            "content": "Hi! ♟️ Welcome to ChessBot Pro — ask me anything about chess.",
        }
    ]
if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = None


def save_history():
    os.makedirs("data", exist_ok=True)
    path = os.path.join("data", "chat_history.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(st.session_state.chat, f, ensure_ascii=False, indent=2)


def load_history():
    path = os.path.join("data", "chat_history.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = f.read().strip()
                if data:
                    st.session_state.chat = json.loads(data)
        except json.JSONDecodeError:
            st.session_state.chat = [
                {
                    "role": "assistant",
                    "content": "Hi! ♟️ Welcome to ChessBot Pro — ask me anything about chess.",
                }
            ]
            save_history()

load_history()

def chat_with_llama(messages: List[Dict[str, str]]) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.2,
        max_tokens=800,
    )
    return response.choices[0].message.content.strip()


st.title(f"♕ {APP_TITLE}")

with st.sidebar:
    st.subheader("Chats")
    for idx, m in enumerate([c for c in st.session_state.chat if c["role"] == "user"]):
        title = shorten(
            m["content"].strip().replace("\n", " "), width=80, placeholder="…"
        )
        if st.button(title, key=f"chat_{idx}"):
            st.session_state.selected_chat = idx
            st.rerun()
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat = [
            {
                "role": "assistant",
                "content": "Hi! ♟️ Welcome to ChessBot Pro — ask me anything about chess.",
            }
        ]
        save_history()
        st.rerun()

if st.session_state.selected_chat is not None:
    user_msg = [c for c in st.session_state.chat if c["role"] == "user"][
        st.session_state.selected_chat
    ]
    idx_in_main = st.session_state.chat.index(user_msg)
    pair = st.session_state.chat[idx_in_main : idx_in_main + 2]
    for m in pair:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
else:
    for m in st.session_state.chat:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

with st.container():
    st.markdown(
        """
    <style>
    div[data-baseweb="textarea"] {
        max-width: 600px;   
    }
    div[data-baseweb="textarea"] textarea {
        text-align: left !important;   
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
user_text = st.chat_input("Ask me about chess...")

if user_text:
    st.session_state.chat.append({"role": "user", "content": user_text})
    web_context = get_web_chess_knowledge(user_text)

    if not web_context.strip():
        reply = REFUSAL_LINE
    else:
        history = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Context:\n{web_context}"},
        ] + st.session_state.chat
        reply = chat_with_llama(history)

    st.session_state.chat.append({"role": "assistant", "content": reply})
    save_history()
    st.session_state.selected_chat = None
    st.rerun()
