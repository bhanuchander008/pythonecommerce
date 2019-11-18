from models import Banner_images
from config import ma,db
from marshmallow.fields import Nested

class BannerImageSchema(ma.ModelSchema):
    class Meta:
        model = Banner_images
        fields = ("id","image","status","created_at","updated_at")
        sqla_session = db.session

class BannerImageGetSchema(ma.ModelSchema):
    class Meta:
        model = Banner_images
        sqla_session = db.session
