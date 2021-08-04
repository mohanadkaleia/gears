from pathlib import Path
from flask import Flask
from flask_login import LoginManager

import app.models.users as users_model


app = Flask(__name__)
app.config["SECRET_KEY"] = "my_precious"
app.config["IMAGES_DIR_PATH"] = Path.cwd() / Path("app/static/images")

# Install Login Manager
login_mng = LoginManager()
login_mng.login_view = 'auth.login'
login_mng.init_app(app)


@login_mng.user_loader
def load_user(user_id):
    return users_model.load_user(user_id)


# Register all views
from app import views  # noqa

views.register(app)
