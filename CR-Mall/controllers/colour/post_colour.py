from datetime import datetime
from flask import make_response,request
from models import Colours
from schemas.colour import ColourSchema
from config import *
from flask_restful import Api, Resource
from exceptions import Nodata,PostFailed
import boto3
import os
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('colour')

class GetCreateColours(Resource):
    def __init__(self):
        pass

    # Colour get call
    def get(self):
        try:
            role=db.session.query(Colours).order_by(Colours.id).all()
            if role:
                colour_schema = ColourSchema(many=True)
                data = colour_schema.dump(role).data
                logger.info("Colours data fetched succesfully ")
                return data
            logger.warning("no data is available on colours")
            return("no data is available on colours")
        except:
            raise Nodata("no data is available")

    # Colours post call
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
        dit = {key:value for key,value in da.items()}
        dit['image'] = url
        existing_one = db.session.query(Colours).filter(Colours.name == name).one_or_none()
        if existing_one is None:
            schema = ColourSchema()
            new_colour = schema.load(dit, session=db.session).data
            print("=========",new_colour.__dict__)
            db.session.add(new_colour)
            db.session.commit()
            data = schema.dump(new_colour).data
            logger.info("Colour data added succesfully ")
            return data
        logger.warning("Colour already exists")
        return ("Colour already exists")
