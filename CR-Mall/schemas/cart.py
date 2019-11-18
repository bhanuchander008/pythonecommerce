from models import Cart
from config import ma,db
from marshmallow.fields import Nested
from .users import UsersSchema
from .products import ProductsSchema

class CartSchema(ma.ModelSchema):
    class Meta:
        model =Cart
        fields = ('id','user_id','product_id','category_id')
        sqla_session = db.session

class  GetCartSchema(ma.ModelSchema):
    products = ma.Nested(ProductsSchema)
    carts_u  = ma.Nested(UsersSchema)
    class Meta:
        model = Cart
        sqla_session = db.session
