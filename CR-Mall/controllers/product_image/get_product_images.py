from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from config import db,basedir
from flask import request
from models import Product_Images
from schemas.product_image import Product_ImagesSchema
import os
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('product_image')

class GetActiveProductImages(Resource):
    def __init__(self):
        pass

    def get(self):
        # call to get the active product_class
        product_images = db.session.query(Product_Images).filter(Product_Images.status == True).all()
        if product_images:
            schema = Product_ImagesSchema()
            data = schema.dump(product_images,many=True).data
            logger.info("product image fetched succesfully based on status")
            return data
        else:
            logger.warning("no product_image with such status")
            return("no product image with such status")

class GetProductImageByProduct(Resource):
    def __init__(self):
        pass

    def get(self,id):
        # call to get the product_image by product
        product = db.session.query(Product_Images).filter(Product_Images.product_id == id).all()
        if product:
            schema = Product_ImagesSchema()
            data = schema.dump(product,many=True).data
            logger.info("product image fetched succesfully based on product")
            return data
        else:
            logger.warning("no product images  with such product")
            return("no product images  with such product")
