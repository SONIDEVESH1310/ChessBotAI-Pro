
# ♕ ChessBot Pro

ChessBot Pro is an AI-powered interactive assistant specialized in chess. Ask questions about chess rules, strategies, openings, game history, and more — and get accurate, context-aware answers. Built with **Streamlit**, **Groq AI**, and live web-based chess knowledge retrieval.

---

## 🛠 Features

- Interactive chat interface for chess queries  
- Dynamically retrieves authoritative chess knowledge from the web  
- Remembers chat history across sessions  
- Enforces chess-only responses (refuses off-topic questions)  
- Friendly, enthusiastic, and educational responses  
- Supports pawn promotion, illegal move warnings, and rule clarification  

---

## ⚡ Installation & Run Instructions

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/chessbot-pro.git
cd chessbot-pro
```

2. **Create a virtual environment** (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** in the project root with your API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the app**:

```bash
streamlit run app.py
```

6. Open the browser link shown in the terminal (usually `http://localhost:8501`).  

---

## 🔑 API Key Setup (Groq AI)

1. Go to [Groq AI](https://www.groq.com/) and create an account if you don’t have one.  
2. Navigate to the API key section in your dashboard.  
3. Generate a new API key.  
4. Copy the key and paste it into the `.env` file like this:

```env
GROQ_API_KEY=your_generated_key
```

5. Save `.env` and restart the app.  

---

## ⚡ Usage Instructions

- Type your chess-related questions in the chat input.  
- The assistant will retrieve relevant chess knowledge and answer accurately.  
- If you ask non-chess questions, ChessBot Pro will politely refuse:  
  ```
  I'm ChessBot Pro, specialized in chess only. I don't cover topics outside chess.
  ```
- You can clear chat history using the sidebar “🗑️ Clear Chat” button.  

---

## 📌 Assumptions

- Only chess-related questions are processed.  
- Chat history is stored locally in `data/chat_history.json`.  
- Web scraping is limited to Chess.com and Wikipedia rules pages for safety.  
- Large language model responses are limited to 800 tokens per message.  

---

## ✨ Extra Features

- Chat message previews in the sidebar for easy navigation  
- Automatic handling of illegal positions and rule violations  
- Context-aware replies using dynamically fetched chess knowledge  
- Styled and responsive UI for a smooth user experience  

---

## ⚠ Requirements

- Python 3.9+  
- Streamlit  
- Groq API key  

---

## 📝 License

MIT License. Feel free to use and adapt ChessBot Pro for personal or educational purposes.
