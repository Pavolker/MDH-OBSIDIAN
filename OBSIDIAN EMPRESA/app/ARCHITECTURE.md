# O Cérebro App Architecture

This directory contains the production app for a web-first Obsidian alternative.

## Source of truth

- Notes live in a separate GitHub repository.
- This app repository contains the product code only.
- Railway ingests the content repo, indexes markdown, and serves the API.
- Netlify serves the browser UI.

## Runtime components

- `backend/main.py`: FastAPI API entrypoint
- `backend/sync_script.py`: GitHub repo ingestion and index build
- `backend/database.py`: Postgres and pgvector models
- `frontend/`: static web UI

## Data flow

1. A change is pushed to the content repo.
2. GitHub webhook or manual sync triggers the backend.
3. The backend clones or updates the repo in a cache directory.
4. Markdown files are parsed into documents and chunks.
5. Embeddings are generated and stored in Postgres.
6. The frontend queries the API for search, document views, and chat.

## Required environment variables

- `DATABASE_URL`
- `OPENAI_API_KEY`
- `OPENROUTER_API_KEY`
- `GITHUB_REPO_URL`
- `GITHUB_TOKEN`
- `GITHUB_REPO_BRANCH`
- `CONTENT_CACHE_DIR`
- `CORS_ORIGIN`

## Implementation decisions

- GitHub is the canonical content source.
- Railway owns ingestion and indexing.
- Postgres + pgvector stores semantic search data.
- Netlify only serves the UI.
- Sync is incremental and content-hash aware.
