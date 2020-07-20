"""
Auth schema
"""
from marshmallow import Schema, fields, validate


class SignUpPostSchema(Schema):
    """
    SignupPostSchema
    """

    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=255))


class SignInPostSchema(Schema):
    """
    SigninPostSchema
    """

    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=255))
