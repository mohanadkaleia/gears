import tinydb

from app import util
from app.models.db import vehicles


class ErrNotFound(Exception):
    pass


class ErrInvalidParameters(Exception):
    pass


class ErrVehicleAlreadyExisit(Exception):
    pass


def insert(
    shop_id="",
    make="",
    model="",
    year="",
    trim="",
    engine="",
    title="",
    condition="",
    drive="",
    fuel="",
    transmission="",
    exterior="",
    interior="",
    description="",
    images=None,
):
    # Initialize id with randomly generated string
    id = util.random_id(initial="v")

    vehicles.insert(
        {
            "id": id,
            "shop_id": shop_id,
            "make": make,
            "model": model,
            "year": year,
            "trim": trim,
            "engine": engine,
            "title": title,
            "condition": condition,
            "drive": drive,
            "fuel": fuel,
            "transmission": transmission,
            "exterior": exterior,
            "interior": interior,
            "description": description,
            "images": images or [],
        }
    )
    return id


def update(
    id,
    shop_id=None,
    make=None,
    model=None,
    year=None,
    trim=None,
    engine=None,
    title=None,
    condition=None,
    drive=None,
    fuel=None,
    transmission=None,
    exterior=None,
    interior=None,
    description=None,
    images=None,
):
    query = tinydb.Query()

    doc = {}
    if shop_id:
        doc["shop_id"] = shop_id

    if make:
        doc["make"] = make

    if model is not None:
        doc["model"] = model

    if year is not None:
        doc["year"] = year

    if trim is not None:
        doc["trim"] = trim

    if engine is not None:
        doc["engine"] = engine

    if title is not None:
        doc["title"] = title

    if condition is not None:
        doc["condition"] = condition

    if drive is not None:
        doc["drive"] = drive

    if fuel is not None:
        doc["fuel"] = fuel

    if transmission is not None:
        doc["transmission"] = transmission

    if exterior is not None:
        doc["exterior"] = exterior

    if interior is not None:
        doc["interior"] = interior

    if description is not None:
        doc["description"] = description

    if images is not None:
        doc["images"] = images

    vehicles.update(doc, query.id == id)
    return id


def delete(id):
    query = tinydb.Query()
    vehicles.remove(query.id == id)


def all():
    results = vehicles.all()
    return results


def get(id):
    service = tinydb.Query()
    result = vehicles.search(service.id == id)

    if not result:
        raise ErrNotFound(f"no service found for the provided id: {id}")

    return result[0]
