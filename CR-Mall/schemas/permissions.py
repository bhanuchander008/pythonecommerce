from models import Permissions
from config import ma,db
from marshmallow.fields import Nested
from schemas.roles import RolesSchema

class PermissionsSchema(ma.ModelSchema):
    #Permission = ma.Nested(RolesSchema)
    class Meta:
        model = Permissions
        fields = ("role_id","add","edit","read","view_name","created_at","updated_at")
        sqla_session = db.session

class PermissionsGetSchema(ma.ModelSchema):
    Role_Permissions = ma.Nested(RolesSchema)
    class Meta:
        model = Permissions
        sqla_session = db.session
