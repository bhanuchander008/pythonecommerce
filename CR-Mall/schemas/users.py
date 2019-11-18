from models import Users,Roles,RevokedTokenModel
from config import ma,db
from marshmallow import fields
from marshmallow.fields import Nested
from .roles import RolesGetSchema
#/home/ganesh/test/schemas/roles.py

class UsersGetSchema(ma.ModelSchema):
    Role_user = ma.Nested(RolesGetSchema)
    class Meta:
        model = Users
        sqla_session = db.session

class UsersSchema(ma.ModelSchema):
    class Meta:
        models = Users
        fields = ("id","first_name","last_name","role_id","email","phone","address","gender","status","created_at")
        sqla_session = db.session

class user_signupSchema(ma.ModelSchema):
    class Meta:
        model = Users
        fields = ("id","email","password")
        sqla_session = db.session

class Password_ResetSchema(ma.ModelSchema):
    class Meta:
        model = Users
        fields = ("password","email")
        sqla_session = db.session


class UserlogoutSchema(ma.ModelSchema):
    class Meta:
        model = RevokedTokenModel
        sqla_session = db.session
