"""
DatabaseClient
"""
import random
from contextlib import contextmanager
from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, Session


class DatabaseEngineManager:
    """
    Manage master and slave connections
    """

    masters: List[Engine] = []
    slaves: List[Engine] = []

    @staticmethod
    def create_engines(
        master_database_url: List[str], slave_database_url: Optional[List[str]] = None
    ):
        """
        Create master and slave engines
        @param master_database_url:
        @param slave_database_url:
        @return:
        """
        for url in master_database_url:
            DatabaseEngineManager.masters.append(create_engine(url, pool_pre_ping=True))
        if slave_database_url:
            for url in slave_database_url:
                DatabaseEngineManager.slaves.append(
                    create_engine(url, pool_pre_ping=True)
                )


class RoutingSession(Session):
    """
    Split read and write
    """

    def get_bind(self, mapper=None, clause=None) -> Engine:
        """
        Override to split read and write
        @param mapper:
        @param clause:
        @return:
        """
        if not self._flushing and DatabaseEngineManager.slaves:
            return DatabaseEngineManager.slaves[
                random.randrange(len(DatabaseEngineManager.slaves))
            ]
        return DatabaseEngineManager.masters[
            random.randrange(len(DatabaseEngineManager.masters))
        ]


class DatabaseClient:
    """
    DatabaseClient
    """

    def __init__(self):
        """
        Init
        """
        self.session: Session = sessionmaker(class_=RoutingSession)

    @contextmanager
    def scoped_session(self) -> Session:
        """
        Scoped session
        @return:
        """
        session = self.session()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.expunge_all()
            session.close()
