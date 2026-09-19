from __future__ import annotations

import subprocess
from pathlib import Path

from app.config import get_repo_root


class RepoService:
    def __init__(self, repo_root: str | None = None):
        self.repo_root = Path(repo_root or get_repo_root()).resolve()
        self.repo_root.mkdir(parents=True, exist_ok=True)

    def _safe_join(self, relative_path: str) -> Path:
        candidate = (self.repo_root / relative_path).resolve()
        if self.repo_root not in candidate.parents and candidate != self.repo_root:
            raise ValueError(f"Path escapes repo root: {relative_path}")
        return candidate

    def list_repo(self, relative_path: str = ".") -> list[str]:
        base = self._safe_join(relative_path)
        if base.is_file():
            return [base.name]

        entries: list[str] = []
        for child in sorted(base.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
            rel = child.relative_to(self.repo_root).as_posix()
            entries.append(rel)
        return entries

    def read_file(self, relative_path: str) -> str:
        file_path = self._safe_join(relative_path)
        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {relative_path}")
        return file_path.read_text(encoding="utf-8")

    def write_file(self, relative_path: str, content: str, *, create_dirs: bool = True) -> str:
        file_path = self._safe_join(relative_path)
        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return file_path.relative_to(self.repo_root).as_posix()

    def get_git_status(self) -> str:
        try:
            result = subprocess.run(
                ["git", "-C", str(self.repo_root), "status", "--short"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                return result.stdout.strip() or "Working tree clean"
            return "Git status unavailable"
        except FileNotFoundError:
            return "Git is not installed or repository is not initialized"

    def get_diff_for_file(self, relative_path: str) -> str:
        file_path = self._safe_join(relative_path)
        try:
            result = subprocess.run(
                ["git", "-C", str(self.repo_root), "diff", "--", str(file_path.relative_to(self.repo_root))],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                return result.stdout.strip() or "No diff for this file"
            return "No tracked diff found"
        except FileNotFoundError:
            return "Git is not installed or repository is not initialized"
