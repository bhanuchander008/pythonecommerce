from models import Users
from schemas.users import UsersSchema,UsersGetSchema
from config import *
from flask_restful import Resource, reqparse
from flask import request
import logging, logging.config, yaml
from flask_jwt_extended import jwt_required
import os

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('users')

parser = reqparse.RequestParser()
parser.add_argument('first_name', help = 'This field is mandatory', required = True)
parser.add_argument('last_name', help = 'This field is mandatory', required = True)
parser.add_argument('phone', help = 'This field is mandatory', required = True)
parser.add_argument('gender', help = 'This field is mandatory', required = True)

class GetUsers(Resource):
    def __init__(self):
        pass

    # call to get all the user details
    def get(self):
        user = Users.query.order_by(Users.id).all()
        if user:
            user_schema = UsersGetSchema(many = True)
            data = user_schema.dump(user).data
            logger.info("User data fetched succesfully based on id")
            return data
        else:
            logger.warning("Data Not Found.")
            return ("Data Not Found.")

class GetUpdateUser(Resource):
    def __init__(self):
        pass

    # call to get the user details based on user_id
    def get(self,id):
        user = db.session.query(Users).filter(Users.id == id).one_or_none()
        if user is not None:
            user_schema = UsersGetSchema()
            data = user_schema.dump(user).data
            logger.info("User data fetched succesfully based on Id")
            return data
        else:
            logger.warning("User does not exists")
            return ("User does not exists")

    # call to update the user details based on user_id
    @jwt_required
    def put(self,id):
        data = request.get_json()
        user = db.session.query(Users).filter_by(id = id).update(data)
        if user:
            db.session.commit()
            user_obj = Users.query.filter(Users.id == id).one()
            user_schema = UsersSchema()
            data = user_schema.dump(user_obj).data
            logger.info("User updated succesfully")
            return data
        else:
            logger.warning("User does not exists")
            return ("User does not exists")

class ActiveUsers(Resource):
    def __init__(self):
        pass

    # call to get the users with active status
    def get(self):
        users = db.session.query(Users).filter(Users.status == True).all()
        print("users",users)
        if users:
            schema = UsersSchema()
            data = schema.dump(users,many=True).data
            logger.info("User fetched succesfully based on status")
            return data
        else:
            logger.warning("no users found with these status")
            return("no users found with these status")
