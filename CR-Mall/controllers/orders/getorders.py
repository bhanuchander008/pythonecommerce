from models import Orders
from schemas.orders import OrdersSchema
from flask import request, Flask
from flask_restful import Resource
import logging, logging.config, yaml
from config import *

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('order')

class GetOrderByUser(Resource):
    def __init__(self):
        pass

    # call to get the orders based on user id
    def get(self,id):
        order = db.session.query(Orders).filter_by(user_id=id).all()
        if order:
            schema = OrdersSchema(many = True)
            data = schema.dump(order).data
            logger.info("Order data fetched succesfully based on User")
            return data
        else:
            logger.warning("No orders found based on this user id")
            return("No orders found based on this user id")

class GetOrderByCart(Resource):
    def __init__(self):
        pass

    # call to get the orders based on cart id
    def get(self,id):
        order = db.session.query(Orders).filter_by(cart_id=id).one()
        if order:
            schema = OrdersSchema()
            data = schema.dump(order).data
            logger.info("Order data fetched succesfully based on Cart")
            return data
        else:
            logger.warning("No orders found based on this cart id")
            return("No orders found based on this cart id")


class GetOrderByStatus(Resource):
    def __init__(self):
        pass

    # call to get the orders based on status
    def get(self,status):
        order = db.session.query(Orders).filter_by(order_status = status).all()
        if order:
            schema = OrdersSchema(many = True)
            data = schema.dump(order).data
            logger.info("Order data fetched succesfully based on status")
            return data
        else:
            logger.warning("No orders found based on this status")
            return("No orders found based on this status")
