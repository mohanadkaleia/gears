from pathlib import Path
from flask import Flask


# Application
app = Flask(__name__)
app.config["SECRET_KEY"] = "my_precious"
app.config["IMAGES_DIR_PATH"] = Path.cwd() / Path("app/static/images")


from app import views  # noqa
