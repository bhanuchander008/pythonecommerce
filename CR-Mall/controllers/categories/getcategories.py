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

class GetActiveCategories(Resource):
    def __init__(self):
        pass

    # call to get the active categories
    def get(self):
        categories = db.session.query(Categories).filter(Categories.status == True).all()
        if categories:
            schema = CategoryGetSchema()
            data = schema.dump(categories,many=True).data
            logger.info("Category data fetched succesfully based on status")
            return data
        else:
            logger.warning("no category with such status")
            return("no category with such status")


class GetCategorieBy_name(Resource):
    def __init__(self):
        pass

    # call to get the categorie by name
    def get(self,name):
        categories = db.session.query(Categories).filter(Categories.name == name).all()
        if categories:
            schema = CategoryGetSchema()
            data = schema.dump(categories,many=True).data
            logger.info("Category data fetched succesfully based on name")
            return data
        else:
            logger.warning("no category with such name")
            return("no category with such name")
