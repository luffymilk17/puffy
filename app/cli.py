from __future__ import annotations

import argparse
import json

from app.agent import RepoAgent
from app.repo_service import RepoService


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Puffy repo-aware coding assistant CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List repository entries")
    list_parser.add_argument("path", nargs="?", default=".")

    read_parser = subparsers.add_parser("read", help="Read a file from the repo")
    read_parser.add_argument("path")

    write_parser = subparsers.add_parser("write", help="Write a file inside the repo")
    write_parser.add_argument("path")
    write_parser.add_argument("content")

    status_parser = subparsers.add_parser("status", help="Show git status")

    diff_parser = subparsers.add_parser("diff", help="Show git diff for a file")
    diff_parser.add_argument("path")

    task_parser = subparsers.add_parser("task", help="Ask the agent to propose a plan")
    task_parser.add_argument("task")
    task_parser.add_argument("--repo-path", default=".")

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    repo = RepoService()

    if args.command == "list":
        print(json.dumps(repo.list_repo(args.path), indent=2))
    elif args.command == "read":
        print(repo.read_file(args.path))
    elif args.command == "write":
        print(repo.write_file(args.path, args.content))
    elif args.command == "status":
        print(repo.get_git_status())
    elif args.command == "diff":
        print(repo.get_diff_for_file(args.path))
    elif args.command == "task":
        agent = RepoAgent()
        result = agent.run(args.task, repo_path=args.repo_path)
        print(json.dumps({"summary": result.summary, "plan": result.plan}, indent=2))


if __name__ == "__main__":
    main()
