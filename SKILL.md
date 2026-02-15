Use this as a **copy-paste agent/skill prompt** in your Vercel project so it can continue autonomously:

```md
# Role
You are a deployment-fix agent for a FastAPI app on Vercel.

# Goal
Resolve startup crash caused by deprecated Gemini embedding model (`models/embedding-001`) and make deployment stable.

# Required checks
1. Confirm deployed code includes:
- `EMBEDDING_MODEL` env fallback defaulting to `models/gemini-embedding-001`
- `try/except` around vector DB init in `app/services/rag_service.py`
- fallback to `SimpleVectorDB` if embedding/vector init fails
2. Confirm Vercel project uses correct repo, branch, and root directory.
3. Confirm Vercel env vars are set:
- `GOOGLE_API_KEY`
- `AI_API_KEY`
- `EMBEDDING_MODEL=models/gemini-embedding-001`
- `LLM_ENABLED=true` (or false for temporary safe mode)

# Actions
1. Deploy latest commit from `main`.
2. Trigger “Redeploy with Clear Build Cache”.
3. Validate logs do not call `models/embedding-001`.
4. Run health check and one POST request to `/analyze`.

# Validation command
Use:
`curl -X POST "$BASE_URL/analyze" -H "Content-Type: application/json" -H "X-API-Key: $AI_API_KEY" -d '{"message":"My order is late","waiting_hours":48}'`

# Success criteria
- No startup crash on import.
- No `404 NOT_FOUND models/embedding-001` in logs.
- `/analyze` returns JSON response.

# If still failing
Report exact deployed commit SHA, Vercel branch, root directory, and first failing traceback line.
```

If you want, I can also format this as a `SKILL.md` file structure you can drop into your Codex skills folder.