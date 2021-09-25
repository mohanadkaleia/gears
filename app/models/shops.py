import tinydb
from app import util
from app.models.db import shops


class ErrNotFound(Exception):
    pass


class ErrInvalidParameters(Exception):
    pass


def insert(name="", description="", logo="", phone="", email="", hours=""):
    # TODO: validate the information, for example we can't have two shops with same name
    pass

    # TODO: upload the logo as an image
    pass

    shop_id = util.random_id(initial="S")
    shops.insert(
        {
            "id": shop_id,
            "name": name,
            "description": description,
            "logo": logo,
            "phone": phone,
            "email": email,
            "hours": hours,
        }
    )

    return shop_id


def get_by_name(name):
    if not name:
        raise ErrInvalidParameters("name parameter is required")

    shop = tinydb.Query()
    result = shops.search(shop.name == name)

    if not result:
        raise ErrNotFound(f"no data found for the provided name: {name}")

    return result[0]


def all():
    return shops.all()
