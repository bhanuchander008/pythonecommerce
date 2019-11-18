from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from config import *
from flask import request
from models import Sub_Categories
from schemas.sub_categories import Sub_CategoriesSchema, GetSub_CategoriesSchema
from exceptions import PostFailed
import os
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('sub_category')

class GetUpdateDeleteSub_Categories(Resource):
    def __init__(self):
        pass

    # call to get the categorie based on id
    def get(self,id):
        try:
            categorie = db.session.query(Sub_Categories).filter(Sub_Categories.id == id).first()
            if categorie:
                schema = GetSub_CategoriesSchema()
                data = schema.dump(categorie).data
                logger.info("Sub-Category data fetched succesfully based on Id")
                return data
            logger.warning("Sub-Category does not exists with this id")
            return ("no data is available with this id")
        except:
            raise PostFailed("call failed")

    # call to update the categorie based on id
    def put(self,id):
        try:
            categorie = db.session.query(Sub_Categories).filter(Sub_Categories.id == id).update(request.get_json())
            if categorie:
                db.session.commit()
                obj=db.session.query(Sub_Categories).filter(Sub_Categories.id==id).one()
                schema = Sub_CategoriesSchema()
                data = schema.dump(obj).data
                logger.info("Sub-Category updated succesfully")
                return data
            logger.warning("Sub-Category does not exists with this id")
            return("Sub-Categorie with this id is not available")
        except:
            raise PostFailed("call failed")

    # call to delete the categorie based on id
    def delete(self,id):
        try:
            obj = db.session.query(Sub_Categories).filter_by(id=id).one()
            if obj:
                db.session.delete(obj)
                db.session.commit()
                logger.info("Sub-Category deleted succesfully")
                return("succesfully deleted the categorie")
            logger.warning("Sub-Category does not exists with this id")
            return ("no category is found with this id")
        except:
            raise PostFailed("call failed")

class Sub_CategorieImageUpdate(Resource):
    def __init__(self):
        pass

    # call to update the image in categories
    def put(self,id):
        try:
            file = request.files['image']
            upload_folder = os.path.basename('/upload')
            f = os.path.join(upload_folder, file.filename)
            file.save(f)
            dit ={"image": f}
            categorie = db.session.query(Sub_Categories).filter_by(id = id).update(dit)
            if categorie:
                db.session.commit()
                obj=db.session.query(Sub_Categories).filter_by(id=id).one()
                schema = Sub_CategoriesSchema()
                data = schema.dump(obj).data
                logger.info("Sub-Category image updated succesfully")
                return data
            logger.warning("Sub-Category does not exists with this id")
            return("categorie with this id is not available")
        except:
            raise PostFailed("call failed")
