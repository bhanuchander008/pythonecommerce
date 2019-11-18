from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from config import db,basedir
from flask import request
from models import Products
from schemas.products import ProductsSchema
from exceptions import PostFailed
import os
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('product')

class GetcreateProducts(Resource):
    def __init__(self):
        pass

    # call to get  all the data from model Product
    def get(self):
        try:
            product = db.session.query(Products).order_by(Products.id).all()
            if product:
                schema = ProductsSchema(many = True)
                data  = schema.dump(product).data
                logger.info("Product data fetched succesfully ")
                return data
            logger.warning("no data is available in products")
            return("no data is available in products")
        except:
            raise PostFailed("call failed")

    # call to add the data to Product_Class
    def post(self):
        try:
            da = request.get_json()
            name = da['name']
            dit ={key:value for key,value in da.items()}
            existing_one = db.session.query(Products).filter(Products.name == name).one_or_none()
            if existing_one is None:
                schema = ProductsSchema()
                new_product = schema.load(dit,session=db.session,partial=True).data
                db.session.add(new_product)
                db.session.commit()
                data = schema.dump(new_product).data
                logger.info("Product data added succesfully ")
                return data
            logger.warning("product name already exists")
            return ("product name already exists")
        except:
            raise PostFailed("call failed")
