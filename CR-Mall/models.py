from config import *
from datetime import datetime
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import Flask
import os
import datetime
from sqlalchemy.orm import relationship

app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Welcome@123@104.199.146.29/mall"

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

#Roles table
class Roles(db.Model):
    __tablename__ = "roles"
    id         = db.Column(db.Integer, primary_key = True)
    name       = db.Column(db.String(50))
    status     = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())

    User = db.relationship("Users", backref = db.backref("Role_user"))
    Staff =  db.relationship("Staff", backref = db.backref("Role_staff"))
    Permission = db.relationship("Permissions", backref = db.backref("Role_Permissions"))

class Permissions(db.Model):
    __tablename__ = "permissions"
    id            = db.Column(db.Integer, primary_key =  True)
    role_id       = db.Column(db.Integer, db.ForeignKey('roles.id'))
    POST           = db.Column(db.Boolean, default = False)
    PUT          = db.Column(db.Boolean, default = False)
    GET          = db.Column(db.Boolean, default = False)
    view_name     = db.Column(db.String(50))
    created_at    = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at    = db.Column(db.DateTime, default = datetime.datetime.utcnow())

#staff details table
class Staff(db.Model):
    __tablename__  = "staff"
    id             = db.Column(db.Integer, primary_key = True)
    role_id        = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable = True)
    first_name     = db.Column(db.String(30),nullable = True)
    last_name      = db.Column(db.String(30),nullable = True)
    phone          = db.Column(db.String(10),nullable = True)
    email          = db.Column(db.String(120), unique = True, nullable = False)
    password       = db.Column(db.String(246))
    address        = db.Column(db.Text(),nullable = True)
    gender         = db.Column(db.Enum('M','F','O'),nullable=True)
    status         = db.Column(db.Boolean, default = True)
    created_at     = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at     = db.Column(db.DateTime, default = datetime.datetime.utcnow())


#User details table
class Users(db.Model):
    __tablename__  = "users"
    id             = db.Column(db.Integer, primary_key = True)
    role_id        = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable = True)
    first_name     = db.Column(db.String(30),nullable = True)
    last_name      = db.Column(db.String(30),nullable = True)
    phone          = db.Column(db.String(10),nullable = True)
    email          = db.Column(db.String(120), unique = True, nullable = False)
    password       = db.Column(db.String(246))
    address        = db.Column(db.Text(),nullable = True)
    gender         = db.Column(db.Enum('M','F','O'),nullable=True)
    email_otp      = db.Column(db.String(10), nullable = True)
    mobile_otp     = db.Column(db.String(10), nullable = True)
    phone_verified = db.Column(db.Boolean, default = False)
    email_verified = db.Column(db.Boolean, default = False)
    status         = db.Column(db.Boolean, default = True)
    created_at     = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at     = db.Column(db.DateTime, default = datetime.datetime.utcnow())

    user_cart      = db.relationship("Cart", backref = db.backref("users"))
    user_Bill     = db.relationship("Billing_info", backref = db.backref("users_bill"))

    def __init__(self, email, password):
        self.email      = email
        self.password   = password
        self.created_at = datetime.datetime.now()

    # it will check the mail id of the user is valid or not
    @validates('email')
    def validate_email(self,key,address):
        assert '@' in address
        return address

#Banner_images detals table
class Banner_images(db.Model):
   __tablename__ = "banner_images"
   id         = db.Column(db.Integer, primary_key = True)
   image      = db.Column(db.String(246), nullable = True)
   status     = db.Column(db.Boolean, default = True)
   created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())
   updated_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())

#Categories details table
class Categories(db.Model):
    __tablename__ = "categories"
    id         = db.Column(db.Integer, primary_key = True)
    name       = db.Column(db.String(50))
    status     = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, default = datetime.datetime.utcnow())

    sub_cat    = db.relationship("Sub_Categories", backref = db.backref("categories"))
    cat_cart   = db.relationship("Cart", backref = db.backref("categories_cart"))

#Sub Category details table
class Sub_Categories(db.Model):
    __tablename__ = "sub_categories"
    id            = db.Column(db.Integer, primary_key = True)
    name          = db.Column(db.String(50))
    image         = db.Column(db.String(246), nullable = True)
    category_id   = db.Column(db.Integer, db.ForeignKey("categories.id"))
    status        = db.Column(db.Boolean, default = True)
    created_at    = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at    = db.Column(db.DateTime, default = datetime.datetime.utcnow())

    sub_pro       = db.relationship("Product_Class", backref = db.backref("sub_category"))

#Products types details table
class Product_Class(db.Model):
    __tablename__  = "product_class"
    id             = db.Column(db.Integer, primary_key = True)
    name           = db.Column(db.String(50))
    image          = db.Column(db.String(246), nullable = True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey("sub_categories.id"))
    status         = db.Column(db.Boolean, default = True)
    created_at     = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at     = db.Column(db.DateTime, default = datetime.datetime.utcnow())

    pro_type       = db.relationship("Products", backref = db.backref("product_class"))


