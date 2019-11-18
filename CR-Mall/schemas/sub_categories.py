from models import Sub_Categories
from .categories import CategoriesSchema
from config import ma,db
from marshmallow.fields import Nested

class GetSub_CategoriesSchema(ma.ModelSchema):
    categories = ma.Nested(CategoriesSchema)
    class Meta:
        model = Sub_Categories
        sqla_session = db.session

class Sub_CategoriesSchema(ma.ModelSchema):
    categories = ma.Nested(CategoriesSchema)
    class Meta:
        model = Sub_Categories
        fields = ("id","name","category_id","image","status","created_at","updated_at")
        sqla_session = db.session
