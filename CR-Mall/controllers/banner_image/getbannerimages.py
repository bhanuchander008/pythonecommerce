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



class GetActiveBannerImages(Resource):
    def __init__(self):
        pass

    # call to get the active banner images
    def get(self):
        banner_image = db.session.query(Banner_images).filter(Banner_images.status == True).all()
        if banner_image:
            schema = BannerImageGetSchema()
            data = schema.dump(banner_image,many=True).data
            logger.info("banner image data fetched succesfully based on status")
            return data
        else:
            logger.warning("no banner image with such status")
            return("no banner image with such status")
