"""
UserRepository
"""
from crypt import METHOD_SHA256, crypt, mksalt
from typing import Dict, Optional

from marshmallow_sqlalchemy import ModelSchema

from application.model.role import Role
from application.model.user import User
from application.repository.base import BaseRepository


class UserSchema(ModelSchema):
    """
    UserSchema
    """

    class Meta:
        """
        Meta
        """

        model = User
        fields = ("id", "email")


class UserRepository(BaseRepository):
    """
    UserRepository
    """

    def create(self, email: str, password: str) -> Optional[Dict[str, str]]:
        """
        Create user
        @param email:
        @param password:
        @return:
        """
        salt: str = mksalt(METHOD_SHA256)
        with self.db_client.scoped_session() as session:
            role = session.query(Role).filter(Role.name == "user").first()
            user = User(
                email=email, password=crypt(password, salt), salt=salt, role_id=role.id
            )
            session.add(user)
            session.commit()
            return UserSchema().dump(user)

    def find_by_email(self, email) -> Optional[Dict[str, str]]:
        """
        Find user by email
        @param email:
        @return:
        """
        with self.db_client.scoped_session() as session:
            user = session.query(User).filter(User.email == email).first()
            if not user:
                return None
            return UserSchema().dump(user)

    def find_by_email_password(
        self, email: str, password: str
    ) -> Optional[Dict[str, str]]:
        """
        Find user by email and password
        @param email:
        @param password:
        @return:
        """
        with self.db_client.scoped_session() as session:
            user = session.query(User).filter(User.email == email).first()
            if not user:
                return None
            if crypt(password, user.salt) == user.password:
                return UserSchema().dump(user)
            return None
