
from os import access
from typing import Tuple
from flask import Blueprint,jsonify, request,abort
from markupsafe import re
from werkzeug.security import check_password_hash,generate_password_hash
import re
import validators
from src.database import User,db
from flask_jwt_extended import create_refresh_token,create_access_token, jwt_required, get_jwt_identity

auth = Blueprint('auth',__name__,url_prefix='/api/v1/auth')

def validatePassword(input):
    reg = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")

    if not re.search(reg,input):
        abort(400,'password not valid!')

def validateUser(input):

    if User.query.filter_by(username=input).first() is not None:
        abort(400,'username already in use!')

def validateEmail(email):
    if not validators.email(email) or User.query.filter_by(email=email).first() is not None:
        abort(400,'email not valid or already in use!')
        
def userExists(user,password):
    
    if user is None:
        abort(404,'account does not exist')
    
    if check_password_hash(user.password,password):
        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)
        
        return refresh,access
    
    else:
        abort(401,'password is wrong!')    
        
        
        
@auth.post('/register')
def register():
    username= request.json['username']
    email= request.json['email']
    password = request.json['password']
    
    validatePassword(password)
    validateUser(username)
    validateEmail(email)
    
    pw_hash = generate_password_hash(password)
    
    user = User(username=username,email=email,password=pw_hash)
    db.session.add(user)
    db.session.commit()
    
    return {'message':'User created',
            
                'username':username,
                'email':email
            },201
    
@auth.post('/login')
def login():
    email = request.json.get('email','')
    password = request.json.get('password','')
    
    user = User.query.filter_by(email=email).first()
    
    refresh,access = userExists(user,password)
    
    return jsonify({
            'username':user.username,
            'email': email,
            'refresh':refresh,
            'access':access
        })

@auth.get('/me')
@jwt_required()
def me():
    user_id = get_jwt_identity()
    
    user = User.query.filter_by(id=user_id).first()
    
    return jsonify({
        'user':{
            'username':user.username,
            'email':user.email
        }
    })

@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    
    access = create_access_token(identity=user_id)
    
    return jsonify({
        'access':access
    }),200
    
