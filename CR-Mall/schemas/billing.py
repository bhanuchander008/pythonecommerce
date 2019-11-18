from models import Billing_info
from config import ma,db
from marshmallow.fields import Nested

class BillingSchema(ma.ModelSchema):
    class Meta:
        model = Billing_info
        fields = ("id","user_id","cart_id","card_type","card_number","name_on_card","expire_month","expire_year","cvv","status","created_at","updated_at")
        sqla_session = db.session
