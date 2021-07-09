from flask import Flask

# Application
app = Flask(__name__)
app.config["SECRET_KEY"] = "my_precious"
app.config["WTF_CSRF_SECRET_KEY"] = "my_precious"

from app import views  # noqa
