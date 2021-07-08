import tinydb
from app import util

db = tinydb.TinyDB("db.json")
shops = db.table("shops")

# TODO: we need to generate an id for shops here
def insert(name="", description="", logo="", phone="", email="", hours=""):
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
