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
    }


def get_repo_root() -> Path:
    root = Path(settings()["repo_root"]).resolve()
    return root
