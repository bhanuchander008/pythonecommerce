from models import Products
from config import ma,db
from marshmallow.fields import Nested
from .product_class import Product_ClassSchema

class ProductsSchema(ma.ModelSchema):
    class Meta:
        model = Products
        fields = ("id","name","productclass_id","brand",
                   "quantity_in","quantity_allocated","description",
                      "add_to_cart","status","created_at","updated_at")
        sqla_session = db.session


class ProductsGetSchema(ma.ModelSchema):
    product_class = ma.Nested(Product_ClassSchema)
    class Meta:
        model = Products
        sqla_session = db.session
