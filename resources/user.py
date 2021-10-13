import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    def post(self):
        data = UserRegister.parser.parse_args()
        username = data['username']
        user = UserModel.find_by_username(username)

        if user:
            return {'Message': f'user {username} is already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successufully."}, 201
