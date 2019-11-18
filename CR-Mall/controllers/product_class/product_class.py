from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from config import db,basedir
from flask import request
from models import Product_Class
from schemas.product_class import Product_ClassSchema,Product_ClassGetSchema
from exceptions import PostFailed
import os
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('product_class')

class GetUpdateDeleteProductClass(Resource):
    def __init__(self):
        pass

    # call to get the product-class based on id
    def get(self,id):
        try:
            product_class = db.session.query(Product_Class).filter(Product_Class.id == id).first()
            if product_class:
                schema = Product_ClassGetSchema()
                data = schema.dump(product_class).data
                logger.info("Product-Class data fetched succesfully based on Id")
                return data
            logger.warning("Product-Class does not exists with this id")
            return ("no data is available with this id")
        except:
            raise PostFailed("call failed")

    # call to update the product-class based on id
    def put(self,id):
        try:
            categorie = db.session.query(Product_Class).filter(Product_Class.id == id).update(request.get_json())
            if categorie:
                db.session.commit()
                obj=db.session.query(Product_Class).filter(Product_Class.id==id).one()
                schema = Product_ClassSchema()
                data = schema.dump(obj).data
                logger.info("Product-Class data updated succesfully")
                return data
            logger.warning("Product-Class does not exists with this id")
            return("Product-Class with this id is not available")
        except:
            raise PostFailed("call failed")

    # call to delete the product-class based on id
    def delete(self,id):
        try:
            obj = db.session.query(Product_Class).filter_by(id=id).one()
            if obj:
                db.session.delete(obj)
                db.session.commit()
                logger.info("Product-Class deleted succesfully")
                return("succesfully deleted the product-class")
            logger.warning("Product-Class does not exists with this id")
            return ("no product-class is found with this id")
        except:
            raise PostFailed("call failed")
class ProductClassImageUpdate(Resource):
    def __init__(self):
        pass

    # call to update the image in product-class
    def put(self,id):

        try:
            file = request.files['image']
            upload_folder = os.path.basename('/upload')
            f = os.path.join(upload_folder, file.filename)
            file.save(f)
            dit ={"image": f}
            categorie = db.session.query(Product_Class).filter_by(id = id).update(dit)
            if categorie:
                db.session.commit()
                obj=db.session.query(Product_Class).filter_by(id=id).one()
                schema = Product_ClassSchema()
                data = schema.dump(obj).data
                logger.info("Product-Class image update succesfully")
                return data
            logger.warning("Product-Class does not exists with this id")
            return("Product-Class with this id is not available")
        except:
            raise PostFailed("call failed")
