from models import Staff,Roles
from config import ma,db
from marshmallow import fields
from marshmallow.fields import Nested
from .roles import RolesSchema

class StaffGetSchema(ma.ModelSchema):
    role= ma.Nested(RolesSchema)
    class Meta:
        model =Staff
        sqla_session = db.session

class StaffSchema(ma.ModelSchema):
    class Meta:
        models = Staff
        fields = ("id","first_name","last_name","role_id","email","phone","address","gender","status","created_at")
        sqla_session = db.session

class Staff_signupSchema(ma.ModelSchema):
    class Meta:
        model = Staff
        fields = ("id","email","password")
        sqla_session = db.session

class Password_ResetSchema(ma.ModelSchema):
    class Meta:
        model = Staff
        fields = ("password",)
        sqla_session = db.session
