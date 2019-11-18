from flask import request
from config import *
import json
import re
from werkzeug.wrappers import Request, Response
from sqlalchemy import and_
from models import Users, Permissions
class LoggerMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        request = Request(environ)
        print("+++++++++++++",'path: %s, url: %s, headers: %s, method: %s' % (request.path, request.url, request.headers, request.method))
        path = ('%s' % (request.path))
        digit = re.findall(r'\d+', path)
        if digit == []:
            l = ['/addrole','/usersignin','/getupdatedeleteroles']
        else:
            dig = digit[0]
            l = ['/addrole','/usersignin','/getupdatedeleteroles/'+dig]
        #print(digit)
        if path in l:
            return self.app(environ, start_response)
        else:
            Id = request.headers.get('id')
            query = db.session.query(Users).filter(Users.id == Id).first()
            role_obj = query.__dict__
            role = role_obj['role_id']
            permissions = db.session.query(Permissions).filter(and_(Permissions.role_id == role, Permissions.view_name == 'dashboard')).first()
            permission_obj = permissions.__dict__
            call = ('%s' % (request.method))
            if permission_obj[call] != True:
                text = {'error':False}
                response = Response(json.dumps({
                    'error':False,
                    'message':'error',
                }))
            else:
                response = Response(json.dumps({
                    'message':'success',
                }))

        return response(environ, start_response)

        '''if request.headers['Make'] != 'xyz':
           text = {'error':False}
           response = Response(json.dumps({
               'error':False,
               'message':'error',
           }))
           return response(environ, start_response)'''
