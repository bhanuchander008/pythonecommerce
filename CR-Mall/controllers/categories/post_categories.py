from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from config import *
from flask import request
from models import Categories
from schemas.categories import CategoriesSchema, CategoryGetSchema
from exceptions import PostFailed
import os
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('category')


class GetcreateCategories(Resource):
    def __init__(self):
        pass

    # call to get all the categories
    def get(self):
        category = db.session.query(Categories).order_by(Categories.id).all()
        if category:
            schema = CategoryGetSchema(many = True)
            data = schema.dump(category).data
            logger.info("Category data fetched succesfully ")
            return data
        else:
            logger.warning("no data is available in categories")
            return("no data is available in categories")

    #call to post the categorie details
    def post(self):
        '''
        file = request.files['image']
        upload_folder = os.path.basename('/upload')
        f = os.path.join(upload_folder, file.filename)
        file.save(f)
        '''
        da = request.get_json()
        name = da['name']
        dit = {key:value for key,value in da.items()}
        #dit['image'] = f
        existing_one = db.session.query(Categories).filter(Categories.name == name).one_or_none()
        if existing_one is None:
            schema = CategoriesSchema()
            new_categorie = schema.load(dit, session=db.session).data
            db.session.add(new_categorie)
            db.session.commit()
            data = schema.dump(new_categorie).data
            logger.info("Category data added succesfully")
            return data
        else:
            logger.warning("categorie with this name already exists")
            return ("categorie with this name already exists")
