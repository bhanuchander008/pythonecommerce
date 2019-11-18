from models import Users
from flask_restful import Resource
from flask import request
from config import *
import random
from random import randint
import pyotp
from config import db
#from schema.users import UsersSchema

class VerifyEmail(Resource):
    def __init__(self):
        pass
    def get(self,id):
        obj = db.session.query(Users).filter(Users.id == id).one_or_none()
        email = obj.email
        email_status = obj.email_verified
        totp = pyotp.TOTP('base32secret3232')
        number = totp.now()
        mail = index('Verify Email',email,'OTP for for your account is : '+number)
        if email_status == False:
            if mail:
                dit = {"email_otp":number}
                email_otp = db.session.query(Users.id == id).update(dit)
                db.session.commit()
                return ("OTP is Successfully sent")
            return ("please check your email")
        return ("email is already verified.")

    def put(self,id):
        otp1 = request.get_json()
        otp = otp1["email_otp"]
        obj = db.session.query(Users).filter(Users.id == id).one_or_none()
        saved_otp = obj.email_otp
        if saved_otp == otp:
            dit = {"email_verified":True}
            verify_email = db.session.query(Users.id == id).update(dit)
            db.session.commit()
            return ("Email Verfication is Successfully Completed")
        return ("Please check your otp")
