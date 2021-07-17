import tinydb
from pathlib import Path

# DB initializtion
db = tinydb.TinyDB(str(Path.cwd() / Path("db.json")))

# Tables
services = db.table("services")
shops = db.table("shops")
vehicles = db.table("vehicles")
