from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from config import *
from flask import request
from models import Sub_Categories
from schemas.sub_categories import Sub_CategoriesSchema, GetSub_CategoriesSchema
import logging, logging.config, yaml
import os

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('sub_category')

class GetActiveSubCategories(Resource):
    def __init__(self):
        pass

    # call to get the active subcategories
    def get(self):

        subcategories = db.session.query(Sub_Categories).filter(Sub_Categories.status == True).all()
        if subcategories:
            schema = GetSub_CategoriesSchema()
            data = schema.dump(subcategories,many=True).data
            logger.info("Sub-Category data fetched succesfully based on status")
            return data
        logger.warning("No sub-categorie with such status")
        return("no sub-categorie with such status")

class GetSubCategoryBy_name(Resource):
    def __init__(self):
        pass

    # call to get the subcategorie by name
    def get(self,name):
        subcategories = db.session.query(Sub_Categories).filter(Sub_Categories.name ==  name).all()
        if subcategories:
            schema = GetSub_CategoriesSchema()
            data = schema.dump(subcategories,many=True).data
            logger.info("Sub-Category data fetched succesfully based on name")
            return data
        logger.warning("No sub-categorie with such name")
        return("no sub-categorie with such name")

class GetSubCategoryByCategory(Resource):
    def __init__(self):
        pass

    # call to get the subcategorie by category
    def get(self,id):
        subcategories = db.session.query(Sub_Categories).filter(Sub_Categories.category_id == id).all()
        if subcategories:
            schema = GetSub_CategoriesSchema()
            data = schema.dump(subcategories,many=True).data
            logger.info("Sub-Category data fetched succesfully based on category")
            return data
        logger.warning("No sub-categorie with such category")
        return("no sub-categorie with such category")
