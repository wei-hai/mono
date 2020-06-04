"""
Base Repository
"""
from application.service.db_client.client import DatabaseClient


class BaseRepository:
    """
    BaseRepository
    """

    def __init__(self, db_client: DatabaseClient):
        """
        Init
        @param db_client:
        """
        self.db_client = db_client
