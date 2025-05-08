from pathlib import Path
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session as SQLAlchemySession
from ..utils.cache import get_cache_dir
from .base import Base


def init() -> None:
    db_path: Path = get_cache_dir() / "primitive.sqlite3"

    # Drop DB existing database if it exists
    if db_path.exists():
        db_path.unlink()

    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)


def engine() -> Engine:
    db_path: Path = get_cache_dir() / "primitive.sqlite3"
    return create_engine(f"sqlite:///{db_path}", echo=False)


def Session() -> SQLAlchemySession:
    from sqlalchemy.orm import sessionmaker

    return sessionmaker(bind=engine())()
