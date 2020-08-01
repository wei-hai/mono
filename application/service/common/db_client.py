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
    Manage primary and replica connections
    """

    primaries: List[Engine] = []
    replicas: List[Engine] = []

    @staticmethod
    def create_engines(
        primary_db_urls: List[str], replica_db_urls: Optional[List[str]] = None
    ):
        """
        Create primary and replica engines
        @param primary_db_urls:
        @param replica_db_urls:
        @return:
        """
        for url in primary_db_urls:
            DatabaseEngineManager.primaries.append(
                create_engine(url, pool_pre_ping=True)
            )
        if replica_db_urls:
            for url in replica_db_urls:
                DatabaseEngineManager.replicas.append(
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
        if not self._flushing and DatabaseEngineManager.replicas:
            return DatabaseEngineManager.replicas[
                random.randrange(len(DatabaseEngineManager.replicas))
            ]
        return DatabaseEngineManager.primaries[
            random.randrange(len(DatabaseEngineManager.primaries))
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
            session.close()
