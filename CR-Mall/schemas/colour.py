from models import Colours
from config import ma, db

class ColourSchema(ma.ModelSchema):
    class Meta:
        model = Colours
        fields = ("name","product_id","image","status","created_at","updated_at")
        sqla_session = db.session

class UpdateColourSchema(ma.ModelSchema):
    class Meta:
        model = Colours
        sqla_session = db.session
