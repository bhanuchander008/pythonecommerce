from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from config import *
from flask import request
from models import Banner_images
from schemas.banner_image import BannerImageSchema, BannerImageGetSchema
import os
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('banner_image')

class GetUpdateBannerimageById(Resource):
   def __init__(self):
       pass

   def get(self,id):
       # call to get the banner image by id
       banner_images = db.session.query(Banner_images).filter_by(id = id).first()
       if banner_images:
           schema = BannerImageGetSchema()
           data = schema.dump(banner_images).data
           logger.info("banner image fetched succesfully")
           return data
       logger.warning("No images available on this id")
       return("No images available on this id")

   # call to update the banner image status based on id
   def put(self,id):
       banner_obj = db.session.query(Banner_images).filter(Banner_images.id == id).update(request.get_json())
       if banner_obj:
           db.session.commit()
           obj=db.session.query(Banner_images).filter(Banner_images.id==id).one()
           schema = BannerImageSchema()
           data = schema.dump(obj).data
           logger.info("Banner image updated succesfully")
           return data
       else:
           logger.warning("Banner image does not exists")
           return("banner image with this id is not available")

   # call to delete the banner image based on id
   def delete(self,id):
       try:
           obj = db.session.query(Banner_images).filter_by(id=id).one()
           if obj:
               db.session.delete(obj)
               db.session.commit()
               logger.info("Banner image deleted succesfully")
               return("Banner image deleted succesfully")
           else:
               logger.warning("Banner image does not exists")
               return ("Banner image does not exists")
       except:
           raise PostFailed("call failed")

class BannerImageUpdate(Resource):
    def __init__(self):
        pass

    # call to update Banner Image
    def put(self,id):
        file = request.files['image']
        upload_folder = os.path.basename('/upload')
        f = os.path.join(upload_folder, file.filename)
        file.save(f)
        dit ={"image": f}
        banner_image = db.session.query(Banner_images).filter_by(id = id).update(dit)
        if banner_image:
            db.session.commit()
            obj=db.session.query(Banner_images).filter_by(id=id).one()
            schema = BannerImageSchema()
            data = schema.dump(obj).data
            logger.info("Banner image updated succesfully")
            return data
        else:
            logger.warning("Banner image does not exists")
            return("Banner image with this id is not available")
