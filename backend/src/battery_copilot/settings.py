from functools import lru_cache
from pathlib import Path
from shutil import which
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "data/sources/kit-battery"
PDF = ROOT / "data/sources/pem-module-pack-guide.pdf"
DERIVED = ROOT / "data/derived"
SNAPSHOT = "kit-v1"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env", env_file_encoding="utf-8-sig", extra="ignore"
    )
    neo4j_uri: str = "bolt://127.0.0.1:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_api_key: str = ""
    model_name: str = ""
    model_provider: Literal["openai", "codex"] = "codex"

    @property
    def model_ready(self) -> bool:
        if self.model_provider == "codex":
            return bool(which("codex") and self.model_name)
        return bool(self.openai_api_key and self.model_name)


@lru_cache
def settings() -> Settings:
    return Settings()
