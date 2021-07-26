from pathlib import Path
from flask import Flask


app = Flask(__name__)
app.config["SECRET_KEY"] = "my_precious"
app.config["IMAGES_DIR_PATH"] = Path.cwd() / Path("app/static/images")

# Register all views
from app import views  # noqa

views.register(app)
