import tinydb

from pathlib import Path

# DB initializtion
DBJSON_PATH = Path.cwd() / Path("db.json")
db = tinydb.TinyDB(str(DBJSON_PATH))
