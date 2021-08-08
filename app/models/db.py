import tinydb

from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), "TinyDate")

# DB initializtion
db = tinydb.TinyDB(
    "db.json", storage=serialization, sort_keys=True, indent=4, separators=(",", ": ")
)

shops = db.table("shops")
services = db.table("services")
appointments = db.table("appointments")
promos = db.table("promos")
vehicles = db.table("vehicles")
users = db.table("users")
