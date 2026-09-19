from app.repo_service import RepoService


def test_safe_join_rejects_escape(tmp_path):
    repo = RepoService(str(tmp_path))
    try:
        repo._safe_join("../outside.txt")
    except ValueError:
        assert True
    else:
        assert False, "Expected ValueError for path escape"


def test_write_and_read_file(tmp_path):
    repo = RepoService(str(tmp_path))
    written = repo.write_file("example.txt", "hello world")
    assert written == "example.txt"
    assert repo.read_file("example.txt") == "hello world"


def test_list_repo(tmp_path):
    repo = RepoService(str(tmp_path))
    repo.write_file("nested/alpha.txt", "alpha")
    repo.write_file("beta.txt", "beta")
    entries = repo.list_repo(".")
    assert "beta.txt" in entries
    assert "nested" in entries


def test_rejects_sensitive_and_executable_writes(tmp_path):
    repo = RepoService(str(tmp_path))
    try:
        repo.write_file(".env", "SECRET=abc")
    except ValueError:
        assert True
    else:
        assert False, "Sensitive files should be denied"

    try:
        repo.write_file("payload.exe", "MZ")
    except ValueError:
        assert True
    else:
        assert False, "Executable files should be denied"
