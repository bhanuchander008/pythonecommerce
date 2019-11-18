from models import Users, RevokedTokenModel
from schemas.users import user_signupSchema, UserlogoutSchema
from flask_restful import Resource
from config import *
from flask import request,session
from werkzeug.security import check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import os
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('users')

class SecretResource(Resource):
    @jwt_required
    def get(self):
        return ("success")

class Signin(Resource):
    def __init__(self):
        pass

    # login call for the user
    def post(self):
        sign_in = request.get_json()
        email_id = sign_in['email']
        password = sign_in['password']
        email_check = db.session.query(Users).filter(Users.email == email_id).first()
        print("============",email_check)
        if email_check is not None:
            schema = user_signupSchema()
            hashed_password = email_check.password
            if check_password_hash(hashed_password,password):
                status = email_check.status
                if status == True:
                    session[email_id] = True
                    access_token = create_access_token(identity = email_id)
                    refresh_token = create_refresh_token(identity = email_id)
                    logger.info("User loged in succesfully")
                    return {
                        'message': 'logined successfully',
                        'access_token': access_token,
                        'refresh_token': refresh_token
                        }
                else:
                    logger.warning("Your account is deactivated")
                    return "Your account is deactivated"
            else:
                logger.warning("Invalid Password")
                return "Invalid Password"
        else:
            logger.warning("Invalid Username")
            return "Invalid UserName"

class UserLogoutAccess(Resource):
   @jwt_required
   def post(self):
       jti = get_raw_jwt()['jti']

       revoked_token = RevokedTokenModel(jti = jti)
       revoked_token.add()
       return {'message': 'Access token has been revoked'}



class UserLogoutRefresh(Resource):
   @jwt_refresh_token_required
   def post(self):
       jti = get_raw_jwt()['jti']
       revoked_token = RevokedTokenModel(jti = jti)
       revoked_token.add()
       return {'message': 'Refresh token has been revoked'}
