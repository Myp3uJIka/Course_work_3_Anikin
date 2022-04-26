import hashlib
import datetime
import calendar

import jwt
from flask import current_app
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


def create_tokens_from_rtoken(data):
    try:
        user_data = jwt.decode(data['access_token'], current_app.config['SECRET_KEY'], algorithms=ALGO)
        return create_tokens(user_data)
    except Exception:
        try:
            user_data = jwt.decode(data['refresh_token'], current_app.config['SECRET_KEY'], algorithms=ALGO)
            return create_tokens(user_data)
        except Exception:
            abort(401)
    abort(401)


