import shutil
import subprocess
from pathlib import Path

from settings import settings


def _build_clone_url(repo_url: str) -> str:
    if settings.github_token and repo_url.startswith("https://github.com/"):
        return repo_url.replace(
            "https://github.com/",
            f"https://x-access-token:{settings.github_token}@github.com/",
            1,
        )
    return repo_url


def ensure_content_repo() -> str:
    if not settings.github_repo_url:
        raise RuntimeError("GITHUB_REPO_URL is not configured.")

    cache_dir = Path(settings.content_cache_dir).resolve()
    cache_dir.parent.mkdir(parents=True, exist_ok=True)

    git_dir = cache_dir / ".git"
    clone_url = _build_clone_url(settings.github_repo_url)

    if not git_dir.exists():
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                settings.github_branch,
                clone_url,
                str(cache_dir),
            ],
            check=True,
        )
        return str(cache_dir)

    subprocess.run(
        ["git", "-C", str(cache_dir), "fetch", "--all", "--prune"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(cache_dir), "reset", "--hard", f"origin/{settings.github_branch}"],
        check=True,
    )
    return str(cache_dir)
