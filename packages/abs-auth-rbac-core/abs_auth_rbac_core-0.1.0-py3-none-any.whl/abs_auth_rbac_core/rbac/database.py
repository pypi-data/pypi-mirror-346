from contextlib import AbstractContextManager, contextmanager
from typing import Any, Generator
from loguru import logger

from sqlalchemy import create_engine, orm
from sqlalchemy.orm import Session
from abs_repository_core.models import BaseModel


class Database:
    def __init__(self, db_url: str) -> None:
        """
        Initialize the database engine and session factory
        """
        self._engine = create_engine(
            db_url,
            echo=False,
            echo_pool=False,
            pool_pre_ping=True,
            pool_recycle=3600,
            query_cache_size=0,
        )
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    def create_database(self) -> None:
        """
        Create all the tables in the database
        """
        BaseModel.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Generator[Any, Any, AbstractContextManager[Session]]:
        """
        Provides a database session for the request
        """
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as e:
            session.rollback()
            import traceback

            logger.error(f"Exception: {e}\n{traceback.format_exc()}")
            raise e
        finally:
            session.close()
