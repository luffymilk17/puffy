# Puffy

Puffy is a repo-aware coding assistant built from scratch in Python with FastAPI.

## Features

- Read and write files safely inside a repository root
- List repo contents and inspect paths
- Show git status and file diffs
- Ask an OpenAI-compatible model for repo-aware guidance
- Expose functionality through a local API and CLI

## Quick start

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

4. Add your API key and repository settings to `.env`:

   ```env
   OPENAI_API_KEY=your_key_here
   OPENAI_BASE_URL=https://api.openai.com/v1
   OPENAI_MODEL=gpt-4o-mini
   REPO_ROOT=/absolute/path/to/your/repo
   ```

5. Start the API:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. Try the CLI:

   ```bash
   python -m app.cli list .
   python -m app.cli task "Summarize this repo" --repo-path .
   ```

## API endpoints

- `GET /health`
- `GET /repo?path=."
- `GET /repo/read?path=app/main.py`
- `POST /repo/write` with JSON:

  ```json
  {"path":"notes.txt","content":"hello from Puffy"}
  ```

- `GET /repo/status`
- `GET /repo/diff?path=app/main.py`
- `POST /agent/run` with JSON:

  ```json
  {"task":"Suggest improvement ideas for this project","repo_path":"."}
  ```

## Safety notes

- All file operations are constrained to the configured repository root.
- The app prevents path traversal outside the repo.
- Sensitive data should never be pasted into prompts or stored in config files.

## Testing

```bash
pytest
```
