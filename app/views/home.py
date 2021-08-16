from app.config import get_config
from flask import render_template, request, Blueprint, abort

import app.models.vehicles as vehicles_model
import app.models.promos as promos_model
import app.models.services as services_model
import app.models.appointments as appintments_model

from app.third_parties import sendgrid

config = get_config()
bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    vehicles = vehicles_model.all() or []
    promos = promos_model.all() or []
    services = services_model.all() or []

    content = {"vehicles": vehicles, "services": services, "promos": promos}

    return render_template("index.html", config=config, content=content)


@bp.route("/services/<id>/<slug>")
def services_detail(id, slug):
    service = services_model.get(id)

    # if the service from db not match with the slug then return 404 page (not 100% necessary)
    if service["slug"] != slug:
        abort(404)

    return render_template("service_details.html", service=service)


@bp.route("/inventory")
def inventory():
    vehicles = vehicles_model.all()
    return render_template("inventory.html", config=config, vehicles=vehicles)


@bp.route("/inventory/<id>")
def get_vehicle(id):
    try:
        # Search for the vehicle and render it
        data = vehicles_model.get(id)
        return render_template("vehicle_details.html", config=config, vehicle=data)
    except vehicles_model.ErrNotFound:
        # TODO: return a 404 page
        return "oops not vehicle found"


@bp.route("/contact")
def contact():
    return render_template("contact.html", config=config)


@bp.route("/login")
def login():
    return render_template("login.html")


@bp.route("/send_email", methods=["POST"])
def send_email():
    from_email = request.form["from_email"]
    subject = request.form["subject"]
    content = request.form["content"]

    try:
        # FIXME: set the to email in the configurations instead of hard coding it
        sendgrid.send(from_email, "ms.kaleia@gmail.com", subject, content)
    except sendgrid.ErrSendEmail:
        return "oops, my bird just chewed the cable and we can't send your email now 😢.. please try again later "

    return "email sent 🥴"


@bp.route("/appointment")
def appointment():
    booked_appointments = appintments_model.get_booked_slots()
    timeslots = [a["timeslot"].date() for a in booked_appointments]
    print(timeslots)
    data = {"appointments": timeslots}
    return render_template("appointment.html", config=config, data=data)


@bp.errorhandler(404)
def page_not_found(error):
    return "oops.. page not found 😝"
