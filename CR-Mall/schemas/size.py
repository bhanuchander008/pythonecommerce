from models import Sizes
from config import ma,db
from marshmallow.fields import Nested
from .product_class import Product_ClassSchema

class SizesSchema(ma.ModelSchema):
    class Meta:
        model =Sizes
        fields = ("id","size","product_id","status","created_at","updated_at")
        sqla_session = db.session

class SizesGetSchema(ma.ModelSchema):
    size_productclass = ma.Nested(Product_ClassSchema)
    class Meta:
        model = Sizes
        sqla_session = db.session
