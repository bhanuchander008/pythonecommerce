from datetime import datetime
from flask import make_response,abort,request
from models import Sizes
from schemas.size import SizesSchema,SizesGetSchema
from config import basedir,db
from flask_restful import reqparse, abort, Api, Resource
from exceptions import Nodata,PostFailed
import os
parser = reqparse.RequestParser()
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('size')

class GetUpdatedeleteSizes(Resource):
    def __init__(self):
        pass

    # call to get the size based on id
    def get(self,id):
        size=db.session.query(Sizes).filter(Sizes.id==id).first()
        if size:
            size_schema = SizesGetSchema()
            data = size_schema.dump(size).data
            logger.info("Size data fetched succesfully based on Id")
            return data
        else:
            logger.warning("Size does not exists with this id")
            return ("no data is found on this id")


    # call to update the size based on id
    def put(self,id):
        try:
            obj=db.session.query(Sizes).filter(Sizes.id==id).update(request.get_json())
            if obj:
                db.session.commit()
                obj=db.session.query(Sizes).filter_by(id=id).one()
                schema = SizesSchema()
                data = schema.dump(obj).data
                logger.info("Size data updated succesfully")
                return data
            else:
                logger.warning("Size does not exists with this id")
                return ("Size does not exists with this id")
        except:
            raise PostFailed("call failed")

    # call to delete the size based on id
    def delete(self,id):
        try:
            obj=db.session.query(Sizes).filter(Sizes.id==id).first()
            if obj:
                db.session.delete(obj)
                db.session.commit()
                logger.info("Size data deleted succesfully")
                return("success")
            else:
                logger.warning("Size does not exists with this id")
                return("Size does not exists with this id")
        except:
            raise PostFailed("call failed")
