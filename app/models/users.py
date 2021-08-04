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
    def __init__(self, id,  email, password):
        self.id = id
        self.email = email
        self.password = password

    def get_id(self):
        return self.id


def insert(email="", password=""):
    user_id = util.random_id(initial="U")
    users.insert(
        {
            "id": user_id,
            "email": email,
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


def get_by_email(email):
    if not email:
        raise ErrInvalidParameters("email parameter is required")

    user = tinydb.Query()
    result = users.search(user.email == email)

    if not result:
        raise ErrNotFound(f"no data found for the provided email: {email}")

    return result[0]


def load_user(user_id):
    record = get(user_id)
    return User(record["id"], record["email"], record["password"])