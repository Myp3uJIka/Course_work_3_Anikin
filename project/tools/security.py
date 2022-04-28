import hashlib
import datetime
import calendar

import jwt
from flask import current_app, request
from flask_restx import abort

from project.schemas.user import UserSchema

ALGO = 'HS256'


def generate_password_digest(password):
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def create_access_token(user):
    user_data = UserSchema().dump(user)
    token_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
    user_data['exp'] = calendar.timegm(token_time.timetuple())
    access_token = jwt.encode(user_data, current_app.config['SECRET_KEY'], algorithm=ALGO)
    return access_token


def create_refresh_token(user):
    user_data = UserSchema().dump(user)
    token_time = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
    user_data['exp'] = calendar.timegm(token_time.timetuple())
    refresh_token = jwt.encode(user_data, current_app.config['SECRET_KEY'], algorithm=ALGO)
    return refresh_token


def create_tokens(user):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def create_tokens_from_token(data):
    try:
        user_data = jwt.decode(data['access_token'], current_app.config['SECRET_KEY'], algorithms=ALGO)
        return create_tokens(user_data)
    except Exception:
        try:
            user_data = jwt.decode(data['refresh_token'], current_app.config['SECRET_KEY'], algorithms=ALGO)
            return create_tokens(user_data)
        except Exception:
            abort(401)


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=ALGO)
        except Exception as e:
            print('JWT Decode Exception', e)
            abort(401)
        return func(*args, **kwargs)
    return wrapper


def get_user_from_token(req):
    if "Authorization" not in req:
        abort(401)
    data = req['Authorization']
    token = data.split("Bearer ")[-1]
    try:
        user_data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=ALGO)
        return user_data
    except Exception as e:
        print('JWT Decode Exception', e)
        abort(401)


def compare_password(data):
    hashed_old_password = generate_password_digest(data['old_password'])
    if data['current_password'] == hashed_old_password:
        return True
    else:
        return False

