Treema-Ai
=========

Overview
--------
This project is a small customer-support AI demo built with LangGraph. It runs a
linear pipeline that:
- analyzes intent and sentiment,
- scores priority,
- retrieves relevant knowledge (RAG),
- generates reply suggestions.

How It Works
------------
The pipeline is defined in `app/agents/graph.py` and executes these nodes in
order:
1. intent_sentiment (TextBlob sentiment + Gemini intent classification)
2. priority (rule-based scoring)
3. rag (vector search over small default docs)
4. suggested_reply (Gemini-generated responses)

Files to Know
-------------
- `main.py`: Runs example scenarios through the graph and prints results.
- `app/agents/graph.py`: Builds and compiles the LangGraph flow.
- `app/agents/nodes.py`: Node implementations (sentiment, intent, priority, RAG, reply).
- `app/agents/state.py`: Typed state passed between nodes.
- `app/services/llm_service.py`: Gemini LLM wrapper (reads `GOOGLE_API_KEY`).
- `app/services/rag_service.py`: Chroma (macOS) or FAISS vector store.

Setup
-----
1) Create a `.env` file with your API key:
   `GOOGLE_API_KEY=your_key_here`
2) Create a virtual environment and install dependencies:
   `uv venv`
   `uv pip install -r requirement.txt`

Run
---
`python main.py`

API
---
Start the server:
`uvicorn app.api:app --reload`

Then POST:
`POST http://127.0.0.1:8000/analyze`
Body JSON:
`{"message":"My order is late","waiting_hours":48}`

Docker
------
Create `.env` in the repo root:
`GOOGLE_API_KEY=your_key_here`

Build:
`docker build -t treema-ai .`

Run:
`docker run --rm -p 8000:8000 -e GOOGLE_API_KEY=your_key_here treema-ai`

Compose (foreground):
`docker compose up --build`

Compose (background / keep running):
`docker compose up --build -d`

Stop Compose:
`docker compose down`

Check logs (background):
`docker compose logs -f`
