import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost/o_cerebro",
    )
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openrouter_api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")
    github_repo_url: Optional[str] = os.getenv("GITHUB_REPO_URL")
    github_token: Optional[str] = os.getenv("GITHUB_TOKEN")
    github_webhook_secret: Optional[str] = os.getenv("GITHUB_WEBHOOK_SECRET")
    github_branch: str = os.getenv("GITHUB_REPO_BRANCH", "main")
    content_cache_dir: str = os.getenv(
        "CONTENT_CACHE_DIR",
        os.path.join(os.path.dirname(__file__), "..", "..", ".content-cache"),
    )
    cors_origin: str = os.getenv("CORS_ORIGIN", "*")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    chat_model: str = os.getenv("CHAT_MODEL", "anthropic/claude-3-haiku")


settings = Settings()
