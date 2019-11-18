from datetime import datetime
from flask_restful import Resource
from config import db,basedir
from models import Product_Class
from schemas.product_class import Product_ClassSchema,Product_ClassGetSchema
import logging, logging.config, yaml
import os

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('product_class')

class GetActiveProductClass(Resource):
    def __init__(self):
        pass

    # call to get the active product-class
    def get(self):
        product_class = db.session.query(Product_Class).filter(Product_Class.status == True).all()
        if product_class:
            schema = Product_ClassSchema()
            data = schema.dump(product_class,many=True).data
            logger.info("Product-Class data fetched succesfully based on status")
            return data
        logger.warning("Product-Class does not exists with this status")
        return("no product_class with such status")

class GetProductClassBy_name(Resource):
    def __init__(self):
        pass

    # call to get the product-class by name
    def get(self,name):
        product_class = db.session.query(Product_Class).filter(Product_Class.name.like('%'+name+'%')).all()
        if product_class:
            schema = Product_ClassSchema()
            data = schema.dump(product_class,many=True).data
            logger.info("Product-Class data fetched succesfully based on name")
            return data
        logger.warning("Product-Class does not exists with this name")
        return("no subcategorie with such name")

class GetProductClassBySubCategory(Resource):
    def __init__(self):
        pass

    # call to get the product-class by category
    def get(self,id):
        product_class = db.session.query(Product_Class).filter(Product_Class.subcategory_id == id).all()
        if product_class:
            schema = Product_ClassSchema()
            data = schema.dump(product_class,many=True).data
            logger.info("Product-Class data fetched succesfully based on SubCategory")
            return data
        logger.warning("Product-Class does not exists with this SubCategory")
        return("no product_class with such SubCategory")
