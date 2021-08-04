import tinydb

from app import util
from app.models.db import promos


class ErrNotFound(Exception):
    pass


class ErrAlreadyExisit(Exception):
    pass


# CRUD functions
def insert(shop_id=None, code="", description=""):
    # TODO: validate the input data
    pass

    promo_id = util.random_id(initial="p")

    promos.insert(
        {"id": promo_id, "shop_id": shop_id, "code": code, "description": description}
    )

    return promo_id


def delete(promo_id):
    query = tinydb.Query()
    promos.remove(query.id == promo_id)


def all():
    return promos.all()


def get(id):
    promo = tinydb.Query()
    result = promos.search(promo.id == id)

    if not result:
        raise ErrNotFound(f"no data found for the provided id: {id}")

    return result[0]


def get_by_code(code):
    promo = tinydb.Query()
    result = promos.search(promo.code == code)

    if not result:
        raise ErrNotFound(f"no data found for the provided id: {id}")

    return result[0]
