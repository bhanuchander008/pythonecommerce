from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from config import db,basedir
from flask import request
from models import Product_Class
from schemas.product_class import Product_ClassSchema
from exceptions import PostFailed
import os
import boto3
import logging, logging.config, yaml
CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('product_class')


class GetCreateProductClass(Resource):
    def __init__(self):
        pass

    # call to get  all the data from model Product_Class
    def get(self):
        try:
            product = db.session.query(Product_Class).order_by(Product_Class.id).all()
            if product:
                schema = Product_ClassSchema(many = True)
                data  = schema.dump(product).data
                logger.info("Product Class data fetched succesfully ")
                return data
            logger.warning("no data is available in product class")
            return("no data is available")
        except:
            raise PostFailed("call failed")

    # call to add the data to Product_Class
    def post(self):
        file = request.files['image']
        upload_folder = os.path.basename('/upload')
        f = os.path.join(upload_folder, file.filename)
        file.save(f)
        s3 = boto3.client('s3')
        url = "{}/{}/{}".format(s3.meta.endpoint_url,'prasanth-mall',f)
        s3.upload_file(f,'prasanth-mall',f)
        da = request.form
        name = da['name']
        dit ={key:value for key,value in da.items()}
        dit['image'] = url
        existing_one = db.session.query(Product_Class).filter(Product_Class.name == name).one_or_none()
        if existing_one is None:
            schema = Product_ClassSchema()
            new_product_class = schema.load(dit,session=db.session).data
            db.session.add(new_product_class)
            db.session.commit()
            data = schema.dump(new_product_class).data
            logger.info("Product class data added succesfully ")
            return data
        logger.warning("Product-Class with this name already exists")
        return ("product_class with this already exists")
