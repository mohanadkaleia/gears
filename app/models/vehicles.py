import tinydb

from app import util


class ErrVehicleNotFound(Exception):
    pass


class ErrVehicleAlreadyExisit(Exception):
    pass


# DB initializtion
db = tinydb.TinyDB("db.json")
vehicles = db.table("vehicles")


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
    # TODO: validate the input data
    pass

    vehicle_id = util.random_id(initial="v")

    if not images:
        images = []

    vehicles.insert(
        {
            "id": vehicle_id,
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

    return vehicle_id


def delete(vehicle_id):
    query = tinydb.Query()
    vehicles.remove(query.id == vehicle_id)


def all():
    return vehicles.all()


def get(vehicle_id):
    vehicle = tinydb.Query()
    result = vehicles.search(vehicle.vehicle_id == vehicle_id)

    if not result:
        raise ErrVehicleNotFound(f"no vehicle found for the provided id: {vehicle_id}")

    return result[0]


def find(make="", model="", year=""):
    pass
