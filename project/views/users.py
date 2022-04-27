from flask import request
from flask_restx import Namespace, Resource, reqparse, abort

from project.services.users_service import UsersService
from project.setup_db import db
from project.tools.security import auth_required, generate_password_digest, get_user_from_token, \
    compare_password

users_ns = Namespace("user")
# parser = reqparse.RequestParser()
# parser.add_argument('page', type=int)


@users_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        return UsersService(db.session).get_all()

    @auth_required
    def patch(self):
        req_json = request.json
        req_json['id'] = get_user_from_token(request.headers)['id']
        UsersService(db.session).update(req_json)
        return ''

        # @users_ns.expect(parser)
        # def get():
        #     page = parser.pase_args().get("page")
        #     if page:
        #         abort(401)
        #         return UsersService(db.session).get_limit_users(page)
        #     abort(401)
        #     return UsersService(db.session).get_all_users()


@users_ns.route('/<int:u_id>/')
class UserView(Resource):
    @auth_required
    def get(self, u_id: int):
        return UsersService(db.session).get_one(u_id)


@users_ns.route('/password/')
class SecurityView(Resource):
    @auth_required
    def put(self):
        req_json = request.json
        user_data = get_user_from_token(request.headers)
        req_json['current_password'] = UsersService(db.session).get_user_password(user_data['id'])
        if compare_password(req_json):
            data = {
                "id": user_data['id'],
                "password": generate_password_digest(req_json['new_password'])
            }
            UsersService(db.session).update(data)
        return ''
