# Deployment plan

A FastAPI + LangChain + Chroma RAG API in `src/`, with a Streamlit client in `app.py`.

## Rules

- Keep the existing layering (api -> services -> infrastructure
  providers, wired in `src/dependencies`). Do not restructure it.
- Small, readable changes. I must be able to explain every file
  in an interview.
- In the PR description, explain what changed and why, file by file.
- Run the tests if you can install `requirements.txt`. If you cannot,
  say so clearly in the PR instead of claiming they pass.

## Step 1 - make it work, with tests

1. Fix the broken calls:
   - `DocumentService.process` calls `embeddingService.embed_documents`,
     but `EmbeddingService` only defines `embed_chunks`, which itself
     calls a provider method that does not exist (the provider has
     `embed_documents`).
   - `RagService.ask` calls `vectorStore.similarity_search`, but the
     `VectorStore` service only defines `save`.
2. `POST /ask`: take a JSON body `{question}`. Pass only the retrieved
   chunk texts into the prompt (not Chroma's whole result dict).
   Return `{answer, sources}`. Put request/response models in
   `src/schemas`.
3. `POST /documents`: return `{filename, chunks}` instead of the
   embedding vectors.
4. Update `app.py` to match the new request/response shapes.
5. Tests (pytest): use FastAPI `dependency_overrides` to swap in a fake
   embedding provider and a fake LLM provider, so no test calls
   OpenAI or needs a key. Use a tiny PDF fixture. Cover: upload a
   PDF, ask a question, and check the prompt contains the retrieved
   chunk text.
6. A GitHub Actions workflow that runs the tests on every push and
   pull request.

Done when: the tests pass in CI.

## Step 2 - Docker and first deploy

One Dockerfile, two start commands (API, Streamlit), docker compose for
local use. `render.yaml` with two free Render web services. The UI calls
the API's public URL (free Render services cannot receive
private-network traffic) and pings `GET /health` on load.

## Step 3 - safe to share

PDF only, upload size cap, question length cap, daily caps on uploads
and questions (HTTP 429). Each browser session searches only its own
uploads (session id stored in chunk metadata and used as a query
filter). Clean error when OpenAI fails. A test per rule.

## Step 4 - README

Live link, architecture sketch, limits, a "not done yet" list, a screen
recording.

## Out of scope

Persistent storage, login, Azure, retrieval evaluation.
