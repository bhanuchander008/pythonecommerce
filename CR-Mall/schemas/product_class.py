from models import Product_Class
from config import ma,db
from marshmallow.fields import Nested
from .sub_categories import Sub_CategoriesSchema
from .categories import CategoriesSchema

class Product_ClassSchema(ma.ModelSchema):
    class Meta:
        model =Product_Class
        fields = ("id","name","subcategory_id","image","status","created_at","updated_at")
        sqla_session = db.session

class Product_ClassGetSchema(ma.ModelSchema):
    sub_category = ma.Nested(Sub_CategoriesSchema)
    class Meta:
        model = Product_Class
        sqla_session = db.session
