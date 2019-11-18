from models import Product_Images
from config import ma,db

class Product_ImagesSchema(ma.ModelSchema):
    class Meta:
        model = Product_Images
        fields = ("image","product_id","status","created_at","updated_at")
        sqla_session = db.session
