from datetime import datetime
from flask_restful import Resource
from config import *
from models import Sizes
from schemas.size import SizesSchema

import logging, logging.config, yaml
CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('size')

class GetActiveSizes(Resource):
    def __init__(self):
        pass

    # call to get the active sizes
    def get(self):
        sizes = db.session.query(Sizes).filter(Sizes.status == True).all()
        if sizes:
            schema = SizesSchema()
            data = schema.dump(sizes,many=True).data
            logger.info("Size data fetched succesfully based on status")
            return data
        logger.warning("No sizes with such statu")
        return("No sizes with such status")

class GetSizesBy_name(Resource):
    def __init__(self):
        pass

    # call to get the sizes by name
    def get(self,size):
        sizes = db.session.query(Sizes).filter(Sizes.size == size).all()
        if sizes:
            schema = SizesSchema()
            data = schema.dump(sizes,many=True).data
            logger.info("Size data fetched succesfully based on size")
            return data
        logger.warning("No sizes with such size")
        return("no sizes with such size")

class GetSizesByProduct(Resource):
    def __init__(self):
        pass

    # call to get the sizes by category
    def get(self,id):
        sizes = db.session.query(Sizes).filter(Sizes.product_id == id).all()
        if sizes:
            schema = SizesSchema()
            data = schema.dump(sizes,many=True).data
            logger.info("Size data fetched succesfully based on products")
            return data
        logger.warning("No sizes with such product")
        return("no sizes with such product")
