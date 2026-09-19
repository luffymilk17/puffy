from __future__ import annotations

from dataclasses import dataclass

from app.llm import LLMClient, build_repo_context
from app.repo_service import RepoService


@dataclass
class AgentResult:
    summary: str
    plan: list[str]


class RepoAgent:
    def __init__(self, repo_root: str | None = None):
        self.repo = RepoService(repo_root)
        self.llm = LLMClient()

    def run(self, task: str, *, repo_path: str = ".") -> AgentResult:
        target = repo_path if repo_path != "." else "."
        repo_context = self.repo.list_repo(target)
        context = build_repo_context(self.repo)
        prompt = (
            f"Task: {task}\n\n"
            f"Target path: {target}\n\n"
            f"Repository snapshot:\n{context}\n\n"
            f"Current directory contents:\n{chr(10).join(f'- {item}' for item in repo_context[:200])}"
        )
        system_prompt = (
            "You are a repo-aware coding assistant. Provide a concise action plan for the task, "
            "mention likely files to inspect, and keep the response structured and safe."
        )
        answer = self.llm.ask(prompt, system_prompt=system_prompt)
        lines = [line.strip() for line in answer.splitlines() if line.strip()]
        return AgentResult(summary=answer, plan=lines or ["No additional plan generated"])
