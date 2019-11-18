import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask
from flask_mail import Mail, Message
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))
connex_app = connexion.App(__name__)
app = connex_app.app

db = SQLAlchemy(app)
mail = Mail(app)

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Welcome@123@104.199.146.29/mall"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')

#--------------------------------------------flask-mail--------------------------------------------------
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bhanuchander008@gmail.com'
app.config['MAIL_PASSWORD'] = 'abhi1015'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def index(subject, email, body):
   msg = Message(subject, sender = 'bhanuchander008@gmail.com', recipients = [email])
   msg.body = body
   mail.send(msg)
   return "Sent"

#---------------------------------------------------------------------------------------------------------

'''
def view(page,per_page):
    banner_image = Banner_images.query.order_by(Banner_images.id.desc()).paginate(page,per_page,error_out=False)
    print("---",banner_image.__dict__)
    return banner_image
'''


db.init_app(app)
ma = Marshmallow(app)
