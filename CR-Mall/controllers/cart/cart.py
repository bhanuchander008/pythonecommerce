from models import Cart
from schemas.cart import CartSchema
from schemas.products import ProductsGetSchema
from flask import request, Flask
from flask_restful import Resource
from  sqlalchemy import and_
from config import *
import logging, logging.config, yaml

CONFIG_PATH = os.path.join(basedir,'logger.yaml')
logging.config.dictConfig(yaml.load(open(CONFIG_PATH)))
logger = logging.getLogger('cart')


class AddCart(Resource):
    def __init__(self):
        pass

    #This call is used to fetch the data in the cart
    def get(self):
        cart = db.session.query(Cart).order_by(Cart.id).all()
        if cart:
            schema = CartSchema(many = True)
            data = schema.dump(cart).data
            logger.info("Cart data fetched succesfully ")
            return data
        else:
            logger.warning("no data is available in cart")
            return("no data is available in cart")

    #This call is used to add the products to cart.
    def post(self):
       data = request.get_json()
       user = data['user_id']
       dit = {key:value for key,value in data.items()}
       obj = db.session.query(Cart).filter(and_(Cart.user_id == user,Cart.status == False)).first()
       if obj is None:
           schema = CartSchema()
           new_cart = schema.load(dit, session=db.session).data
           db.session.add(new_cart)
           db.session.commit()
           data = schema.dump(new_cart).data
           logger.info("Product successfully added to cart ")
           return data
       else:
           logger.warning("you already have one item in cart")
           return("you already have one item in cart")


class DeleteCart(Resource):
    def __init__(self):
        pass

    #This call is used to delete the products from the cart
    def delete(self,id):
        obj = db.session.query(Cart).filter_by(id = id).first()
        if obj:
            db.session.delete(obj)
            db.session.commit()
            logger.info("Product successfully deleted from cart")
            return ("Product successfully deleted from cart")
        logger.warning("No Product available in the cart")
        return ("No Product available in the cart")

class GetCartStatus(Resource):
    def __init__(self):
        pass

    # call to get the cart status
    def get(self,status):
        cart = db.session.query(Cart).filter(Cart.status == status).all()
        if cart:
            schema = CartSchema()
            data = schema.dump(cart,many=True).data
            logger.info("Cart data fetched succesfully based on status")
            return data
        else:
            logger.warning("no product is available in the cart with such status")
            return("no product is available in the cart with such status")




'''
class AddQuantity(Resource):
    def __init__(self):
        pass

    def get(self,id):
        obj = db.session.query(Cart).filter(Cart.id == id).first()
        quantity = obj.quantity
        prod_obj = db.session.query(Products).filter(Cart.product_id == id).first()
        product_id = prod_obj.id
        quantity_allocated = prod_obj.quantity_allocated
        quantity_in = prod_obj.quantity_in
        if quantity_allocated >= quantity:
            quantity_include = quantity_in-1
            quantities = quantity+1
            dit = {"quantity":quantities}
            data = {"quantity_in":quantity_include}
            pro_update = db.session.query(Products).filter(Products.id == product_id).update(data)
            cart_update = db.session.query(Cart).filter(Cart.id == id).update(dit)
            db.session.commit()
            return ("One more quantity added to the cart")
        else:
            return("out of stock")


class RemoveQuantity(Resource):
    def __init__(self):
        pass

    def get(self,id):
        obj = db.session.query(Cart).filter(Cart.id == id).first()
        quantity = obj.quantity
        prod_obj = db.session.query(Products).filter(Cart.product_id == id).first()
        product_id = prod_obj.id
        quantity_allocated = prod_obj.quantity_allocated
        quantity_in = prod_obj.quantity_in
        if quantity_allocated >= quantity and quantity <= 1:
            quantity_include = quantity_in+1
            quantities = quantity-1
            dit = {"quantity":quantities}
            data = {"quantity_in":quantity_include}
            pro_update = db.session.query(Products).filter(Products.id == product_id).update(data)
            cart_update = db.session.query(Cart).filter(Cart.id == id).update(dit)
            db.session.commit()
            return ("One more quantity removed from the cart")
        else:
            return("out of stock")
'''
