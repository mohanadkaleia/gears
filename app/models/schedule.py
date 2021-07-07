import tinydb

from app import util


class ErrInvalidParameters(Exception):
    pass


class ErrNotFound(Exception):
    pass


# DB initializtion
db = tinydb.TinyDB("db.json")
schedule = db.table("schedule")


def insert(service_id, shop_id, timeslot, name, contact, description):
    # TODO: check the date is not less than today
    pass

    # TODO: checl for availability for the provided timeslot
    pass

    # Initialize id with randomly generated string, "t" for timeslot
    id = util.random_id(initial="t")

    schedule.insert(
        {
            "id": id,
            "shop_id": shop_id,
            "service_id": service_id,
            "timeslot": timeslot,
            "name": name,
            "contact": contact,
            "description": description,
        }
    )

    return id


def delete(id):
    query = tinydb.Query()
    schedule.remove(query.id == id)


def all():
    results = schedule.all()

    if not results:
        raise ErrNotFound("oops.. no data found in the db")

    return results


def get(id):
    timeslot = tinydb.Query()
    result = schedule.search(timeslot.id == id)

    if not result:
        raise ErrNotFound(f"no timeslot found for the provided id: {id}")

    return result[0]
