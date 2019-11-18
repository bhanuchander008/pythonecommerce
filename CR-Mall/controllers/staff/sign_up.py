import jwt
from models import Staff
from schemas.staff import Staff_signupSchema,StaffSchema
from config import *
from flask import request, make_response, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash
#from mails.signupmail import SendMail
import logging, logging.config, yaml
import os
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('staff')

@jwt_required
def get(self):
    pass


class StaffSignup(Resource):
    def __init__(self):
        pass

    # SignUp call for staff
    def post(self):
        post_user = request.get_json()
        email = post_user['email']
        password = post_user['password']
        dit =  {key:value for key,value in post_user.items()}
        email_id  = db.session.query(Staff).filter(Staff.email == email).one_or_none()
        if email_id is None:
            hash_password = generate_password_hash(password)
            schema = Staff_signupSchema()
            new_signup = schema.load(dit, session = db.session).data
            new_signup.password = hash_password
            index("Staff Registration", email, "succesfully registered.")
            db.session.add(new_signup)
            db.session.commit()
            access_token = create_access_token(identity = email)
            refresh_token = create_refresh_token(identity = email)
            user_schema = StaffSchema()
            user = db.session.query(Staff).filter(Staff.email == email).one()
            data = user_schema.dump(user).data
            logger.info("Staff signed up succesfully")
            return {
                'message': 'Staff {} was created'.format(email),
                'access_token' : access_token,
                'refresh_token': refresh_token,
                'data  '       : data
                }
        else:
            logger.warning("Email already exists")
            return ("Email already exists")
