from flask import Flask, request
from middleware import LoggerMiddleware
from config import *
import logging,logging.config
from config import db
from flask_restful import reqparse, Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
app = Flask(__name__)
app.wsgi_app = LoggerMiddleware(app.wsgi_app)
'''
@app.before_request
def hook():
    # request - flask.request
    lol = 'endpoint: %s, url: %s, path: %s, headers: %s, method: %s' % (request.endpoint,request.url,request.path,request.headers,request.method)
    print("==========",lol)
'''

api = Api(app)
CORS(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#-------------------------------------------Roles---------------------------------------------------------------------------

from controllers.roles.post_roles import Getcreateroles
from controllers.roles.roles import GetUpdateDeleteRoles
api.add_resource(Getcreateroles, '/addrole')
api.add_resource(GetUpdateDeleteRoles, '/getupdatedeleteroles/<int:id>')

#-------------------------------------------Permissions---------------------------------------------------------------------

from controllers.permissions.post_permissions import Getcreatepermissions
from controllers.permissions.getupdatepermissions import GetUpdatePermissions
api.add_resource(Getcreatepermissions,'/addpermissions')
api.add_resource(GetUpdatePermissions,'/getupdatepermissions/<int:id>')

#-------------------------------------------Staff---------------------------------------------------------------------------

from controllers.staff.sign_up import StaffSignup
from controllers.staff.login import StaffSignin
from controllers.staff.password import StaffForget_Password, StaffReset_password
from controllers.staff.staff import GetStaff, GetUpdateStaff, ActiveStaff,StaffUpdateByAdmin
api.add_resource(StaffSignup,"/staffsignup")
api.add_resource(StaffSignin,"/stafflogin")
api.add_resource(StaffForget_Password,"/staffforget_password")
api.add_resource(StaffReset_password,"/staffreset_password/<int:id>")
api.add_resource(GetStaff,"/getstaff")
api.add_resource(GetUpdateStaff,"/getupdatestaff/<int:id>")
api.add_resource(ActiveStaff,"/activestaff")
api.add_resource(StaffUpdateByAdmin,"/staffupdatebyadmin/<int:id>")

#-------------------------------------------Users---------------------------------------------------------------------------

from controllers.users.user_signin import Signin, SecretResource, UserLogoutAccess, UserLogoutRefresh
from controllers.users.user_signup import Signup
from controllers.users.user_resetpassword import UserForget_Password,UserReset_password
from controllers.users.user import GetUsers, GetUpdateUser, ActiveUsers
from controllers.users.verifyemail import VerifyEmail
from controllers.users.verifymobile import MobileVerification
api.add_resource(Signup,'/usersignup')
api.add_resource(Signin,'/usersignin')
api.add_resource(VerifyEmail,'/userverifyemail/<int:id>')
api.add_resource(MobileVerification,'/userverifymobile/<int:id>')
api.add_resource(GetUsers,'/getallusers')
api.add_resource(GetUpdateUser,'/getupdateuser/<int:id>')
api.add_resource(UserReset_password,"/user_resetpassword/<int:id>")
api.add_resource(UserForget_Password,"/user_forgetpassword")
api.add_resource(ActiveUsers,'/activeusers')
api.add_resource(UserLogoutAccess,'/userlogoutaccess')
api.add_resource(UserLogoutRefresh,'/userlogoutrefresh')
api.add_resource(SecretResource,'/secretresource')


#-------------------------------------------Banner-Image--------------------------------------------------------------------

from controllers.banner_image.post_bannerimage import GetCreateBanner_images, GetBanner_imagespages
from controllers.banner_image.banner_images import GetUpdateBannerimageById, BannerImageUpdate
from controllers.banner_image.getbannerimages import GetActiveBannerImages
api.add_resource(GetCreateBanner_images,'/getcreatebannerimages')
api.add_resource(GetUpdateBannerimageById,'/getupdatebannerimage/<int:id>')
api.add_resource(BannerImageUpdate,'/bannerimageupdate/<int:id>')
api.add_resource(GetActiveBannerImages,'/getactivebannerimage')
api.add_resource(GetBanner_imagespages,'/pages/<int:start>/<int:end>')

#-------------------------------------------Categories----------------------------------------------------------------------

from controllers.categories.post_categories import GetcreateCategories
from controllers.categories.categories import UpdateDeleteCategories
from controllers.categories.getcategories import GetCategorieBy_name,GetActiveCategories
api.add_resource(GetcreateCategories,'/getcreatecategories')
api.add_resource(UpdateDeleteCategories,'/getupdatedeletecategories/<int:id>')
#api.add_resource(ImageUpdate,"/updatecategoryimage/<int:id>")
api.add_resource(GetActiveCategories,"/getactivecategories")
api.add_resource(GetCategorieBy_name,"/getcategoriebyname/<name>")



#-------------------------------------------Sub-Category--------------------------------------------------------------------

from controllers.sub_categories.post_sub_categories import GetCreateSubCategories
from controllers.sub_categories.sub_categories import GetUpdateDeleteSub_Categories,Sub_CategorieImageUpdate
from controllers.sub_categories.getsub_categories import GetActiveSubCategories,GetSubCategoryBy_name,GetSubCategoryByCategory
api.add_resource(GetCreateSubCategories,"/getcreatesubcategories")
api.add_resource(GetUpdateDeleteSub_Categories,"/getupdatedeletesubcategories/<int:id>")
api.add_resource(Sub_CategorieImageUpdate,"/updatesubcategoryimage/<int:id>")
api.add_resource(GetActiveSubCategories,"/getactivesubcategories")
api.add_resource(GetSubCategoryBy_name,"/getsubcategorybyname/<name>")
api.add_resource(GetSubCategoryByCategory,"/getsubcategorybycategory/<int:id>")

#-------------------------------------------Product-Class-------------------------------------------------------------------

from controllers.product_class.post_product_class import GetCreateProductClass
from controllers.product_class.product_class import GetUpdateDeleteProductClass,ProductClassImageUpdate
from controllers.product_class.getproduct_class import GetActiveProductClass,GetProductClassBy_name,GetProductClassBySubCategory
api.add_resource(GetCreateProductClass,'/getcreateproductclass')
api.add_resource(GetUpdateDeleteProductClass,"/getupdatedeleteproductclass/<int:id>")
api.add_resource(ProductClassImageUpdate,"/updateproductclassimage/<int:id>")
api.add_resource(GetActiveProductClass,"/getactiveproductclass")
api.add_resource(GetProductClassBy_name,"/getproductclassbyname/<name>")
api.add_resource(GetProductClassBySubCategory,"/getproductclassbysubcategory/<int:id>")

#-------------------------------------------Products------------------------------------------------------------------------

from controllers.products.post_products import GetcreateProducts
from controllers.products.products import GetUpdateDeleteProducts
from controllers.products.getproducts import GetActiveProducts,GetProductsByProduct_Class
api.add_resource(GetcreateProducts,"/getcreateproducts")
api.add_resource(GetUpdateDeleteProducts,"/getupdatedeleteproducts/<int:id>")
api.add_resource(GetActiveProducts,"/getactiveproducts")
api.add_resource(GetProductsByProduct_Class,"/getproductsbyproductclass/<int:id>")

#-------------------------------------------Sizes---------------------------------------------------------------------------

from controllers.sizes.post_sizes import GetcreateSizes
from controllers.sizes.sizes import GetUpdatedeleteSizes
from controllers.sizes.getsizes import GetActiveSizes,GetSizesByProduct,GetSizesBy_name
api.add_resource(GetcreateSizes,"/getcreatesizes")
api.add_resource(GetUpdatedeleteSizes,"/getupdatedeletesizes/<int:id>")
api.add_resource(GetActiveSizes,"/getactivesizes")
api.add_resource(GetSizesBy_name,"/getsizesbysize/<size>")
api.add_resource(GetSizesByProduct,"/getsizebyproduct/<int:id>")

#-------------------------------------------Product-Images------------------------------------------------------------------

from controllers.product_image.product_images import GetUpdateProductimageById
from controllers.product_image.post_product_image import GetCreateProduct_images
from controllers.product_image.get_product_images import GetActiveProductImages,GetProductImageByProduct
api.add_resource(GetCreateProduct_images,"/getcreateproductimages")
api.add_resource(GetActiveProductImages,"/getactiveproductimages")
api.add_resource(GetProductImageByProduct,"/getproductimagebyproduct/<int:id>")
api.add_resource(GetUpdateProductimageById,"/getupdateproductimage/<int:id>")

#-------------------------------------------Colours-------------------------------------------------------------------------

from controllers.colour.post_colour import GetCreateColours
from controllers.colour.colours import GetUpdateDeleteColours, ColourImageUpdate
from controllers.colour.getcolour import GetColourByProduct, GetActiveColours
api.add_resource(GetCreateColours,"/getcreatecolour")
api.add_resource(GetUpdateDeleteColours,"/getupdatedeletecolour/<int:id>")
api.add_resource(ColourImageUpdate,"/colourimageupdate/<int:id>")
api.add_resource(GetColourByProduct,"/getcolourbyproduct/<int:id>")
api.add_resource(GetActiveColours,"/getactivecolours")

#-------------------------------------------Cart----------------------------------------------------------------------------

from controllers.cart.cart import AddCart, DeleteCart, GetCartStatus
api.add_resource(DeleteCart,"/deletecart/<int:id>")
api.add_resource(AddCart,"/addcart")
api.add_resource(GetCartStatus,"/getcartstatus/<int:status>")
#api.add_resource(AddQuantity,"/addquantity/<int:id>")
#api.add_resource(RemoveQuantity,"/removequantity/<int:id>")

#-------------------------------------------Orders--------------------------------------------------------------------------
'''
from controllers.orders.post_orders import GetCreateOrders
from controllers.orders.orders import GetDeleteOrders
from controllers.orders.getorders import GetOrderByUser, GetOrderByCart, GetOrderByStatus
api.add_resource(GetCreateOrders,"/getcreateorders")
api.add_resource(GetDeleteOrders,"/getdeleteorders/<int:id>")
api.add_resource(GetOrderByUser,"/getoderbyuser/<int:id>")
api.add_resource(GetOrderByCart,"/getorderbycart/<int:id>")
api.add_resource(GetOrderByStatus,"/getorderbystatus/<status>")
'''
#-------------------------------------------Billing-Info--------------------------------------------------------------------

from controllers.billing.post_billing import GetCreateBilling
api.add_resource(GetCreateBilling,"/getcreatebilling")


#---------------------------------------------------------------------------------------------------------------------------
import jwt
#from models import RevokedTokenModel
import models
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
   jti = decrypted_token['jti']
   return models.RevokedTokenModel.is_jti_blacklisted(jti)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)
