from datetime import datetime
from flask import make_response,abort,request
from models import Billing_info
from schemas.billing import BillingSchema
from config import *
from flask_restful import reqparse, abort, Api, Resource
from exceptions import Nodata,PostFailed
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('billing')


parser = reqparse.RequestParser()
parser.add_argument('card_type', help = 'This field is mandatory', required = True)
parser.add_argument('card_number', help = 'This field is mandatory', required = True)
parser.add_argument('name_on_card', help = 'This field is mandatory', required = True)
parser.add_argument('expire_month', help = 'This field is mandatory', required = True)
parser.add_argument('expire_year', help = 'This field is mandatory', required = True)
parser.add_argument('cvv', help = 'This field is mandatory', required = True)
#,'card_number','name_on_card','expire_month','expire_year','cvv'

class GetCreateBilling(Resource):
    def __init__(self):
        pass

    # Billing get call
    def get(self):
        size = db.session.query(Billing_info).order_by(Billing_info.id).all()
        if size:
            billing_schema = BillingSchema(many=True)
            data = billing_schema.dump(billing_schema).data
            logger.info("Billing_info data fetched succesfully ")
            return data
        else:
            logger.warning("no data is available in Billing")
            return("no data is available on Billing_info")

    # Billing post call
    def post(self):
        da = parser.parse_args()
        number = da['card_number']
        dit = {key:value for key,value in da.items()}
        existing_size = db.session.query(Billing_info).filter(Billing_info.card_number == number).first()
        if existing_size is None:
            schema = BillingSchema()
            billing = schema.load(dit, session=db.session).data
            db.session.add(billing)
            db.session.commit()
            data = schema.dump(billing).data
            logger.info("Size data added succesfully ")
            return "sucessfully added"
        else:
            logger.warning("Billing_info with this number already exist")
            return("Billing_info with this number already exist")
