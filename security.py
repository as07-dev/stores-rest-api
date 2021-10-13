from werkzeug.security import safe_str_cmp  # es wird check_password_hash benutzt
from werkzeug.security import check_password_hash
from models.user import UserModel


# function to authenticate a user
def authenticate(username, password):

    user = UserModel.find_by_username(username)
    if user and check_password_hash(user.password, password):
        return user

    # user = UserModel.find_by_username(username)
    # # if user and user.password == password:
    # if user and safe_str_cmp(user.password, password):
    #     return user


# this is unique to flask JWT; payload is contents of jwt token
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
