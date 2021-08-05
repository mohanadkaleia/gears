import tinydb
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from app import util
from app.models.db import users


class ErrNotFound(Exception):
    pass


class ErrInvalidParameters(Exception):
    pass


class User(UserMixin):
    def __init__(self, id,  username):
        self.id = id
        self.username = username

    def get_id(self):
        # This function is requried by Flask-Login
        return self.id


def insert(username="", password=""):
    user_id = util.random_id(initial="U")
    users.insert(
        {
            "id": user_id,
            "username": username,
            "password": generate_password_hash(password, method='sha256'),
        }
    )

    return user_id


def get(user_id):
    if not id:
        raise ErrInvalidParameters("user id parameter is required")

    user = tinydb.Query()
    result = users.search(user.id == user_id)

    if not result:
        raise ErrNotFound(f"no data found for the provided id: {user_id}")

    return result[0]


def get_by_username(username):
    if not username:
        raise ErrInvalidParameters("username parameter is required")

    user = tinydb.Query()
    result = users.search(user.username == username)

    if not result:
        raise ErrNotFound(f"no data found for the provided username: {username}")

    return result[0]


def load_user(user_id):
    '''
        This is a dedicated function for Flask-Login. 
        To convert user dict into a object since the lib expect the user to be a object
    '''
    record = get(user_id)
    return User(record["id"], record["username"], record["password"])