#Product details table
class Products(db.Model):
    __tablename__      = 'products'
    id                 = db.Column(db.Integer, primary_key = True)
    name               = db.Column(db.String(233))
    productclass_id    = db.Column(db.Integer, db.ForeignKey("product_class.id"))
    brand              = db.Column(db.String(233))
    quantity_in        = db.Column(db.Integer())
    quantity_allocated = db.Column(db.Integer())
    description        = db.Column(db.Text(), nullable =True)
    status             = db.Column(db.Boolean(), default = True)
    add_to_cart        = db.Column(db.Boolean(), nullable = True)
    created_at         = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at         = db.Column(db.DateTime, default = datetime.datetime.utcnow())

    Pro_cart           = db.relationship("Cart", backref = db.backref("products"))
    Pro_size           = db.relationship("Sizes", backref = db.backref("product_sizes"))
    Pro_images         = db.relationship("Product_Images", backref = db.backref("product_images"))
    Pro_colour         = db.relationship("Colours", backref = db.backref("product_colour"))

# table to define different sizes of the products
class Sizes(db.Model):
    __tablename__      = "sizes"
    id                 = db.Column(db.Integer, primary_key = True)
    size               = db.Column(db.String(10), nullable = True)
    price              = db.Column(db.Integer)
    product_id         = db.Column(db.Integer, db.ForeignKey("products.id"))
    status             = db.Column(db.Boolean(), default = True)
    created_at         = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at         = db.Column(db.DateTime, default = datetime.datetime.utcnow())

    #size_prices        = db.relationship("Prices",backref = db.backref("sizes"))

'''
#table to define price of the products based on the sizes
class Prices(db.Model):
    __tablename__      = "prices"
    id                 = db.Column(db.Integer, primary_key = True)
    price              = db.Column(db.Integer)
    size_id            = db.Column(db.Integer, db.ForeignKey("sizes.id"))
    status             = db.Column(db.Boolean(), default = True)
    created_at         = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at         = db.Column(db.DateTime, default = datetime.datetime.utcnow())

'''

#Product Colours details table
class Colours(db.Model):
    __tablename__      = "colours"
    id                 = db.Column(db.Integer, primary_key = True)
    name               = db.Column(db.String(246))
    image              = db.Column(db.String(246), nullable = True)
    product_id         = db.Column(db.Integer, db.ForeignKey("products.id"))
    status             = db.Column(db.Boolean(), default = True)
    created_at         = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at         = db.Column(db.DateTime, default = datetime.datetime.utcnow())


#Product Images details table
class Product_Images(db.Model):
    __tablename__      = "product_images"
    id                 = db.Column(db.Integer, primary_key = True)
    image              = db.Column(db.String(233), nullable = True)
    product_id         = db.Column(db.Integer, db.ForeignKey("products.id"))
    status             = db.Column(db.Boolean(), default = True)
    created_at         = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at         = db.Column(db.DateTime, default = datetime.datetime.utcnow())

#Cart details table
class Cart(db.Model):
    __tablename__  = "cart"
    id             = db.Column(db.Integer, primary_key = True)
    user_id        = db.Column(db.Integer, db.ForeignKey("users.id"))
    product_id     = db.Column(db.Integer, db.ForeignKey("products.id"))
    category_id    = db.Column(db.Integer, db.ForeignKey("categories.id"))
    status         = db.Column(db.Boolean(), default = False)
    created_at     = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at     = db.Column(db.DateTime, default = datetime.datetime.utcnow())

    Cart_Bill    = db.relationship("Billing_info", backref = db.backref("Cart"))
'''
#Order details table
class Orders(db.Model):
    __tablename__ = "orders"
    id            = db.Column(db.Integer, primary_key = True)
    cart_id       = db.Column(db.Integer, db.ForeignKey("cart.id"))
    user_id       = db.Column(db.Integer, db.ForeignKey("users.id"))
    order_status   = db.Column(db.Enum("waiting","placed","shipped","delivered"),default = "waiting")
    created_at    = db.Column(db.DateTime, default = datetime.datetime.utcnow())
    updated_at    = db.Column(db.DateTime, default = datetime.datetime.utcnow())
'''
#{"user_id":1,"cart_id":1,"cart_type":"Debit","card_number":123456789012,"name_on_card":"ganesh singamaneni","expire_month":03,"expire_year":2022,"cvv":234}
#Billing information table
class Billing_info(db.Model):
   __tablename__ = "billing_info"
   id            = db.Column(db.Integer, primary_key = True)
   user_id       = db.Column(db.Integer, db.ForeignKey("users.id"))
   cart_id       = db.Column(db.Integer,db.ForeignKey("cart.id"))
   card_type     = db.Column(db.Enum("Credit","Debit"))
   card_number   = db.Column(db.String(12))
   name_on_card  = db.Column(db.String(233),nullable=True)
   expire_month  = db.Column(db.String(2))
   expire_year   = db.Column(db.String(4))
   cvv           = db.Column(db.String(3))
   status        = db.Column(db.Boolean(), default = False)
   created_at    = db.Column(db.DateTime, default = datetime.datetime.utcnow())
   updated_at    = db.Column(db.DateTime, default = datetime.datetime.utcnow())

class RevokedTokenModel(db.Model):
   __tablename__ = 'revoked_tokens'
   id = db.Column(db.Integer, primary_key = True)
   jti = db.Column(db.String(120))

   def add(self):
       db.session.add(self)
       db.session.commit()

   @classmethod
   def is_jti_blacklisted(cls, jti):
       query = cls.query.filter_by(jti = jti).first()
       return bool(query)

db.create_all()
db.session.commit()
if __name__ == '__main__':
    manager.run()
