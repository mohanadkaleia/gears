from .home import bp as home_bp
from .services_adm import bp as service_bp


def register(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(service_bp)
