from datetime import datetime
from flask_restful import Resource
from config import db,basedir
from models import Products
from schemas.products import ProductsSchema
import logging, logging.config, yaml
import os
CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('product')

class GetActiveProducts(Resource):
    def __init__(self):
        pass

    def get(self):
        # call to get the active products
        products = db.session.query(Products).filter(Products.status == 1).all()
        if products:
            schema = ProductsSchema()
            data = schema.dump(products,many=True).data
            logger.info("Product data fetched succesfully based on status")
            return data
        logger.warning("no product with such status")
        return("no product with such status")

class GetProductsByProduct_Class(Resource):
    def __init__(self):
        pass
    def get(self,id):
        # call to get the sizes by products
        products = db.session.query(Products).filter(Products.productclass_id == id).all()
        if products:
            schema = ProductsSchema()
            data = schema.dump(products,many=True).data
            logger.info("Product data fetched succesfully based on product-class")
            return data
        logger.warning("no sizes with such product-class")
        return("no sizes with such product-class")

'''
class GetProductsBy_size(Resource):
    def __init__(self):
        pass
    def get(self,size):
        # call to get the products by name
        products = db.session.query(Products).filter(Products.size.like('%'+size+'%')).all()
        if products:
            schema = ProductsSchema()
            data = schema.dump(products,many=True).data
            return data
        return("no sizes with such size")
'''
