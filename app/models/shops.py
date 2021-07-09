import tinydb
from app import util


class ErrNotFound(Exception):
    pass


class ErrInvalidParameters(Exception):
    pass


db = tinydb.TinyDB("db.json")
shops = db.table("shops")


def insert(name="", description="", logo="", phone="", email="", hours=""):
    # TODO: validate the information, for example we can't have two shops with same name
    pass

    # TODO: upload the logo as an image
    pass

    shop_id = util.random_id(initial="s")
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
