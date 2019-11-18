from models import Users
from flask_restful import Resource
import urllib.request
import urllib.parse
import pyotp
from config import db
from flask import request

class MobileVerification(Resource):
    def __init__(self):
        pass

    def get(self,id):
        obj = Users.query.filter(Users.id == id).one_or_none()
        mobile = obj.phone
        phone_verified = obj.phone_verified
        if phone_verified == False:
            totp = pyotp.TOTP('base32secret3232')
            number = totp.now()
            params = {'apikey':'/UM543b2Ssg-GUq4g0hwBT648rJfEJbambSbQmlwsQ', 'numbers': mobile, 'message' : 'Dear customer your otp is '+number+'.', 'sender': 'HOMASO'}
            f = urllib.request.urlopen('https://api.textlocal.in/send/?'
                + urllib.parse.urlencode(params))
            if f:
                dit = {"mobile_otp":number}
                mobile_otp = db.session.query(Users.id == id).update(dit)
                db.session.commit()
                return ("otp sended to your mobile number.")
            return ("failed, please check your mobile number.")
        return ("Phone number is already verified.")

    def put(self,id):
        otp1 = request.get_json()
        otp = otp1["mobile_otp"]
        obj = Users.query.filter(Users.id == id).one_or_none()
        saved_otp = obj.mobile_otp
        if saved_otp == otp:
            dit = {"phone_verified":True}
            verify_email = db.session.query(Users.id == id).update(dit)
            db.session.commit()
            return ("Mobile Verfication is Successfully Completed")
        return ("Please check your otp")
