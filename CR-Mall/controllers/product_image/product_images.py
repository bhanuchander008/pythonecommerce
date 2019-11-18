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

class GetUpdateProductimageById(Resource):
   def __init__(self):
       pass

   def get(self,id):
       # call to get the product image by id
       product_images = db.session.query(Product_Images).filter_by(id = id).first()
       if product_images:
           schema = Product_ImagesSchema()
           data = schema.dump(product_images).data
           logger.info("product image fetched succesfully")
           return data
       logger.warning("No images available on this id")
       return("No images available on this id")

   def put(self,id):
       # call to update the product image based on id
       file = request.files['image']
       upload_folder = os.path.basename('/upload')
       f = os.path.join(upload_folder, file.filename)
       file.save(f)
       da = request.form
       dit ={key:value for key,value in da.items()}
       dit['image'] = f
       product_images = db.session.query(Product_Images).filter_by(id = id).update(dit)
       if product_images:
           db.session.commit()
           obj=db.session.query(Product_Images).filter_by(id=id).one()
           schema = Product_ImagesSchema()
           data = schema.dump(obj).data
           logger.info("product image updated succesfully")
           return data
       logger.warning("product_image  with this id is not available")
       return("product_image  with this id is not available")
