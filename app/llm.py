from __future__ import annotations

from typing import Any

from openai import OpenAI

from app.config import settings


class LLMClient:
    def __init__(self):
        cfg = settings()
        self.client = OpenAI(api_key=cfg["openai_api_key"], base_url=cfg["openai_base_url"])
        self.model = cfg["model"]

    def ask(self, prompt: str, *, system_prompt: str | None = None) -> str:
        if not settings()["openai_api_key"]:
            return "OpenAI API key is not configured. Set OPENAI_API_KEY in the environment before using the LLM feature."

        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content or ""


def build_repo_context(repo_service: Any) -> str:
    entries = repo_service.list_repo(".")
    return "Repository entries:\n" + "\n".join(f"- {entry}" for entry in entries[:200])
