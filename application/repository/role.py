"""
UserRepository
"""
from typing import Dict, Optional

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from application.model.role import Role
from application.model.user import User
from application.repository.base import BaseRepository


class RoleSchema(SQLAlchemyAutoSchema):
    """
    RoleSchema
    """

    class Meta:
        """
        Meta
        """

        model = Role
        fields = ("id", "name")


class RoleRepository(BaseRepository):
    """
    RoleRepository
    """

    def find_by_user_id(self, user_id: int) -> Optional[Dict[str, str]]:
        """
        Find role by user id
        @param user_id:
        @return:
        """
        with self.db_client.scoped_session() as session:
            role = (
                session.query(Role)
                .join(User, Role.id == User.role_id)
                .filter(User.id == user_id)
                .first()
            )
            if not role:
                return None
            return RoleSchema().dump(role)
