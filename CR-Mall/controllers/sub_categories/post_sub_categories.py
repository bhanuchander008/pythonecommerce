from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from config import *
from flask import request
from models import Sub_Categories
from schemas.sub_categories import Sub_CategoriesSchema, GetSub_CategoriesSchema
from exceptions import PostFailed
import os
import boto3
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('sub_category')

class GetCreateSubCategories(Resource):
    def __init__(self):
        pass

    # call to get all the categories
    def get(self):
        try:
            categorie = db.session.query(Sub_Categories).order_by(Sub_Categories.id).all()
            if categorie:
                schema = GetSub_CategoriesSchema(many = True)
                data = schema.dump(categorie).data
                logger.info("Sub-Category data fetched succesfully ")
                return data
            logger.warning("no data is available in sub-categories")
            return("No data is available in sub-categories")
        except:
            raise PostFailed("call failed due to some reasons")

    # call to post the categorie details
    def post(self):
        file = request.files['image']
        upload_folder = os.path.basename('/sub_category')
        f = os.path.join(upload_folder, file.filename)
        file.save(f)
        s3 = boto3.client('s3')
        url = "{}/{}/{}".format(s3.meta.endpoint_url,'prasanth-mall',f)
        s3.upload_file(f,'prasanth-mall',f)
        da = request.form
        name = da['name']
        dit = {key:value for key,value in da.items()}
        dit['image'] = url
        existing_one = db.session.query(Sub_Categories).filter(Sub_Categories.name == name).one_or_none()
        if existing_one is None:
            schema = Sub_CategoriesSchema()
            new_categorie = schema.load(dit, session=db.session,partial=True).data
            db.session.add(new_categorie)
            db.session.commit()
            data = schema.dump(new_categorie).data
            logger.info("Sub-Category data added succesfully ")
            return data
        logger.warning("Sub-Categorie with this name already exists")
        return ("Sub-Categorie with this name already exists")
