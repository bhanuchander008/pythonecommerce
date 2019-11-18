from models import Staff
from schemas.staff import StaffSchema,StaffGetSchema
from config import *
from flask_restful import Resource, reqparse
from flask import request
import logging, logging.config, yaml
import os

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('staff')

parser = reqparse.RequestParser()
parser.add_argument('first_name', help = 'This field is mandatory', required = True)
parser.add_argument('last_name', help = 'This field is mandatory', required = True)
parser.add_argument('phone', help = 'This field is mandatory', required = True)
parser.add_argument('gender', help = 'This field is mandatory', required = True)

class GetStaff(Resource):
    def __init__(self):
        pass

    # call to get all the Staff details
    def get(self):
        staff = Staff.query.order_by(Staff.id).all()
        if staff:
            staff_schema = StaffGetSchema(many = True)
            data = staff_schema.dump(staff).data
            logger.info("Data has fetched succesfully")
            return data
        else:
            logger.warning("Data not found")
            return ("Data Not Found.")

class GetUpdateStaff(Resource):
    def __init__(self):
        pass

    # call to get the user details based on user_id
    def get(self,id):
        staff = Staff.query.filter(Staff.id == id).one_or_none()
        if staff is not None:
            staff_schema = StaffGetSchema()
            data = staff_schema.dump(staff).data
            logger.info("Data has succesfully fetched based on Id")
            return data
        else:
            logger.warning("Staff does not exists")
            return ("Staff does not exists")

    # call to update the staff details based on staff_id
    def put(self,id):
        data = parser.parse_args()
        staff = db.session.query(Staff).filter_by(id = id).update(data)
        if staff:
            db.session.commit()
            staff_obj = db.session.query(Staff).filter(Staff.id == id).one()
            staff_schema = StaffSchema()
            data = staff_schema.dump(staff_obj).data
            logger.info("Data has succesfully updated")
            return data
        else:
            logger.warning("Staff does not exists")
            return ("Staff does not exists")

class ActiveStaff(Resource):
    def __init__(self):
        pass

    # call to get the users with active status
    def get(self):
        staff = db.session.query(Staff).filter(Staff.status == True).all()
        if staff:
            schema = StaffSchema()
            data = schema.dump(staff,many=True).data
            logger.info("Data has succesfully fetched based on status")
            return data
        else:
            logger.warning("No Staff found with these status")
            return("No Staff found with these status")
class StaffUpdateByAdmin(Resource):
    def __init__(self):
        pass

    # admimn's call to update staff
    def put(self,id):
        data = request.get_json()
        staff = db.session.query(Staff).filter_by(id = id).update(data)
        if staff:
            db.session.commit()
            staff_obj = db.session.query(Staff).filter(Staff.id == id).one()
            staff_schema = StaffSchema()
            data = staff_schema.dump(staff_obj).data
            logger.info("Data has succesfully updated")
            return data
        else:
            logger.warning("Staff does not exists")
            return ("Staff does not exists")
