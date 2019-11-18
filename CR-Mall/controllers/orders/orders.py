from models import Orders
from schemas.orders import OrdersSchema
from flask import request, Flask
from flask_restful import Resource
import logging, logging.config, yaml
from config import *

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('order')

class GetDeleteOrders(Resource):
    def __init__(self):
        pass

    # call to get the orders based on id
    def get(self,id):
        order = db.session.query(Orders).filter_by(id =id).first()
        if order:
            schema = OrdersSchema()
            data = schema.dump(order).data
            logger.info("Order data fetched succesfully based on Id")
            return data
        else:
            logger.warning("No orders found based on this id")
            return("No orders found based on this id")

    #This call is user to Delete the Orders
    def delete(self,id):
        obj = db.session.query(Orders).filter_by(id = id).first()
        if obj:
            db.session.delete(obj)
            db.session.commit()
            logger.info("Order deleted succesfully")
            return ("order deleted successfully")
        else:
            logger.warning("No order is available")
            return ("No order is available")
