from models import Orders
from config import ma,db

class OrdersSchema(ma.ModelSchema):
    class Meta:
        model =Orders
        fields = ('id','cart_id','user_id','order_status','created_at','updated_at')
        sqla_session = db.session
