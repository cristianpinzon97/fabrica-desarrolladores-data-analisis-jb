import os


def _default_sqlite_url() -> str:
    # Default SQLite database file in working directory
    return os.getenv("SQLITE_PATH", "sqlite:///app.db")


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-too")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", _default_sqlite_url())
    SQLALCHEMY_TRACK_MODIFICATIONS = False
