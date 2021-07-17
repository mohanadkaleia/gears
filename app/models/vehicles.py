import tinydb

from app import util
from app.database import vehicles


class ErrVehicleNotFound(Exception):
    pass


class ErrVehicleAlreadyExisit(Exception):
    pass


# CRUD functions
def insert(
    shop_id=None,
    make="",
    model="",
    year="",
    price="",
    title="",
    condition="",
    description="",
    images=None,
):

    if not images:
        images = []

    # TODO: add shop id as a FK
    id = util.random_id(initial="v")
    vehicles.insert(
        {
            "id": id,
            "shop_id": shop_id,
            "make": make,
            "model": model,
            "year": year,
            "price": price,
            "title": title,
            "condition": condition,
            "description": description,
            "images": images,
        }
    )

    # TODO: Upload images into disk
    pass

    return id


def delete(vehicle_id):
    query = tinydb.Query()
    vehicles.remove(query.vehicle_id == vehicle_id)


def all():
    results = vehicles.all()

    if not results:
        raise ErrVehicleNotFound("oops.. no vehicles found in the db")

    return results


def get(vehicle_id):
    vehicle = tinydb.Query()
    result = vehicles.search(vehicle.vehicle_id == vehicle_id)

    if not result:
        raise ErrVehicleNotFound(f"no vehicle found for the provided id: {vehicle_id}")

    return result.pop()


def find(make="", model="", year=""):
    pass
