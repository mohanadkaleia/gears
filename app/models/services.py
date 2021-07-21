import tinydb

from slugify import slugify
from app import util


class ErrNotFound(Exception):
    pass


class ErrInvalidParameters(Exception):
    pass


# DB initializtion
db = tinydb.TinyDB("db.json")
services = db.table("services")


def insert(shop_id="", name="", description="", price="", images=None):
    # Initialize id with randomly generated string
    id = util.random_id(initial="s")

    services.insert(
        {
            "id": id,
            "shop_id": shop_id,
            "name": name,
            "slug": slugify(name),
            "description": description,
            "price": price,
            "images": images or [],
        }
    )
    return id


def update(id="", shop_id="", name="", description="", price="", images=None):
    query = tinydb.Query()
    doc = {
        "name": name,
        "slug": slugify(name),
        "description": description,
        "price": price,
        "images": images,
    }
    services.update(doc, query.id == id)
    return id


def delete(id):
    query = tinydb.Query()
    services.remove(query.id == id)


def all():
    results = services.all()
    return results


def get(id):
    service = tinydb.Query()
    result = services.search(service.id == id)

    if not result:
        raise ErrNotFound(f"no service found for the provided id: {id}")

    return result[0]


def get_by_name(name=""):
    if not name:
        raise ErrInvalidParameters("service name must be provided")

    service = tinydb.Query()
    result = services.search(service.name == name)

    if not result:
        raise ErrNotFound(f"no service found for the provided name: {name}")

    return result[0]
