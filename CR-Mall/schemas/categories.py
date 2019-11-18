from models import Categories
from config import ma,db
from marshmallow.fields import Nested

class CategoriesSchema(ma.ModelSchema):
    class Meta:
        model = Categories
        fields = ("id","name","status","created_at","updated_at")
        sqla_session = db.session

class CategoryGetSchema(ma.ModelSchema):
    class Meta:
        model = Categories
        fields = ("id","name","status","created_at","updated_at")
        sqla_session = db.session
