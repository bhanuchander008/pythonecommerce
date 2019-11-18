from datetime import datetime
from flask import make_response,abort,request
from models import Sizes
from schemas.size import SizesSchema,SizesGetSchema
from sqlalchemy import and_
from config import *
from flask_restful import reqparse, abort, Api, Resource
from exceptions import Nodata,PostFailed
parser = reqparse.RequestParser()
import logging, logging.config, yaml
CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('size')

class GetcreateSizes(Resource):
    def __init__(self):
        pass

    # Sizes get call
    def get(self):
        try:
            size = db.session.query(Sizes).order_by(Sizes.id).all()
            if size:
                size_schema = SizesSchema(many=True)
                data = size_schema.dump(size).data
                logger.info("Sizes data fetched succesfully ")
                return data
            else:
                logger.warning("no data is available in sizes")
                return("no data is available on sizes")
        except:
            raise Nodata("no data is available")

    # Sizes post call
    def post(self):
        da = request.get_json()
        size = da['size']
        product_id = da['product_id']
        dit = {key:value for key,value in da.items()}
        existing_size = db.session.query(Sizes).filter(and_(Sizes.product_id == product_id, Sizes.size == size)).first()
        if existing_size is None:
            schema = SizesSchema()
            new_size = schema.load(dit, session=db.session).data
            db.session.add(new_size)
            db.session.commit()
            data = schema.dump(new_size).data
            logger.info("Size data added succesfully ")
            return data, 201
        else:
            logger.warning("size with this product already exist")
            return("size with this product already exist")
