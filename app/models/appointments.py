import tinydb
import datetime
from app import util
from app.models.db import appointments


class ErrInvalidParameters(Exception):
    pass


class ErrNotFound(Exception):
    pass


def insert(shop_id, service_id, timeslot, name, email, vehicle, description):

    if timeslot <= datetime.datetime.today() - datetime.timedelta(1):
        raise ErrInvalidParameters("Can't schedule an appointment in the past")

    # TODO: check for availability for the provided timeslot
    pass

    # Initialize id with randomly generated string, "t" for timeslot
    id = util.random_id(initial="a")

    appointments.insert(
        {
            "id": id,
            "shop_id": shop_id,
            "service_id": service_id,
            "timeslot": timeslot,
            "name": name,
            "vehicle": vehicle,
            "email": email,
            "description": description,
        }
    )

    return id


def update(
    id,
    shop_id=None,
    service_id=None,
    timeslot=None,
    name=None,
    email=None,
    vehicle=None,
    description=None,
):
    query = tinydb.Query()
    doc = {}

    if shop_id is not None:
        doc["shop_id"] = shop_id

    if service_id is not None:
        doc["service_id"] = service_id

    if timeslot is not None:
        if timeslot <= datetime.datetime.today() - datetime.timedelta(1):
            raise ErrInvalidParameters("can't schedule an appointment in the past")
        # TODO: check for availability for the provided timeslot
        doc["timeslot"] = timeslot

    if name is not None:
        doc["name"] = name

    if email is not None:
        doc["email"] = email

    if vehicle is not None:
        doc["vehicle"] = vehicle

    if description is not None:
        doc["description"] = description

    appointments.update(doc, query.id == id)
    return id


def delete(id):
    query = tinydb.Query()
    appointments.remove(query.id == id)


def all():
    return appointments.all()


def get(id):
    timeslot = tinydb.Query()
    result = appointments.search(timeslot.id == id)

    if not result:
        raise ErrNotFound(f"no timeslot found for the provided id: {id}")

    return result[0]


def get_booked_slots(start=None):
    if not start:
        start = datetime.datetime.today() - datetime.timedelta(1)

    query = tinydb.Query()
    return appointments.search(query.timeslot >= start)
