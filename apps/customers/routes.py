# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 12:07:25 2021

@author: S@tZ
"""
from flask import Blueprint, jsonify, request, make_response
from functools import wraps
from .extract_data import return_json
import jwt
from functools import wraps
import datetime
#from config import config
import os
from dotenv import load_dotenv
load_dotenv()

"""blueprint instance for the customer api, the customer api facilitates the following services
    - name matching
    - payment screening
"""
customer = Blueprint('customer',__name__,url_prefix='/DAAI-API/v1')


"""exception handling for the HTTP status codes"""
@customer.errorhandler(400)
def handle_400_error(_e400):
    """Return a 404 HTTP status code"""
    print(_e400)
    return make_response(jsonify({"status":"error", "message":"Bad request, please check the url...","status_code":"400"}), 400)

@customer.errorhandler(404)
def handle_404_error(_e404):
    """Return a 400 HTTP status code"""
    print(_e404)
    return make_response(jsonify({"status":"error", "message":"Requested page not found, please check the URL...","status_code":"404"}), 404)

@customer.errorhandler(500)
def handle_500_error(_e500):
    """Return a 500 HTTP status code"""
    print(_e500)
    return make_response(jsonify({"status":"error", "message":"Something went wrong, please contact admin...","status_code":"500"}), 500)


def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            #print('token is missing')
            #return make_response(jsonify({'message' : 'token is missing!'}), 500)
            return make_response(jsonify({"status":"error", "message":"token is missing!...","status_code":"500-1"}), 500)
        try:
            #data = jwt.decode(token, customer.config['SECRET_KEY'], algorithms="HS256")
            #data = jwt.decode(token, 'thisissecretkey', algorithms="HS256")
            jwt.decode(token, str(os.getenv("SECRET_KEY")), algorithms="HS256")
        except jwt.InvalidTokenError as _e:
            print('token is invalid! -> ',_e)
            return make_response(jsonify({"status": "error", "message": "token is invalid!...", "status_code": "500-2"}), 500)
            #return make_response(jsonify({'message' : 'token is invalid!'}), 500)
        except jwt.ExpiredSignatureError as _e:
            print('expired signature! -> ', _e)
            return make_response(jsonify({"status": "error", "message": "token is invalid!...", "status_code": "500-3"}), 500)
            #return make_response(jsonify({'message' : 'token is invalid!'}), 500)
        except jwt.DecodeError as _e:
            print('can not decode given token! -> ', _e)
            return make_response(jsonify({"status": "error", "message": "token is invalid!...", "status_code": "500-4"}), 500)
            #return make_response(jsonify({'message': 'token is invalid!'}), 500)
        except Exception as _e:
            print('Exception occured while decoding token ->', _e)
            return make_response(jsonify({'message': 'token is invalid!'}), 500)

        return f(*args, **kwargs)
    return decorated


"""
    this route does the athentication. Gets user name and password and along with the 
    secret key it creates the JWT token and sends back the token as json response
    
    URL -> http(s)://<domain-name>/DAAI-API/customers/v1/auth?user=xxxx&password=xxxxx
    Response -> JWT token
    
"""
@customer.route('/auth',methods=['GET'])
def _authenticate():
    res=request.args
    print(res)
    print(os.getenv("SECRET_KEY"))
    if res['user'] == 'sathish' and res['password'] == 'Satz@2021':
        #print('Credentials valid')
        #token = jwt.encode({'user' : res['user'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, customer.config['SECRET_KEY'], algorithm="HS256")
        token = jwt.encode(
            {
                'user' : res['user'], 
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, 
            str(os.getenv("SECRET_KEY")), 
            algorithm="HS256"
        )
        return make_response(jsonify({"status": "success", "message": "token given!...", "status_code": "200", 'token':token}), 200)
        #return jsonify({'message' : 'token generated','token':token})
    else:
        #print('credentials not valid...')
        return make_response(jsonify({"status": "error", "message": "credential invalid!...", "status_code": "401"}), 401)


"""
    this route is for authorization. Gets the jwt token and validates it with jwt module
    
    URL -> http(s)://<domain-name>/DAAI-API/v1/customers?token=<jwt-token>&names=<single name or multiple names with separator>
    Response -> JWT token
    
"""
@customer.route('/customers', methods=["GET"])
@verify_token
def get_data():
    #print('in get_data')
    res = request.args.get('names')
    if res:
        data = return_json(str(res).strip().split('|'))
        return make_response(jsonify({"status": "success", "message": "data attached!...", "status_code": "200", 'data':data}), 200)
    else:
        return make_response(jsonify({"status":"error", "message":"Bad request, please check the url for parameters...","status_code":"400"}), 400)
    
@customer.route('/')
def home():
    return 'hi'


