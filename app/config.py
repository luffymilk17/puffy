import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@lru_cache(maxsize=1)
def settings() -> dict[str, str]:
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "openai_base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "repo_root": os.getenv("REPO_ROOT", os.getcwd()),
        "app_api_key": os.getenv("APP_API_KEY", ""),
        "allowed_origins": os.getenv("ALLOWED_ORIGINS", ""),
        "max_requests_per_minute": os.getenv("MAX_REQUESTS_PER_MINUTE", "60"),
    }


def get_repo_root() -> Path:
    configured = settings()["repo_root"]
    repo_root = Path(configured).expanduser().resolve()
    if not repo_root.exists():
        repo_root.mkdir(parents=True, exist_ok=True)
    return repo_root
