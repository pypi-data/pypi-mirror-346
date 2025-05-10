from pathlib import Path

from loguru import logger
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session as SQLAlchemySession

from ..utils.cache import get_cache_dir
from .base import Base


def init() -> None:
    db_path: Path = get_cache_dir() / "primitive.sqlite3"

    # Drop DB existing database if it exists
    # if db_path.exists():
    #     logger.warning(f"[*] Deleting existing SQLite database at {db_path}")
    #     db_path.unlink()
    if db_path.exists():
        return

    logger.info(f"[*] Initializing SQLite database at {db_path}")
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)


def engine() -> Engine:
    db_path: Path = get_cache_dir() / "primitive.sqlite3"
    return create_engine(f"sqlite:///{db_path}", echo=False)


def Session() -> SQLAlchemySession:
    from sqlalchemy.orm import sessionmaker

    return sessionmaker(bind=engine())()
