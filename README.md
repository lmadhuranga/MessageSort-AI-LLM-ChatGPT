MessageSort AI
=========
![enter image description here](https://github.com/lmadhuranga/Messages-Analysis-Reply-Suggestion-With-LLM-GeminiAi/blob/main/ai-system.jpg?raw=true)
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
1) Create a `.env` file with your API keys:
   `GOOGLE_API_KEY=your_key_here`
   `AI_API_KEY=your_api_key_here`
   `LLM_ENABLED=true`
2) Create a virtual environment and install dependencies:
   `uv venv`
   `uv pip install -r requirement.txt`

Run
---
`python main.py`

Local (no Docker)
-----------------
1) Activate the virtual environment:
   `source .venv/bin/activate`
2) Start the API server:
   `uvicorn app.api:app --reload`
3) Call the endpoint:
   `POST http://127.0.0.1:8000/analyze`
   Header: `X-API-Key: your_api_key_here`
   Body: `{"message":"My order is late","waiting_hours":48}`

Ports
-----
- API server runs on port 8000 (http://127.0.0.1:8000).
- Docker/Docker Compose publish container port 8000 to host port 8000.

API
---
Start the server:
`uvicorn app.api:app --reload`

Then POST:
`POST http://127.0.0.1:8000/analyze`
Body JSON:
`{"message":"My order is late","waiting_hours":48}`
Header:
`X-API-Key: your_api_key_here`

Docker
------
Create `.env` in the repo root:
`GOOGLE_API_KEY=your_key_here`
`AI_API_KEY=your_api_key_here`
`LLM_ENABLED=true`

Build:
`docker build -t treema-ai .`

Run:
`docker run --rm -p 8000:8000 -e GOOGLE_API_KEY=your_key_here -e AI_API_KEY=your_api_key_here treema-ai`

Compose (foreground):
`docker compose up --build`

Compose (background / keep running):
`docker compose up --build -d`

Stop Compose:
`docker compose down`

Check logs (background):
`docker compose logs -f`

Vercel
------
1) Ensure `requirements.txt` exists (already included) and commit `vercel.json`.
2) In Vercel project settings, set environment variables:
   `GOOGLE_API_KEY=your_key_here`
   `AI_API_KEY=your_api_key_here`
3) Deploy the repo in Vercel. The API will be available at:
   `https://<your-app>.vercel.app/analyze`
Note: Vercel builds skip native vector DBs; the app falls back to a simple
in-memory text matcher for RAG in that environment.
