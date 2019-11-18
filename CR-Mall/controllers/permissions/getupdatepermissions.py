from datetime import datetime
from flask_restful import reqparse, abort, Api, Resource
from config import db,basedir
from flask import request
from models import Permissions
from schemas.permissions import PermissionsSchema, PermissionsGetSchema
from exceptions import PostFailed
import os
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('permissions')

class GetUpdatePermissions(Resource):
    def __init__(self):
        pass

    # call to get the permissions based on id
    def get(self,id):
        try:
            permission = db.session.query(Permissions).filter(Permissions.id == id).first()
            if permission:
                schema = PermissionsGetSchema()
                data = schema.dump(permission).data
                logger.info("permission data fetched succesfully based on Id")
                return data
            logger.warning("permission does not exists with this id")
            return ("no data is available with this id")
        except:
            raise PostFailed("call failed")

    # call to update the permissions based on id
    def put(self,id):
        permission = db.session.query(Permissions).filter(Permissions.id == id).update(request.get_json())
        if permission:
            db.session.commit()
            obj=db.session.query(Permissions).filter(Permissions.id==id).one()
            schema = PermissionsSchema()
            data = schema.dump(obj).data
            logger.info("Permission data updated succesfully")
            return data
        logger.warning("Permission does not exists with this id")
        return("Permission with this id is not available")
