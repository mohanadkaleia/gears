import sys
import tinydb

from pathlib import Path

# DB initializtion
DBJSON_PATH = Path(sys.path[1]) / Path("db.json")
print(DBJSON_PATH)
db = tinydb.TinyDB(str(DBJSON_PATH))
