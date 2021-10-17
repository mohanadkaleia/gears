import tinydb

from slugify import slugify
from app import util
from app.models.db import services


class ErrNotFound(Exception):
    pass


class ErrInvalidParameters(Exception):
    pass


def insert(shop_id="", name="", description="", prices="", images=None, max_slot=None):
    # Initialize id with randomly generated string
    id = util.random_id(initial="s")

    services.insert(
        {
            "id": id,
            "shop_id": shop_id,
            "name": name,
            "slug": slugify(name),
            "description": description,
            "prices": prices,
            "images": images or [],
            "max_slot": max_slot
        }
    )
    return id


def update(id, shop_id="", name=None, description=None, prices=None, images=None):
    query = tinydb.Query()
    doc = {}

    if shop_id:
        doc["shop_id"] = shop_id

    if name is not None:
        doc["name"] = name
        doc["slug"] = slugify(name)

    if description is not None:
        doc["description"] = description

    if prices is not None:
        doc["prices"] = prices

    if images is not None:
        doc["images"] = images

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
