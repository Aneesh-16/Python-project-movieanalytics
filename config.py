"""Configuration. Secrets come from environment variables (or a local .env file that is never committed)."""
import logging
import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _load_env_file(path: Path) -> None:
    """Tiny .env reader. Real environment variables always win (setdefault)."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file(BASE_DIR / ".env")


def _normalize_db_url(url: str) -> str:
    """Accept Supabase/Render style postgres:// URLs and select the psycopg2 driver."""
    import urllib.parse
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if url.startswith("postgresql://") and not url.startswith("postgresql+"):
        url = "postgresql+psycopg2://" + url[len("postgresql://"):]

    # Safely handle passwords containing @ or special characters
    if "://" in url and url.count("@") > 1:
        scheme, rest = url.split("://", 1)
        last_at = rest.rfind("@")
        user_pwd = rest[:last_at]
        host_db = rest[last_at + 1:]
        if ":" in user_pwd:
            user, pwd = user_pwd.split(":", 1)
            url = f"{scheme}://{user}:{urllib.parse.quote_plus(pwd)}@{host_db}"
    return url


# Local development default: a SQLite file. Production/demo: your Supabase PostgreSQL URL.
raw_db = os.environ.get("DATABASE_URL")
if not raw_db or "YOUR-DB-PASSWORD" in raw_db or "PROJECTREF" in raw_db or "YOUR-PASSWORD" in raw_db:
    raw_db = f"sqlite:///{(BASE_DIR / 'local_dev.db').as_posix()}"
DATABASE_URL = _normalize_db_url(raw_db)

SECRET_KEY = os.environ.get("SECRET_KEY", "")
if not SECRET_KEY:
    SECRET_KEY = secrets.token_hex(32)   # fine for one local process; set SECRET_KEY on the server
    logging.getLogger("movie_analytics").warning("SECRET_KEY not set: using a random key (logins reset on restart).")
TOKEN_TTL_SECONDS = int(os.environ.get("TOKEN_TTL_SECONDS", 8 * 3600))
# Local SQLite dev: allow any origin. Hosted PostgreSQL: allow origins specified or wildcard for demo.
_default_cors = "*"
CORS_ORIGINS = [o.strip() for o in os.environ.get("CORS_ORIGINS", _default_cors).split(",") if o.strip()]
API_BASE_URL = os.environ.get("API_BASE_URL", "")   # documentation only: your deployed URL
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "8265bd1679663a7ea12ac168da84d2e8")

DATA_DIR = BASE_DIR / "data"
MOVIES_CSV = DATA_DIR / "tmdb_5000_movies.csv"
CREDITS_CSV = DATA_DIR / "tmdb_5000_credits.csv"

DATASET_NAME = "TMDB 5000 Movie Dataset"
CURRENCY_NOTE = "USD, nominal values as recorded in the dataset"
DEFAULT_MIN_VOTES = 500
ROI_MIN_BUDGET = 1_000_000
MAX_LIMIT = 100
