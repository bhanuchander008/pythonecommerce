from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from config import db,basedir
from flask import request
from models import Products
from schemas.products import ProductsSchema,ProductsGetSchema
from exceptions import PostFailed
import os
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('product')

class GetUpdateDeleteProducts(Resource):
    def __init__(self):
        pass

    # call to get the products based on id
    def get(self,id):
        try:
            products = db.session.query(Products).filter(Products.id == id).first()
            if products:
                schema = ProductsGetSchema()
                data = schema.dump(products).data
                logger.info("Product data fetched succesfully based on Id")
                return data
            logger.warning("product does not exists with this id")
            return ("no data is available with this id")
        except:
            raise PostFailed("call failed")

    # call to update the producta based on id
    def put(self,id):
        product = db.session.query(Products).filter(Products.id == id).update(request.get_json())
        if product:
            db.session.commit()
            obj=db.session.query(Products).filter(Products.id==id).one()
            schema = ProductsGetSchema()
            data = schema.dump(obj).data
            logger.info("Product data updated succesfully")
            return data
        logger.warning("product does not exists with this id")
        return("product with this id is not available")


    # call to delete the product based on id
    def delete(self,id):
        try:
            obj = db.session.query(Products).filter_by(id=id).one()
            if obj:
                db.session.delete(obj)
                db.session.commit()
                logger.info("Product deleted succesfully")
                return("succesfully deleted the product")
            logger.warning("product does not exists with this id")
            return ("no product is found with this id")
        except:
            raise PostFailed("call failed")

'''
class ImageUpdateInProducts(Resource):
    def __init__(self):
        pass

    # call to update the image in products
    def put(self,id):
            file = request.files['image']
            upload_folder = os.path.basename('/home/ganesh/test/upload_folder')
            f = os.path.join(upload_folder, file.filename)
            file.save(f)

            dit ={"image": f}
            product = db.session.query(Products).filter_by(id = id).update(dit)
            if product:
                db.session.commit()
                obj=db.session.query(Products).filter_by(id=id).one()
                schema = ProductsGetSchema()
                data = schema.dump(obj).data
                logger.info("Product image updated succesfully")
                return data
            logger.warning("product does not exists with this id")
            return("products with this id is not available")
        except:
            raise PostFailed("call failed")
'''
