from datetime import datetime
from flask_restful import Resource
from config import *
from models import Colours
from schemas.colour import ColourSchema
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('colour')

class GetActiveColours(Resource):
    def __init__(self):
        pass

    def get(self):
        # call to get the active product_class
        colour = db.session.query(Colours).filter(Colours.status == True).all()
        if colour:
            schema = ColourSchema()
            data = schema.dump(colour,many=True).data
            logger.info("Colour data fetched succesfully based on status")
            return data
        logger.warning("No colour with such status")
        return("No colour with such status")

class GetColourByProduct(Resource):
    def __init__(self):
        pass

    # call to get the sizes by category
    def get(self,id):
        colour = db.session.query(Colours).filter(Colours.product_id == id).all()
        if colour:
            schema = ColourSchema()
            data = schema.dump(colour, many=True).data
            logger.info("Colour data fetched succesfully based on product")
            return data
        logger.warning("No colour with such product")
        return("no colour with such product")
