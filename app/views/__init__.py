from .home import bp as home_bp
from .auth import bp as auth_bp
from .services_adm import bp as service_bp
from .vehicles_adm import bp as vehicle_bp
from .appointments_adm import bp as appointment_bp


def register(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(vehicle_bp)
    app.register_blueprint(appointment_bp)
