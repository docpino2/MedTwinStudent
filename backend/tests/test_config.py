from app.core.config import normalize_database_url


def test_normalize_render_postgres_url_to_psycopg() -> None:
    assert (
        normalize_database_url("postgresql://user:pass@host:5432/db")
        == "postgresql+psycopg://user:pass@host:5432/db"
    )


def test_normalize_render_postgres_url_with_driver_typo() -> None:
    assert (
        normalize_database_url(" postgresql +psycopg://user:pass@host:5432/db ")
        == "postgresql+psycopg://user:pass@host:5432/db"
    )
