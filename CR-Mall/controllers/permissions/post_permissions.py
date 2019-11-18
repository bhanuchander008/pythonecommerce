from datetime import datetime
from flask import make_response,abort,request
from models import Permissions
from schemas.permissions import PermissionsSchema
from config import db,basedir
from sqlalchemy import and_
from flask_restful import reqparse, abort, Api, Resource
from exceptions import Nodata,PostFailed
import logging, logging.config, yaml
import os
parser = reqparse.RequestParser()
CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('permissions')

class Getcreatepermissions(Resource):
    def __init__(self):
        pass

    # Permissions get call
    def get(self):
        permission = db.session.query(Permissions).order_by(Permissions.id).all()
        if permission:
            schema = PermissionsSchema(many=True)
            data = schema.dump(permission).data
            logger.info("Data has Fetched Successfully")
            return data
        else:
            logger.warning("No data is available on permissions")
            return("No data is available on permissions")


    # Permissions post call
    def post(self):
        da = request.get_json()
        role_id = da['role_id']
        view_name = da['view_name']
        dit = {key:value for key,value in da.items()}
        existing_role = (Permissions.query.filter(and_(Permissions.role_id == role_id,Permissions.view_name == view_name)).one_or_none())
        if existing_role is None:
            schema = PermissionsSchema()
            new_permissions = schema.load(dit, session=db.session).data
            db.session.add(new_permissions)
            db.session.commit()
            data = schema.dump(new_permissions).data
            logger.info("Data added successfully to role")
            return data, 201
        else:
            logger.warning("permission exists already ")
            return("permission exists already")
