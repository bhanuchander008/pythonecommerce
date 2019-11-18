from models import Staff
from schemas.staff import Staff_signupSchema
from flask_restful import Resource
from config import *
from flask import request,session
from werkzeug.security import check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
import logging, logging.config, yaml
import os
CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('staff')

@jwt_required
def get(self):
    pass

class StaffSignin(Resource):
    def __init__(self):
        pass

    # login call for the staff
    def post(self):
        sign_in = request.get_json()
        email_id = sign_in['email']
        password = sign_in['password']
        email_check = Staff.query.filter(Staff.email == email_id).one_or_none()
        status = email_check.status
        if status == True:
            if email_check is not None:
                schema = Staff_signupSchema()
                hashed_password = email_check.password
                if check_password_hash(hashed_password,password):
                    session[email_id] = True
                    access_token = create_access_token(identity = email_id)
                    refresh_token = create_refresh_token(identity = email_id)
                    logger.info("Staff loged in succesfully")
                    return {
                        'message': 'logined successfully',
                        'access_token': access_token,
                        'refresh_token': refresh_token
                        }
                else:
                    logger.warning("Invalid Password")
                    return "Invalid Password"
            else:
                logger.warning("Invalid Username")
                return "Invalid UserName"
        else:
            logger.warning("Your account is deactivated")
            return "Your account is deactivated"
